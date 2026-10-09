"""loopback TCP前端：认证与静态拒绝先于懒安装，共享原生会话逐回复监督。"""
import hmac
import importlib.util
import json
import os
from pathlib import Path
import re
import secrets
import signal
import socket
import socketserver
import subprocess
import sys
import threading

MAX_REQUEST_BYTES=1<<20
MAX_CONNECTIONS=16
IO_TIMEOUT=30

def load(name):
    spec=importlib.util.spec_from_file_location('craft_tcp_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def launch(argv):
    """校验公开启动配置，不安装、不创建目录或令牌文件。"""
    allowed={'--port','--control-token','--control-token-file','--automation-read-root','--automation-write-root'}
    values={};index=1
    while index<len(argv):
        token=argv[index];location='$argv['+str(index)+']'
        if '=' in token and token.startswith('--'):key,value=token.split('=',1)
        elif token in allowed:
            key=token;index+=1
            if index>=len(argv):raise ValueError('missing_cli_value: '+location)
            value=argv[index]
        elif token in {'--help','-h'}:index+=1;continue  # 固定原生忽略子命令后的help，仍须监督。
        else:raise ValueError('invalid_cli_option: '+location)
        if key not in allowed:raise ValueError('invalid_cli_option: '+location)
        values[key]=value;index+=1
    port=values.get('--port')
    if port is None or not re.fullmatch(r'\+?[0-9]+',port):raise ValueError('invalid_tcp_port: $argv')
    digits=port.lstrip('+').lstrip('0') or '0'
    if len(digits)>5 or int(digits)>65535:raise ValueError('invalid_tcp_port: $argv')
    token=values.get('--control-token',os.environ.get('PHOTOCRAFT_CONTROL_TOKEN'))
    token_file=values.get('--control-token-file',os.environ.get('PHOTOCRAFT_CONTROL_TOKEN_FILE'))
    if token is not None and token_file is not None:raise ValueError('conflicting_control_tokens: $argv')
    if token is not None:validate_token(token)
    if token_file is not None and not token_file:raise ValueError('invalid_control_token_file: $argv')
    native=['serve']
    for key in ('--automation-read-root','--automation-write-root'):
        if key in values:
            root=values[key]
            if not root or not Path(root).is_dir():raise ValueError('invalid_automation_root: $argv')
            native.extend([key,root])
    return int(digits),token,Path(token_file) if token_file is not None else None,native


def validate_token(token):
    if not isinstance(token,str) or not re.fullmatch('[0-9a-fA-F]{64}',token):raise ValueError('invalid_control_token: $argv')
    return token.lower()


def server_token(supplied,path):
    """复用固定原生的令牌选择语义；已有文件不覆盖，创建使用0600及O_EXCL。"""
    if supplied is not None:return validate_token(supplied)
    generated=secrets.token_hex(32)
    if path is None:return generated
    try:return validate_token(path.read_text().strip())
    except FileNotFoundError:
        # 原生允许创建缺失父目录；仅在整个启动配置已验证后执行。
        path.parent.mkdir(parents=True,exist_ok=True)
        try:fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except FileExistsError:return validate_token(path.read_text().strip())
        with os.fdopen(fd,'w') as output:output.write(generated+'\n')
        return generated


def emit(output,reply):
    output.write((json.dumps(reply,ensure_ascii=True,allow_nan=False)+'\n').encode());output.flush()


def failure(error,message,receipts,phase='validation',installed=None):
    detail=load('operation_errors').describe(error,phase=phase)
    detail.update(request=message,receipts=list(receipts),replayAllowed=False)
    if installed:detail['runtimeSha256']=installed['binarySha256']
    if hasattr(error,'dependencySetup'):detail['dependencySetup']=error.dependencySetup
    reply=dict(getattr(error,'nativeReply',{'id':message.get('id') if message else None,'ok':False,'error':detail['code']}))
    reply['errorData']=detail;return reply


class Gateway:
    """所有连接共用一个自有原生进程；完整请求和回复在同一互斥锁中执行。"""
    def __init__(self,native,install):
        self.native=native;self.install=install;self.lock=threading.RLock();self.stream=load('serve_stream')
        self.wire=None;self.installed=None;self.receipts=[];self.quarantined=None;self.closed=False
    def execute(self,message):
        with self.lock:
            if self.closed or self.quarantined is not None:
                reply=failure(ValueError('serve_session_quarantined'),message,self.receipts)
                reply['errorData'].pop('category',None);reply['errorData']['recoveryAction']='reconcile'
                if self.quarantined is not None:reply['errorData']['priorFailure']=self.quarantined
                return reply,False
            phase='validation'
            try:
                if self.wire is None:
                    self.installed=self.install();self.wire=self.stream.Wire([self.installed['executable'],*self.native])
                phase='submitted';self.wire.send(message)
                reply=self.wire.receive(message,None);phase='reply_received';self.stream.validate_reply(message,reply)
                self.receipts.append({'request':message,'phase':'reply_validated'})
                return reply,True
            except (ValueError,OSError,RuntimeError,subprocess.SubprocessError) as error:
                reply=failure(error,message,self.receipts,phase,self.installed)
                # 任何原生失败停止共享会话；不能由另一连接重启或继续编辑。
                self.quarantined=reply['errorData'];self.close_wire();return reply,False
    def close_wire(self):
        wire=self.wire;self.wire=None
        if wire:wire.close()
    def delivery_lost(self,message):
        with self.lock:
            error=load('operation_errors').error('outcome_unknown: tcp_reply_delivery_lost');error.phase='reply_validated'
            self.quarantined=failure(error,message,self.receipts,installed=self.installed)['errorData'];self.close_wire()
    def close(self):
        self.closed=True
        # 先终止自有进程，唤醒可能等待回复的线程，不能等待执行锁至超时。
        wire=self.wire
        if wire and wire.process.poll() is None:
            try:wire.process.terminate()
            except ProcessLookupError:pass
        with self.lock:self.close_wire()


class Handler(socketserver.StreamRequestHandler):
    """有界JSON-lines连接；认证消息不进入编辑回执或错误诊断。"""
    def handle(self):
        self.connection.settimeout(IO_TIMEOUT);authenticated=False;last_submitted=None
        try:
            while True:
                raw=self.rfile.readline(MAX_REQUEST_BYTES+1)
                if not raw:return
                if len(raw)>MAX_REQUEST_BYTES:
                    emit(self.wfile,{'id':None,'ok':False,'error':f'request exceeds {MAX_REQUEST_BYTES} bytes'});return
                if not raw.strip():continue
                if not authenticated:
                    try:message=load('strict_json').loads(raw)
                    except (ValueError,UnicodeError):message={}
                    if not isinstance(message,dict):message={}
                    params=message.get('params');provided=params.get('token','') if isinstance(params,dict) else ''
                    authenticated=(message.get('method')=='auth' and isinstance(provided,str)
                                   and re.fullmatch('[0-9a-fA-F]{64}',provided) is not None
                                   and hmac.compare_digest(self.server.token.encode(),provided.lower().encode()))
                    reply={'id':message.get('id'),'ok':authenticated}
                    if authenticated:reply['result']={'authenticated':True}
                    else:reply['error']='authentication required'
                    emit(self.wfile,reply)
                    if not authenticated:return
                    continue
                try:message=self.server.gateway.stream.preflight(raw)
                except (ValueError,UnicodeError) as error:
                    emit(self.wfile,failure(error,None,[]));return
                # 回复交付也是确认边界；另一连接不能在交付失败判定前进入编辑。
                with self.server.gateway.lock:
                    reply,keep=self.server.gateway.execute(message);last_submitted=message if keep else None
                    try:emit(self.wfile,reply)
                    except (OSError,ValueError):
                        if keep:self.server.gateway.delivery_lost(message)
                        last_submitted=None;return
                    last_submitted=None
                if not keep:return
        except (OSError,ValueError):
            if last_submitted is not None:self.server.gateway.delivery_lost(last_submitted)


class Server(socketserver.ThreadingMixIn,socketserver.TCPServer):
    """与固定原生一致的loopback和16连接限制；跨连接共享Gateway。"""
    daemon_threads=True
    def __init__(self,address,token,gateway):
        self.token=token;self.gateway=gateway;self.permits=threading.BoundedSemaphore(MAX_CONNECTIONS)
        super().__init__(address,Handler)
    def process_request(self,request,client_address):
        if not self.permits.acquire(blocking=False):
            try:
                request.settimeout(IO_TIMEOUT);request.sendall(b'{"id":null,"ok":false,"error":"connection limit reached"}\n')
            except OSError:pass
            self.shutdown_request(request);return
        try:super().process_request(request,client_address)
        except BaseException:self.permits.release();raise
    def process_request_thread(self,request,client_address):
        try:super().process_request_thread(request,client_address)
        finally:self.permits.release()


def run(argv,install):
    """启动已认证TCP前端；仅拥有本次进程，退出时不触碰桌面或其他服务。"""
    gateway=None;previous=None
    try:
        port,supplied,path,native=launch(argv);token=server_token(supplied,path)
        gateway=Gateway(native,install)
        with Server(('127.0.0.1',port),token,gateway) as server:
            if path is not None:print('photocraft-cli control token file: '+str(path),file=sys.stderr,flush=True)
            elif supplied is None:print('photocraft-cli control token: '+token,file=sys.stderr,flush=True)
            print('photocraft-cli serving on 127.0.0.1:'+str(server.server_address[1]),file=sys.stderr,flush=True)
            if threading.current_thread() is threading.main_thread():
                previous=signal.getsignal(signal.SIGTERM)
                def stop(signum,frame):raise KeyboardInterrupt()
                signal.signal(signal.SIGTERM,stop)
            server.serve_forever(poll_interval=0.2)
        return 0
    except KeyboardInterrupt:return 0
    except (ValueError,OSError) as error:
        reply=failure(error,None,[]);print(json.dumps(reply,ensure_ascii=True));return 1
    finally:
        if previous is not None:signal.signal(signal.SIGTERM,previous)
        if gateway:gateway.close()
