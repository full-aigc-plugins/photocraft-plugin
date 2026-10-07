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

def output_path(value):
    if not isinstance(value, str) or not value or "\\" in value or Path(value).is_absolute() or any(p in ("", ".", "..") for p in value.split("/")) or value.split("/")[0] in {"journal.json", "success.json", "failure.json", "inputs", "tool-images", "desktop-session.json", "desktop.log", ".desktop-data", "artcraft-domain-command.json"}:
        raise ValueError("invalid_output_path")
    return value

def references(value, aliases):
    if isinstance(value, dict):
        if set(value) == {"$output"}:
            output_path(value["$output"])
        elif set(value) == {"$ref"}:
            text = value["$ref"]
            if not isinstance(text, str) or not re.fullmatch(r"[a-zA-Z][\w-]*(?:\.[\w-]+)*", text):
                raise ValueError("invalid_reference")
            if text.split(".")[0] not in aliases:
                raise ValueError("forward_or_unknown_reference: " + text)
        else:
            for child in value.values():
                references(child, aliases)
    elif isinstance(value, list):
        for child in value:
            references(child, aliases)

def validate(plan, input_names=()):
    if (not isinstance(plan, dict) or set(plan) != {"schema", "operations"}
            or plan["schema"] != "craft-command-plan/v1"
            or not isinstance(plan["operations"], list)
            or not 1 <= len(plan["operations"]) <= 1000):
        raise ValueError("invalid_command_plan")
    rows = {r["id"]: r for r in catalog()["commands"]}
    tools = set(catalog()["nativeTools"])
    aliases = {"output", *input_names}
    for index, step in enumerate(plan["operations"]):
        if not isinstance(step, dict) or set(step) - {"command", "tool", "params", "as"}:
            raise ValueError("invalid_operation: " + str(index))
        if ("command" in step) == ("tool" in step) or not isinstance(step.get("params"), dict):
            raise ValueError("command_or_tool_and_params_required: " + str(index))
        key = "command" if "command" in step else "tool"
        if not isinstance(step[key], str) or step[key] not in (rows if key == "command" else tools):
            raise ValueError("unknown_" + key + ": " + str(step[key]))
        try:
            json.dumps(step["params"], allow_nan=False)
        except (ValueError, TypeError):
            raise ValueError("invalid_json_parameters: " + str(index)) from None
        if key == "tool" and step[key] == ROUTES[DOMAIN][1]:
            raise ValueError("use_command_operation_for_native_registry")
        references(step["params"], aliases)
        alias = step.get("as")
        if alias is not None:
            if not isinstance(alias, str) or not re.fullmatch(r"[a-zA-Z][\w-]*", alias) or alias in aliases:
                raise ValueError("invalid_or_duplicate_alias")
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

def reply_json(text):
    """拒绝重复键与非有限值；保留合法 JSON 标量及普通文字工具兼容性。"""
    def constant(value):
        raise ValueError('nonfinite_json_value')
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate_json_key')
            result[key] = value
        return result
    value = json.loads(text, parse_constant=constant, object_pairs_hook=object_pairs)
    # 1e999 等合法数值字面量仍可能溢出；不能等到写回执时才发现。
    json.dumps(value, allow_nan=False)
    return value

def parse_reply(reply, output=None, index=0):
    if (not isinstance(reply, dict)
            or ('isError' in reply and not isinstance(reply['isError'], bool))
            or not isinstance(reply.get('content'), list)
            or any(not isinstance(item, dict) or not isinstance(item.get('type'), str)
                   or (item.get('type') == 'text' and not isinstance(item.get('text'), str))
                   for item in reply['content'])):
        raise RuntimeError('outcome_unknown: invalid_tool_reply')
    if reply.get("isError"):
        raise RuntimeError("command_failed: " + json.dumps(reply.get("content"), ensure_ascii=False))
    content = reply.get("content", [])
    texts = [item["text"] for item in content if item.get("type") == "text"]
    if len(content) == 1 and len(texts) == 1:
        try:
            result = reply_json(texts[0])
        except json.JSONDecodeError:
            if output is None:
                raise RuntimeError("outcome_unknown: unexpected_reply") from None
        except (ValueError, TypeError):
            raise RuntimeError('outcome_unknown: unsafe_json_reply') from None
        else:
            if isinstance(result, dict) and result.get("error"):
                raise RuntimeError("semantic_error: " + json.dumps(result, ensure_ascii=False))
            return result
    if output is None or not content:
        raise RuntimeError("outcome_unknown: unexpected_reply")
    # 原生工具允许图片和普通文字；附件落盘，日志不保留大块 base64。
    result = {"content": []}
    for number, item in enumerate(content):
        if item.get("type") == "text":
            try:
                parsed = reply_json(item["text"])
            except json.JSONDecodeError:
                parsed = item["text"]
            except (ValueError, TypeError):
                raise RuntimeError('outcome_unknown: unsafe_json_reply') from None
            if isinstance(parsed, dict) and parsed.get("error"):
                raise RuntimeError("semantic_error: " + json.dumps(parsed, ensure_ascii=False))
            result["content"].append({"type": "text", "value": parsed})
        elif item.get("type") == "image" and item.get("mimeType") in ("image/png", "image/jpeg", "image/webp"):
            extension = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}[item["mimeType"]]
            try:
                data = base64.b64decode(item["data"], validate=True)
            except (ValueError, KeyError, TypeError):
                raise RuntimeError("outcome_unknown: invalid_image_reply") from None
            path = Path(output) / "tool-images" / (str(index) + "-" + str(number) + "." + extension)
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(data)
            result["content"].append({"type": "image", "mimeType": item["mimeType"],
                "path": str(path.relative_to(output)), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        else:
            raise RuntimeError("outcome_unknown: unsupported_tool_content")
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
        raise RuntimeError("outcome_unknown: unexpected_registry")
    return rows

def execute(plan, output, runtime_home=None, mode="headless", connect=None, token_file=None,
            installer=None, session_factory=None, inputs=None):
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
    # 验证连接参数在安装和创建目录之前完成；不偷偷回退到另一会话。
    backend_argv("native", output, mode, connect, token_file)
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
        bindings = {"output": "" if DOMAIN == "photocraft" else str(output)}
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
            bindings[name] = {"path": relative if DOMAIN == "photocraft" else str(target), "sha256": digest}
            receipt["inputs"][name] = {"path": relative, "sha256": digest}
        with session_factory(backend_argv(installed["executable"], output, mode, connect, token_file)) as session:
            discovery = session.request("tools/list", {})
            if (not isinstance(discovery, dict) or not isinstance(discovery.get('tools'), list)
                    or any(not isinstance(tool, dict) or not isinstance(tool.get('name'), str)
                           or not tool['name'] for tool in discovery['tools'])):
                raise RuntimeError('outcome_unknown: unexpected_tools_reply')
            available = {tool['name'] for tool in discovery['tools']}
            required = {native_call(s["command"], {})[0] if "command" in s else s["tool"]
                        for s in plan["operations"]}
            # 目录查询也是原生能力合同；旧服务不能冒充新入口。
            if not required.issubset(available) or ROUTES[DOMAIN][0] not in available:
                raise RuntimeError("native_tool_missing")
            current = {r["id"]: r for r in runtime_rows(session)}
            expected = {r["id"] for r in catalog()["commands"]}
            if not expected.issubset(current):
                raise RuntimeError("native_registry_drift")
            receipt["registeredCommands"] = len(current)
            for index, step in enumerate(plan["operations"]):
                params = resolve(step["params"], bindings)
                record = {"index": index, "command": step.get("command"), "tool": step.get("tool"),
                          "params": params, "state": "started"}
                if "command" in step:
                    states = {r["id"]: r for r in runtime_rows(session, {"filter": step["command"]})}
                    row = states.get(step["command"])
                    if row is None or row.get("enabled") is not True:
                        record["state"] = "blocked"
                        record["reason"] = row.get("why", "native_context_disabled") if row else "native_command_missing"
                        receipt["steps"].append(record)
                        raise RuntimeError("precondition_failed: " + step["command"] + ": " + record["reason"])
                    tool, args = native_call(step["command"], params)
                else:
                    tool, args = step["tool"], params
                receipt["steps"].append(record)
                write(output / "journal.json", receipt)
                result = parse_reply(session.request("tools/call", {"name": tool, "arguments": args}),
                                     output if "tool" in step else None, index)
                record["result"] = result
                record["state"] = "succeeded"
                if "as" in step:
                    bindings[step["as"]] = result
                write(output / "journal.json", receipt)
        receipt["result"] = "PASS"
        write(output / "success.json", receipt)
    except (ValueError, RuntimeError, OSError, TimeoutError, subprocess.SubprocessError) as error:
        uncertain = isinstance(error, (TimeoutError, subprocess.TimeoutExpired)) or any(s in str(error) for s in
                    ("outcome_unknown", "mcp_disconnected", "mcp_response_too_large"))
        receipt["result"] = "unknown" if uncertain else "FAIL"
        receipt["error"] = str(error)
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
        print(json.dumps({"result":"FAIL", "error":str(error)}, ensure_ascii=False))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
