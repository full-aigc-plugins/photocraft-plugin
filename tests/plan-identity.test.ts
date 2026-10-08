import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {join} from 'node:path';
import {PLAN_IDENTITY,planDigest} from '../src/protocol/plan_identity.ts';
import {canonical,digest} from '../src/protocol/files.ts';
test('versioned plan identity matches Python for finite numeric and UTF16 edge cases',()=>{
 const values=[{x:0.000001,small:1e-7,large:1e21,zero:-0,integer:100,float:100.0},[Number.MIN_VALUE,Number.MAX_VALUE,1.0000000000000002,333333333.3333333],{'😀':1,'\ue000':2,zh:'中文\n"\\',control:'\u007f',surrogate:'\ud800'},null,true,{},[],{'nested':[1,{'number':'3ff0000000000000'}]}];
 const script=join(process.env.PHOTOCRAFT_SKILL_ROOT??join(import.meta.dirname,'../skills/photocraft-use'),'scripts/plan_identity.py');
 for(const value of values){const result=spawnSync(process.env.PHOTOCRAFT_PYTHON??'python3',['-I','-B',script],{input:JSON.stringify(value),encoding:'utf8'});assert.equal(result.status,0,result.stdout+result.stderr);assert.equal(JSON.parse(result.stdout).sha256,planDigest(value,PLAN_IDENTITY));}
});
test('legacy plan identity stays unchanged and unknown/nonfinite algorithms fail',()=>{
 const plan={operations:[],x:1};assert.equal(planDigest(plan),digest(canonical(plan)));assert.throws(()=>planDigest(plan,'unknown'));for(const value of [NaN,Infinity,-Infinity])assert.throws(()=>planDigest({value},PLAN_IDENTITY));
});
test('typed plan identity has no user object or boolean-number collisions',()=>{
 const values=[1,true,'1',['number','3ff0000000000000'],{number:'3ff0000000000000'},null,'null'];assert.equal(new Set(values.map(value=>planDigest(value,PLAN_IDENTITY))).size,values.length);assert.equal(planDigest({n:100},PLAN_IDENTITY),planDigest({n:100.0},PLAN_IDENTITY));assert.equal(planDigest({n:-0},PLAN_IDENTITY),planDigest({n:0},PLAN_IDENTITY));
});
