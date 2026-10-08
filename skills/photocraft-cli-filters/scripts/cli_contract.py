"""原生 argv 的离线预检；原生执行和输出格式继续由锁定 CLI 持有。"""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EDITING = {'run', 'batch', 'droplet', 'convert'}
FLAGS = {
    'run': ({'--new', '--cmd', '--params', '--out', '--format', '--quality'}, set()),
    'batch': ({'--actions', '--in', '--out', '--format', '--quality'}, set()),
    'droplet': ({'--out'}, set()),
    'convert': ({'--format', '--quality'}, set()),
}


def load(name):
    spec = importlib.util.spec_from_file_location('native_cli_' + name, ROOT / (name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def reject(code, path):
    raise ValueError(code + ': ' + path)


def json_value(text, path):
    try:
        return load('strict_json').loads(text)
    except ValueError as error:
        message = str(error)
        if ': $' in message:
            raise ValueError(message.replace(': $', ': ' + path, 1)) from None
        reject('invalid_json', path)


def command(identifier, params, path, id_path):
    commands = load('commands')
    if not isinstance(identifier, str) or identifier not in {r['id'] for r in commands.catalog()['commands']}:
        reject('unknown_command', id_path)
    # 原生 argv 不解释工作流 $ref/$output；按已解析字面值校验，不能假造绑定。
    commands.validate_parameters(identifier, params, path, resolved=True)


def actions(value, path, batch=False):
    """固定维护版 batch 只接受对象；droplet 另支持元组和裸 ID。"""
    if not isinstance(value, list):
        reject('invalid_action', path)
    for index, step in enumerate(value):
        location = path + '[' + str(index) + ']'
        if batch and not isinstance(step, dict):
            reject('invalid_action_step', location)
        if isinstance(step, str):
            identifier, params, id_path, param_path = step, {}, location, location
        elif isinstance(step, list) and step:
            identifier = step[0]; params = step[1] if len(step) > 1 else {}
            id_path, param_path = location + '[0]', location + '[1]'
        elif isinstance(step, dict):
            key = 'command' if 'command' in step else 'id'
            identifier, params = step.get(key), step.get('params', {})
            id_path, param_path = location + '.' + key, location + '.params'
        else:
            reject('invalid_action_step', location)
        command(identifier, params, param_path, id_path)


def preflight(argv):
    """不写目录、不安装、不启动会话，使用当前技能登记的完整命令参数合同。"""
    sub = argv[0]
    if sub not in EDITING:
        return
    values, bare = FLAGS[sub]; positional = []; flags = []; index = 1
    while index < len(argv):
        token = argv[index]; path = '$argv[' + str(index) + ']'
        if token.startswith('--') and '=' in token:
            key, value = token.split('=', 1)
            if key not in values:
                reject('invalid_cli_option', path)
        elif token in values:
            key = token; index += 1
            if index >= len(argv):
                reject('missing_cli_value', path)
            value = argv[index]; path = '$argv[' + str(index) + ']'
        elif token in bare:
            key, value = token, None
        elif token.startswith('--'):
            reject('invalid_cli_option', path)
        else:
            positional.append((token, path)); index += 1; continue
        flags.append((key, value, path)); index += 1
    last = {key: (value, path) for key, value, path in flags}
    if '--quality' in last:
        value, path = last['--quality']
        if not re.fullmatch(r'\+?[0-9]+', value) or not 1 <= int(value) <= 100:
            reject('invalid_quality', path)
    if sub == 'run':
        if not ((len(positional) == 1 and '--new' not in last) or (not positional and '--new' in last)):
            reject('invalid_run_input', '$argv')
        if '--new' in last:
            value, path = last['--new']; command('file.new', json_value(value, path), path, path)
        previous = None
        for key, value, path in flags:
            if key == '--cmd':
                command(value, {}, path, path); previous = value
            elif key == '--params':
                if previous is None:
                    reject('params_without_command', path)
                command(previous, json_value(value, path), path, path)
        if previous is None and '--out' not in last:
            reject('run_operation_required', '$argv')
    elif sub == 'convert':
        if len(positional) != 2:
            reject('invalid_convert_inputs', '$argv')
    elif sub == 'batch':
        if positional or any(key not in last for key in ('--actions', '--in', '--out')):
            reject('invalid_batch_inputs', '$argv')
        filename, path = last['--actions']; value = json_value(Path(filename).read_text(), path)
        if isinstance(value, dict) and 'actions' in value:
            value, path = value['actions'], path + '.actions'
        actions(value, path, batch=True)
    else:
        if len(positional) < 2:
            reject('invalid_droplet_inputs', '$argv')
        filename, path = positional[0]; value = json_value(Path(filename).read_text(), path)
        if not isinstance(value, dict) or 'photocraftDroplet' not in value or not isinstance(value.get('action'), dict) or 'steps' not in value['action']:
            reject('invalid_droplet', path)
        actions(value['action']['steps'], path + '.action.steps')
