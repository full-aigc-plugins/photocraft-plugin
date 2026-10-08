import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { existsSync, mkdtempSync, realpathSync, mkdirSync, writeFileSync, rmSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { Ledger } from '../src/harness/ledger.ts';
import { Runner } from '../src/harness/runner.ts';
import { Review } from '../src/evaluation/review.ts';
import { canonical, digest, fileDigest } from '../src/protocol/files.ts';

async function until(check:()=>boolean) {
 const deadline=Date.now()+10000;while(!check()){if(Date.now()>deadline)throw new Error('condition_timeout');await new Promise(resolve=>setTimeout(resolve,25));}
}

for(const mode of ['stop','deadline'])test('interrupted runner retains supervisor ownership and restart confirms '+mode+' without resetting budgets',async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-supervisor-')));let outer:any;let ledger:Ledger|undefined;
 const outsider=spawn(process.execPath,['-e','setInterval(()=>{},1000)']);
 try{
  const skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));writeFileSync(join(skill,'scripts/runtime.lock.json'),'{}');
  writeFileSync(join(skill,'scripts/workflow.py'),`import sys,time,json,signal\nfrom pathlib import Path\nif '--check' in sys.argv: print(json.dumps({'result':'PASS'}))\nelse:\n output=Path(sys.argv[sys.argv.index('--output')+1]);output.mkdir()\n def late(signum,frame):\n  time.sleep(.3);(output/'project.pcraft').write_text('late fixture');sys.exit(0)\n signal.signal(signal.SIGTERM,late)\n (output/'ready').write_text('ready')\n while True: time.sleep(.05)\n`);
  const state=join(root,'state');ledger=new Ledger(state);const request={idempotencyKey:'interrupted',brief:'cancel fixture',plan:{operations:[]},output:join(root,'output'),authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+(mode==='deadline'?1800:30000),maxRevisions:2,maxConcurrent:1,reserveBytes:1024}};
  const task=ledger.create(request);const cli=resolve('src/cli.ts');outer=spawn(process.execPath,[cli,'run','--state-dir',state,'--task',task.id,'--skill-root',skill,'--python',process.env.PHOTOCRAFT_PYTHON??'python3'],{stdio:'ignore'});
  await until(()=>existsSync(join(request.output,'ready')));const running=ledger.status(task.id);assert.ok(running.worker.supervisor);
  const closed=new Promise(resolve=>outer.once('close',resolve));outer.kill('SIGKILL');await closed;
  const before=ledger.status(task.id);if(mode==='stop')ledger.stop(task.id);else await until(()=>existsSync(join(state,task.id+'.stop')));const runner=new Runner(ledger,{skillRoot:skill,python:'python3'});
  const pending=await runner.reconcile(task.id);assert.equal(pending.state,'reconciling');assert.equal(pending.worker.exited,undefined);await assert.rejects(()=>runner.verify(task.id),/stopped_task_verification_forbidden/);
  const second=ledger.create({...request,idempotencyKey:'second',output:join(root,'second'),budget:{...request.budget,deadline:Date.now()+30000}});assert.throws(()=>ledger!.claim(second.id),/concurrency_budget_exhausted/);
  ledger.close();ledger=new Ledger(state);const restarted=new Runner(ledger,runner.options);
  await until(()=>existsSync(join(state,task.id+'-worker-exit.json')));
  let result=await restarted.reconcile(task.id);for(let i=0;i<100 && result.state!=='cancelled';i++){await new Promise(resolve=>setTimeout(resolve,25));result=await restarted.reconcile(task.id);}
  assert.equal(result.state,'cancelled');assert.equal(result.stopEvidence.processGroupGone,true);assert.equal(result.worker.exited,true);assert.deepEqual(result.request.budget,request.budget);assert.equal(result.startedAt,before.startedAt);assert.equal(result.revisions,before.revisions);assert.ok(result.elapsedMs>=300);assert.equal(result.technical.status,'NOT_RUN');assert.equal(result.replayAllowed,false);assert.ok(result.lateArtifactObservations.at(-1).files['project.pcraft']);assert.equal(outsider.exitCode,null);
  await assert.rejects(()=>restarted.run(task.id),/reconcile_required/);assert.equal(ledger.claim(second.id),1);
 }finally{if(ledger){for(const row of ledger.db.prepare('SELECT id FROM tasks').all() as any[])try{ledger.stop(row.id);}catch{}}outer?.kill();outsider.kill();await new Promise(resolve=>setTimeout(resolve,250));ledger?.close();rmSync(root,{recursive:true,force:true});}
});

test('receipt mismatches and live process groups cannot release a stopped reservation',async()=>{
 const {confirmedWorkerReceipt}=await import('../src/harness/worker_receipt.ts');const {canonical,fileDigest}=await import('../src/protocol/files.ts');
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-receipt-')));const alive=spawn(process.execPath,['-e','setInterval(()=>{},1000)'],{detached:true,stdio:'ignore'});
 try{
  const launchPath=join(root,'task-worker-launch.json');writeFileSync(launchPath,'{}');const launchSha256=fileDigest(launchPath);
  const task={id:'task',identity:'identity',epoch:1,executionIdentity:{sha256:'source'},worker:{supervisor:true,token:'token',childPid:alive.pid,startedAt:Date.now()-100,launchSha256}};
  const path=join(root,'task-worker-exit.json');const receipt={schema:'photocraft-worker-exit/v1',taskId:'task',taskIdentity:'identity',epoch:1,workerToken:'token',sourceSha256:'source',launchSha256,supervisorPid:alive.pid,workflowPid:null,processGroupGone:true,finishedAt:Date.now()};
  assert.equal(confirmedWorkerReceipt(root,task),undefined);
  writeFileSync(path,canonical(receipt));assert.equal(confirmedWorkerReceipt(root,task),undefined);
  for(const mismatch of [{taskId:'other'},{taskIdentity:'other'},{epoch:2},{workerToken:'other'},{sourceSha256:'other'},{launchSha256:'other'},{supervisorPid:0},{workflowPid:-1},{processGroupGone:false},{finishedAt:0}]){
   writeFileSync(path,canonical({...receipt,...mismatch}));assert.throws(()=>confirmedWorkerReceipt(root,task),/worker_receipt_identity_mismatch/);
  }
  writeFileSync(path,canonical(receipt));writeFileSync(launchPath,'changed');assert.throws(()=>confirmedWorkerReceipt(root,task),/worker_receipt_identity_mismatch/);
 }finally{alive.kill();rmSync(root,{recursive:true,force:true});}
});

test('real native worker cancellation survives runner interruption and retains the source project',{skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-native-stop-')));let outer:any;let ledger:Ledger|undefined;
 try{
  const options={skillRoot:process.env.PHOTOCRAFT_SKILL_ROOT!,python:process.env.PHOTOCRAFT_PYTHON??'python3'};const state=join(root,'state');ledger=new Ledger(state);const runner=new Runner(ledger,options);
  const budget={deadline:Date.now()+120000,maxRevisions:1,reserveBytes:1048576,maxConcurrent:1};
  const baseline=ledger.create({idempotencyKey:'baseline',brief:'retain the saved title project',plan:{document:{width:64,height:64,background:'#ffffff'},operations:[{command:'type.create',params:{text:'KEEP',font:'Arial',size:12,x:8,y:20},as:'title'}],exports:[{format:'png'}]},output:join(root,'baseline'),authorization:{ref:'test-user',writeRoot:root},budget});
  const created=await runner.run(baseline.id);assert.equal(created.technical.status,'PASS');
  const project=join(root,'baseline/project.pcraft');const original=readFileSync(project);const manifest=JSON.parse(readFileSync(join(root,'baseline/manifest.json'),'utf8'));
  // 合成审查回执仅建立父子任务合同，不是创作质量验收。
  const review=new Review(ledger);const requested=review.request(baseline.id);
  review.import(baseline.id,{requestId:requested.id,projectSha256:requested.projectSha256,previewSha256:requested.previewSha256,manifestSha256:requested.manifestSha256,referencesSha256:requested.referencesSha256,briefSha256:requested.briefSha256,rubricVersion:requested.rubricVersion,evaluator:{kind:'external',identity:'cancellation-contract-fixture',version:'v1',contextIsolation:'fixture-not-creative-acceptance'},verdict:'FAIL',gaps:[{id:'title',layer:manifest.bindings.title.layer,property:'text',reason:'fixture title changes for cancellation'}]});
  const task=await runner.revise(baseline.id,{baseProjectSha256:created.technical.projectSha256,baseManifestSha256:created.technical.manifestSha256,authorizationRef:'test-user',operations:Array.from({length:100},(_,index)=>({command:'type.edit',params:{layer:manifest.bindings.title.layer,text:'CANCEL '+index}}))});
  outer=spawn(process.execPath,[resolve('src/cli.ts'),'run','--state-dir',state,'--task',task.id,'--skill-root',options.skillRoot,'--python',options.python],{stdio:['ignore','pipe','ignore']});
  let native:any;let diagnostic='';outer.stdout?.on('data',(data:Buffer)=>{diagnostic+=data.toString();});
  try{await until(()=>{const rows=execFileSync('ps',['-axo','pid,ppid,pgid,command'],{encoding:'utf8'}).split('\n');const row=rows.find(row=>row.includes(root+'/.photocraft-') && row.includes(' mcp '));if(!row)return false;const match=row.trim().match(/^(\d+)\s+(\d+)\s+(\d+)/)!;native={pid:Number(match[1]),parent:Number(match[2]),group:Number(match[3])};return true;});}catch(error){throw new Error(String(error)+'; '+diagnostic+'; state='+ledger.status(task.id).state);}
  assert.ok(native.pid>0);process.kill(native.pid,0);const before=ledger.status(task.id);assert.equal(before.state,'running');
  const closed=new Promise(resolve=>outer.once('close',resolve));outer.kill('SIGKILL');await closed;ledger.stop(baseline.id);ledger.close();ledger=new Ledger(state);const restarted=new Runner(ledger,options);
  const parentPending=await restarted.reconcile(baseline.id);assert.equal(parentPending.state,'reconciling');assert.ok(ledger.db.prepare('SELECT owner FROM resources WHERE owner=?').get(baseline.id));
  let result=await restarted.reconcile(task.id);await until(()=>existsSync(join(state,task.id+'-worker-exit.json')));
  for(let i=0;i<100 && result.state!=='cancelled';i++){await new Promise(resolve=>setTimeout(resolve,25));result=await restarted.reconcile(task.id);}
  assert.equal(result.state,'cancelled');assert.equal(result.stopEvidence.processGroupGone,true);assert.equal(result.workerExitReceipt.workflowPid,native.group);assert.equal(result.technical.status,'NOT_RUN');assert.deepEqual(result.request.budget,task.request.budget);assert.equal(result.request.budget.deadline,budget.deadline);assert.equal(ledger.status(baseline.id).revisions,1);assert.equal(result.startedAt,before.startedAt);assert.deepEqual(readFileSync(project),original);
  assert.throws(()=>process.kill(native.pid,0),(error:any)=>error.code==='ESRCH');await assert.rejects(()=>restarted.run(task.id),/reconcile_required/);const parent=await restarted.reconcile(baseline.id);assert.equal(parent.state,'cancelled');
  if(process.env.PHOTOCRAFT_STOP_REPORT){const runtime=JSON.parse(readFileSync(join(options.skillRoot,'scripts/runtime.lock.json'),'utf8'));writeFileSync(process.env.PHOTOCRAFT_STOP_REPORT,JSON.stringify({schema:'photocraft-native-stop-evidence/v1',platform:process.platform+'-'+process.arch,node:process.version,runtimeVersion:runtime.resolvedVersion,runtimeSha256:runtime.artifacts['darwin-arm64'].binarySha256,sourceSha256:before.executionIdentity.sha256,taskId:task.id,taskIdentity:task.identity,parentTask:baseline.id,planSha256:digest(canonical(task.request.plan)),sourceProjectSha256:digest(original),retainedProjectSha256:fileDigest(project),observedNative:native,workerExitReceipt:result.workerExitReceipt,childState:result.state,parentState:parent.state,technical:result.technical.status,creative:result.creative.status,replayAllowed:result.replayAllowed,scope:'real native child process cancellation and runner interruption; synthetic review only establishes parent-child contract; fixed installed release not verified'},null,2)+'\n');}
 }finally{if(ledger){for(const row of ledger.db.prepare('SELECT id FROM tasks').all() as any[])try{ledger.stop(row.id);}catch{}}outer?.kill();await new Promise(resolve=>setTimeout(resolve,250));ledger?.close();rmSync(root,{recursive:true,force:true});}
});

test('supervisor refuses a new workflow when cancellation or deadline predates its startup',async()=>{
 const {fileDigest,canonical}=await import('../src/protocol/files.ts');
 for(const reason of ['stop','deadline']){
  const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-prelaunch-')));
  try{
   const launchPath=join(root,'launch.json');const output=join(root,'side-effect');const receipt=join(root,'exit.json');const stopFile=join(root,'stop');if(reason==='stop')writeFileSync(stopFile,'stop');
   writeFileSync(launchPath,canonical({taskId:'fixture',taskIdentity:'fixture',epoch:1,workerToken:'fixture',sourceSha256:'fixture',python:process.execPath,args:['-e',`require('node:fs').writeFileSync(${JSON.stringify(output)},'unexpected')`],stopFile,deadline:Date.now()+(reason==='deadline'?-1:30000),receipt}));
   const child=spawn(process.execPath,[resolve('src/harness/worker_supervisor.ts'),launchPath,fileDigest(launchPath)],{stdio:'ignore'});await new Promise(resolve=>child.once('close',resolve));
   assert.equal(existsSync(output),false);const result=JSON.parse(readFileSync(receipt,'utf8'));assert.equal(result.workflowPid,null);assert.equal(result.processGroupGone,true);assert.ok(result.stoppedAt);assert.equal(existsSync(stopFile),true);
  }finally{rmSync(root,{recursive:true,force:true});}
 }
});
