#!/usr/bin/env python3
"""完整原生命令的单技能入口：参数说明、实时前置检查、同会话调用及失败回执。"""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
import shutil
from pathlib import Path
import re
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
DOMAIN = json.loads((ROOT / "scripts/runtime.lock.json").read_text())["artifact"].removesuffix("-cli")
ROUTES = {
    "filmcraft": ("command_list", "command_run", "id"),
    "effectcraft": ("list_commands", "execute_command", "command"),
    "photocraft": ("command_list", "command_run", "id"),
    "vectorcraft": ("list_commands", "run_command", "command"),
}

def catalog():
    return json.loads((ROOT / "references/command-coverage.json").read_text())

def load(name):
    spec = importlib.util.spec_from_file_location("craft_command_" + name, ROOT / "scripts" / (name + ".py"))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

def validate_parameters(identifier, params, path='$.params', resolved=False):
    rows={row['id']:row for row in catalog()['commands']}
    return load('parameter_contract').validate(identifier,params,rows,path,resolved)

def validate_tool_parameters(identifier, params, path='$.params', resolved=False):
    snapshot=json.loads((ROOT/'references/native-command-snapshot.json').read_text())
    tools={tool['name']:tool for tool in snapshot['tools']}
    if identifier not in tools:raise ValueError('unknown_tool: '+identifier)
    load('parameter_contract').validate_schema(params,tools[identifier]['inputSchema'],path,resolved,close=True)
    if identifier=='command_batch':
        contract=load('parameter_contract')
        if not resolved and contract.is_reference(params['steps']):return params
        if len(params['steps'])>256:raise ValueError('invalid_batch_steps: '+path+'.steps')
        for index,step in enumerate(params['steps']):
            if not resolved and contract.is_reference(step):continue
            command=step['id'];location=path+'.steps['+str(index)+']'
            if not resolved and load('parameter_contract').is_reference(command):continue
            if not isinstance(command,str) or command not in {row['id'] for row in catalog()['commands']}:raise ValueError('unknown_command: '+location+'.id')
            if set(step)-{'id','params'}:raise ValueError('parameter_unknown_field: '+location)
            values=step.get('params')
            if not resolved and contract.is_reference(values):continue
            validate_parameters(command,{} if values is None else values,location+'.params',resolved)
    return params

def command_ids(step):
    if 'command' in step:return [step['command']]
    if step.get('tool')==ROUTES[DOMAIN][1] and isinstance(step.get('params',{}).get(ROUTES[DOMAIN][2]),str):return [step['params'][ROUTES[DOMAIN][2]]]
    if step.get('tool')=='command_batch' and isinstance(step['params'].get('steps'),list):
        return [item['id'] for item in step['params']['steps'] if isinstance(item,dict) and isinstance(item.get('id'),str)]
    return []

def output_path(value):
    if not isinstance(value, str) or not value or "\\" in value or Path(value).is_absolute() or any(p in ("", ".", "..") for p in value.split("/")) or value.split("/")[0] in {"journal.json", "success.json", "failure.json", "inputs", "tool-images", "desktop-session.json", "desktop.log", ".desktop-data", "artcraft-domain-command.json"}:
        raise ValueError("invalid_output_path")
    return value

def references(value, aliases, path='$'):
    if isinstance(value, dict):
        if set(value) == {"$output"}:
            output_path(value["$output"])
        elif set(value) == {"$ref"}:
            text = value["$ref"]
            if not isinstance(text, str) or not re.fullmatch(r"[a-zA-Z][\w-]*(?:\.[\w-]+)*", text):
                raise ValueError('invalid_reference: '+path)
            if text.split(".")[0] not in aliases:
                raise ValueError('forward_or_unknown_reference: '+path+' => '+text)
        else:
            for key,child in value.items():
                references(child, aliases,path+'.'+str(key))
    elif isinstance(value, list):
        for index,child in enumerate(value):
            references(child, aliases,path+'['+str(index)+']')

def validate(plan, input_names=()):
    if not isinstance(plan, dict):
        raise ValueError('invalid_command_plan: $')
    unknown = set(plan) - {'schema', 'operations'}
    if unknown:
        raise ValueError('invalid_command_plan: $.' + sorted(unknown)[0])
    if plan.get('schema') != 'craft-command-plan/v1':
        raise ValueError('invalid_command_plan: $.schema')
    if not isinstance(plan.get('operations'), list) or not 1 <= len(plan['operations']) <= 1000:
        raise ValueError('invalid_command_plan: $.operations')
    rows = {r["id"]: r for r in catalog()["commands"]}
    tools = set(catalog()["nativeTools"])
    aliases = {"output", *input_names}
    for index, step in enumerate(plan["operations"]):
        location = '$.operations[' + str(index) + ']'
        if not isinstance(step, dict):
            raise ValueError('invalid_operation: ' + location)
        unknown = set(step) - {'command', 'tool', 'params', 'as'}
        if unknown:
            raise ValueError('invalid_operation: ' + location + '.' + sorted(unknown)[0])
        if ("command" in step) == ("tool" in step) or not isinstance(step.get("params"), dict):
            raise ValueError('command_or_tool_and_params_required: ' + location + '.params')
        key = "command" if "command" in step else "tool"
        if not isinstance(step[key], str) or step[key] not in (rows if key == "command" else tools):
            raise ValueError('unknown_' + key + ': ' + location + '.' + key)
        try:
            json.dumps(step["params"], allow_nan=False)
        except (ValueError, TypeError):
            raise ValueError("invalid_json_parameters: " + str(index)) from None
        if key == "tool" and step[key] == ROUTES[DOMAIN][1]:
            raise ValueError("use_command_operation_for_native_registry")
        references(step["params"], aliases,'$.operations['+str(index)+'].params')
        if key=='command':validate_parameters(step[key],step['params'],'$.operations['+str(index)+'].params')
        else:validate_tool_parameters(step[key],step['params'],'$.operations['+str(index)+'].params')
        alias = step.get("as")
        if alias is not None:
            if not isinstance(alias, str) or not re.fullmatch(r"[a-zA-Z][\w-]*", alias) or alias in aliases:
                raise ValueError('invalid_or_duplicate_alias: ' + location + '.as')
            aliases.add(alias)
    return plan

def resolve(value, bindings):
    if isinstance(value, dict):
        if set(value) == {"$output"}:
            return str(Path(bindings["output"]) / output_path(value["$output"]))
        if set(value) == {"$ref"}:
            try:
                parts = value["$ref"].split(".")
                result = bindings[parts[0]]
                for part in parts[1:]:
                    result = result[int(part)] if isinstance(result, list) else result[part]
                return result
            except (KeyError, IndexError, TypeError, ValueError, AttributeError):
                raise ValueError("unresolved_reference: " + str(value["$ref"])) from None
        return {key: resolve(child, bindings) for key, child in value.items()}
    if isinstance(value, list):
        return [resolve(child, bindings) for child in value]
    return value

def native_call(identifier, params):
    _, tool, key = ROUTES[DOMAIN]
    return tool, {key: identifier, "params": params}


def supervised_batch(params,invoke,confirmed):
    """原生聚合拆为单步确认；累计预算与停止合同不被continue参数绕过。"""
    results=[];remaining=(8<<20)-(1<<20)-4096
    for index,step in enumerate(params['steps']):
        try:
            result=invoke(step)
            row={'ok':True,'result':result}
            size=len(json.dumps(row,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode())+1
            if size>remaining:
                error=load('operation_errors').error('outcome_unknown: command_batch_response_budget');error.phase='reply_received';raise error
            remaining-=size;results.append(row);confirmed(index,step,row)
        except (ValueError,RuntimeError,OSError,TimeoutError,subprocess.SubprocessError) as error:
            error.aggregate={'stepIndex':index,'confirmedSteps':len(results),'request':step}
            error.partialResult={'completed':len(results),'failed':0,'results':results}
            raise
    return {'completed':len(results),'failed':0,'results':results}

def reply_json(text):
    return load('strict_json').loads(text)

def validate_tool_reply(identifier,result,params):
    if identifier in {'doc_new', 'doc_open'}:
        indices = [result[key] for key in ('index', 'document') if isinstance(result, dict) and key in result]
        # 桌面 doc_open 返回路径与警告，headless 返回索引；两者都是真实合法合同。
        path_reply = (identifier == 'doc_open' and isinstance(result, dict)
                      and isinstance(result.get('path'), str) and bool(result['path'])
                      and ('warnings' not in result or isinstance(result['warnings'], list)))
        if ((not indices and not path_reply) or any(type(value) is not int or value < 0 for value in indices)
                or indices and len(set(indices)) != 1):
            raise load('operation_errors').error('outcome_unknown: invalid_document_reply')
    if identifier == 'doc_inspect':
        if (not isinstance(result, dict)
                or any(type(result.get(key)) is not int or result[key] <= 0 for key in ('width', 'height'))
                or not isinstance(result.get('layers'), list)
                or any(not isinstance(layer, dict) for layer in result['layers'])):
            raise load('operation_errors').error('outcome_unknown: invalid_inspection_reply')
    # 保存回执必须证明具体返回路径；标量、空对象或附件不是已确认的保存结果。
    # 扩展字段保持兼容，未知结果不能绑定为下一项编辑的输入。
    if identifier in {'doc_save', 'doc_export'}:
        if (not isinstance(result, dict) or not isinstance(result.get('path'), str)
                or not result['path'] or ('warnings' in result and not isinstance(result['warnings'], list))):
            raise load('operation_errors').error('outcome_unknown: invalid_save_reply')
    if identifier=='command_batch':
        counts=('completed','failed')
        if (not isinstance(result,dict) or any(type(result.get(k)) is not int or result[k]<0 for k in counts)
                or not isinstance(result.get('results'),list) or any(not isinstance(row,dict) or type(row.get('ok')) is not bool for row in result['results'])
                or result['completed']+result['failed']!=len(result['results']) or result['failed']!=sum(not row['ok'] for row in result['results'])
                or len(result['results'])>len(params['steps'])):
            raise load('operation_errors').error('outcome_unknown: invalid_batch_reply')
        if result['failed'] or result['completed'] != len(params['steps']):
            error = load('operation_errors').error('outcome_unknown: partial_batch; inspect completed steps, no replay')
            error.partialResult = result
            raise error
    return result


def parse_reply(reply, output=None, index=0):
    if (not isinstance(reply, dict)
            or ('isError' in reply and not isinstance(reply['isError'], bool))
            or not isinstance(reply.get('content'), list)
            or any(not isinstance(item, dict) or not isinstance(item.get('type'), str)
                   or (item.get('type') == 'text' and not isinstance(item.get('text'), str))
                   for item in reply['content'])):
        raise load("operation_errors").error('outcome_unknown: invalid_tool_reply')
    if reply.get("isError"):
        raise load("operation_errors").error("command_failed: " + json.dumps(reply.get("content"), ensure_ascii=False))
    content = reply.get("content", [])
    texts = [item["text"] for item in content if item.get("type") == "text"]
    if len(content) == 1 and len(texts) == 1:
        try:
            result = reply_json(texts[0])
        except json.JSONDecodeError:
            if output is None:
                raise load("operation_errors").error("outcome_unknown: unexpected_reply") from None
        except (ValueError, TypeError):
            raise load("operation_errors").error('outcome_unknown: unsafe_json_reply') from None
        else:
            if isinstance(result, dict) and result.get("error"):
                raise load("operation_errors").error("semantic_error: " + json.dumps(result, ensure_ascii=False))
            return result
    if output is None or not content:
        raise load("operation_errors").error("outcome_unknown: unexpected_reply")
    # 原生工具允许图片和普通文字；附件落盘，日志不保留大块 base64。
    result = {"content": []}
    for number, item in enumerate(content):
        if item.get("type") == "text":
            try:
                parsed = reply_json(item["text"])
            except json.JSONDecodeError:
                parsed = item["text"]
            except (ValueError, TypeError):
                raise load("operation_errors").error('outcome_unknown: unsafe_json_reply') from None
            if isinstance(parsed, dict) and parsed.get("error"):
                raise load("operation_errors").error("semantic_error: " + json.dumps(parsed, ensure_ascii=False))
            result["content"].append({"type": "text", "value": parsed})
        elif item.get("type") == "image" and item.get("mimeType") in ("image/png", "image/jpeg", "image/webp"):
            extension = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}[item["mimeType"]]
            try:
                data = base64.b64decode(item["data"], validate=True)
            except (ValueError, KeyError, TypeError):
                raise load("operation_errors").error("outcome_unknown: invalid_image_reply") from None
            path = Path(output) / "tool-images" / (str(index) + "-" + str(number) + "." + extension)
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(data)
            result["content"].append({"type": "image", "mimeType": item["mimeType"],
                "path": str(path.relative_to(output)), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        else:
            raise load("operation_errors").error("outcome_unknown: unsupported_tool_content")
    return result

def backend_argv(executable, output, mode="headless", connect=None, token_file=None):
    if mode not in ("headless", "bridge"):
        raise ValueError("invalid_mode")
    if mode == "headless":
        if connect or token_file:
            raise ValueError("bridge_options_in_headless_mode")
        argv = [executable, "--empty", "mcp"] if DOMAIN == "effectcraft" else [executable, "mcp"]
        if DOMAIN == "vectorcraft":
            argv.append("--headless")
    else:
        if not isinstance(connect, str) or not re.fullmatch(r"127\.0\.0\.1:([1-9][0-9]{0,4})", connect):
            raise ValueError("explicit_loopback_connection_required")
        if int(connect.rsplit(":", 1)[1]) > 65535:
            raise ValueError("invalid_port")
        if DOMAIN == "vectorcraft":
            argv = [executable, "mcp", "--connect", connect]
        elif DOMAIN == "effectcraft":
            argv = [executable, "mcp", "--bridge", connect.rsplit(":", 1)[1]]
        else:
            argv = [executable, "mcp", "--bridge", connect]
    if DOMAIN == "photocraft":
        argv += ["--automation-read-root", str(output), "--automation-write-root", str(output)]
        if token_file:
            token = Path(token_file)
            if not token.is_file():
                raise ValueError("missing_control_token_file")
            argv += ["--control-token-file", str(token.resolve())]
    elif token_file:
        raise ValueError("control_token_option_only_for_photocraft")
    return argv

def write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)

def runtime_rows(session, params=None):
    reply = session.request("tools/call", {"name": ROUTES[DOMAIN][0], "arguments": params or {}})
    result = parse_reply(reply)
    rows = result.get("commands") if isinstance(result, dict) else result
    if (not isinstance(rows, list)
            or any(not isinstance(row, dict) or not isinstance(row.get('id'), str)
                   or not row['id'] for row in rows)
            or len({row['id'] for row in rows}) != len(rows)):
        raise load("operation_errors").error("outcome_unknown: unexpected_registry")
    return rows

def execute(plan, output, runtime_home=None, mode="headless", connect=None, token_file=None,
            installer=None, session_factory=None, inputs=None, session_root=None,
            session_identity=None, expected_capabilities=None):
    inputs = inputs or {}
    if not isinstance(inputs, dict) or any(not isinstance(k, str) or not re.fullmatch(r"[a-zA-Z][\w-]*", k) or k == "output" for k in inputs):
        raise ValueError("invalid_input_name")
    sources = {}
    for name, value in inputs.items():
        source = Path(value)
        if source.is_symlink() or not source.is_file():
            raise ValueError("invalid_input_file: " + name)
        with source.open("rb") as stream:
            sources[name] = (source, hashlib.file_digest(stream, "sha256").hexdigest())
    validate(plan, sources)
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise ValueError("output_exists")
    if not output.parent.is_dir():
        raise ValueError("output_parent_missing")
    output = output.absolute()
    # 连续任务的原生沙箱根固定不变；阶段仅在自己的子目录记录和交付。
    backend_root = output
    if session_root is not None:
        backend_root = Path(session_root).absolute()
        if (not backend_root.is_dir() or backend_root.is_symlink()
                or backend_root.resolve() != backend_root
                or output.resolve() != output or not output.is_relative_to(backend_root)):
            raise ValueError('invalid_session_root')
    # 验证连接参数在安装和创建目录之前完成；不偷偷回退到另一会话。
    backend_argv("native", backend_root, mode, connect, token_file)
    if mode=='bridge':
        pinned=reply_json((ROOT/'references/desktop-command-snapshot.json').read_text())
        identifiers={row['id'] for row in pinned['commands']}
        for step in plan['operations']:
            for identifier in command_ids(step):
                if identifier not in identifiers:raise ValueError('backend_command_unavailable: '+identifier)
    plan_bytes = json.dumps(plan, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()
    receipt = {"schema": "craft-command-receipt/v1", "pluginId": DOMAIN,
               "planSha256": hashlib.sha256(plan_bytes).hexdigest(),
               "catalogSha256": hashlib.sha256((ROOT / "references/command-coverage.json").read_bytes()).hexdigest(),
               "mode": mode, "result": "running", "steps": [],
               "creativeAcceptance": "NOT_RUN", "nativeProjectReopenAcceptance": "NOT_RUN"}
    output.mkdir()
    write(output / "journal.json", receipt)
    try:
        installer = installer or load("bootstrap").install
        lock = json.loads((ROOT / "scripts/runtime.lock.json").read_text())
        installed = installer(lock, runtime_home or os.environ.get("CRAFT_RUNTIME_HOME",
                               str(Path.home() / ".local/share/craft-runtimes")))
        receipt["runtimeSha256"] = installed["binarySha256"]
        session_factory = session_factory or load("mcp_session").Session
        bindings = {"output": (str(output.relative_to(backend_root)) if session_root is not None else "") if DOMAIN == "photocraft" else str(output)}
        receipt["inputs"] = {}
        if sources:
            (output / "inputs").mkdir()
        for name, (source, digest) in sources.items():
            target = output / "inputs" / (name + source.suffix)
            shutil.copyfile(source, target)
            with target.open("rb") as stream:
                copied = hashlib.file_digest(stream, "sha256").hexdigest()
            with source.open("rb") as stream:
                after = hashlib.file_digest(stream, "sha256").hexdigest()
            if copied != digest or after != digest:
                raise ValueError("input_changed: " + name)
            relative = str(target.relative_to(output))
            native_relative = str(target.relative_to(backend_root)) if session_root is not None else relative
            bindings[name] = {"path": native_relative if DOMAIN == "photocraft" else str(target), "sha256": digest}
            receipt["inputs"][name] = {"path": relative, "sha256": digest}
        with session_factory(backend_argv(installed["executable"], backend_root, mode, connect, token_file)) as session:
            discovery = session.request("tools/list", {})
            if (not isinstance(discovery, dict) or not isinstance(discovery.get('tools'), list)
                    or any(not isinstance(tool, dict) or not isinstance(tool.get('name'), str)
                           or not tool['name'] for tool in discovery['tools'])):
                raise load("operation_errors").error('outcome_unknown: unexpected_tools_reply')
            available = {tool['name'] for tool in discovery['tools']}
            required = {native_call(s["command"], {})[0] if "command" in s else s["tool"]
                        for s in plan["operations"]}
            if 'command_batch' in required:required.add(ROUTES[DOMAIN][1])
            # 目录查询也是原生能力合同；旧服务不能冒充新入口。
            if not required.issubset(available) or ROUTES[DOMAIN][0] not in available:
                raise load("operation_errors").error("native_tool_missing")
            current = {r["id"]: r for r in runtime_rows(session)}
            expected = {r["id"] for r in catalog()["commands"]}
            if mode!='bridge' and not expected.issubset(current):
                raise load("operation_errors").error("capability_missing: native_registry_drift")
            receipt["registeredCommands"] = len(current)
            gate=load('capabilities').Gate(session,sys.modules.get(__name__) or load('commands'),installed['binarySha256'],mode,runtime_identity=installed.get('runtimeIdentity'))
            if session_identity is not None:gate.session_id=session_identity
            receipt['capabilitySnapshot']=gate.check();receipt['capabilityChecks']=gate.checks
            if expected_capabilities is not None:load('capabilities').ensure(expected_capabilities,receipt['capabilitySnapshot'])
            for index, step in enumerate(plan["operations"]):
                params = resolve(step["params"], bindings)
                if 'command' in step:validate_parameters(step['command'],params,'$.operations['+str(index)+'].params',True)
                else:validate_tool_parameters(step['tool'],params,'$.operations['+str(index)+'].params',True)
                gate.check_scope(command_ids({**step,'params':params}),[native_call(step['command'],{})[0] if 'command' in step else step['tool']])
                if mode=='bridge':
                    for identifier in command_ids({**step,'params':params}):
                        if identifier not in current:raise ValueError('backend_command_unavailable: '+identifier)
                record = {"index": index, "command": step.get("command"), "tool": step.get("tool"),
                          "params": params, "state": "started"}
                if "command" in step:
                    states = {r["id"]: r for r in runtime_rows(session, {"filter": step["command"]})}
                    row = states.get(step["command"])
                    if row is None or row.get("enabled") is not True:
                        record["state"] = "blocked"
                        record["reason"] = row.get("why", "native_context_disabled") if row else "native_command_missing"
                        receipt["steps"].append(record)
                        raise load("operation_errors").error("precondition_failed: " + step["command"] + ": " + record["reason"])
                    tool, args = native_call(step["command"], params)
                else:
                    tool, args = step["tool"], params
                receipt["steps"].append(record)
                record['phase'] = 'submitted'
                write(output / "journal.json", receipt)
                try:
                    if tool=='command_batch':
                        original_timeout=getattr(session,'timeout',120);deadline=time.monotonic()+original_timeout
                        record['substeps']=[]
                        def invoke(child):
                            if hasattr(session,'timeout'):session.timeout=deadline-time.monotonic()
                            if time.monotonic()>=deadline:raise load('operation_errors').error('outcome_unknown: command_batch_deadline')
                            gate.check_scope([child['id']],[ROUTES[DOMAIN][1]],enabled_command=child['id'])
                            if hasattr(session,'timeout'):session.timeout=deadline-time.monotonic()
                            if time.monotonic()>=deadline:raise load('operation_errors').error('outcome_unknown: command_batch_deadline')
                            reply=session.request('tools/call',{'name':ROUTES[DOMAIN][1],'arguments':child})
                            try:return parse_reply(reply)
                            except RuntimeError as error:error.phase='reply_received';raise
                        def confirmed(child_index,child,row):
                            record['substeps'].append({'index':child_index,'request':child,'phase':'reply_validated','result':row['result']})
                            write(output/'journal.json',receipt)
                        try:result=supervised_batch(args,invoke,confirmed)
                        finally:
                            if hasattr(session,'timeout'):session.timeout=original_timeout
                    else:
                        result = parse_reply(session.request("tools/call", {"name": tool, "arguments": args}),
                                             output if "tool" in step else None, index)
                    validate_tool_reply(tool, result, args)
                except RuntimeError as error:
                    # 保留结构已验证的部分批次诊断，继续保持未知状态且不绑定别名。
                    if hasattr(error, 'partialResult'):
                        record['result'] = error.partialResult
                    raise
                record["result"] = result
                record["state"] = "succeeded"
                record['phase']='reply_validated'
                if "as" in step:
                    bindings[step["as"]] = result
                write(output / "journal.json", receipt)
        receipt["result"] = "PASS"
        write(output / "success.json", receipt)
    except (ValueError, RuntimeError, OSError, TimeoutError, subprocess.SubprocessError) as error:
        uncertain = isinstance(error, (TimeoutError, subprocess.TimeoutExpired)) or getattr(error, "outcome", None) == "unknown"
        receipt["result"] = "unknown" if uncertain else "FAIL"
        receipt["error"] = str(error)
        receipt["errorDetails"] = load("operation_errors").describe(error, "submitted")
        receipt['errorDetails']['replayAllowed']=False
        if hasattr(error,'aggregate'):receipt['errorDetails']['aggregate']=error.aggregate
        if receipt["steps"] and receipt["steps"][-1]["state"] == "started":
            receipt["steps"][-1]["state"] = "unknown" if uncertain else "failed"
        write(output / "failure.json", receipt)
    write(output / "journal.json", receipt)
    return receipt

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    listing = sub.add_parser("list"); listing.add_argument("--filter", default="")
    detail = sub.add_parser("describe"); detail.add_argument("command")
    check = sub.add_parser("check"); check.add_argument("plan", type=Path); check.add_argument("--input", action="append", default=[])
    run = sub.add_parser("run"); run.add_argument("plan", type=Path); run.add_argument("--output", type=Path, required=True)
    run.add_argument("--input", action="append", default=[]); run.add_argument("--runtime-home"); run.add_argument("--mode", choices=["headless", "bridge"], default="headless")
    run.add_argument("--connect"); run.add_argument("--control-token-file")
    args = parser.parse_args()
    try:
        if args.action == "list":
            result = [row for row in catalog()["commands"] if args.filter.lower() in
                      (row["id"] + " " + row["label"]).lower()]
        elif args.action == "describe":
            result = next((row for row in catalog()["commands"] if row["id"] == args.command), None)
            if result is None:
                raise ValueError("unknown_command: " + args.command)
        else:
            plan = reply_json(args.plan.read_text())
            inputs = {}
            for item in args.input:
                name, separator, path = item.partition("=")
                if not separator or name in inputs:
                    raise ValueError("invalid_or_duplicate_input")
                inputs[name] = path
            validate(plan, inputs)
            if args.action == "check":
                result = {"result": "PASS", "scope": "plan structure and catalog membership only",
                          "nativeExecution": "NOT_RUN", "operations": len(plan["operations"])}
            else:
                result = execute(plan, args.output, args.runtime_home, args.mode, args.connect, args.control_token_file, inputs=inputs)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0 if not isinstance(result, dict) or result.get("result", "PASS") == "PASS" else 1
    except (ValueError, OSError) as error:
        print(json.dumps({'result':'FAIL',**load('operation_errors').describe(error)},ensure_ascii=False))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
