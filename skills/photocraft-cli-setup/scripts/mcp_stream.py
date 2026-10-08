"""公开MCP串行转发：静态拒绝在安装前，回复验证在下一编辑前，不重放。"""
import base64
import binascii
import importlib.util
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import tempfile
import time


def load(name):
    spec=importlib.util.spec_from_file_location('craft_stream_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def preflight(raw):
    message=load('strict_json').loads(raw)
    if (not isinstance(message,dict) or message.get('jsonrpc')!='2.0'
            or not isinstance(message.get('method'),str)
            or message.get('params') is not None and not isinstance(message['params'],dict)):
        raise ValueError('invalid_mcp_request: $')
    if 'id' in message and type(message['id']) not in (int,str):
        raise ValueError('invalid_mcp_request_id: $.id')
    if message['method']=='tools/call':
        if 'id' not in message:raise ValueError('tool_request_requires_id: $.id')
        params=message.get('params') or {}
        if set(params)-{'name','arguments','_meta'} or not isinstance(params.get('name'),str):
            raise ValueError('invalid_tool_request: $.params')
        arguments=params.get('arguments');arguments={} if arguments is None else arguments
        if not isinstance(arguments,dict):raise ValueError('parameter_type: $.params.arguments')
        commands=load('commands');name=params['name']
        commands.validate_tool_parameters(name,arguments,'$.params.arguments',resolved=True)
        if name=='command_run':
            values=arguments.get('params')
            commands.validate_parameters(arguments['id'],{} if values is None else values,'$.params.arguments.params',resolved=True)
    elif 'id' not in message and message['method'] not in {'notifications/initialized','notifications/cancelled','notifications/progress'}:
        raise ValueError('unknown_mcp_notification: $.method')
    return message


def reply_error(message):
    error=load('operation_errors').error(message);error.phase='reply_received';return error


class Wire:
    """仅拥有本次启动的进程；原始客户端ID不重写，超时不重试。"""
    def __init__(self,argv,timeout=120):
        self.timeout=timeout;self.buffer=b'';self.stderr=tempfile.TemporaryFile()
        try:self.process=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.stderr)
        except BaseException:self.stderr.close();raise
    def send(self,message):
        try:
            self.process.stdin.write((json.dumps(message,allow_nan=False)+'\n').encode());self.process.stdin.flush()
        except OSError as error:raise load('operation_errors').error('outcome_unknown: mcp_write_failed; no replay') from error
    def read_line(self,deadline):
        while b'\n' not in self.buffer:
            remaining=deadline-time.monotonic()
            if remaining<=0 or not select.select([self.process.stdout],[],[],remaining)[0]:
                raise load('operation_errors').error('outcome_unknown: mcp_reply_timeout; no replay')
            chunk=os.read(self.process.stdout.fileno(),65536)
            if not chunk:raise load('operation_errors').error('mcp_disconnected: no replay')
            self.buffer+=chunk
            if len(self.buffer)>64*1024*1024:raise load('operation_errors').error('mcp_response_too_large: no replay')
        line,self.buffer=self.buffer.split(b'\n',1);return line
    def drain_notifications(self,output):
        # 当前请求只允许一帧响应；已有额外响应必须在确认成功／下一编辑前拒绝。
        deadline=time.monotonic()+self.timeout
        while self.buffer or select.select([self.process.stdout],[],[],0)[0]:
            raw=self.read_line(deadline)
            try:message=load('strict_json').loads(raw)
            except (ValueError,UnicodeError) as error:raise reply_error('outcome_unknown: invalid_pending_mcp_json') from error
            if (not isinstance(message,dict) or message.get('jsonrpc')!='2.0' or 'id' in message
                    or not isinstance(message.get('method'),str) or 'result' in message or 'error' in message
                    or 'params' in message and not isinstance(message['params'],dict)):
                raise reply_error('outcome_unknown: unsolicited_mcp_reply')
            emit(output,message)
    def receive(self,message,output):
        deadline=time.monotonic()+self.timeout
        while True:
            raw=self.read_line(deadline)
            try:reply=load('strict_json').loads(raw)
            except (ValueError,UnicodeError) as error:raise reply_error('outcome_unknown: invalid_mcp_json; no replay') from error
            if not isinstance(reply,dict) or reply.get('jsonrpc')!='2.0':raise reply_error('outcome_unknown: invalid_mcp_envelope')
            if 'id' not in reply and isinstance(reply.get('method'),str):
                if 'result' in reply or 'error' in reply or 'params' in reply and not isinstance(reply['params'],dict):raise reply_error('outcome_unknown: invalid_mcp_notification')
                emit(output,reply);continue
            if type(reply.get('id')) is not type(message['id']) or reply.get('id')!=message['id']:
                raise reply_error('outcome_unknown: mismatched_mcp_reply_id')
            if ('result' in reply)==('error' in reply):raise reply_error('outcome_unknown: ambiguous_mcp_reply')
            if 'error' in reply:
                error=reply['error']
                if not isinstance(error,dict) or type(error.get('code')) is not int or not isinstance(error.get('message'),str):
                    raise reply_error('outcome_unknown: invalid_mcp_error')
                raise reply_error('mcp_error: '+json.dumps(error))
            self.drain_notifications(output)
            return reply
    def close(self):
        try:self.process.stdin.close()
        except OSError:pass
        try:self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:self.process.kill();self.process.wait()
        self.process.stdout.close();self.stderr.close()


def emit(output,message):
    output.write(json.dumps(message,ensure_ascii=False,allow_nan=False)+'\n');output.flush()


def validate_reply(message,reply,expected_version=None):
    if message['method']=='tools/list':
        result=reply['result']
        if (not isinstance(result,dict) or not isinstance(result.get('tools'),list)
                or any(not isinstance(tool,dict) or not isinstance(tool.get('name'),str)
                       or not isinstance(tool.get('inputSchema'),dict) for tool in result['tools'])):
            raise reply_error('outcome_unknown: invalid_tools_list_reply')
        return
    if message['method']=='initialize':
        result=reply['result']
        if (not isinstance(result,dict) or not isinstance(result.get('protocolVersion'),str)
                or not isinstance(result.get('capabilities'),dict) or not isinstance(result.get('serverInfo'),dict)
                or any(not isinstance(result['serverInfo'].get(key),str) for key in ('name','version'))):
            raise reply_error('outcome_unknown: invalid_initialize_reply')
        if expected_version is not None and result['serverInfo']['version']!=expected_version:
            raise reply_error('outcome_unknown: initialize_runtime_version_mismatch')
        return
    if message['method']!='tools/call':return
    params=message['params'];tool=params['name'];result=reply['result'];commands=load('commands')
    # 这两种工具原生返回图像；不落盘也不把图像收窄为JSON文本。
    if tool in {'doc_render_preview','ui_screenshot'}:
        if (not isinstance(result,dict) or type(result.get('isError',False)) is not bool
                or not isinstance(result.get('content'),list) or not result['content']):
            raise load('operation_errors').error('outcome_unknown: invalid_image_reply')
        if result.get('isError'):raise load('operation_errors').error('command_failed: '+json.dumps(result['content']))
        for item in result['content']:
            if not isinstance(item,dict) or item.get('type') not in {'image','text'}:
                raise load('operation_errors').error('outcome_unknown: invalid_image_content')
            if item['type']=='image' and (not isinstance(item.get('data'),str) or not isinstance(item.get('mimeType'),str)):
                raise load('operation_errors').error('outcome_unknown: invalid_image_content')
            if item['type']=='image':
                try:base64.b64decode(item['data'],validate=True)
                except (ValueError,binascii.Error) as error:raise reply_error('outcome_unknown: invalid_image_base64') from error
            if item['type']=='text':
                if not isinstance(item.get('text'),str):raise load('operation_errors').error('outcome_unknown: invalid_text_content')
                try:value=load('strict_json').loads(item['text'])
                except json.JSONDecodeError:continue
                except (ValueError,UnicodeError) as error:raise reply_error('outcome_unknown: invalid_image_text_json') from error
                if isinstance(value,dict) and value.get('error'):raise reply_error('semantic_error: image_tool_failure')
        if not any(item['type']=='image' for item in result['content']):
            raise reply_error('outcome_unknown: missing_tool_image')
        return
    parsed=commands.parse_reply(result)
    arguments=params.get('arguments');arguments={} if arguments is None else arguments
    commands.validate_tool_reply(tool,parsed,arguments)
    if tool in {'doc_open','doc_save','doc_export'} and isinstance(parsed,dict) and 'path' in parsed:
        requested=arguments.get('path')
        if requested is not None and parsed['path']!=requested:raise load('operation_errors').error('outcome_unknown: mismatched_tool_path')


def run(argv,install,source=None,output=None):
    """逐条转发并验证；install仅在首条有效请求之后执行。"""
    source=sys.stdin if source is None else source;output=sys.stdout if output is None else output
    wire=None;receipts=[];message=None;phase='validation';installed=None
    try:
        for raw in source:
            if not raw.strip():continue
            message=None;phase='validation';message=preflight(raw)
            if wire is None:
                installed=install();wire=Wire([installed['executable'],*argv])
            phase='submitted';wire.send(message)
            if 'id' not in message:continue
            reply=wire.receive(message,output);phase='reply_received';validate_reply(message,reply,installed.get('expectedRuntimeVersion'))
            receipts.append({'request':message,'phase':'reply_validated'})
            emit(output,reply)
        return 0
    except (ValueError,OSError,RuntimeError,subprocess.SubprocessError) as error:
        detail=load('operation_errors').describe(error,phase=phase)
        if phase=='reply_received' and detail['phase']=='submitted':detail['phase']=phase
        detail.update(replayAllowed=False,request=message,receipts=receipts)
        if installed:detail['runtimeSha256']=installed['binarySha256']
        if hasattr(error,'dependencySetup'):detail['dependencySetup']=error.dependencySetup
        emit(output,{'jsonrpc':'2.0','id':message.get('id') if message else None,'error':{'code':-32602 if phase=='validation' else -32000,'message':detail['code'],'data':detail}})
        return 1
    finally:
        if wire:wire.close()
