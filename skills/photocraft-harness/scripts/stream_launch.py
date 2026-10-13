"""固定原生流式启动配置的只读预检；不连接、不安装、不创建凭据。"""
import os
from pathlib import Path
import re

# 对齐固定原生 Args 解析：最后一次赋值生效，未知选项和位置参数仍由原生处理。
VALUE_FLAGS = {'--format','--quality','--new','--cmd','--params','--out','--actions',
               '--in','--filter','--bridge','--port','--control-token','--control-token-file',
               '--automation-read-root','--automation-write-root'}


def reject(code, path):
    """只返回错误码及位置，不把目录、令牌或文件正文放进诊断。"""
    raise ValueError(code + ': ' + path)


def preflight(argv):
    """检查当前生效的原生配置；运行时仍负责目录能力及实际连接。"""
    flags = {}; index = 1
    while index < len(argv):
        token = argv[index]; path = '$argv[' + str(index) + ']'
        if token.startswith('--') and '=' in token:
            key, value = token.split('=', 1); flags[key] = (value, path)
        elif token in VALUE_FLAGS:
            if index + 1 >= len(argv):reject('missing_option_value', path)
            index += 1; flags[token] = (argv[index], '$argv[' + str(index) + ']')
        elif token.startswith('--'):
            flags[token] = (None, path)
        index += 1

    bridge, bridge_path = flags.get('--bridge', (None, '$argv'))
    if argv[0] == 'mcp' and bridge is not None:
        # 与原生构造器相同：地址的连接/端口错误仍在实际调用阶段报告。
        host = bridge.rsplit(':', 1)[0] if ':' in bridge else bridge
        if host not in {'127.0.0.1','localhost','[::1]','::1'}:
            reject('bridge_not_loopback', bridge_path)
        token, token_path = flags.get('--control-token', (None, '$env.PHOTOCRAFT_CONTROL_TOKEN'))
        file, file_path = flags.get('--control-token-file', (None, '$env.PHOTOCRAFT_CONTROL_TOKEN_FILE'))
        if token is None:token = os.environ.get('PHOTOCRAFT_CONTROL_TOKEN')
        if file is None:file = os.environ.get('PHOTOCRAFT_CONTROL_TOKEN_FILE')
        if token is not None and file is not None:reject('control_token_conflict', file_path)
        if token is None:
            if file is None:reject('control_token_required', '$argv')
            try:token = Path(file).read_text(encoding='utf-8').strip()
            except (OSError,ValueError,UnicodeError):reject('control_token_file_invalid', file_path)
            token_path = file_path
        if not re.fullmatch(r'[0-9a-fA-F]{64}', token):reject('control_token_invalid', token_path)
        return

    # bridge MCP 不使用这些根；headless MCP 与 serve stdio 才持有目录能力。
    for key in ['--automation-read-root','--automation-write-root']:
        value, path = flags.get(key, (None, '$argv'))
        if value is None:continue
        try:valid = bool(value) and Path(value).is_dir()
        except (OSError,ValueError):valid = False
        if not valid:reject('automation_root_invalid', path)
