"""单请求串行 stdio MCP 会话；超时不重试有副作用的请求。"""
import json
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("craft_mcp_errors", Path(__file__).with_name("operation_errors.py"))
_errors = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_errors)
from contextlib import suppress
import os
import select
import subprocess
import tempfile
import time


def strict_json(data):
    spec=importlib.util.spec_from_file_location('craft_strict_json',Path(__file__).with_name('strict_json.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.loads(data)


def reply_error(message):
    error=_errors.error(message);error.phase='reply_received';return error


def notification(value):
    return (isinstance(value,dict) and value.get('jsonrpc')=='2.0' and 'id' not in value
            and isinstance(value.get('method'),str) and 'result' not in value and 'error' not in value
            and ('params' not in value or isinstance(value['params'],dict)))


class Session:
    def __init__(self, argv, timeout=120):
        self.timeout = timeout
        self.buffer = b''
        self.sequence = 0
        self.stderr = tempfile.TemporaryFile()
        self.process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr)
        try:
            self.request('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'craft-skill', 'version': '0.1.0'}})
            self.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        except BaseException:
            self.close()
            raise

    def send(self, value):
        encoded = (json.dumps(value, allow_nan=False) + '\n').encode()
        try:
            self.process.stdin.write(encoded)
            self.process.stdin.flush()
        except OSError:
            # 写入／flush 失败不能证明对端没有接收编辑请求。
            raise _errors.error('outcome_unknown: mcp_write_failed; request not retried') from None

    def request(self, method, params):
        self.sequence += 1
        identifier = self.sequence
        self.send({'jsonrpc': '2.0', 'id': identifier, 'method': method, 'params': params})
        deadline = time.monotonic() + self.timeout
        while True:
            if time.monotonic() >= deadline:
                raise TimeoutError('outcome_unknown: request not retried')
            if b'\n' in self.buffer:
                line, self.buffer = self.buffer.split(b'\n', 1)
                if not line.strip():
                    continue
                try:
                    response = strict_json(line)
                except (ValueError, UnicodeError):
                    raise reply_error('outcome_unknown: invalid_mcp_json; request not retried') from None
                if notification(response):
                    continue
                if not isinstance(response, dict) or response.get('jsonrpc')!='2.0':
                    raise reply_error('outcome_unknown: invalid_mcp_response; request not retried')
                if type(response.get('id')) is not int or response.get('id') != identifier:
                    raise reply_error('outcome_unknown: mismatched_mcp_reply_id; request not retried')
                if ('error' in response) == ('result' in response):
                    raise reply_error('outcome_unknown: missing_or_ambiguous_mcp_result; request not retried')
                if 'error' in response:
                    error=response['error']
                    if not isinstance(error,dict) or type(error.get('code')) is not int or not isinstance(error.get('message'),str):
                        raise reply_error('outcome_unknown: invalid_mcp_error; request not retried')
                    raise reply_error('mcp_error: ' + json.dumps(error))
                result = response['result']
                if method == 'tools/call':
                    if (not isinstance(result, dict)
                            or not isinstance(result.get('isError', False), bool)
                            or not isinstance(result.get('content'), list)
                            or any(not isinstance(entry, dict)
                                   or not isinstance(entry.get('type'), str)
                                   or (entry['type'] == 'text' and not isinstance(entry.get('text'), str))
                                   for entry in result.get('content', []))):
                        raise reply_error('outcome_unknown: invalid_tool_reply; request not retried')
                self.drain_pending(deadline)
                return result
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([self.process.stdout], [], [], remaining)[0]:
                raise TimeoutError('outcome_unknown: request not retried')
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise _errors.error('mcp_disconnected: outcome may be unknown')
            self.buffer += chunk
            if len(self.buffer) > 64 * 1024 * 1024:
                raise _errors.error('mcp_response_too_large')

    def drain_pending(self,deadline):
        """确认成功前消费合法通知；额外回复或不完整帧必须先核清，禁止下一编辑。"""
        while self.buffer or select.select([self.process.stdout],[],[],0)[0]:
            while b'\n' not in self.buffer:
                remaining=deadline-time.monotonic()
                if remaining<=0 or not select.select([self.process.stdout],[],[],remaining)[0]:
                    raise reply_error('outcome_unknown: pending_mcp_frame_timeout; request not retried')
                chunk=os.read(self.process.stdout.fileno(),65536)
                if not chunk:raise reply_error('mcp_disconnected: pending frame; request not retried')
                self.buffer+=chunk
                if len(self.buffer)>64*1024*1024:raise reply_error('mcp_response_too_large')
            line,self.buffer=self.buffer.split(b'\n',1)
            if not line.strip():continue
            try:value=strict_json(line)
            except (ValueError,UnicodeError) as error:raise reply_error('outcome_unknown: invalid_pending_mcp_json') from error
            if not notification(value):raise reply_error('outcome_unknown: unsolicited_mcp_reply')

    def command(self, identifier, params):
        result = self.request('tools/call', {'name': 'run_command', 'arguments': {'command': identifier, 'params': params}})
        if result.get('isError'):
            raise _errors.error('command_failed: ' + identifier + ': ' + json.dumps(result.get('content')))
        content = result.get('content', [])
        texts = [entry['text'] for entry in content if entry.get('type') == 'text']
        if len(texts) != 1:
            raise _errors.error('unexpected_command_result')
        return strict_json(texts[0])

    def close(self):
        if self.process.stdin:
            with suppress(BrokenPipeError):
                self.process.stdin.close()
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        self.process.stdout.close()
        self.stderr.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
