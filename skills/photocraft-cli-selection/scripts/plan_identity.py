#!/usr/bin/env python3
"""有版本的计划身份：有限原生 binary64、类型标签和 UTF-16 键序；旧记录保持旧摘要。"""
import hashlib
import json
import math
import struct
import sys
ALGORITHM = 'photocraft-json-f64/v2'


def tagged(value):
    if value is None: return ['null']
    if type(value) is bool: return ['boolean', value]
    if isinstance(value, str): return ['string', value]
    if type(value) in (int, float):
        try: number = float(value)
        except OverflowError as error: raise ValueError('nonfinite_plan_identity') from error
        if not math.isfinite(number): raise ValueError('nonfinite_plan_identity')
        return ['number', struct.pack('>d', 0.0 if number == 0 else number).hex()]
    if isinstance(value, list): return ['array', [tagged(item) for item in value]]
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        return ['object', [[key, tagged(value[key])] for key in sorted(value, key=lambda key: key.encode('utf-16-be', 'surrogatepass'))]]
    raise ValueError('invalid_plan_identity_value')


def sha(value, algorithm=None):
    """算法缺失表示只读兼容历史 Python JSON 身份；新写入显式使用 ALGORITHM。"""
    if algorithm is None:
        data = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()
    elif algorithm == ALGORITHM:
        data = json.dumps(tagged(value), ensure_ascii=True, separators=(',', ':'), allow_nan=False).encode()
    else: raise ValueError('unknown_plan_identity_algorithm')
    return hashlib.sha256(data).hexdigest()


if __name__ == '__main__':
    try: print(json.dumps({'sha256': sha(json.load(sys.stdin), ALGORITHM)}))
    except (ValueError, TypeError, OverflowError) as error:
        print(json.dumps({'result': 'FAIL', 'error': str(error)})); raise SystemExit(1)
