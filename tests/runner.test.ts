import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, realpathSync, rmSync, writeFileSync, mkdirSync, readFileSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Ledger } from '../src/harness/ledger.ts';
import { Review } from '../src/evaluation/review.ts';

function fixture() {
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-runner-test-')));
 const request={idempotencyKey:'one',brief:'Edit the title only',plan:{document:{width:32,height:32},operations:[],exports:[{format:'png'}]},output:join(root,'delivery'),authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+60000,maxRevisions:1,reserveBytes:1024}};
 return {root,request,close:()=>rmSync(root,{recursive:true,force:true})};
}
test('invalid preflight preserves every task/event and writes no persistent plan or recovery record',async()=>{
 const {Runner}=await import('../src/harness/runner.ts');const f=fixture();
 try{
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);
  const before=JSON.stringify(ledger.status(task.id));const events=JSON.stringify(ledger.db.prepare('SELECT * FROM events').all());const files=readdirSync(ledger.root).sort();
  const runner=new Runner(ledger,{skillRoot:f.root,python:'python3'});runner.identity=()=>({sha256:'unchanged',runtimeLockSha256:'lock',files:{}});
  let checks=0;runner.python=(script,args)=>{checks++;assert.equal(script,'workflow.py');assert.ok(args.includes('--check'));throw new Error('invalid fixture plan');};
  await assert.rejects(()=>runner.run(task.id),/invalid fixture plan/);
  assert.equal(checks,1);assert.equal(JSON.stringify(ledger.status(task.id)),before);assert.equal(JSON.stringify(ledger.db.prepare('SELECT * FROM events').all()),events);assert.deepEqual(readdirSync(ledger.root).sort(),files);ledger.close();
 }finally{f.close();}
});
test('revision retains PSD requirements and scopes accepted losses to the exact base source',async()=>{
 const {Runner}=await import('../src/harness/runner.ts');
 for(const matchingSource of [false,true]){
  const f=fixture();try{
   const policy={requiredFeatures:['text','structure'],acceptedForSourceSha256:(matchingSource?'a':'d').repeat(64),acceptedLosses:{'0:structure':{status:'lost',observationSha256:'e'.repeat(64),reason:'test fixture only'}}};
   const ledger=new Ledger(join(f.root,'state'));const task=ledger.create({...f.request,plan:{...f.request.plan,exports:[{format:'png'},{format:'psd'}],psdPolicy:policy,flatExport:{colorSpace:'Rgb',transparency:'preserve'}}});const epoch=ledger.claim(task.id);ledger.transition(task.id,epoch,'verifying');ledger.recordTechnical(task.id,epoch,{status:'PASS',projectSha256:'a'.repeat(64),previewSha256:'b'.repeat(64),manifestSha256:'c'.repeat(64)});
   const review=new Review(ledger);const req=review.request(task.id);review.import(task.id,{requestId:req.id,projectSha256:req.projectSha256,previewSha256:req.previewSha256,manifestSha256:req.manifestSha256,referencesSha256:req.referencesSha256,briefSha256:req.briefSha256,rubricVersion:req.rubricVersion,evaluator:{kind:'human',identity:'test-fixture',version:'v1',contextIsolation:'fixture'},verdict:'FAIL',gaps:[{id:'title',layer:2,property:'text',reason:'Change title'}]});
   const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});/* 预算与策略单测隔离预检；真实预检及有效修订由 native-harness 验证。 */runner.preflight=()=>({sha256:'fixture',runtimeLockSha256:'fixture',files:{}});const child=await runner.revise(task.id,{baseProjectSha256:req.projectSha256,baseManifestSha256:req.manifestSha256,authorizationRef:'user',operations:[{command:'type.edit',params:{layer:2,text:'NEW'}}]});
   assert.deepEqual(child.request.plan.flatExport,{colorSpace:'Rgb',transparency:'preserve'});assert.deepEqual(child.request.plan.psdPolicy,matchingSource?policy:{requiredFeatures:policy.requiredFeatures});assert.deepEqual(ledger.status(task.id).request.plan.psdPolicy,policy);ledger.close();
  }finally{f.close();}
 }
});
test('unknown native completion is reconciled by observation, never replayed',async()=>{
 const { Runner }=await import('../src/harness/runner.ts');const f=fixture();
 try{
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);ledger.claim(task.id);
  const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});
  const state=await runner.reconcile(task.id);
  assert.equal(state.state,'reconciling');assert.equal(state.replayAllowed,false);
  await assert.rejects(()=>runner.run(task.id),/reconcile_required/);ledger.close();
 }finally{f.close();}
});
test('corrupt ledger is preserved, never silently recreated',()=>{
 const f=fixture();try{const dir=join(f.root,'state');mkdirSync(dir);const file=join(dir,'tasks.sqlite');writeFileSync(file,'not sqlite');assert.throws(()=>new Ledger(dir),/ledger_invalid/);}finally{f.close();}
});
test('reconcile refuses an unbound checkpoint without replay or technical acceptance',async()=>{
 const { Runner }=await import('../src/harness/runner.ts');const f=fixture();
 try {
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const epoch=ledger.claim(task.id);
  mkdirSync(f.request.output);writeFileSync(join(f.request.output,'failure.json'),'{}');
  const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});
  runner.python=(script,args)=>{assert.equal(script,'checkpoint_verify.py');return {result:'PASS',nativeReopened:true,projectSha256:'a'.repeat(64),replayAllowed:false};};
  ledger.update(task.id,epoch,current=>{current.executionIdentity={sha256:'original'};});
  const state=await runner.reconcile(task.id);assert.equal(state.state,'reconciling');assert.equal(state.checkpoint,undefined);assert.equal(state.technical.status,'NOT_RUN');assert.equal(state.replayAllowed,false);ledger.close();
 }finally{f.close();}
});
test('revision proposal cannot edit unrelated layers or reset revision budget',async()=>{
 const f=fixture();try{
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const epoch=ledger.claim(task.id);ledger.transition(task.id,epoch,'verifying');
  ledger.recordTechnical(task.id,epoch,{status:'PASS',projectSha256:'a'.repeat(64),previewSha256:'b'.repeat(64),manifestSha256:'c'.repeat(64)});
  const review=new Review(ledger);const request=review.request(task.id);
  review.import(task.id,{requestId:request.id,projectSha256:request.projectSha256,previewSha256:request.previewSha256,manifestSha256:request.manifestSha256,referencesSha256:request.referencesSha256,briefSha256:request.briefSha256,rubricVersion:request.rubricVersion,evaluator:{kind:'human',identity:'reviewer',version:'test-fixture/v1',contextIsolation:'independent-artifact-review'},verdict:'FAIL',gaps:[{id:'title',layer:2,property:'text',reason:'Wrong title'}]});
  const proposal={baseProjectSha256:'a'.repeat(64),baseManifestSha256:'c'.repeat(64),authorizationRef:'user',operations:[{command:'type.edit',params:{layer:2,text:'New title'}}]};
  assert.equal(review.propose(task.id,proposal).operations.length,1);
  assert.throws(()=>review.propose(task.id,{...proposal,operations:[{command:'type.edit',params:{layer:3,text:'Wrong layer'}}]}),/revision_gap_mismatch/);
  assert.throws(()=>review.propose(task.id,{...proposal,operations:[{command:'doc_new',params:{}}]}),/revision_scope_violation/);
  ledger.update(task.id,epoch,current=>{current.revisions=1;});assert.throws(()=>review.propose(task.id,proposal),/budget_exhausted/);ledger.close();
 }finally{f.close();}
});

test('unsupported ledger schema is refused without changing original bytes',()=>{
 const f=fixture();try{const ledger=new Ledger(join(f.root,'state'));ledger.db.exec('UPDATE metadata SET version=99');ledger.close();const file=join(f.root,'state/tasks.sqlite');const before=readFileSync(file);assert.throws(()=>new Ledger(join(f.root,'state')),/unsupported_ledger_schema/);assert.deepEqual(readFileSync(file),before);}finally{f.close();}
});
test('active tasks retain aggregate disk and process reservations',()=>{
 const f=fixture();try{const ledger=new Ledger(join(f.root,'state'));const first=ledger.create({...f.request,budget:{...f.request.budget,maxConcurrent:1}});ledger.claim(first.id);const second=ledger.create({...f.request,idempotencyKey:'second',output:join(f.root,'two'),budget:{...f.request.budget,maxConcurrent:1}});assert.throws(()=>ledger.claim(second.id),/concurrency_budget_exhausted/);assert.equal(ledger.status(second.id).state,'planned');ledger.close();}finally{f.close();}
});

test('descendant revisions spend the root budget once and parent stop waits for children',async()=>{
 const {Runner}=await import('../src/harness/runner.ts');const f=fixture();
 try{
  const ledger=new Ledger(join(f.root,'state'));const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});/* 预算与策略单测隔离预检；真实预检及有效修订由 native-harness 验证。 */runner.preflight=()=>({sha256:'fixture',runtimeLockSha256:'fixture',files:{}});const review=new Review(ledger);
  const failReview=(id:string)=>{
   const epoch=ledger.claim(id);ledger.transition(id,epoch,'verifying');ledger.recordTechnical(id,epoch,{status:'PASS',projectSha256:'a'.repeat(64),previewSha256:'b'.repeat(64),manifestSha256:'c'.repeat(64)});
   const request=review.request(id);review.import(id,{requestId:request.id,projectSha256:request.projectSha256,previewSha256:request.previewSha256,manifestSha256:request.manifestSha256,referencesSha256:request.referencesSha256,briefSha256:request.briefSha256,rubricVersion:request.rubricVersion,evaluator:{kind:'human',identity:'test-fixture',version:'v1',contextIsolation:'fixture'},verdict:'FAIL',gaps:[{id:'title',layer:2,property:'text',reason:'Fix title'}]});
  };
  const task=ledger.create({...f.request,budget:{...f.request.budget,maxRevisions:2}});failReview(task.id);
  const proposal={baseProjectSha256:'a'.repeat(64),baseManifestSha256:'c'.repeat(64),authorizationRef:'user',operations:[{command:'type.edit',params:{layer:2,text:'NEW'}}]};
  const child=await runner.revise(task.id,proposal);failReview(child.id);const grandchild=await runner.revise(child.id,proposal);
  assert.equal(ledger.status(task.id).revisions,2);assert.equal(grandchild.request.budget.maxRevisions,0);assert.equal(grandchild.request.budget.deadline,f.request.budget.deadline);
  review.request(task.id);assert.throws(()=>review.propose(task.id,proposal),/verified_gaps_required|budget_exhausted/);
  ledger.stop(task.id);assert.equal(ledger.status(grandchild.id).state,'cancelled');assert.equal(ledger.status(child.id).state,'cancel_requested');
  const current=ledger.status(task.id);ledger.update(task.id,current.epoch,t=>{t.stopEvidence={processGroupGone:true};});ledger.transition(task.id,current.epoch,'reconciling');
  assert.throws(()=>ledger.transition(task.id,current.epoch,'cancelled'),/child_stop_confirmation_required/);
  const stoppedChild=ledger.status(child.id);ledger.update(child.id,stoppedChild.epoch,t=>{t.stopEvidence={processGroupGone:true};});ledger.transition(child.id,stoppedChild.epoch,'reconciling');ledger.transition(child.id,stoppedChild.epoch,'cancelled');
  assert.equal(ledger.transition(task.id,current.epoch,'cancelled').state,'cancelled');ledger.close();
 }finally{f.close();}
});

test('disk shortage refuses intent and mutable GUI writes refuse before execution',async()=>{
 const {Runner}=await import('../src/harness/runner.ts');const f=fixture();
 try{
  const ledger=new Ledger(join(f.root,'state'));const enormous=ledger.create({...f.request,budget:{...f.request.budget,reserveBytes:Number.MAX_SAFE_INTEGER}});assert.throws(()=>ledger.claim(enormous.id),/disk_budget_exhausted/);assert.equal(ledger.status(enormous.id).attempted,false);
  const native=join(f.root,'mutable.pcraft');writeFileSync(native,'native');const {fileDigest}=await import('../src/protocol/files.ts');const task=ledger.create({...f.request,idempotencyKey:'mutable',mutableProject:native,expectedProjectSha256:fileDigest(native)});
  const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});await assert.rejects(()=>runner.run(task.id),/mutable_desktop_execution_not_supported/);assert.equal(readFileSync(native,'utf8'),'native');assert.equal(ledger.status(task.id).attempted,false);
  const copies=[1,2].map(index=>ledger.create({...f.request,idempotencyKey:'copy'+index,source:f.root,output:join(f.root,'copy'+index)}));for(const task of copies)assert.equal(ledger.claim(task.id),1);ledger.close();
 }finally{f.close();}
});

test('stop confirms only the owned worker and leaves unrelated process alive',async()=>{
 const { Runner }=await import('../src/harness/runner.ts');const { spawn }=await import('node:child_process');
 const f=fixture();const outsider=spawn(process.execPath,['-e','setInterval(()=>{},1000)']);
 try{
  const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));
  writeFileSync(join(skill,'scripts/runtime.lock.json'),'{}');
  writeFileSync(join(skill,'scripts/workflow.py'),'import sys,time,json,signal\nfrom pathlib import Path\nif "--check" in sys.argv: print(json.dumps({"result":"PASS"}))\nelse:\n def late(signum,frame):\n  output=Path(sys.argv[sys.argv.index("--output")+1]);output.mkdir();(output/"manifest.json").write_text("{}");sys.exit(0)\n signal.signal(signal.SIGTERM,late)\n Path(__file__).with_name("worker-ready").write_text("ready")\n while True: time.sleep(.1)\n');
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const runner=new Runner(ledger,{skillRoot:skill,python:'python3'});
  const running=runner.run(task.id);
  for(let i=0;i<100 && !ledger.status(task.id).worker;i++)await new Promise(resolve=>setTimeout(resolve,10));
  const ready=join(skill,'scripts/worker-ready');const deadline=Date.now()+10000;while(!existsSync(ready)){if(Date.now()>deadline)throw new Error('worker_readiness_timeout');await new Promise(resolve=>setTimeout(resolve,10));}ledger.stop(task.id);const stopped=await running;
  assert.equal(stopped.state,'cancelled');assert.equal(stopped.stopEvidence.processGroupGone,true);assert.equal(stopped.technical.status,'NOT_RUN');assert.equal(outsider.exitCode,null);ledger.close();
  assert.equal(stopped.stopEvidence.lateArtifacts,true);assert.equal(stopped.lateArtifactObservations[0].taskId,task.id);assert.equal(stopped.lateArtifactObservations[0].status,'OBSERVED_UNVERIFIED');
 }finally{outsider.kill();f.close();}
});

test('local adjustment revision is bound to the editable enabled mask and exact changed properties',async()=>{
 const {Runner}=await import('../src/harness/runner.ts');const {fileDigest}=await import('../src/protocol/files.ts');const f=fixture();
 try{
  const native=join(f.root,'native.json');const facts=join(f.root,'native-facts.json');
  const row={id:5,kind:'Adjustment',hasMask:true,adjustment:{BrightnessContrast:{brightness:30,contrast:0,legacy:false}}};writeFileSync(native,JSON.stringify({layers:[row]}));writeFileSync(facts,JSON.stringify({objects:{'5':{hasMask:true,maskEnabled:true,maskLinked:true,maskSurfaceSha256:'d'.repeat(64)}}}));
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create({...f.request,authorization:{...f.request.authorization,objects:[5]}});const epoch=ledger.claim(task.id);ledger.transition(task.id,epoch,'verifying');ledger.recordTechnical(task.id,epoch,{status:'PASS',projectSha256:'a'.repeat(64),previewSha256:'b'.repeat(64),manifestSha256:'c'.repeat(64),files:{[native]:fileDigest(native),[facts]:fileDigest(facts)}});
  const review=new Review(ledger);const req=review.request(task.id);review.import(task.id,{requestId:req.id,projectSha256:req.projectSha256,previewSha256:req.previewSha256,manifestSha256:req.manifestSha256,referencesSha256:req.referencesSha256,briefSha256:req.briefSha256,rubricVersion:req.rubricVersion,evaluator:{kind:'external',identity:'fixture',version:'v1',contextIsolation:'fixture'},verdict:'FAIL',gaps:[{id:'local-light',layer:5,property:'brightness',reason:'Darken only the masked product area'}]});
  const proposal={baseProjectSha256:req.projectSha256,baseManifestSha256:req.manifestSha256,authorizationRef:f.request.authorization.ref,operations:[{command:'layer.setAdjustment',params:{layer:5,brightness:-30}}],protectedRegions:[{id:'control',rect:[20,0,12,32]}]};
  assert.equal(review.propose(task.id,proposal).operations[0].command,'layer.setAdjustment');
  assert.throws(()=>review.propose(task.id,{...proposal,protectedRegions:[]}),/revision_protection_required/);
  for(const protectedRegions of [[{id:'fractional',rect:[0.5,0,1,1]}],[{id:'duplicate',rect:[0,0,1,1]},{id:'duplicate',rect:[2,0,1,1]}],[{id:'outside-limit',rect:[0,0,20000,1]}],[{id:'unknown',rect:[0,0,1,1],extra:true}]])assert.throws(()=>review.propose(task.id,{...proposal,protectedRegions}),/revision_protection_invalid/);
  assert.throws(()=>review.propose(task.id,{...proposal,operations:[{command:'layer.setAdjustment',params:{layer:5,brightness:151}}]}),/revision_parameter_invalid/);
  assert.throws(()=>review.propose(task.id,{...proposal,operations:[{command:'layer.setAdjustment',params:{layer:5,brightness:30}}]}),/revision_no_improvement/);
  assert.throws(()=>review.propose(task.id,{...proposal,operations:[{command:'layer.setAdjustment',params:{layer:5,brightness:-30,contrast:10}}]}),/revision_gap_mismatch/);
  const originalFacts=readFileSync(facts);const originalNative=readFileSync(native);
  for(const invalid of [{maskEnabled:false},{maskSurfaceSha256:undefined}]){
   writeFileSync(facts,JSON.stringify({objects:{'5':{hasMask:true,maskEnabled:true,maskLinked:true,maskSurfaceSha256:'d'.repeat(64),...invalid}}}));ledger.update(task.id,epoch,current=>{current.technical.files[facts]=fileDigest(facts);});assert.throws(()=>review.propose(task.id,proposal),/revision_object_not_editable/);
  }
  writeFileSync(facts,originalFacts);writeFileSync(native,JSON.stringify({layers:[{...row,kind:'Pixel'}]}));ledger.update(task.id,epoch,current=>{current.technical.files[facts]=fileDigest(facts);current.technical.files[native]=fileDigest(native);});assert.throws(()=>review.propose(task.id,proposal),/revision_object_not_editable/);
  writeFileSync(native,originalNative);ledger.update(task.id,epoch,current=>{current.technical.files[native]=fileDigest(native);});
  const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});/* 预算与策略单测隔离预检；真实预检及有效修订由 native-harness 验证。 */runner.preflight=()=>({sha256:'fixture',runtimeLockSha256:'fixture',files:{}});const child=await runner.revise(task.id,proposal);assert.deepEqual(child.request.plan.preserveObjects,{'5':['adjustment.BrightnessContrast.brightness']});assert.equal(child.request.plan.operations[1].params.command,'layer.setAdjustment');assert.equal(child.request.plan.assertions[0].maskEnabled,true);ledger.close();
 }finally{f.close();}
});

test('cancelled tasks register late files after ledger restart without acceptance or replay',async()=>{
 const {Runner}=await import('../src/harness/runner.ts');const {fileDigest}=await import('../src/protocol/files.ts');const {symlinkSync}=await import('node:fs');const f=fixture();
 try{
  let ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const epoch=ledger.claim(task.id);
  ledger.update(task.id,epoch,current=>{current.worker={token:'owned-fixture',exited:true,processGroupGone:true};});ledger.stop(task.id);
  const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});
  const stopped=await runner.reconcile(task.id);assert.equal(stopped.state,'cancelled');
  mkdirSync(f.request.output);writeFileSync(join(f.request.output,'project.pcraft'),'late native fixture');
  ledger.close();ledger=new Ledger(join(f.root,'state'));const reopened=new Runner(ledger,runner.options);
  const registered=await reopened.reconcile(task.id);
  assert.equal(registered.state,'cancelled');assert.equal(registered.technical.status,'NOT_RUN');assert.equal(registered.replayAllowed,false);
  assert.equal(registered.lateArtifactObservations.length,1);
  const receipt=registered.lateArtifactObservations[0];assert.equal(receipt.taskId,task.id);assert.equal(receipt.taskIdentity,task.identity);assert.equal(receipt.workerToken,'owned-fixture');assert.equal(receipt.status,'OBSERVED_UNVERIFIED');assert.equal(receipt.files['project.pcraft'],fileDigest(join(f.request.output,'project.pcraft')));
  const eventsBefore=ledger.db.prepare('SELECT COUNT(*) AS total FROM events').get();assert.equal((await reopened.reconcile(task.id)).lateArtifactObservations.length,1);assert.deepEqual(ledger.db.prepare('SELECT COUNT(*) AS total FROM events').get(),eventsBefore);
  writeFileSync(join(f.root,'outside'),'private fixture');symlinkSync(join(f.root,'outside'),join(f.request.output,'escape'));
  const unsafe=await reopened.reconcile(task.id);assert.equal(unsafe.state,'cancelled');assert.equal(unsafe.lateArtifactObservations.length,2);assert.equal(unsafe.lateArtifactObservations[1].status,'INCOMPLETE');assert.equal(unsafe.lateArtifactObservations[1].files.escape,undefined);assert.ok(unsafe.lateArtifactObservations[1].errors.some((e:any)=>e.code==='symlink_not_allowed'));
  await assert.rejects(()=>reopened.run(task.id),/reconcile_required/);ledger.close();
 }finally{f.close();}
});


test('stale mutable project revision reports conflict before unsupported desktop dispatch without changing intent',async()=>{
 const {Runner}=await import('../src/harness/runner.ts');const {fileDigest}=await import('../src/protocol/files.ts');const f=fixture();
 try{
  const ledger=new Ledger(join(f.root,'state'));const project=join(f.root,'mutable.pcraft');writeFileSync(project,'original native fixture');
  const task=ledger.create({...f.request,mutableProject:project,expectedProjectSha256:fileDigest(project)});
  writeFileSync(project,'new user-saved native fixture');const before=JSON.stringify(ledger.status(task.id));const events=JSON.stringify(ledger.db.prepare('SELECT * FROM events').all());const files=readdirSync(ledger.root).sort();
  const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});runner.preflight=()=>assert.fail('stale revision reached skill preflight');
  await assert.rejects(()=>runner.run(task.id),(error:any)=>{assert.equal(error.code,'revision_conflict');assert.equal(error.phase,'validation');assert.equal(error.outcome,'not_executed');assert.equal(error.fieldPath,'$.expectedProjectSha256');return true;});
  assert.equal(readFileSync(project,'utf8'),'new user-saved native fixture');assert.equal(JSON.stringify(ledger.status(task.id)),before);assert.equal(JSON.stringify(ledger.db.prepare('SELECT * FROM events').all()),events);assert.deepEqual(readdirSync(ledger.root).sort(),files);assert.equal(existsSync(task.request.output),false);ledger.close();
 }finally{f.close();}
});


test('unavailable mutable project observation refuses before native work without claiming a revision',async()=>{
 const {Runner}=await import('../src/harness/runner.ts');const f=fixture();
 try{
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create({...f.request,mutableProject:join(f.root,'missing.pcraft'),expectedProjectSha256:'a'.repeat(64)});const before=JSON.stringify(ledger.status(task.id));
  const runner=new Runner(ledger,{skillRoot:join(f.root,'absent'),python:'python3'});runner.preflight=()=>assert.fail('missing project reached preflight');
  await assert.rejects(()=>runner.run(task.id),(error:any)=>{assert.equal(error.code,'project_revision_unavailable');assert.equal(error.phase,'validation');assert.equal(error.outcome,'not_executed');assert.equal(error.recoveryAction,'inspect');return true;});assert.equal(JSON.stringify(ledger.status(task.id)),before);assert.equal(existsSync(task.request.output),false);ledger.close();
 }finally{f.close();}
});
