import {canonical,digest} from './files.ts';

/** 新计划以原生 binary64 数值身份编码；旧记录无算法字段时沿用原合同。 */
export const PLAN_IDENTITY='photocraft-json-f64/v2';
function tagged(value:any):any {
 if(value===null)return ['null'];
 if(typeof value==='boolean')return ['boolean',value];
 if(typeof value==='string')return ['string',value];
 if(typeof value==='number'){
  if(!Number.isFinite(value))throw new Error('nonfinite_plan_identity');
  const bytes=Buffer.alloc(8);bytes.writeDoubleBE(value===0?0:value);return ['number',bytes.toString('hex')];
 }
 if(Array.isArray(value))return ['array',value.map(tagged)];
 if(typeof value==='object')return ['object',Object.keys(value).sort().map(key=>[key,tagged(value[key])])];
 throw new Error('invalid_plan_identity_value');
}
/** 类型标签防止数值编码与用户对象碰撞；ASCII UTF-16 转义在两种语言一致。 */
export function planDigest(plan:any,algorithm?:string|null):string {
 if(algorithm==null)return digest(canonical(plan));
 if(algorithm!==PLAN_IDENTITY)throw new Error('unknown_plan_identity_algorithm');
 const encoded=JSON.stringify(tagged(plan)).replace(/[\u007f-\uffff]/g,unit=>'\\u'+unit.charCodeAt(0).toString(16).padStart(4,'0'));
 return digest(encoded);
}
