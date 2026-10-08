import test from 'node:test';
import assert from 'node:assert/strict';
import { strictJson } from '../src/protocol/strict_json.ts';
test('JSON accepts only grammar whitespace and own prototype-named keys',()=>{
 for(const text of ['\u00a0{}','[1,\u20032]','{}\ufeff'])assert.throws(()=>strictJson(text),/invalid_json/);
 const value=strictJson('{"__proto__":{"polluted":true},"constructor":1}');
 assert.equal(Object.hasOwn(value,'__proto__'),true);assert.equal(({} as any).polluted,undefined);
 assert.equal(strictJson(' \t\r\n{"x":1} ').x,1);
});
