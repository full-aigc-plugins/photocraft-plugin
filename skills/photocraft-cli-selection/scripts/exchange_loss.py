"""从实际导出与重开记录生成交换损失报告；不把格式能力推断当成保真验证。"""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

PLUGIN = 'photocraft'
NATIVE = 'project.pcraft'

def sha(path):
 with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def safe_file(root,location):
 if not isinstance(location,str) or not location or '\\' in location or ':' in location or Path(location).is_absolute() or any(p in ('..','') for p in location.split('/')):raise ValueError('loss_location_invalid')
 path=root/location
 if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):raise ValueError('loss_file_missing_or_escaping')
 return path

def write_report(root,outputs,warnings):
 root=Path(root)
 native=safe_file(root,NATIVE);inspection=safe_file(root,'native.json')
 model=json.loads(inspection.read_text())
 report={'schema':'craft-exchange-loss/v1','pluginId':PLUGIN,'native':{'location':NATIVE,'sha256':sha(native)},'inspection':{'location':'native.json','sha256':sha(inspection)},'outputs':[],'acceptance':'technical-observations-only'}
 if len(outputs)!=len(set(outputs)):raise ValueError('loss_duplicate_output')
 for location in outputs:
  path=safe_file(root,location);fmt=path.suffix[1:].lower();observations={};changes=[]
  def change(code,status,reason):changes.append({'code':code,'status':status,'reason':reason})
  change('native-editing-model','lost','Derivative formats do not retain the complete application-native project model; the native project is delivered separately.')
  if fmt in ('png','jpg','jpeg','webp','mp4'):
   change('editable-layers-paths-text','lost','Layer, path and live text editing are rendered into pixels; edit the retained native project.')
   change('effect-keyframe-parameters','lost','Rendered pixels do not carry editable native effects, masks or keyframes.')
   change('font-appearance','unknown','Rendered appearance has not been compared with an approved visual reference.')
  if fmt=='png':
   with path.open('rb') as stream:header=stream.read(26)
   if len(header)!=26 or header[:8]!=bytes.fromhex('89504e470d0a1a0a'):raise ValueError('loss_png_invalid')
   observations['pngColorType']=header[25]
   change('alpha-channel','observed' if header[25] in (4,6) else 'unknown','PNG IHDR records channel representation; indexed transparency and visual alpha fidelity are not inferred.')
  elif fmt=='mp4':
   change('alpha-channel','lost','The supported H.264 export does not retain native composition transparency.')
   change('editable-timeline','lost','MP4 contains rendered streams rather than editable clips, tracks and subtitle style parameters.')
   if PLUGIN=='effectcraft':change('audio-output','lost','This public export explicitly renders with audio off; native media remains in the project.')
   if (root/'export-probe.json').is_file():
    probe=json.loads((root/'export-probe.json').read_text());observations['audioStreamPresent']=bool(probe.get('audio'))
  elif fmt=='svg':
   if path.stat().st_size>16*1024*1024:raise ValueError('loss_svg_too_large')
   xml=ET.fromstring(path.read_bytes())
   if xml.tag.split('}')[-1]!='svg':raise ValueError('loss_svg_invalid')
   tags=[element.tag.split('}')[-1] for element in xml.iter()];observations['svg']={name:tags.count(name) for name in ('path','text','image','filter','mask','clipPath')}
   change('vector-structure','observed','XML element counts record actual vector/text/raster structure, not semantic round-trip equivalence.')
   change('font-portability','unknown','Font embedding, substitution and text layout across consumers are not verified.')
   change('effect-fidelity','unknown','Native effects, masks and grouping are not proven equivalent in SVG consumers.')
  elif fmt=='psd':
   change('font-portability','unknown','PSD font availability and substitution in other editors are not verified.')
   change('effect-fidelity','unknown','Native adjustment, mask, blend and effect equivalence is not proven by layer count.')
   change('editable-layer-roundtrip','unknown','A reopened PSD inspection is evidence of observed structure, not complete editability equivalence.')
   if (root/'psd-inspection.json').is_file():
    psd=json.loads((root/'psd-inspection.json').read_text());observations['nativeLayerCount']=len(model.get('layers',[]));observations['psdLayerCount']=len(psd.get('layers',[]))
    report['psdInspection']={'location':'psd-inspection.json','sha256':sha(root/'psd-inspection.json')}
  elif fmt=='pdf':
   change('font-portability','unknown','PDF font embedding and substitution are not verified.')
   change('effect-fidelity','unknown','Native effect/mask appearance in PDF consumers is not verified.')
   change('vector-structure','unknown','PDF output does not prove editable vector-path round-trip.')
  elif fmt=='srt':
   change('subtitle-styling','lost','SRT exchanges timing and text; native font, position, color and animation styling is not retained.')
  elif fmt=='tif':
   change('editable-layer-roundtrip','unknown','TIFF layer extensions and native mask/effect fidelity are not verified.')
   change('font-portability','unknown','Native live-text portability is not verified.')
  elif fmt not in ('jpg','jpeg','webp'):raise ValueError('loss_format_unsupported')
  report['outputs'].append({'location':location,'sha256':sha(path),'format':fmt,'role':'derivative','nativeSubstitute':False,'changes':changes,'observations':observations,'warnings':warnings.get(location,[])})
 (root/'exchange-loss.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report
