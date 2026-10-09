"""严格 JSON：字段路径、重复键、有限数值及 JSON 语法空白。"""
import json
import math
import re

NUMBER=re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?')

class JSONContractError(ValueError):
    """保留ValueError兼容性，并携带不依赖展示文本解析的字段位置。"""
    def __init__(self,code,path):
        super().__init__(code+': '+path);self.fieldPath=path

def loads(text,fragments=None):
    if isinstance(text,bytes):text=text.decode('utf-8')
    if not isinstance(text,str):raise TypeError('JSON text required')
    offset=0
    decoder=json.JSONDecoder()
    def syntax(message):raise json.JSONDecodeError(message,text,offset)
    def space():
        nonlocal offset
        while offset<len(text) and text[offset] in ' \t\r\n':offset+=1
    def string(path,is_key=False):
        nonlocal offset
        value,length=decoder.raw_decode(text,offset)
        if not isinstance(value,str):syntax('string required')
        offset=length
        try:value.encode('utf-8')
        except UnicodeEncodeError:
            location=path+'['+json.dumps(value)+']' if is_key else path
            raise JSONContractError('invalid_json_unicode',location) from None
        return value
    def value(path='$',depth=0):
        # 仅记录调用方指定的已验证值片段，不给大数组逐元素保留副本。
        space();start=offset;result=parse_value(path,depth)
        if fragments is not None and path in fragments:fragments[path]=text[start:offset]
        return result
    def parse_value(path='$',depth=0):
        nonlocal offset
        if depth>128:raise JSONContractError('json_depth_limit',path)
        space()
        if offset>=len(text):syntax('value required')
        token=text[offset]
        if token=='"':return string(path)
        if token in '{[':
            is_object=token=='{';offset+=1;result={} if is_object else [];closing='}' if is_object else ']'
            space()
            if offset<len(text) and text[offset]==closing:offset+=1;return result
            while True:
                space()
                if is_object:
                    if offset>=len(text) or text[offset]!='"':syntax('object key required')
                    key=string(path,True);child=path+'.'+key if re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',key) else path+'['+json.dumps(key,ensure_ascii=False)+']'
                    if key in result:raise JSONContractError('duplicate_json_key',child)
                    space()
                    if offset>=len(text) or text[offset]!=':':syntax('colon required')
                    offset+=1;result[key]=value(child,depth+1)
                else:result.append(value(path+'['+str(len(result))+']',depth+1))
                space()
                if offset>=len(text):syntax('unterminated container')
                delimiter=text[offset];offset+=1
                if delimiter==closing:return result
                if delimiter!=',':syntax('comma required')
        for literal,result in [('true',True),('false',False),('null',None)]:
            if text.startswith(literal,offset):offset+=len(literal);return result
        for literal in ('NaN','Infinity','-Infinity'):
            if text.startswith(literal,offset):raise JSONContractError('nonfinite_json_value',path)
        match=NUMBER.match(text,offset)
        if not match:syntax('invalid value')
        offset=match.end();number=match.group()
        # 先按原生有限f64边界检查文本，避免Python超长整数限制丢失字段路径。
        if not math.isfinite(float(number)):raise JSONContractError('nonfinite_json_value',path)
        result=json.loads(number)
        return result
    result=value();space()
    if offset!=len(text):syntax('trailing content')
    return result
