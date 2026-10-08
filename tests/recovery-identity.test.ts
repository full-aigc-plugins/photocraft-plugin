import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, realpathSync, rmSync, mkdirSync, writeFileSync, readFileSync, cpSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Ledger } from '../src/harness/ledger.ts';
import { Runner } from '../src/harness/runner.ts';
import { canonical, digest, fileDigest } from '../src/protocol/files.ts';

function setup(){
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-recovery-identity-')));const ledger=new Ledger(join(root,'state'));
 const request={idempotencyKey:'original',brief:'original title',plan:{document:{width:32,height:32},operations:[]},output:join(root,'output'),authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+60000,maxRevisions:1,reserveBytes:1024}};
 return {root,ledger,request,close(){ledger.close();rmSync(root,{recursive:true,force:true});}};
}

test('corrupt attempt flags and missing persisted intent never restore permission to dispatch',()=>{
 for(const mutation of ['missingAttempt','epochReset','plannedReset','missingStart','missingIntentEvent']){
  const f=setup();try{
   const task=f.ledger.create(f.request);f.ledger.claim(task.id);const value=f.ledger.status(task.id);
   if(mutation==='missingAttempt')delete value.attempted;
   if(mutation==='epochReset')value.epoch=0;
   if(mutation==='plannedReset'){value.state='planned';value.attempted=false;value.epoch=0;delete value.startedAt;}
   if(mutation==='missingStart')delete value.startedAt;
   f.ledger.db.prepare('UPDATE tasks SET data=? WHERE id=?').run(canonical(value),task.id);
   if(mutation==='missingIntentEvent')f.ledger.db.prepare('DELETE FROM events WHERE task=?').run(task.id);
   const before=JSON.stringify(f.ledger.db.prepare('SELECT * FROM tasks').all());const events=JSON.stringify(f.ledger.db.prepare('SELECT * FROM events').all());
   assert.throws(()=>f.ledger.status(task.id),/task_intent_invalid/,mutation);
   assert.throws(()=>f.ledger.claim(task.id),/task_intent_invalid/,mutation);
   assert.equal(JSON.stringify(f.ledger.db.prepare('SELECT * FROM tasks').all()),before);assert.equal(JSON.stringify(f.ledger.db.prepare('SELECT * FROM events').all()),events);
  }finally{f.close();}
 }
});

test('recovery refuses a self-consistent foreign plan before native verification',async()=>{
 const f=setup();try{
  const task=f.ledger.create(f.request);const epoch=f.ledger.claim(task.id);mkdirSync(f.request.output);
  writeFileSync(join(f.request.output,'project.pcraft'),'fixture');writeFileSync(join(f.request.output,'plan.json'),JSON.stringify({document:{width:64,height:64},operations:[]}));
  const manifest={schema:'photocraft-delivery/v1',sourceProjectSha256:null,files:{'project.pcraft':fileDigest(join(f.request.output,'project.pcraft')),'plan.json':fileDigest(join(f.request.output,'plan.json'))}};writeFileSync(join(f.request.output,'manifest.json'),JSON.stringify(manifest));
  const runner=new Runner(f.ledger,{skillRoot:f.root,python:'python3'});runner.identity=()=>({sha256:'fixture',files:{},runtimeLockSha256:'fixture'});f.ledger.update(task.id,epoch,t=>{t.executionIdentity=runner.identity();});
  const calls:string[]=[];runner.python=(script)=>{calls.push(script);if(script!=='delivery.py')throw new Error('native verification must not start');return {schema:'photocraft-delivery-integrity/v1',result:'PASS',manifestSha256:fileDigest(join(f.request.output,'manifest.json')),nativeSha256:manifest.files['project.pcraft'],files:2};};
  const result=await runner.reconcile(task.id);assert.equal(result.state,'reconciling');assert.equal(result.technical.status,'NOT_RUN');assert.match(result.reconcileError,/task_delivery_plan_mismatch/);assert.deepEqual(calls,['delivery.py']);assert.equal(result.replayAllowed,false);
 }finally{f.close();}
});

test('actual native recovery rejects another valid task package and preserves original intent',{skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const f=setup();try{
  const runner=new Runner(f.ledger,{skillRoot:process.env.PHOTOCRAFT_SKILL_ROOT!,python:process.env.PHOTOCRAFT_PYTHON??'python3'});
  const make=(key:string,text:string)=>f.ledger.create({...f.request,idempotencyKey:key,output:join(f.root,key),plan:{document:{width:64,height:64,background:'#ffffff'},operations:[{command:'type.create',params:{text,font:'Arial',size:12,x:8,y:20}}],exports:[{format:'png'}]}});
  const original=make('original','ORIGINAL');const foreign=make('foreign','FOREIGN');const first=await runner.run(original.id);const second=await runner.run(foreign.id);assert.equal(first.technical.status,'PASS');assert.equal(second.technical.status,'PASS');
  const retained=join(f.root,'retained-original');cpSync(original.request.output,retained,{recursive:true});rmSync(original.request.output,{recursive:true});cpSync(foreign.request.output,original.request.output,{recursive:true});
  f.ledger.transition(original.id,first.epoch,'reconciling');const before=f.ledger.status(original.id);const attempts=before.epoch;const reply=await runner.reconcile(original.id);
  assert.equal(reply.state,'reconciling');assert.equal(reply.technical.status,'NOT_RUN');assert.equal(reply.artifact,undefined);assert.match(reply.reconcileError,/task_delivery_plan_mismatch/);assert.equal(reply.attempted,true);assert.equal(reply.epoch,attempts);await assert.rejects(()=>runner.run(original.id),/reconcile_required/);
  rmSync(original.request.output,{recursive:true});cpSync(retained,original.request.output,{recursive:true});const recovered=await runner.reconcile(original.id);assert.equal(recovered.state,'verifying');assert.equal(recovered.technical.status,'PASS');assert.equal(recovered.epoch,attempts);assert.equal(recovered.artifact.producerTaskId,original.id);
  if(process.env.PHOTOCRAFT_RECOVERY_REPORT)writeFileSync(process.env.PHOTOCRAFT_RECOVERY_REPORT,JSON.stringify({schema:'photocraft-recovery-identity-evidence/v1',status:'PASS',originalTaskId:original.id,foreignTaskId:foreign.id,originalPlanSha256:digest(canonical(original.request.plan)),foreignPlanSha256:digest(canonical(foreign.request.plan)),originalProjectSha256:first.technical.projectSha256,foreignProjectSha256:second.technical.projectSha256,sourceSha256:first.executionIdentity.sha256,foreignPackageRefused:true,staleTechnicalRevoked:true,staleArtifactRevoked:true,originalRestored:true,repeatedEdits:0,epoch:recovered.epoch,creative:recovered.creative.status},null,2)+'\n');
 }finally{f.close();}
});

test('incomplete schema is refused without rebuilding missing state tables',()=>{
 for(const table of ['tasks','resources','events']){
  const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-incomplete-ledger-')));
  try{
   const state=join(root,'state');const ledger=new Ledger(state);ledger.db.exec('DROP TABLE '+table);ledger.close();const path=join(state,'tasks.sqlite');const before=readFileSync(path);
   assert.throws(()=>new Ledger(state),/ledger_schema_incomplete/,table);assert.deepEqual(readFileSync(path),before);
  }finally{rmSync(root,{recursive:true,force:true});}
 }
});
