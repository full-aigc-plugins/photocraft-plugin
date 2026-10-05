"""单请求串行 stdio MCP 会话；超时不重试有副作用的请求。"""
import json
from contextlib import suppress
import os
import select
import subprocess
import tempfile
import time


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
        self.process.stdin.write((json.dumps(value, allow_nan=False) + '\n').encode())
        self.process.stdin.flush()

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
                response = json.loads(line)
                if response.get('id') != identifier:
                    continue
                if 'error' in response:
                    raise RuntimeError('mcp_error: ' + json.dumps(response['error']))
                return response['result']
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([self.process.stdout], [], [], remaining)[0]:
                raise TimeoutError('outcome_unknown: request not retried')
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError('mcp_disconnected: outcome may be unknown')
            self.buffer += chunk
            if len(self.buffer) > 64 * 1024 * 1024:
                raise RuntimeError('mcp_response_too_large')

    def command(self, identifier, params):
        result = self.request('tools/call', {'name': 'run_command', 'arguments': {'command': identifier, 'params': params}})
        if result.get('isError'):
            raise RuntimeError('command_failed: ' + identifier + ': ' + json.dumps(result.get('content')))
        content = result.get('content', [])
        texts = [entry['text'] for entry in content if entry.get('type') == 'text']
        if len(texts) != 1:
            raise RuntimeError('unexpected_command_result')
        return json.loads(texts[0])

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
