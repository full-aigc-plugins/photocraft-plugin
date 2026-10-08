#!/usr/bin/env python3
"""当前插件／固定技能／维护版运行时一致性，不把身份检查当作宿主验收。"""
import argparse
import json
from pathlib import Path
import re

def validate(plugin,source,runtime,active,harness):
 errors=[]
 if not re.fullmatch(r'v\d+\.\d+\.\d+(?:-[0-9A-Za-z.]+)?',source.get('ref','')) or not re.fullmatch(r'[a-f0-9]{40}',source.get('sha','')):errors.append('skill_source_not_immutable')
 if source.get('package') not in ('photocraft-skills','full-aigc-skills/photocraft-skills') or ('repo' in source and source['repo'].removesuffix('.git')!='https://github.com/full-aigc-skills/photocraft-skills'):errors.append('skill_source_authority_mismatch')
 if active!=runtime:errors.append('active_runtime_lock_mismatch')
 if harness.get('version')!=plugin.get('version'):errors.append('harness_version_mismatch')
 official='https://github.com/storytold/photocraft'
 if runtime.get('repository','').removesuffix('.git')!=official and not runtime.get('runtimeVariant'):errors.append('maintained_runtime_variant_missing')
 if runtime.get('runtimeVariant') and (not re.fullmatch(r'[a-f0-9]{40}',runtime.get('upstreamCommit','')) or runtime.get('upstreamRepository','').removesuffix('.git')!=official):errors.append('maintained_runtime_provenance_missing')
 if runtime.get('artifact')!='photocraft-cli':errors.append('runtime_domain_mismatch')
 return errors

def check(root):
 plugin=json.loads((root/'plugin.json').read_text());lock=json.loads((root/'skills.lock.json').read_text());runtime=json.loads((root/'skills/photocraft-use/scripts/runtime.lock.json').read_text());active=json.loads((root/'runtime/photocraft-cli.lock.json').read_text());harness=json.loads((root/'package.json').read_text())
 source=lock['sources'][0];errors=validate(plugin,source,runtime,active,harness)
 return {'status':'FAIL' if errors else 'PASS','pluginVersion':plugin['version'],'skillSource':{'package':source['package'],'ref':source['ref'],'sha':source['sha']},'runtimeVersion':runtime['resolvedVersion'],'runtimeVariant':runtime.get('runtimeVariant','upstream'),'errors':errors,'scope':'identity only; fixed installation, model routing and creative acceptance separate'}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();result=check(args.root);print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(result['errors']))
