"""维护版 run／batch／convert／droplet 的逐回复监督器；确认前停止，不重放命令。

公开argv编辑入口与内部测试共用；仅匹配显式 supervised-run 协议的固定维护运行时。
流式mcp／serve和嵌套聚合合同仍单独验收。
"""
import importlib.util
import json
import os
from pathlib import Path
import select
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent
SCHEMA = 'photocraft-supervised-run/v1'
# 固定 f114f621 crates/codecs/src/format.rs 的可读扩展；AVIF 仅写，不能选入。
BATCH_CODEC_EXTENSIONS = frozenset('png apng jpg jpeg jpe jfif tif tiff webp gif bmp dib tga icb vda vst ico pnm pbm pgm ppm pam pfm qoi exr hdr'.split())


def load(name):
    spec = importlib.util.spec_from_file_location('supervised_run_' + name, ROOT / (name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def expected_events(argv):
    """由预检后的原生 argv 生成身份序列，不启动进程或写输出。"""
    contract = load('cli_contract')
    if not argv or argv[0] not in {'run','convert'}:
        raise ValueError('unsupported_supervised_subcommand: $argv')
    contract.preflight(argv)
    positional, flags, last = contract.parse_argv(argv)
    if argv[0] == 'convert':
        arguments = {'path':positional[1][0]}
        if '--format' in last:
            arguments['format'] = last['--format'][0]
        if '--quality' in last:
            arguments['quality'] = int(last['--quality'][0])
        return [('doc_open',{'path':positional[0][0]},False),('doc_save',arguments,False)]
    events = []
    if '--new' in last:
        value, path = last['--new']
        events.append(('doc_new', contract.json_value(value, path), False))
    else:
        events.append(('doc_open', {'path': positional[0][0]}, False))
    commands = []
    for key, value, path in flags:
        if key == '--cmd':
            commands.append({'id':value, 'params':{}})
        elif key == '--params':
            commands[-1]['params'] = contract.json_value(value, path)
    events.extend(('command_run', command, True) for command in commands)
    if '--out' in last:
        arguments = {'path':last['--out'][0]}
        if '--format' in last:
            arguments['format'] = last['--format'][0]
        if '--quality' in last:
            arguments['quality'] = int(last['--quality'][0])
        events.append(('doc_save', arguments, False))
    return events


def capability_error(reason):
    """固定原生的只读元数据查询失败，尚未发送任何编辑。"""
    return load('operation_errors').OperationError('supervision unavailable: '+reason,
        'supervision_unavailable',phase='capabilities',outcome='not_executed',recovery_action='prepare_supported_runtime')


def supervision_info(executable, subcommand, timeout):
    """编辑前检查显式监督能力；二进制来源锁仍由调用方验证。"""
    if timeout <= 0:
        raise capability_error('deadline_expired')
    try:
        reply = subprocess.run([str(executable),'--supervision-info'],capture_output=True,text=True,timeout=min(30,timeout))
        if reply.returncode != 0:
            raise ValueError('metadata_query_failed')
        value = load('strict_json').loads(reply.stdout)
        fields = {'schema','protocol','runtimeVersion','subcommands','acknowledgment'}
        if (not isinstance(value,dict) or set(value) != fields
                or value['schema'] != 'photocraft-supervision-info/v1' or value['protocol'] != SCHEMA
                or not isinstance(value['runtimeVersion'],str)
                or re.fullmatch(r'\d+\.\d+\.\d+(?:-craft\.[1-9]\d*)?',value['runtimeVersion']) is None
                or not isinstance(value['subcommands'],list)
                or any(not isinstance(item,str) or item not in {'run','batch','convert','droplet'} for item in value['subcommands'])
                or len(set(value['subcommands'])) != len(value['subcommands'])
                or subcommand not in value['subcommands'] or value['acknowledgment'] != 'continue <sequence>\n'):
            raise ValueError('metadata_contract_mismatch')
        return value
    except (ValueError,OSError,UnicodeError,subprocess.SubprocessError):
        raise capability_error('metadata_invalid_or_unsupported') from None


def batch_plan(argv):
    """绑定固定目录规则、动作与结果清单；任何输出目录写入之前调用。"""
    contract = load('cli_contract'); contract.preflight(argv)
    _, _, last = contract.parse_argv(argv)
    action_path, location = last['--actions']
    value = contract.json_value(Path(action_path).read_text(), location)
    if isinstance(value, dict) and 'actions' in value:
        value = value['actions']; location += '.actions'
    # 再次读取的内容也需预检；原生随后必须返回完全一致的规范化动作。
    contract.actions(value, location, batch=True)
    actions = [{'id':row['command'] if 'command' in row else row['id'], 'params':row.get('params',{})} for row in value]
    input_dir, output_dir = last['--in'][0], last['--out'][0]
    paths = []
    with os.scandir(input_dir) as entries:
        for entry in entries:
            extension = os.path.splitext(entry.name)[1][1:].lower()
            recognized = (extension in {'pcraft','psd','psb'} or extension.rsplit('\\',1)[-1] in BATCH_CODEC_EXTENSIONS)
            try:
                regular = entry.is_file()
            except OSError:
                regular = False
            if regular and recognized:
                paths.append(entry.path)
    paths.sort()
    files = []
    for path in paths:
        stem, suffix = os.path.splitext(os.path.basename(path))
        extension = last['--format'][0] if '--format' in last else suffix[1:]
        files.append({'input':path, 'target':os.path.join(output_dir,stem+'.'+extension)})
    config = {'actions':action_path, 'in':input_dir, 'out':output_dir}
    if '--format' in last:
        config['format'] = last['--format'][0]
    if '--quality' in last:
        config['quality'] = int(last['--quality'][0])
    events = [('batch_plan',config,False)]; lines = {}
    for row in files:
        events.append(('doc_open',{'path':row['input']},False))
        events.extend(('command_run',action,False) for action in actions)
        extension = last['--format'][0] if '--format' in last else os.path.splitext(row['input'])[1][1:]
        arguments = {'path':row['target'],'format':extension}
        if '--quality' in last:
            arguments['quality'] = int(last['--quality'][0])
        events.append(('doc_save',arguments,False))
        lines[len(events)] = 'ok    '+row['input']+' -> '+row['target']+'\n'
    events.append(('batch_complete',{},False))
    lines[len(events)] = str(len(files))+' succeeded, 0 failed\n'
    checks = {1:{'files':files,'steps':actions},len(events):{'succeeded':len(files),'failed':0}}
    return events, checks, lines


# 固定引擎 file_cmds::OPENABLE；不能套用 CLI batch 的另一份解码能力表。
DROPLET_OPENABLE = {'psd','psb','pcraft','png','jpg','jpeg','tif','tiff','webp','gif','bmp','tga','exr','hdr','qoi','ico','pnm','ppm','pgm','dng','cr2','nef','nrw','arw','pef'}


def droplet_plan(argv):
    """独立绑定原引擎的输入顺序、重复文件、动作、输出及0–12质量语义。"""
    contract = load('cli_contract'); contract.preflight(argv)
    positional, _, last = contract.parse_argv(argv)
    filename, location = positional[0]
    value = contract.json_value(Path(filename).read_text(), location)
    steps = value['action']['steps']; contract.actions(steps,location+'.action.steps')
    actions = []
    for step in steps:
        if isinstance(step,str):identifier,params=step,{}
        elif isinstance(step,list):identifier,params=step[0],step[1] if len(step)>1 else {}
        else:identifier,params=step['command'] if 'command' in step else step['id'],step.get('params',{})
        actions.append({'id':identifier,'params':params})
    ascii_case=str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')
    raw = [item[0] for item in positional[1:]];inputs=[]
    for path in raw:
        if os.path.isdir(path):
            paths=[]
            with os.scandir(path) as entries:
                for entry in entries:
                    extension=os.path.splitext(entry.name)[1][1:].translate(ascii_case)
                    try:regular=entry.is_file()
                    except OSError:regular=False
                    if regular and extension in DROPLET_OPENABLE:paths.append(entry.path)
            inputs.extend(sorted(paths))
        else:inputs.append(path)
    if not inputs:raise ValueError('no_droplet_inputs: $argv')
    opts=value.get('options',{});opts=opts if isinstance(opts,dict) else {}
    output=last['--out'][0] if '--out' in last else opts.get('output')
    if not isinstance(output,str):output=os.path.join(os.path.dirname(inputs[0]),'droplet-output')
    if not output:raise ValueError('invalid_droplet_output: $argv')
    format=opts.get('format','same');format=format if isinstance(format,str) else 'same'
    quality=opts.get('quality');quality=float(quality) if isinstance(quality,(int,float)) and not isinstance(quality,bool) else None
    def join(directory,name):return directory+('' if directory.endswith(('/','\\')) else '/')+name if directory else name
    files=[]
    for path in inputs:
        name=re.split(r'[/\\]',path)[-1];at=name.rfind('.');stem=name[:at] if at>0 else name
        extension=path.rsplit('.',1)[-1].translate(ascii_case) if format=='same' else format.lstrip('.').translate(ascii_case)
        files.append({'input':path,'target':join(output,stem+'.'+extension)})
    config={'droplet':filename,'input':raw}
    if '--out' in last:config['output']=last['--out'][0]
    events=[('droplet_plan',config,False)];lines={}
    for row in files:
        events.append(('doc_open',{'path':row['input']},False));events.extend(('command_run',action,False) for action in actions)
        arguments={'path':row['target']}
        if quality is not None:arguments['quality']=quality
        events.append(('doc_save',arguments,False));lines[len(events)]='ok    '+row['target']+'\n'
    events.append(('droplet_complete',{},False))
    checks={1:{'files':files,'steps':actions,'quality':quality},len(events):{'files':[row['target'] for row in files],'errors':[]}}
    return events,checks,lines


def execute(executable, argv, output, timeout=600, stderr=None, runtime_version=None):
    """运行固定候选并逐项校验；异常附带已核验回执和最后请求，绝不重试。

    executable 必须由调用方完成锁校验；output 接收原公开 JSON 命令行。
    """
    expected, checks, lines = (batch_plan(argv) if argv and argv[0] == 'batch' else
        droplet_plan(argv) if argv and argv[0] == 'droplet' else (expected_events(argv), {}, {}))
    errors = load('operation_errors'); commands = load('commands')
    receipts = []; last_attempt = None
    deadline = time.monotonic() + timeout
    supervision = supervision_info(executable,argv[0],timeout)
    if runtime_version is not None and supervision['runtimeVersion'] != runtime_version:
        raise capability_error('runtime_version_mismatch')
    if time.monotonic() >= deadline:
        raise capability_error('deadline_expired')
    process = subprocess.Popen([str(executable), argv[0], '--supervised', *argv[1:]],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)
    buffer = b''
    def unknown(reason):
        return errors.error('outcome_unknown: ' + reason + '; request not retried')
    def line():
        nonlocal buffer
        while True:
            if b'\n' in buffer:
                value, buffer = buffer.split(b'\n', 1)
                return value
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([process.stdout], [], [], remaining)[0]:
                raise unknown('supervised_reply_timeout')
            chunk = os.read(process.stdout.fileno(), 65536)
            if not chunk:
                raise unknown('supervised_reply_disconnected')
            buffer += chunk
            if len(buffer) > 64 * 1024 * 1024:
                raise unknown('supervised_reply_too_large')
    try:
        for sequence, (tool, arguments, visible) in enumerate(expected, 1):
            last_attempt = {'tool':tool, 'arguments':arguments, 'sequence':sequence, 'phase':'submitted'}
            try:
                raw = line()
                last_attempt['phase'] = 'reply_received'
                event = load('strict_json').loads(raw)
            except (ValueError, UnicodeError) as error:
                raise unknown('invalid_supervised_json') from error
            # 原生此时正在等待确认，不可能合法发送下一帧；不能先确认再发现额外回复。
            if buffer:
                raise unknown('unsolicited_supervised_frame')
            fields = {'schema', 'sequence', 'tool', 'arguments', 'visible'}
            if (not isinstance(event, dict) or set(event) not in (fields | {'result'}, fields | {'error'})
                    or event['schema'] != SCHEMA or type(event['sequence']) is not int or event['sequence'] != sequence
                    or event['tool'] != tool or type(event['visible']) is not bool or event['visible'] != visible
                    or json.dumps(event['arguments'], sort_keys=True) != json.dumps(arguments, sort_keys=True)):
                raise unknown('invalid_supervised_identity')
            if 'error' in event:
                if not isinstance(event['error'], str) or not event['error']:
                    raise unknown('invalid_supervised_error')
                raise errors.error('command_failed: ' + event['error'])
            # 复用普通工作流语义，原生合法标量／列表等 JSON 输出不擅自收窄。
            result = commands.parse_reply({'content':[{'type':'text', 'text':json.dumps(event['result'], allow_nan=False)}]})
            result = commands.validate_tool_reply(tool, result, arguments)
            if tool == 'doc_save' and result['path'] != arguments['path']:
                raise unknown('supervised_save_path_mismatch')
            if tool == 'doc_open' and 'path' in result and result['path'] != arguments['path']:
                raise unknown('supervised_open_path_mismatch')
            if sequence in checks and json.dumps(result,sort_keys=True) != json.dumps(checks[sequence],sort_keys=True):
                raise unknown('invalid_supervised_batch_result')
            last_attempt['phase'] = 'reply_validated'
            receipts.append({'tool':tool, 'arguments':arguments, 'result':result, 'sequence':sequence})
            if visible:
                output.write(json.dumps({'command':arguments['id'], 'result':result}, ensure_ascii=False) + '\n')
                output.flush()
            if sequence in lines:
                output.write(lines[sequence]); output.flush()
            try:
                process.stdin.write(('continue ' + str(sequence) + '\n').encode())
                process.stdin.flush()
            except OSError as error:
                raise unknown('supervised_confirmation_disconnected') from error
        process.stdin.close()
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise unknown('supervised_exit_timeout')
        try:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([process.stdout], [], [], remaining)[0]:
                raise unknown('supervised_exit_timeout')
            remainder = os.read(process.stdout.fileno(), 1)
            if remainder or buffer:
                raise unknown('unexpected_supervised_reply')
            code = process.wait(timeout=max(0.001, deadline-time.monotonic()))
        except subprocess.TimeoutExpired as error:
            raise unknown('supervised_exit_timeout') from error
        if code != 0:
            raise unknown('supervised_exit_nonzero')
        return {'result':'PASS', 'receipts':receipts, 'lastAttempt':last_attempt, 'replay':False, 'supervision':supervision}
    except BaseException as error:
        if getattr(error,'phase',None)=='submitted' and last_attempt and last_attempt['phase']=='reply_received':
            error.phase='reply_received'
        error.receipts = receipts
        error.lastAttempt = last_attempt
        raise
    finally:
        if not process.stdin.closed:
            try:
                process.stdin.close()
            except OSError:
                pass
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait()
        process.stdout.close()
