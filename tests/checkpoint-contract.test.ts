import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, realpathSync, rmSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { Ledger } from '../src/harness/ledger.ts';
import { Runner } from '../src/harness/runner.ts';
import { fileDigest, readJson } from '../src/protocol/files.ts';
import { runtimePlatformKey } from '../src/harness/preflight.ts';

function fixture() {
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-checkpoint-contract-')));
 const output=join(root,'delivery'),stage=join(root,'retained');mkdirSync(output);mkdirSync(stage);
 writeFileSync(join(stage,'project.pcraft'),'synthetic contract fixture, not native acceptance');
 writeFileSync(join(stage,'recovery-operations.json'),'[]');
 const files=Object.fromEntries(['project.pcraft','recovery-operations.json'].map(name=>[name,{sha256:fileDigest(join(stage,name)),bytes:readFileSync(join(stage,name)).length}]));
 const record={schema:'craft-failed-stage/v1',status:'failed',outcome:'outcome_unknown',stage:'../retained',files,completedOperations:0,lastAttempt:{tool:'doc_save',arguments:{path:'project.pcraft'},phase:'submitted'},replayAllowed:false};
 for(const path of [join(output,'failure.json'),join(stage,'failure.json')])writeFileSync(path,JSON.stringify(record));
 const ledger=new Ledger(join(root,'state'));const task=ledger.create({idempotencyKey:'checkpoint',brief:'Inspect retained project',plan:{document:{width:32,height:32},operations:[]},output,authorization:{ref:'fixture',writeRoot:root},budget:{deadline:Date.now()+60000,maxRevisions:1,reserveBytes:1024}});
 const runner=new Runner(ledger,{skillRoot:resolve('skills/photocraft-use'),python:process.env.PHOTOCRAFT_PYTHON??'python3'});
 const epoch=ledger.claim(task.id);ledger.update(task.id,epoch,value=>{value.executionIdentity=runner.identity();value.executionResult={outcome:'unknown',phase:'submitted'};});
 const reply={schema:'photocraft-checkpoint-verification/v1',result:'PASS',stage,recordSha256:fileDigest(join(output,'failure.json')),projectSha256:files['project.pcraft'].sha256,files,lastAttempt:record.lastAttempt,completedOperations:0,nativeReopened:true,objectCount:0,runtimeSha256:readJson(join(runner.options.skillRoot,'scripts/runtime.lock.json')).artifacts[runtimePlatformKey()].binarySha256,replayAllowed:false,technical:'NOT_RUN',creative:'NOT_RUN'};
 let calls=0;runner.python=(script)=>{assert.equal(script,'checkpoint_verify.py');calls++;return reply;};
 return {root,output,stage,record,reply,ledger,runner,task,calls:()=>calls,close(){ledger.close();rmSync(root,{recursive:true,force:true});}};
}

test('checkpoint reply binds original record, saved files, runtime and partial acceptance',async()=>{
 const f=fixture();try{const result=await f.runner.reconcile(f.task.id);assert.equal(result.state,'reconciling');assert.equal(result.checkpoint.recordSha256,f.reply.recordSha256);assert.equal(result.executionResult.outcome,'unknown');assert.equal(result.technical.status,'NOT_RUN');assert.equal(result.replayAllowed,false);assert.equal(f.calls(),1);}finally{f.close();}
});
const mutations:Record<string,(reply:any)=>void>={
 missingSchema:r=>delete r.schema,wrongStage:r=>r.stage+='-other',wrongRecord:r=>r.recordSha256='a'.repeat(64),wrongProject:r=>r.projectSha256='a'.repeat(64),wrongRuntime:r=>r.runtimeSha256='a'.repeat(64),missingFiles:r=>delete r.files,wrongCompleted:r=>r.completedOperations++,wrongAttempt:r=>r.lastAttempt={phase:'reply_validated'},notReopened:r=>r.nativeReopened=false,invalidCount:r=>r.objectCount=-1,technicalPass:r=>r.technical='PASS',creativePass:r=>r.creative='PASS',contradictoryError:r=>r.error='not actually verified',extraStatus:r=>r.status='FAIL',failedResult:r=>{r.result='FAIL';r.error='native reopen failed';},
};
for(const [name,mutate]of Object.entries(mutations))test('checkpoint refuses '+name+' without replay or checkpoint acceptance',async()=>{
 const f=fixture();try{mutate(f.reply);const result=await f.runner.reconcile(f.task.id);assert.equal(result.checkpoint,undefined);assert.equal(result.state,'reconciling');assert.equal(result.technical.status,'NOT_RUN');assert.equal(result.executionResult.outcome,'unknown');assert.equal(result.replayAllowed,false);assert.equal(result.verificationError.phase,'verification');assert.equal(result.verificationError.retryable,false);assert.equal(result.verificationError.outcome,name==='failedResult'?'failed':'unknown');}finally{f.close();}
});
test('checkpoint verification refuses source drift before calling native checker',async()=>{
 const f=fixture();try{f.runner.identity=()=>({sha256:'changed',files:{},runtimeLockSha256:'changed'});const result=await f.runner.reconcile(f.task.id);assert.equal(f.calls(),0);assert.equal(result.checkpoint,undefined);assert.equal(result.verificationError.code,'skill_source_changed');}finally{f.close();}
});
test('checkpoint verification refuses files changed during checker and revokes stale current acceptance',async()=>{
 const f=fixture();try{await f.runner.reconcile(f.task.id);f.runner.python=()=>{writeFileSync(join(f.stage,'project.pcraft'),'external writer change');return f.reply;};const result=await f.runner.reconcile(f.task.id);assert.equal(result.checkpoint,undefined);assert.equal(result.verificationError.outcome,'unknown');assert.equal(readFileSync(join(f.stage,'project.pcraft'),'utf8'),'external writer change');}finally{f.close();}
});
test('checkpoint verification rejects corrupt records and escaping dependencies before native dispatch',async()=>{
 for(const name of ['stageEscape','fileEscape','operationCount','lastAttempt','recordConflict']){
  const f=fixture();try{
   const record:any=JSON.parse(JSON.stringify(f.record));
   if(name==='stageEscape')record.stage='../../outside';
   if(name==='fileEscape')record.files['../outside']={sha256:'a'.repeat(64),bytes:1};
   if(name==='operationCount')record.completedOperations=1;
   if(name==='lastAttempt')record.lastAttempt={tool:123,arguments:[],phase:'anything'};
   if(name==='recordConflict')record.lastAttempt.phase='reply_validated';
   writeFileSync(join(f.output,'failure.json'),JSON.stringify(record));
   if(name!=='recordConflict')writeFileSync(join(f.stage,'failure.json'),JSON.stringify(record));
   const result=await f.runner.reconcile(f.task.id);assert.equal(f.calls(),0,name);assert.equal(result.checkpoint,undefined,name);assert.equal(result.verificationError.outcome,'unknown');
  }finally{f.close();}
 }
});
test('checkpoint source identity is checked again after native observation',async()=>{
 const f=fixture();try{f.runner.python=()=>{f.runner.identity=()=>({sha256:'changed',files:{},runtimeLockSha256:'changed'});return f.reply;};const result=await f.runner.reconcile(f.task.id);assert.equal(result.checkpoint,undefined);assert.equal(result.verificationError.code,'skill_source_changed');}finally{f.close();}
});
