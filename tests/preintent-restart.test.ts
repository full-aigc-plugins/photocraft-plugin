import test from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {existsSync,mkdtempSync,realpathSync,writeFileSync,readFileSync,rmSync,statSync,symlinkSync,linkSync,mkdirSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {Ledger} from '../src/harness/ledger.ts';
import {Runner} from '../src/harness/runner.ts';
import {canonical,fileDigest} from '../src/protocol/files.ts';
function fixture(){
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-preintent-')));let ledger=new Ledger(join(root,'state'));
 const task=ledger.create({idempotencyKey:'original',brief:'preserve preintent identity',plan:{document:{width:64,height:64,background:'#ffffff'},operations:[{command:'type.create',params:{text:'ONCE',font:'Arial',size:12,x:8,y:20}}],exports:[{format:'png'}]},output:join(root,'delivery'),authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+120000,maxRevisions:1,reserveBytes:0}});
 const runner=new Runner(ledger,{skillRoot:root,python:'python3'});runner.preflight=()=>({sha256:'fixture',runtimeLockSha256:'fixture',files:{}});
 return {root,ledger,task,runner,planPath:join(ledger.root,task.id+'-plan.json'),reopen(){ledger.close();ledger=new Ledger(join(root,'state'));this.ledger=ledger;},close(){ledger.close();rmSync(root,{recursive:true,force:true});}};
}
test('unattempted task can reuse its exact pinned plan after claim budget refusal',async()=>{
 const f=fixture();try{
  const before=canonical(f.ledger.status(f.task.id));let calls=0;f.ledger.claim=()=>{calls++;throw new Error('budget_exhausted');};
  await assert.rejects(()=>f.runner.run(f.task.id),/budget_exhausted/);const pin=readFileSync(f.planPath),inode=statSync(f.planPath).ino;
  await assert.rejects(()=>f.runner.run(f.task.id),/budget_exhausted/);assert.equal(calls,2);assert.deepEqual(readFileSync(f.planPath),pin);assert.equal(statSync(f.planPath).ino,inode);assert.equal(canonical(f.ledger.status(f.task.id)),before);assert.equal(existsSync(join(f.ledger.root,f.task.id+'-worker-launch.json')),false);
 }finally{f.close();}
});
test('foreign truncated linked or nonregular preintent plans preserve files and ledger without claiming',async()=>{
 for(const kind of ['foreign','truncated','symlink','hardlink','directory']){
  const f=fixture();try{
   const external=join(f.root,'external');writeFileSync(external,canonical(f.task.request.plan));
   if(kind==='symlink')symlinkSync(external,f.planPath);else if(kind==='hardlink')linkSync(external,f.planPath);else if(kind==='directory')mkdirSync(f.planPath);else writeFileSync(f.planPath,kind==='truncated'?'{':canonical({operations:[]}));
   const before=canonical(f.ledger.status(f.task.id)),externalBefore=readFileSync(external);let claims=0;f.ledger.claim=()=>{claims++;throw new Error('claim reached');};
   await assert.rejects(()=>f.runner.run(f.task.id),/pinned_plan_conflict|symlink_not_allowed/);assert.equal(claims,0);assert.equal(canonical(f.ledger.status(f.task.id)),before);assert.deepEqual(readFileSync(external),externalBefore);assert.equal(existsSync(f.task.request.output),false);
  }finally{f.close();}
 }
});
test('native SIGKILL between pinned plan and intent resumes the same task exactly once',{skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const f=fixture();let child:any;try{
  const options={skillRoot:process.env.PHOTOCRAFT_SKILL_ROOT!,python:process.env.PHOTOCRAFT_PYTHON??'python3'},marker=join(f.root,'before-claim'),script=join(f.root,'interrupt.mjs');
  writeFileSync(script,`import {Ledger} from ${JSON.stringify(pathToFileURL(resolve('src/harness/ledger.ts')).href)};import {Runner} from ${JSON.stringify(pathToFileURL(resolve('src/harness/runner.ts')).href)};import {writeFileSync} from 'node:fs';const ledger=new Ledger(${JSON.stringify(f.ledger.root)});ledger.claim=()=>{writeFileSync(${JSON.stringify(marker)},'before intent');Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,60000);throw new Error('interrupt not delivered');};await new Runner(ledger,${JSON.stringify(options)}).run(${JSON.stringify(f.task.id)});`);
  child=spawn(process.execPath,[script],{stdio:['ignore','pipe','pipe']});let diagnostics='';child.stderr.on('data',(data:Buffer)=>{diagnostics+=data.toString();});
  const deadline=Date.now()+15000;while(!existsSync(marker)){if(child.exitCode!==null||Date.now()>deadline)throw new Error('preintent window missing: '+diagnostics);await new Promise(resolve=>setTimeout(resolve,20));}
  const pin=readFileSync(f.planPath),inode=statSync(f.planPath).ino;const closed=new Promise(resolve=>child.once('close',resolve));child.kill('SIGKILL');await closed;f.reopen();
  const before=f.ledger.status(f.task.id);assert.equal(before.state,'planned');assert.equal(before.attempted,false);assert.equal(before.epoch,0);assert.equal(before.worker,undefined);assert.equal(existsSync(join(f.ledger.root,f.task.id+'-worker-launch.json')),false);assert.equal(existsSync(f.task.request.output),false);
  const restarted=new Runner(f.ledger,options),result=await restarted.run(f.task.id);assert.equal(result.technical.status,'PASS');assert.equal(result.id,f.task.id);assert.equal(result.epoch,1);assert.deepEqual(result.request.budget,f.task.request.budget);assert.equal(result.revisions,0);assert.deepEqual(readFileSync(f.planPath),pin);assert.equal(statSync(f.planPath).ino,inode);assert.equal(f.ledger.db.prepare("SELECT count(*) AS n FROM events WHERE task=? AND json_extract(data,'$.event')='intent_persisted'").get(f.task.id).n,1);
  await assert.rejects(()=>restarted.run(f.task.id),/reconcile_required/);const native=JSON.parse(readFileSync(join(f.task.request.output,'native.json'),'utf8'));assert.equal(native.layers.filter((layer:any)=>layer.kind==='Type').length,1);
  if(process.env.PHOTOCRAFT_PREINTENT_REPORT)writeFileSync(process.env.PHOTOCRAFT_PREINTENT_REPORT,JSON.stringify({schema:'photocraft-preintent-native/v1',status:'PASS',taskId:f.task.id,taskIdentity:f.task.identity,originalPlanSha256:fileDigest(f.planPath),retainedPlanInode:true,originalEpoch:0,finalEpoch:1,intentsPersisted:1,repeatedRunRefused:true,typeLayerCount:1,budgetUnchanged:true,sourceSha256:result.executionIdentity.sha256,creative:'NOT_RUN'},null,2)+'\n');
 }finally{if(child && child.exitCode===null && child.signalCode===null)child.kill('SIGKILL');f.close();}
});
