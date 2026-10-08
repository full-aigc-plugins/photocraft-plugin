#!/usr/bin/env python3
"""只读汇总当前发行角色、完整技能内容和协议引用；不提升产品验收状态。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
def load(root,name,path):
 spec=importlib.util.spec_from_file_location(name,root/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def encoded(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):
 def pairs(items):
  result={}
  for k,v in items:
   if k in result:raise ValueError('duplicate_manifest_key')
   result[k]=v
  return result
 return json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite_manifest')))
def check(root,skills_source):
 """核对独立版本映射及源／安装内容，返回摘要或具体拒绝原因，不联网或写入。"""
 root=Path(root).resolve();skills_source=Path(skills_source).resolve();errors=[];files={}
 def value(base,name,prefix=''):
  path=base/name
  if path.is_symlink():raise ValueError('linked_identity_file: '+prefix+name)
  files[prefix+name]=sha(path);return read(path)
 try:
  plugin=value(root,'plugin.json');harness=value(root,'package.json');lock=value(root,'skills.lock.json');active=value(root,'runtime/photocraft-cli.lock.json');historical=value(root,'runtime/history/photocraft-cli-upstream-0.2.0.lock.json');runtime=value(root,'skills/photocraft-use/scripts/runtime.lock.json');protocol=value(root,'docs/contracts-reference.json')
  if len(lock['sources'])!=1:raise ValueError('one_skill_authority_required')
  source=lock['sources'][0];base=load(root,'combination_base','scripts/check_release_identity.py');errors.extend(base.validate(plugin,source,runtime,active,harness))
  package=value(skills_source,'.claude-plugin/plugin.json','source/');suite=value(skills_source,'skill-suite.json','source/');source_runtime=value(skills_source,'skills/photocraft-use/scripts/runtime.lock.json','source/');source_historical=value(skills_source,'runtime/official-runtime-0.2.0.lock.json','source/');version=source['ref'].removeprefix('v')
  if package.get('name')!='photocraft-skills' or package.get('repository','').removesuffix('.git')!='https://github.com/full-aigc-skills/photocraft-skills':errors.append('source_package_authority_mismatch')
  if package.get('version')!=version:errors.append('source_package_version_mismatch')
  if suite.get('version')!=version:errors.append('source_suite_version_mismatch')
  if suite.get('pluginId')!='photocraft' or suite.get('runtimeVersion')!=runtime['resolvedVersion']:errors.append('source_suite_runtime_mapping_mismatch')
  names=[v['name'] for v in suite['skills']]
  if sorted(names)!=sorted(source['skills']) or len(set(names))!=len(names):errors.append('source_suite_skill_inventory_mismatch')
  if source_runtime!=runtime:errors.append('source_runtime_lock_mismatch')
  vendor=load(root,'combination_vendor','scripts/vendor/skill_vendor.py');vendor.validate_no_cross_source_collisions(lock);vendor.validate_plugin_local_inventory(root,lock);vendor.validate_source(source,root)
  for name in source['skills']:
   for base_path,label in [(root,'installed'),(skills_source,'source')]:
    if vendor.hash_skill_dir(base_path/'skills'/name)!=source['sha256'].get(name):errors.append(label+'_skill_digest_mismatch: '+name)
  official='https://github.com/storytold/photocraft'
  if historical.get('repository','').removesuffix('.git')!=official or historical.get('resolvedVersion')!='0.2.0' or historical.get('runtimeVariant'):errors.append('historical_runtime_authority_mismatch')
  for key in ('repository','artifact','resolvedVersion'):
   if historical.get(key)!=source_historical.get(key):errors.append('historical_source_mapping_mismatch: '+key)
  for platform,entry in historical.get('artifacts',{}).items():
   for key in ('url','binarySha256','archiveSha256'):
    if entry.get(key)!=source_historical.get('artifacts',{}).get(platform,{}).get(key):errors.append('historical_source_digest_mismatch: '+platform+'/'+key)
  reference=load(root,'combination_contract','scripts/contract_reference.py');errors.extend(reference.validate_reference(protocol))
  for key,filename in [('taskSchema','craft-task-v1.json'),('artifactSchema','craft-artifact-v1.json')]:
   path=root/'contracts/artcraft'/filename;files[str(path.relative_to(root))]=sha(path)
   if sha(path)!=protocol['files'][key]['sha256']:errors.append('contract_payload_digest_mismatch: '+key)
  for name,pattern in [('README.md',r'^Current plugin: `([^`]+)`; skill source: `([^`]+)`;'),('README.zh-CN.md',r'^当前插件：`([^`]+)`；技能源：`([^`]+)`；')]:
   path=root/name;text=path.read_text();files[name]=sha(path);rows=re.findall(pattern,text,re.M)
   if rows!=[(plugin['version'],version)]:errors.append(name+': current_version_paragraph_mismatch')
   for label,expected in [('Metadata version',plugin['version']),('Skills source',source['package']+' / '+version)]:
    if re.findall(r'^\| '+re.escape(label)+r' \| ([^|]+) \|$',text,re.M)!=[expected]:errors.append(name+': current_version_table_mismatch: '+label)
   if runtime.get('runtimeVariant') and ('First use installs the pinned official CLI' in text or '首次入口会安装锁定官方 CLI' in text):errors.append(name+': current_runtime_provenance_mismatch')
  combination={'plugin':{'version':plugin['version'],'manifestSha256':files['plugin.json'],'harnessVersion':harness['version']},'skills':{'repository':source['repo'],'ref':source['ref'],'commit':source['sha'],'version':version,'packageVersion':package['version'],'suiteVersion':suite['version'],'sha256':source['sha256']},'runtime':runtime,'historicalRuntime':{'path':'runtime/history/photocraft-cli-upstream-0.2.0.lock.json','active':False,'lock':historical,'sourcePath':'runtime/official-runtime-0.2.0.lock.json'},'publicProtocol':protocol,'files':files,'versionRoles':'Plugin and skill-source releases are independent; package and suite describe the same source version; active maintained runtime has its own version, distinct from retained upstream runtime.'}
 except (KeyError,TypeError,ValueError,OSError,RuntimeError) as error:
  errors.append('identity_input_invalid: '+str(error).replace(str(root),'PLUGIN').replace(str(skills_source),'SOURCE'));combination=None
 return {'schema':'photocraft-release-combination/v1','status':'FAIL' if errors else 'PASS','combinationSha256':hashlib.sha256(encoded(combination)).hexdigest() if not errors else None,'combination':combination,'errors':errors,'acceptance':{'native':False,'hostModelRouting':False,'creative':False,'marketplace':False,'remoteTag':'NOT_CHECKED'},'scope':'readonly local combination and complete source/installed managed-skill bytes; remote immutable tag and public archive identity require separate release evidence'}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--skills-source',type=Path,required=True);args=parser.parse_args();result=check(args.root,args.skills_source);print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['status']!='PASS')
