"""固定 v1 保存格式蒙版事实及原生 type.info 布局；只读，不解压像素或推断缺字。"""
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import zipfile

FIELDS={'maskEnabled','maskLinked','lineCount','lineRanges','tracking','font','orientation','size','leading','glyphCoverage'}
def load(name):
 s=importlib.util.spec_from_file_location('facts_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def required(plan):return any(set(item)&FIELDS for item in plan.get('assertions',[]))
def mask_surface_digest(project,mask):
 surface=mask.get('surface')
 if not isinstance(surface,dict) or not isinstance(surface.get('tiles'),list):raise ValueError('native_mask_surface_unavailable')
 blobs={};total=0
 with zipfile.ZipFile(project) as archive:
  for tile in surface['tiles']:
   identity=tile.get('hash') if isinstance(tile,dict) else None
   if not isinstance(identity,str) or not re.fullmatch('[a-f0-9]{64}',identity):raise ValueError('native_mask_tile_invalid')
   if identity in blobs:continue
   entries=[entry for entry in archive.infolist() if entry.filename=='tiles/'+identity+'.zst']
   if len(entries)!=1:raise ValueError('native_mask_tile_missing')
   total+=entries[0].file_size
   if total>64*1024*1024:raise ValueError('native_mask_verification_limit')
   digest=hashlib.sha256()
   with archive.open(entries[0]) as stream:
    while chunk:=stream.read(65536):digest.update(chunk)
   blobs[identity]=digest.hexdigest()
 return hashlib.sha256(json.dumps({'surface':surface,'blobs':blobs},sort_keys=True,separators=(',',':')).encode()).hexdigest()
def collect(project,model,call):
 project=Path(project);digest=hashlib.sha256(project.read_bytes()).hexdigest()
 try:
  with zipfile.ZipFile(project) as archive:
   entries=[item for item in archive.infolist() if item.filename=='manifest.json']
   if len(entries)!=1 or entries[0].file_size>16*1024*1024:raise ValueError('native_manifest_invalid')
   data=load('strict_json').loads(archive.read(entries[0]))
 except (zipfile.BadZipFile,KeyError):raise ValueError('native_manifest_unavailable') from None
 if data.get('format_version')!=1:raise ValueError('native_manifest_version_unsupported')
 saved={}
 def walk(layers):
  for row in layers:
   key=str(row['id'])
   if key in saved:raise ValueError('duplicate_layer_identity')
   saved[key]=row
   if row['content']['kind']=='group':walk(row['content']['children'])
 walk(data['document']['layers']);objects={};rows=load('domain_assertions').index(model)
 if set(rows)!=set(saved):raise ValueError('native_manifest_layer_mismatch')
 for key,row in rows.items():
  mask=saved[key].get('mask')
  if row.get('hasMask') is not (mask is not None):raise ValueError('native_manifest_mask_mismatch')
  facts={'hasMask':mask is not None}
  if mask is not None:
   if type(mask.get('enabled')) is not bool or type(mask.get('linked')) is not bool:raise ValueError('native_mask_state_unavailable')
   facts.update(maskEnabled=mask['enabled'],maskLinked=mask['linked'],maskDensity=mask['density'],maskFeather=mask['feather'],maskSurfaceSha256=mask_surface_digest(project,mask))
  if row['kind']=='Type':
   info=call('command_run',{'id':'type.info','params':{'layer':int(key)}})
   if not isinstance(info,dict) or info.get('layer')!=int(key) or info.get('text')!=row.get('text',{}).get('text') or not isinstance(info.get('lines'),list) or not isinstance(info.get('runs'),list):raise ValueError('native_text_info_mismatch')
   facts['textInfo']=info
  objects[key]=facts
 if hashlib.sha256(project.read_bytes()).hexdigest()!=digest:raise ValueError('native_project_changed')
 return {'schema':'photocraft-native-facts/v1','projectSha256':digest,'objects':objects,'scope':'saved v1 mask ownership/state and readonly type.info; glyph coverage, overflow and cross-editor appearance unknown'}

def preserve(before,after,allowed):
 if set(before['objects'])!=set(after['objects']):raise ValueError('native_facts_structure_changed')
 for key,old in before['objects'].items():
  changes=allowed.get(key,[]);new=after['objects'][key]
  for field in set(old)|set(new):
   if field=='textInfo' and any(name.startswith('text.') or name=='bounds' for name in changes):continue
   if field not in changes and old.get(field)!=new.get(field):raise ValueError('native_facts_object_changed: '+key+': '+field)
 return {'status':'PASS','objects':len(before['objects']),'scope':'non-target text layout and mask facts; explicitly editable target text layout may change'}
