#!/usr/bin/env python3
"""生成宿主配置到明确输出路径；不修改宿主设置或安装插件。"""
import argparse,json,pathlib,shutil
p=argparse.ArgumentParser();p.add_argument('--host',choices=['workbuddy','codex'],required=True);p.add_argument('--workspace',required=True);p.add_argument('--output',required=True);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1];workspace=pathlib.Path(a.workspace).resolve(strict=True);server=root/'ui/bootstrap.mjs'
if not server.is_file():p.error('Missing ui/bootstrap.mjs; build the candidate first')
name=json.loads((root/'plugin.json').read_text())['name']+'-editor'
node=shutil.which('node')
if not node:p.error('Node.js 24+ is required')
entry={'type':'stdio','command':node,'args':[str(server)],'cwd':str(workspace),'env':{'CRAFT_WORKSPACE_ROOT':str(workspace)}}
if a.host=='workbuddy':text=json.dumps({'mcpServers':{name:entry}},ensure_ascii=False,indent=2)+'\n'
else:
 q=lambda value:json.dumps(value,ensure_ascii=False)
 text='[mcp_servers.'+q(name)+']\ncommand = '+q(node)+'\nargs = ['+q(str(server))+']\ncwd = '+q(str(workspace))+'\ntool_timeout_sec = 180\n[mcp_servers.'+q(name)+'.env]\nCRAFT_WORKSPACE_ROOT = '+q(str(workspace))+'\n'
out=pathlib.Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
with out.open('x') as f:f.write(text)
print(out)
