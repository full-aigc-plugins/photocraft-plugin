"""递归对象和定点修改合同；未观察到的文字度量或蒙版状态不能推断为通过。"""
import math

FIELDS={'kind','name','visible','hasMask','maskEnabled','maskLinked','bounds','text','noOverflow','within','parent','order','lineCount','lineRanges','tracking','font','orientation','size','leading','glyphCoverage'}
def index(model):
 result={}
 def walk(layers,parent):
  if not isinstance(layers,list):raise ValueError('invalid_layer_tree')
  for order,layer in enumerate(layers):
   if not isinstance(layer,dict) or type(layer.get('id')) is not int or not isinstance(layer.get('kind'),str):raise ValueError('invalid_layer_tree')
   key=str(layer['id'])
   if key in result:raise ValueError('duplicate_layer_identity')
   row={k:v for k,v in layer.items() if k!='children'};row['_parent']=parent;row['_order']=order;result[key]=row
   if layer['kind']=='Group' or 'children' in layer:walk(layer.get('children'),key)
 walk(model.get('layers'),None)
 return result

def editable_count(model):
 """有效调整层没有像素边界；空像素层和纯分组不能充当可编辑内容。"""
 count=0
 for row in index(model).values():
  bounds=row.get('bounds')
  pixels=isinstance(bounds,list) and len(bounds)==4 and all(type(x) in (int,float) and math.isfinite(x) for x in bounds) and bounds[2]>0 and bounds[3]>0
  adjustment=row['kind']=='Adjustment' and isinstance(row.get('adjustment'),dict) and bool(row['adjustment'])
  if row['kind']!='Group' and (pixels or adjustment):count+=1
 return count

def validate_assertions(assertions):
 if not isinstance(assertions,list) or len(assertions)>1000:raise ValueError('invalid_object_assertions')
 for item in assertions:
  if not isinstance(item,dict) or set(item)-({'layer'}|FIELDS) or 'layer' not in item:raise ValueError('invalid_object_assertion')
  identity=item['layer']
  if not (type(identity) is int and identity>0 or isinstance(identity,dict) and set(identity)=={'$ref'} and isinstance(identity['$ref'],str)):raise ValueError('invalid_object_assertion_identity')
  for key in ('within','bounds'):
   if key in item:
    rect=item[key]
    if not isinstance(rect,list) or len(rect)!=4 or any(type(x) not in (int,float) or not math.isfinite(x) for x in rect) or rect[2]<=0 or rect[3]<=0:raise ValueError('invalid_object_assertion_bounds')
  for key in ('visible','hasMask','maskEnabled','maskLinked','noOverflow','glyphCoverage'):
   if key in item and type(item[key]) is not bool:raise ValueError('invalid_object_assertion_value')
  if 'lineCount' in item and (type(item['lineCount']) is not int or item['lineCount']<0):raise ValueError('invalid_object_assertion_value')
  if 'lineRanges' in item and (not isinstance(item['lineRanges'],list) or any(not isinstance(pair,list) or len(pair)!=2 or any(type(n) is not int or n<0 for n in pair) or pair[1]<pair[0] for pair in item['lineRanges'])):raise ValueError('invalid_object_assertion_value')
  if 'tracking' in item and (type(item['tracking']) not in (float,int) or not math.isfinite(item['tracking'])):raise ValueError('invalid_object_assertion_value')
  if 'size' in item and (type(item['size']) not in (float,int) or not math.isfinite(item['size']) or item['size']<=0):raise ValueError('invalid_object_assertion_value')
  if 'leading' in item and item['leading']!='auto' and (type(item['leading']) not in (float,int) or not math.isfinite(item['leading']) or item['leading']<=0):raise ValueError('invalid_object_assertion_value')
  for key in ('font','orientation','text','name','kind'):
   if key in item and not isinstance(item[key],str):raise ValueError('invalid_object_assertion_value')
 return assertions

def assert_objects(model,assertions,facts=None):
 validate_assertions(assertions);rows=index(model);records=[]
 for item in assertions:
  row=rows.get(str(item['layer']))
  if row is None:raise ValueError('object_assertion_failed: missing_layer')
  for key,value in item.items():
   if key=='layer':continue
   observed=(facts or {}).get('objects',{}).get(str(item['layer']),{})
   if key in ('maskEnabled','maskLinked'):
    if key not in observed:raise ValueError('mask_metric_unavailable: '+key)
    actual=observed[key]
   elif key=='glyphCoverage':raise ValueError('layout_metric_unavailable: glyphCoverage')
   elif key in ('lineCount','lineRanges','tracking','font','orientation','size','leading'):
    info=observed.get('textInfo')
    if not info:raise ValueError('layout_metric_unavailable: '+key)
    if key=='lineCount':actual=len(info['lines'])
    elif key=='lineRanges':actual=[[line['start'],line['end']] for line in info['lines']]
    elif key=='orientation':actual=info.get('orientation')
    else:
     field={'font':'font_family','tracking':'tracking','size':'size_pt','leading':'leading_pt'}[key];runs=info.get('runs',[])
     expected=None if key=='leading' and value=='auto' else value
     actual=bool(runs) and all(field in run.get('style',{}) and run['style'][field]==expected for run in runs);value=True
   elif key=='noOverflow':
    if not isinstance(row.get('text'),dict) or type(row['text'].get('overflow')) is not bool:raise ValueError('layout_metric_unavailable: overflow')
    actual=not row['text']['overflow']
   elif key=='within':
    bounds=row.get('bounds')
    if not isinstance(bounds,list) or len(bounds)!=4:raise ValueError('layout_metric_unavailable: bounds')
    x,y,w,h=bounds;a,b,c,d=value
    actual= w>0 and h>0 and x>=a and y>=b and x+w<=a+c and y+h<=b+d
    value=True
   elif key=='text':actual=row.get('text',{}).get('text')
   elif key=='parent':actual=row['_parent'];value=None if value is None else str(value)
   elif key=='order':actual=row['_order']
   else:actual=row.get(key)
   if actual!=value:raise ValueError('object_assertion_failed: '+str(item['layer'])+': '+key)
  records.append({'layer':item['layer'],'status':'PASS','observed':row})
 return {'schema':'photocraft-object-assertions/v1','objects':records,'scope':'observed native structure and explicitly available metrics; no creative acceptance'}

def leaves(value,prefix=''):
 if isinstance(value,dict):
  result={}
  for key,item in value.items():result.update(leaves(item,prefix+'.'+key if prefix else key))
  return result
 return {prefix:value}
def compare(before,after,allowed_changes):
 old=index(before);new=index(after)
 if set(old)!=set(new):raise ValueError('structure_changed: identities')
 for key,row in old.items():
  if (row['_parent'],row['_order'],row['kind'])!=(new[key]['_parent'],new[key]['_order'],new[key]['kind']):raise ValueError('structure_changed: '+key)
  a=leaves(row);b=leaves(new[key]);allowed=allowed_changes.get(key,[])
  for field in set(a)|set(b):
   if field!='selected' and a.get(field)!=b.get(field) and field not in allowed:raise ValueError('object_changed: '+key+': '+field)
 return {'schema':'photocraft-object-preservation/v1','status':'PASS','objects':len(old),'allowedChanges':allowed_changes}
