#!/usr/bin/env python3
"""公开连续任务：逐阶段调用原命令入口，复用一个所属实例，不重启或重放。"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import secrets
import socket
import sys
import tempfile
import threading
import uuid

sys.dont_write_bytecode = True
MAX_LINE_BYTES = 8 << 20


def load(name):
    spec=importlib.util.spec_from_file_location('photocraft_task_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def sha(path):
    """读取当前文件摘要，用于安装及输入身份核对。"""
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


class BorrowedSession:
    """阶段借用所属连接；退出阶段不结束原生实例。"""
    def __init__(self,owner):self.owner=owner
    def __enter__(self):return self.owner
    def __exit__(self,*args):pass


class TaskSession:
    """固定任务根、运行时与输入范围；首份合法计划才创建输出及原生会话。"""
    def __init__(self,work,runtime_home=None,mode='headless',protected_paths=(),commands=None):
        self.commands=commands or load('commands')
        if mode not in ('headless','bridge'):raise ValueError('invalid_mode')
        if mode=='bridge' and platform.system().lower()+'-'+platform.machine().lower()!='darwin-arm64':raise ValueError('unsupported_desktop_platform')
        self.mode=mode;self.work=Path(work).absolute()
        self.runtime=Path(runtime_home or os.environ.get('CRAFT_RUNTIME_HOME',str(Path.home()/'.local/share/craft-runtimes'))).resolve()
        if self.work.exists() or self.work.is_symlink():raise ValueError('output_exists')
        if not self.work.parent.is_dir():raise ValueError('output_parent_missing')
        if self.work.resolve()!=self.work:raise ValueError('task_output_alias')
        protected_paths=tuple(protected_paths)
        self.protected=tuple(Path(p).resolve() for p in protected_paths)
        if any(Path(p).is_symlink() or not Path(p).exists() for p in protected_paths):raise ValueError('task_protected_path_missing')
        if any(self.work.is_relative_to(p) for p in (self.commands.ROOT,self.runtime,*self.protected)):raise ValueError('task_output_protected')
        self.owner=None;self.installed=None;self.desktop={};self.started=0;self.pids=[];self.plans=[];self.capabilities=None
        self.stopped=False;self.closed=False;self.created=False;self.work_identity=None;self.execution_lock=threading.Lock()
        self.private=None;self.token=None;self.token_sha=None;self.port=None;self.task_id=str(uuid.uuid4())
        if mode=='bridge':
            with socket.socket() as probe:probe.bind(('127.0.0.1',0));self.port=probe.getsockname()[1]
        self.binding=self._binding()

    def _binding(self):
        resources={str(p.relative_to(self.commands.ROOT)):sha(p) for p in sorted(self.commands.ROOT.rglob('*'))
                   if p.is_file() and '__pycache__' not in p.parts and (p.parent.name=='scripts' or p.parent.name=='references' and p.suffix=='.json')}
        return json.dumps({'mode':self.mode,'work':str(self.work),'runtime':str(self.runtime),
                           'protected':[str(p) for p in self.protected],'resources':resources},sort_keys=True)

    def _processes(self):
        if self.owner is None:return []
        if self.mode=='headless':return [self.owner.process]
        return [p for p in (getattr(getattr(self.owner,'session',None),'process',None),self.owner.process) if p is not None]

    def _work_safe(self):
        if not self.created:return False
        if self.work.is_symlink() or not self.work.is_dir() or self.work.resolve()!=self.work:return False
        status=self.work.stat();return (status.st_dev,status.st_ino)==self.work_identity

    def _assert_identity(self):
        if self._binding()!=self.binding or self.created and not self._work_safe():raise ValueError('task_identity_changed')
        if not self.created and (self.work.exists() or self.work.is_symlink()):raise ValueError('output_exists')
        for identity in (self.installed,self.desktop):
            if identity and sha(identity['executable'])!=identity['binarySha256']:raise ValueError('task_identity_changed')
        if self.token and (self.token.is_symlink() or sha(self.token)!=self.token_sha):raise ValueError('task_identity_changed')
        if any(p.poll() is not None for p in self._processes()):raise RuntimeError('task_process_exited')

    def _install(self,lock,home):
        if self.installed is None:
            if self.mode=='bridge':self.desktop.update(self.commands.load('desktop').install(self.commands.reply_json((self.commands.ROOT/'scripts/desktop.lock.json').read_text()),home))
            self.installed=self.commands.load('bootstrap').install(lock,home)
        return self.installed

    def _factory(self,argv):
        if self.owner is None:
            if self.mode=='bridge':
                self.owner=self.commands.load('desktop_session').OwnedSession(argv,self.desktop,self.commands.DOMAIN,self.work,self.port,self.token)
                self.owner.__enter__()
            else:self.owner=self.commands.load('mcp_session').Session(argv)
            self.started+=1
        self._assert_identity();self.pids.append([p.pid for p in self._processes()]);return BorrowedSession(self.owner)

    def execute(self,plan,name,inputs=None):
        """执行一个新阶段；返回原命令回执，未知或失败后禁止后续阶段。"""
        if not self.execution_lock.acquire(blocking=False):raise RuntimeError('task_session_busy')
        try:return self._execute(plan,name,inputs)
        finally:self.execution_lock.release()

    def _execute(self,plan,name,inputs):
        if self.closed or self.stopped:raise RuntimeError('task_session_stopped')
        try:
            self._assert_identity()
            if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,63}',name):raise ValueError('invalid_task_stage_name')
            inputs={} if inputs is None else inputs
            if not isinstance(inputs,dict) or any(not isinstance(k,str) or not re.fullmatch(r'[a-zA-Z][\w-]*',k) or k=='output' for k in inputs):raise ValueError('invalid_input_name')
            self.commands.reply_json(json.dumps(plan,allow_nan=False))
            self.commands.validate(plan,inputs)
            if self.mode=='bridge':
                available={row['id'] for row in self.commands.reply_json((self.commands.ROOT/'references/desktop-command-snapshot.json').read_text())['commands']}
                for step in plan['operations']:
                    for command in self.commands.command_ids(step):
                        if command not in available:raise ValueError('backend_command_unavailable: '+command)
            hashes={}
            for key,value in inputs.items():
                source=Path(value);path=source.resolve()
                if source.is_symlink() or not source.is_file():raise ValueError('invalid_input_file: '+key)
                if not path.is_relative_to(self.work) and not any(path==p or path.is_relative_to(p) for p in self.protected):raise ValueError('task_input_not_protected')
                hashes[key]=sha(path)
            if not self.created:
                self.work.mkdir(mode=0o700);self.created=True;status=self.work.stat();self.work_identity=(status.st_dev,status.st_ino)
                if self.mode=='bridge':
                    self.private=tempfile.TemporaryDirectory(prefix='photocraft-task-')
                    self.token=Path(self.private.name)/'control-token';self.token.write_text(secrets.token_hex(32));self.token.chmod(0o600);self.token_sha=sha(self.token)
                self._record()
            receipt=self.commands.execute(plan,self.work/name,self.runtime,self.mode,
                '127.0.0.1:'+str(self.port) if self.port else None,str(self.token) if self.token else None,
                installer=self._install,session_factory=self._factory,inputs=inputs,session_root=self.work,
                session_identity=self.task_id,expected_capabilities=self.capabilities)
            if self.capabilities is None and receipt['result']=='PASS':self.capabilities=receipt['capabilitySnapshot']
            self.plans.append({'name':name,'result':receipt['result'],'planSha256':receipt['planSha256'],
                               'receiptSha256':sha(self.work/name/'journal.json')})
            if any(sha(inputs[key])!=digest for key,digest in hashes.items()):raise RuntimeError('task_source_changed')
            if receipt['result']!='PASS':self.stopped=True
            self._record();return receipt
        except KeyboardInterrupt:
            self.stopped=True
            journal=self.work/name/'journal.json'
            if self._work_safe() and journal.is_file():
                receipt=self.commands.reply_json(journal.read_text());receipt['result']='unknown';receipt['error']='outcome_unknown: task_interrupted; no replay'
                if receipt.get('steps') and receipt['steps'][-1].get('state')=='started':receipt['steps'][-1]['state']='unknown'
                self.commands.write(journal,receipt);self.commands.write(journal.parent/'failure.json',receipt)
                self.plans.append({'name':name,'result':'unknown','planSha256':receipt['planSha256'],'receiptSha256':sha(journal)})
            self._record();raise
        except BaseException:
            self.stopped=True;self._record();raise

    def _record(self):
        if not self._work_safe():return
        self.commands.write(self.work/'task-session.json',{'schema':'photocraft-task-session/v1','taskId':self.task_id,'mode':self.mode,
            'identityBindingSha256':hashlib.sha256(self.binding.encode()).hexdigest(),'sessionsStarted':self.started,'pids':self.pids,
            'singleProcessIdentity':bool(self.pids) and all(p==self.pids[0] for p in self.pids),'plans':self.plans,
            'stopped':self.stopped,'closed':self.closed,'ownedProcessesStopped':self.closed and all(p.poll() is not None for p in self._processes()),
            'scope':'owned task instance and stage isolation; shared mutable ownership and full V1 not accepted'})

    def close(self):
        """只结束本任务所属进程；不自动保存，不终止用户已有窗口。"""
        if self.closed and all(p.poll() is not None for p in self._processes()):return
        if not self.execution_lock.acquire(blocking=False):raise RuntimeError('task_session_busy')
        try:
            if self.owner is not None:self.owner.close()
        finally:
            self.closed=True
            try:
                if self.private:self.private.cleanup()
                self._record()
            finally:self.execution_lock.release()

    def __enter__(self):
        if self.closed or self.stopped:raise RuntimeError('task_session_stopped')
        return self
    def __exit__(self,*args):self.close()


def serve(session,incoming,outgoing):
    """在同一输入句柄逐行接收阶段；错误停止消费，EOF交由任务上下文清理。"""
    def emit(value):outgoing.write(json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n');outgoing.flush()
    while True:
        line=incoming.readline(MAX_LINE_BYTES+1)
        if not line:return 0
        try:
            try:size=len(line.encode('utf-8'))
            except UnicodeError:raise ValueError('invalid_json_encoding') from None
            if size>MAX_LINE_BYTES:raise ValueError('task_request_too_large')
            if not line.strip():continue
            request=session.commands.reply_json(line)
            if request=={'action':'close'}:session.close();emit({'result':'CLOSED'});return 0
            if not isinstance(request,dict) or not {'name','plan'}.issubset(request) or set(request)-{'name','plan','inputs'}:raise ValueError('invalid_task_request')
            receipt=session.execute(request['plan'],request['name'],request.get('inputs'));emit(receipt)
            if receipt['result']!='PASS':return 1
        except (ValueError,RuntimeError,OSError,TypeError) as error:
            session.stopped=True;session._record();emit({'result':'FAIL',**session.commands.load('operation_errors').describe(error)});return 1


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--runtime-home',type=Path,required=True);parser.add_argument('--mode',choices=['headless','bridge'],default='headless')
    parser.add_argument('--protect-input',action='append',default=[]);args=parser.parse_args()
    try:
        with TaskSession(args.output,args.runtime_home,args.mode,args.protect_input) as session:
            print(json.dumps({'result':'READY','mode':args.mode,'scope':'native starts on first valid plan'}),flush=True)
            return serve(session,sys.stdin,sys.stdout)
    except KeyboardInterrupt:
        print(json.dumps({'result':'unknown','error':'task_interrupted; inspect original journal and files; no replay'}),flush=True);return 130
    except (ValueError,RuntimeError,OSError,TypeError) as error:
        print(json.dumps({'result':'FAIL',**load('operation_errors').describe(error)}),flush=True);return 1


if __name__=='__main__':raise SystemExit(main())
