"""按固定参数说明执行可确定的类型／范围预检；不虚构原生未公开的约束。"""
from functools import lru_cache
import json
import math
import re

def failure(code,path,expected):
 raise ValueError(code+': '+path+' expected '+expected)

def finite(value):
 if type(value) not in (int,float):return False
 try:return math.isfinite(value)
 except OverflowError:return False

def matching(text,start):
 opening=text[start];closing={'{':'}','[':']','(':')'}[opening];stack=[closing];quoted=False;escape=False
 for i in range(start+1,len(text)):
  char=text[i]
  if quoted:
   if escape:escape=False
   elif char=='\\':escape=True
   elif char=='"':quoted=False
   continue
  if char=='"':quoted=True
  elif char in '{[(':stack.append({'{':'}','[':']','(':')'}[char])
  elif char in '}])':
   if stack and char==stack[-1]:stack.pop()
   if not stack:return i
 return len(text)-1

def split(text,delimiter):
 result=[];start=0;i=0
 while i<len(text):
  if text[i]=='"':
   try:_,length=json.JSONDecoder().raw_decode(text[i:]);i+=length;continue
   except ValueError:pass
  if text[i] in '{[(':i=matching(text,i)+1;continue
  if text[i]==delimiter and not (delimiter=='=' and text[max(0,i-2):i]=='..'):result.append(text[start:i].strip());start=i+1
  i+=1
 result.append(text[start:].strip());return result

@lru_cache(maxsize=4096)
def fields(description):
 if not description.startswith('{'):return {},True
 end=matching(description,0);body=description[1:end];markers=[];i=0;pending=[]
 while i<len(body):
  if body[i] in '{[(':i=matching(body,i)+1;continue
  if body[i]=='"':
   try:name,length=json.JSONDecoder().raw_decode(body[i:])
   except ValueError:i+=1;continue
   finish=i+length;j=finish
   while j<len(body) and body[j].isspace():j+=1
   if j<len(body) and body[j]==':':markers.append((name,i,j+1,pending));pending=[]
   elif j==len(body) or body[j]==',':pending.append(name)
   i=finish;continue
  i+=1
 result={}
 for index,(name,start,value_start,group) in enumerate(markers):
  value_end=markers[index+1][1] if index+1<len(markers) else len(body)
  expression=body[value_start:value_end].strip().rstrip(', |')
  # 共用说明的列举键，例如 locks 的多个布尔属性。
  for key in [*group,name]:result[key]=expression
 # 仅顶层省略号表示动态键，嵌套形状的省略号不会打开外层。
 i=0;open_keys=False
 while i<len(body):
  if body[i]=='"':
   try:_,length=json.JSONDecoder().raw_decode(body[i:]);i+=length;continue
   except ValueError:pass
  if body[i] in '{[(':i=matching(body,i)+1;continue
  if body[i]=='…' or body[i:i+3]=='...':open_keys=True
  i+=1
 return result,open_keys

def is_reference(value):
 return isinstance(value,dict) and set(value) in ({'$ref'},{'$output'})

def validate_value(expression,value,path,resolved=False):
 if is_reference(value) and not resolved:return
 expression=split(expression,'=')[0].strip().rstrip('?, |')
 alternatives=split(expression,'|')
 if len(alternatives)>1:
  failures=[]
  for choice in alternatives:
   try:validate_value(choice,value,path,resolved);return
   except ValueError as error:failures.append(error)
  raise failures[0]
 expression=expression.strip().rstrip('?')
 if not expression:return
 if expression.startswith('"'):
  try:quoted,length=json.JSONDecoder().raw_decode(expression)
  except ValueError:return
  if quoted.startswith('#') and any(char in expression[length:] for char in '[{'):return
  if type(value) is not str:failure('parameter_type',path,'string')
  choices=quoted.split('|')
  # 开放枚举和颜色说明不是穷举值；不误拒合法原生字符串。
  if len(choices)>1 and not any('…' in item or '#' in item or '[' in item for item in choices) and value not in choices:failure('parameter_enum',path,quoted)
  return
 if expression.startswith('{'):
  if not isinstance(value,dict):failure('parameter_type',path,'object')
  definitions,opened=fields(expression)
  for key,item in value.items():
   if key not in definitions:
    if not opened:failure('parameter_unknown_field',path+'.'+key,'declared field')
   else:validate_value(definitions[key],item,path+'.'+key,resolved)
  return
 if expression.startswith('['):
  end=matching(expression,0)
  tail=expression[end+1:].strip()
  if tail.startswith('|'):
   return validate_value(expression[:end+1]+tail,value,path,resolved)
  if not isinstance(value,list):failure('parameter_type',path,'array')
  parts=split(expression[1:end],',');repeat=bool(parts and parts[-1] in ('…','...'));parts=[p for p in parts if p not in ('…','...')]
  if len(parts)==1:repeat=True
  if not repeat:
   minimum=sum(not part.rstrip().endswith('?') for part in parts)
   if not minimum<=len(value)<=len(parts):failure('parameter_shape',path,f'array length {minimum}..{len(parts)}')
  for index,item in enumerate(value):
   pattern=parts[min(index,len(parts)-1)] if parts else 'json'
   validate_value(pattern,item,path+'['+str(index)+']',resolved)
  return
 atom=re.split(r'[\s(?,]',expression,maxsplit=1)[0]
 if atom in ('true','false','bool'):
  if type(value) is not bool:failure('parameter_type',path,'boolean')
  return
 if atom=='null':
  if value is not None:failure('parameter_type',path,'null')
  return
 if atom in ('str','string','name','path','file','field'):
  if type(value) is not str:failure('parameter_type',path,'string')
  return
 integer=re.fullmatch(r'([ui])(8|16|32|64)',atom)
 if integer or atom in ('id','layerId','index','i','char','startChar','endChar'):
  if type(value) is not int:failure('parameter_type',path,'integer')
  if integer:
   bits=int(integer[2]);low=0 if integer[1]=='u' else -(2**(bits-1));high=2**bits-1 if integer[1]=='u' else 2**(bits-1)-1
  else:low=0;high=2**64-1
  if not low<=value<=high:failure('parameter_range',path,f'{low}..{high}')
  return
 interval=re.match(r'^(-?\d+(?:\.\d+)?)\.\.=?(-?\d+(?:\.\d+)?)',atom)
 number=interval or re.fullmatch(r'-?\d+(?:\.\d+)?',atom) or atom in ('number','f32','f64','px','pt','ppi','deg','%','n','x','y','w','h','dx','dy','sx','sy','r','g','b','a','c','d','e','f','t','in','out','pressure','tiltX','tiltY','rotation','timeMs','wheel','start','end','1/1000em')
 if number:
  if not finite(value):failure('parameter_type',path,'finite number')
  if interval and not float(interval[1])<=value<=float(interval[2]):failure('parameter_range',path,interval.group(0))
  if atom=='pressure' and not 0<=value<=1:failure('parameter_range',path,'0..1')
 # json、运行时对象名及没有精确定义的符号保持原生约定，不伪造类型。

def validate(identifier,params,rows,path='$.params',resolved=False):
 if not isinstance(params,dict):failure('parameter_type',path,'object')
 description=rows[identifier]['params'];definitions,opened=fields(description);definitions=dict(definitions)
 if identifier=='type.create':
  style,_=fields(rows['type.setStyle']['params']);definitions={**definitions,**style};definitions.pop('layer',None);definitions.pop('range',None)
 if identifier=='shape.create' and 'shape' in params:
  definitions['shape']='str'
 if identifier in ('type.setStyle','type.create'):
  for key in ('features','variations'):definitions[key]='json'
 if identifier=='type.resolveMissingFonts' and 'map' in params:
  definitions['map']='json'
  if not isinstance(params['map'],dict) or any(not isinstance(k,str) or not k or not isinstance(v,str) or not v for k,v in params['map'].items()):failure('parameter_type',path+'.map','font family string mapping')
 for key,value in params.items():
  if key not in definitions:
   if not opened:failure('parameter_unknown_field',path+'.'+key,'declared field')
  else:validate_value(definitions[key],value,path+'.'+key,resolved)
 # 描述中某些后缀写在字段后，替代参数仍是同一顶层公开键。
 return params

def validate_schema(value,schema,path='$.params',resolved=False,close=False,root=None):
 """执行固定 MCP 工具真实公开的 JSON Schema 约束，不从工具名猜测字段。"""
 if is_reference(value) and not resolved:return
 if root is None:root=schema
 if schema is True:return
 if schema is False:failure('parameter_type',path,'schema refuses value')
 if '$ref' in schema:
  reference=schema['$ref']
  if not reference.startswith('#/'):failure('parameter_schema_unsupported',path,'local schema reference')
  target=root
  for part in reference[2:].split('/'):target=target[part.replace('~1','/').replace('~0','~')]
  return validate_schema(value,target,path,resolved,close,root)
 for combinator in ('anyOf','oneOf'):
  if combinator in schema:
   successes=0
   for child in schema[combinator]:
    try:validate_schema(value,child,path,resolved,close,root);successes+=1
    except ValueError:pass
   if successes<1 or combinator=='oneOf' and successes!=1:failure('parameter_type',path,combinator)
   return
 if 'const' in schema and value!=schema['const']:failure('parameter_enum',path,str(schema['const']))
 if 'enum' in schema and value not in schema['enum']:failure('parameter_enum',path,str(schema['enum']))
 kinds=schema.get('type',[]);kinds=[kinds] if isinstance(kinds,str) else kinds
 valid={'null':value is None,'boolean':type(value) is bool,'integer':type(value) is int,'number':finite(value),'string':type(value) is str,'array':type(value) is list,'object':type(value) is dict}
 if kinds and not any(valid.get(kind,False) for kind in kinds):failure('parameter_type',path,'|'.join(kinds))
 if type(value) in (int,float):
  for key,wrong in [('minimum',lambda n:value<n),('maximum',lambda n:value>n),('exclusiveMinimum',lambda n:value<=n),('exclusiveMaximum',lambda n:value>=n)]:
   if key in schema and wrong(schema[key]):failure('parameter_range',path,key+' '+str(schema[key]))
 if isinstance(value,str):
  if 'minLength' in schema and len(value)<schema['minLength'] or 'maxLength' in schema and len(value)>schema['maxLength']:failure('parameter_shape',path,'string length')
  if 'pattern' in schema and not re.search(schema['pattern'],value):failure('parameter_shape',path,'pattern')
 if isinstance(value,list):
  if 'minItems' in schema and len(value)<schema['minItems'] or 'maxItems' in schema and len(value)>schema['maxItems']:failure('parameter_shape',path,'array length')
  for index,item in enumerate(value):validate_schema(item,schema.get('items',{}),path+'['+str(index)+']',resolved,close,root)
 if isinstance(value,dict):
  properties=schema.get('properties',{})
  for key in schema.get('required',[]):
   if key not in value:failure('parameter_required',path+'.'+key,'required field')
  for key,item in value.items():
   if key in properties:validate_schema(item,properties[key],path+'.'+key,resolved,False,root)
   elif schema.get('additionalProperties') is False or close and 'properties' in schema:failure('parameter_unknown_field',path+'.'+key,'declared field')
   elif isinstance(schema.get('additionalProperties'),dict):validate_schema(item,schema['additionalProperties'],path+'.'+key,resolved,False,root)
