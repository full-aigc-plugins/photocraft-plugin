"""绑定实际保存工程的尺寸变体、安全区与编辑图层身份记录。"""
import math
import re

def validate(config):
 if not isinstance(config,dict) or set(config)!={'width','height','safeArea','roles'}:raise ValueError('invalid_variant_schema')
 for name in ('width','height'):
  if type(config[name]) is not int or not 0<config[name]<=16384:raise ValueError('invalid_variant_size')
 rect=config['safeArea']
 if not isinstance(rect,list) or len(rect)!=4 or any(type(v) not in (int,float) or not math.isfinite(v) for v in rect):raise ValueError('invalid_variant_safe_area')
 x,y,w,h=rect
 if x<0 or y<0 or w<=0 or h<=0 or x+w>config['width'] or y+h>config['height']:raise ValueError('invalid_variant_safe_area')
 roles=config['roles']
 if not isinstance(roles,dict) or set(roles)!={'background','product','text'}:raise ValueError('invalid_variant_roles')
 for value in roles.values():
  if type(value) is int and 0<value<2**53:continue
  if isinstance(value,dict) and set(value)=={'$ref'} and isinstance(value['$ref'],str) and re.fullmatch(r'[a-zA-Z][\w-]*(?:\.[a-zA-Z0-9_]+)+',value['$ref']):continue
  raise ValueError('invalid_variant_role_reference')

def assess(config,before,after,steps,roles):
 validate(config)
 ids=roles or config['roles']
 if any(type(v) is not int or not 0<v<2**53 for v in ids.values()) or len(set(ids.values()))!=3:raise ValueError('variant_role_identity')
 if [after['width'],after['height']]!=[config['width'],config['height']]:raise ValueError('variant_size_mismatch')
 result={'schema':'photocraft-layout-variant/v1','sourceSize':[before['width'],before['height']],'targetSize':[after['width'],after['height']],'safeArea':config['safeArea'],'steps':[],'roles':{}}
 for step in steps:
  ow,oh=step['before'];data=step['result'];nw,nh=data['width'],data['height']
  row={'command':step['command'],'before':[ow,oh],'after':[nw,nh]}
  if step['command']=='image.canvasSize':
   dx,dy=data['offset'];row.update(offset=[dx,dy],crop={'left':max(0,-dx),'top':max(0,-dy),'right':max(0,ow+dx-nw),'bottom':max(0,oh+dy-nh)},padding={'left':max(0,dx),'top':max(0,dy),'right':max(0,nw-ow-dx),'bottom':max(0,nh-oh-dy)})
  else:row['scale']=[nw/ow,nh/oh]
  result['steps'].append(row)
 if not steps:raise ValueError('variant_geometry_required')
 x,y,w,h=config['safeArea']
 for role,identity in ids.items():
  original=[v for v in before['layers'] if v['id']==identity];saved=[v for v in after['layers'] if v['id']==identity]
  if len(original)!=1 or len(saved)!=1 or saved[0]['kind']!=original[0]['kind']:raise ValueError('variant_role_changed: '+role)
  layer=saved[0]
  if role=='text' and (layer['kind']!='Type' or not layer.get('text')):raise ValueError('variant_text_not_editable')
  if not layer.get('visible'):raise ValueError('variant_role_hidden: '+role)
  bounds=layer.get('bounds')
  if not isinstance(bounds,list) or len(bounds)!=4 or any(type(v) not in (int,float) or not math.isfinite(v) for v in bounds):raise ValueError('variant_role_bounds')
  a,b,c,d=bounds
  if role!='background' and (c<=0 or d<=0 or a<x or b<y or a+c>x+w or b+d>y+h):raise ValueError('variant_safe_area_violation: '+role)
  result['roles'][role]={'id':identity,'kind':layer['kind'],'name':layer.get('name'),'bounds':bounds,'text':layer.get('text')}
 return result
