"""保留已严格校验的serve词法片段，避免合法请求在转发时数值膨胀。"""
import json


def compact(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':'),allow_nan=False)


def native_integer(text):
    """对应固定serde_json的i64/u64整数范围、负零与有限f64回退。"""
    value=int(text)
    if text=='-0' or not -(1<<63)<=value<(1<<64):return float(text)
    return value


class Frame(dict):
    """字典保留原请求供校验与回执使用，线缆载荷仅来自已校验JSON。"""
    def __init__(self,message,raw,fragments):
        super().__init__(message)
        if isinstance(raw,bytes):raw=raw.decode('utf-8')
        self.wire_payload=(raw.rstrip('\r\n')+'\n').encode('utf-8')
        self.wire_fragments=fragments
        self.native_id=json.loads(fragments.get('$.id') or 'null',parse_int=native_integer)


def batch_child(parent,index,child):
    """拆批时只更换包络，ID与步骤参数的数值词法保持原样。"""
    fragments=getattr(parent,'wire_fragments',{})
    identifier=fragments.get('$.id') or compact(parent.get('id'))
    params=fragments.get('$.params.steps['+str(index)+'].params')
    step=parent['params']['steps'][index]
    if params is None:params=compact(step.get('params'))
    if 'command' in step:params='{"command":'+compact(step['command'])+',"params":'+params+'}'
    raw='{"id":'+identifier+',"method":'+compact(child['method'])+',"params":'+params+'}'
    return Frame(child,raw,{'$.id':identifier})
