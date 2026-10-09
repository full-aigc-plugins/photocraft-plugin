"""公开serve stdio的逐请求预检及回复监督；原生TCP与聚合内部另行验收。"""
import base64
import binascii
import json
import select
import subprocess
import sys
import time

# 复用已验证的有界自有进程传输，保持每技能资源自包含。
import importlib.util
from pathlib import Path

def load(name):
    spec=importlib.util.spec_from_file_location('craft_serve_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def reject(code,path):
    raise ValueError(code+': '+path)


def fields(params,allowed,path):
    if not isinstance(params,dict):reject('parameter_type',path)
    unknown=set(params)-set(allowed)
    if unknown:reject('parameter_unknown_field',path+'.'+sorted(unknown)[0])


def relative_path(value,path):
    """匹配固定原生workspace路径语法；实际目录能力仍由原生持有。"""
    if not isinstance(value,str) or not value or value.startswith('/') or '\\' in value or ':' in value:
        reject('invalid_automation_path',path)
    devices={'CON','PRN','AUX','NUL','CLOCK$','CONIN$','CONOUT$',*[kind+str(i) for kind in ('COM','LPT') for i in range(1,10)]}
    for component in value.split('/'):
        if component in {'','.','..'} or component.endswith(('.', ' ')) or component.split('.')[0].upper() in devices:
            reject('invalid_automation_path',path)


def validate_method(method,params,path='$.params'):
    params={} if params is None else params
    if not isinstance(params,dict):reject('parameter_type',path)
    commands=load('commands')
    if method=='engine.execute':
        fields(params,{'command','params'},path)
        values=params.get('params');values={} if values is None else values
        if not isinstance(params.get('command'),str):reject('parameter_type',path+'.command')
        commands.validate_parameters(params['command'],values,path+'.params',resolved=True)
    elif method=='doc.new':
        # 原生doc.new接收完整file.new参数，不能套用较窄的MCP doc_new结构。
        commands.validate_parameters('file.new',params,path,resolved=True)
    elif method in {'doc.open','doc.save','doc.inspect','doc.select','doc.close','session.list'}:
        if method=='doc.save':
            fields(params,{'path','format','quality','index'},path)
            adjusted=dict(params);adjusted.pop('quality',None)
            commands.validate_tool_parameters('doc_save',adjusted,path,resolved=True)
            if params.get('quality') is not None and (type(params['quality']) is not int or not 0<=params['quality']<2**64):reject('parameter_type',path+'.quality')
        else:commands.validate_tool_parameters(method.replace('.','_'),params,path,resolved=True)
    elif method=='engine.commands':
        fields(params,{'filter'},path)
        if params.get('filter') is not None and not isinstance(params['filter'],str):reject('parameter_type',path+'.filter')
    elif method=='methods':fields(params,set(),path)
    elif method=='doc.render':
        fields(params,{'index','maxSide','path'},path)
        commands.validate_tool_parameters('doc_inspect',{'index':params['index']} if 'index' in params else {},path,resolved=True)
        if 'maxSide' in params and (type(params['maxSide']) is not int or not 0<=params['maxSide']<2**32):reject('parameter_type',path+'.maxSide')
        if params.get('path') is not None and not isinstance(params['path'],str):reject('parameter_type',path+'.path')
    elif method=='batch':
        fields(params,{'steps','stopOnError'},path)
        if not isinstance(params.get('steps'),list) or len(params['steps'])>256:reject('invalid_batch_steps',path+'.steps')
        if 'stopOnError' in params and type(params['stopOnError']) is not bool:reject('parameter_type',path+'.stopOnError')
        for index,step in enumerate(params['steps']):
            location=path+'.steps['+str(index)+']';fields(step,{'command','method','params'},location)
            if ('command' in step)==('method' in step):reject('invalid_batch_step',location)
            if 'command' in step:validate_method('engine.execute',{'command':step['command'],'params':step.get('params')},location)
            else:
                if step['method']=='batch':reject('nested_batch',location+'.method')
                validate_method(step['method'],step.get('params'),location+'.params')
    else:reject('unknown_serve_method','$.method')
    if method in {'doc.open','doc.save','doc.render'} and params.get('path') is not None:
        relative_path(params['path'],path+'.path')


def preflight(raw):
    message=load('strict_json').loads(raw)
    if not isinstance(message,dict):reject('invalid_serve_request','$')
    fields(message,{'id','method','params'},'$')
    if not isinstance(message.get('method'),str):reject('parameter_type','$.method')
    validate_method(message['method'],message.get('params'))
    return message


def reply_error(message):
    error=load('operation_errors').error(message);error.phase='reply_received';return error


def same_id(left,right):
    # 原生允许JSON值作为id；bool和1、int和float不能因Python相等而混淆。
    if type(left) is not type(right):return False
    if isinstance(left,list):return len(left)==len(right) and all(same_id(a,b) for a,b in zip(left,right))
    if isinstance(left,dict):return left.keys()==right.keys() and all(same_id(left[k],right[k]) for k in left)
    return left==right


class Wire(load('mcp_stream').Wire):
    """原生JSON-lines没有服务端通知，一次请求只接收一个匹配回复。"""
    def receive(self,message,output):
        raw=self.read_line(time.monotonic()+self.timeout)
        try:reply=load('strict_json').loads(raw)
        except (ValueError,UnicodeError) as error:raise reply_error('outcome_unknown: invalid_serve_json') from error
        if (not isinstance(reply,dict) or 'id' not in reply or not same_id(reply['id'],message.get('id'))
                or type(reply.get('ok')) is not bool or ('result' in reply)==('error' in reply)
                or reply['ok']!=('result' in reply)):
            raise reply_error('outcome_unknown: invalid_serve_envelope')
        if self.buffer or select.select([self.process.stdout],[],[],0)[0]:raise reply_error('outcome_unknown: unsolicited_serve_reply')
        if not reply['ok']:
            if not isinstance(reply['error'],str):raise reply_error('outcome_unknown: invalid_serve_error')
            error=reply_error('command_failed: native_serve_error');error.nativeReply=reply;raise error
        return reply


def validate_reply(message,reply):
    result=reply['result'];method=message['method'];params=message.get('params') or {};commands=load('commands')
    if isinstance(result,dict) and result.get('error'):raise reply_error('semantic_error: native_serve_failure')
    if method in {'doc.new','doc.open','doc.save','doc.inspect','batch'}:
        commands.validate_tool_reply('command_batch' if method=='batch' else method.replace('.','_'),result,params)
    if method in {'doc.open','doc.save','doc.render'} and isinstance(result,dict) and 'path' in result and params.get('path') is not None:
        if result['path']!=params['path']:raise reply_error('outcome_unknown: mismatched_serve_path')
    if method in {'methods','engine.commands'} and not isinstance(result,list):raise reply_error('outcome_unknown: invalid_serve_list')
    if method in {'session.list','doc.select','doc.close'}:
        if (not isinstance(result,dict) or not isinstance(result.get('documents'),list)
                or 'active' not in result or result['active'] is not None and (type(result['active']) is not int or result['active']<0)
                or any(not isinstance(row,dict) or type(row.get('index')) is not int or row['index']<0 for row in result['documents'])):
            raise reply_error('outcome_unknown: invalid_serve_session')
    if method=='doc.render':
        if params.get('path') is not None:
            if not isinstance(result,dict) or not isinstance(result.get('path'),str) or type(result.get('bytes')) is not int or result['bytes']<=0:raise reply_error('outcome_unknown: invalid_render_file_reply')
        else:
            if not isinstance(result,dict) or result.get('mime')!='image/png' or not isinstance(result.get('base64'),str):raise reply_error('outcome_unknown: invalid_render_image_reply')
            try:data=base64.b64decode(result['base64'],validate=True)
            except (ValueError,binascii.Error) as error:raise reply_error('outcome_unknown: invalid_render_base64') from error
            if not data:raise reply_error('outcome_unknown: empty_render_image')


def run(argv,install,source=None,output=None):
    """安装仅发生于首条有效请求后；失败停止，不重放原操作。"""
    source=sys.stdin if source is None else source;output=sys.stdout if output is None else output
    wire=None;receipts=[];message=None;phase='validation';installed=None
    try:
        for raw in source:
            if not raw.strip():continue
            message=None;phase='validation';message=preflight(raw)
            if wire is None:
                installed=install();wire=Wire([installed['executable'],*argv])
            phase='submitted';wire.send(message)
            reply=wire.receive(message,output);phase='reply_received';validate_reply(message,reply)
            receipts.append({'request':message,'phase':'reply_validated'})
            load('mcp_stream').emit(output,reply)
        return 0
    except (ValueError,OSError,RuntimeError,subprocess.SubprocessError) as error:
        detail=load('operation_errors').describe(error,phase=phase);detail.update(replayAllowed=False,request=message,receipts=receipts)
        if installed:detail['runtimeSha256']=installed['binarySha256']
        if hasattr(error,'dependencySetup'):detail['dependencySetup']=error.dependencySetup
        reply=getattr(error,'nativeReply',{'id':message.get('id') if message else None,'ok':False,'error':detail['code']})
        reply['errorData']=detail;load('mcp_stream').emit(output,reply)
        return 1
    finally:
        if wire:wire.close()
