import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';

test('public lifecycle exposes explicit upgrade rollback and readonly status',()=>{
 const reply=spawnSync(process.execPath,['src/cli.ts','--help'],{encoding:'utf8'});assert.equal(reply.status,0);const actions=JSON.parse(reply.stdout).actions;
 for(const action of ['runtime-upgrade','runtime-rollback','runtime-status'])assert.ok(actions.includes(action),'missing explicit '+action);
});

import {mkdtempSync,realpathSync,mkdirSync,writeFileSync,readFileSync,rmSync,existsSync,cpSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {Ledger} from '../src/harness/ledger.ts';
import {RuntimeManager,probeRuntime} from '../src/harness/runtime_manager.ts';
import {skillIdentity,runtimePlatformKey} from '../src/harness/preflight.ts';
import {canonical,digest,fileDigest} from '../src/protocol/files.ts';

function fixture(){
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-runtime-transition-')));const state=join(root,'state'),ledger=new Ledger(state);
 const make=(name:string)=>{const path=join(root,name);mkdirSync(join(path,'scripts'),{recursive:true});mkdirSync(join(path,'references'));writeFileSync(join(path,'scripts/runtime.lock.json'),canonical({artifact:'photocraft-cli',resolvedVersion:name==='old'?'0.2.0':'0.2.0-craft.1',artifacts:{[runtimePlatformKey()]:{binarySha256:digest('binary')}}}));writeFileSync(join(path,'scripts/identity.py'),name);return path;};
 const old=make('old'),next=make('next'),options={skillRoot:old,python:'python3',runtimeHome:join(root,'runtime')};
 for(const version of ['0.2.0','0.2.0-craft.1']){const folder=join(options.runtimeHome,'photocraft',version);mkdirSync(folder,{recursive:true});writeFileSync(join(folder,'photocraft-cli'),'binary');}
 const identity=(skillRoot:string)=>skillIdentity({...options,skillRoot}).sha256;
 let calls=0;const probe=(options:any,backend:any)=>{calls++;const lock=JSON.parse(readFileSync(join(options.skillRoot,'scripts/runtime.lock.json'),'utf8')),snapshot={backend,commandsSha256:'b'.repeat(64),toolsSha256:'c'.repeat(64)};return {schema:'photocraft-runtime-probe/v1',backend,runtimeVersion:lock.resolvedVersion,runtimeSha256:Object.values(lock.artifacts)[0].binarySha256,snapshot,snapshotSha256:digest(canonical(snapshot)),editingCalls:0};};
 const manager=new RuntimeManager(ledger,options,probe);const proposal={authorizationRef:'user',expectedGeneration:0,expectedActiveSourceSha256:identity(old),candidateSkillRoot:next,candidateSourceSha256:identity(next),backend:'headless',stateSchema:1};
 const request={idempotencyKey:'task',brief:'fixed project',plan:{document:{width:32,height:32},operations:[]},output:join(root,'output'),authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+90000,maxRevisions:1,reserveBytes:0}};
 return {root,state,ledger,old,next,options,identity,manager,proposal,request,calls:()=>calls,close:function(){this.ledger.close();rmSync(root,{recursive:true,force:true});}};
}

test('upgrade rejects pending tasks and live or unknown owned workers before probing',()=>{
 for(const mode of ['planned','reconciling','unknown-worker']){const f=fixture();try{
  const task=f.ledger.create(f.request);if(mode!=='planned'){const epoch=f.ledger.claim(task.id);f.ledger.transition(task.id,epoch,mode==='reconciling'?'reconciling':'failed');if(mode==='unknown-worker')f.ledger.update(task.id,epoch,t=>{t.worker={supervisor:true,token:'unknown',exited:true,processGroupGone:true};});}
  const before=canonical(f.ledger.status(task.id));assert.throws(()=>f.manager.upgrade(f.proposal),mode==='unknown-worker'?/runtime_workers_not_drained/:/runtime_tasks_not_drained/);assert.equal(f.calls(),0);assert.equal(canonical(f.ledger.status(task.id)),before);assert.equal(f.manager.status().generation,0);
 }finally{f.close();}}
});

test('upgrade retains immutable combinations and restorable state backup; rollback rechecks and restores only compatible source',()=>{
 const f=fixture();try{
  const result=f.manager.upgrade(f.proposal);assert.equal(result.generation,1);assert.equal(result.active.sourceSha256,f.identity(f.next));assert.equal(result.previous[0].sourceSha256,f.identity(f.old));
  const backup=result.history[0].backup;assert.ok(existsSync(join(backup.path,'tasks.sqlite')));for(const [name,sha]of Object.entries(backup.files))assert.equal(fileDigest(join(backup.path,name)),sha);
  const state=new Ledger(backup.path,{readOnly:true});assert.equal(state.db.prepare('SELECT COUNT(*) AS n FROM tasks').get().n,0);state.close();
  f.ledger.close();const reopened=new Ledger(f.state);const manager=new RuntimeManager(reopened,f.options,(...args:any[])=>{assert.ok([result.previous[0].skillRoot,result.active.skillRoot].includes(args[0].skillRoot));return f.manager.probe(...args);});
  try{assert.equal(manager.status().generation,1);const back=manager.rollback({authorizationRef:'user',expectedGeneration:1,expectedActiveSourceSha256:result.active.sourceSha256,stateSchema:1});assert.equal(back.generation,2);assert.equal(back.active.sourceSha256,f.identity(f.old));assert.equal(back.previous.length,0);assert.ok(existsSync(result.active.skillRoot));}finally{reopened.close();}
  // fixture cleanup owns a closed ledger after explicit reopen.
  f.ledger=new Ledger(f.state);
 }finally{f.close();}
});

test('schema source generation and probe failures preserve the old selection and do not dispatch edits',()=>{
 const f=fixture();try{
  assert.throws(()=>f.manager.upgrade({...f.proposal,stateSchema:2}),/runtime_state_schema_incompatible/);assert.equal(f.calls(),0);
  assert.throws(()=>f.manager.upgrade({...f.proposal,expectedGeneration:2}),/runtime_generation_conflict/);assert.equal(f.calls(),0);
  assert.throws(()=>f.manager.upgrade({...f.proposal,candidateSourceSha256:'d'.repeat(64)}),/runtime_source_changed/);assert.equal(f.calls(),0);
  const selected=f.manager.upgrade(f.proposal);const before=canonical(f.manager.status()),ordinaryProbe=f.manager.probe;f.manager.probe=()=>{throw new Error('capability_missing');};
  assert.throws(()=>f.manager.rollback({authorizationRef:'user',expectedGeneration:1,expectedActiveSourceSha256:selected.active.sourceSha256,stateSchema:1}),/capability_missing/);assert.equal(canonical(f.manager.status()),before);
  f.manager.probe=(options,backend,root)=>{const reply=ordinaryProbe(options,backend,root);const lock=JSON.parse(readFileSync(join(options.skillRoot,'scripts/runtime.lock.json'),'utf8'));if(lock.resolvedVersion==='0.2.0')writeFileSync(join(options.runtimeHome!,'photocraft','0.2.0','photocraft-cli'),'tampered');return reply;};
  assert.throws(()=>f.manager.rollback({authorizationRef:'user',expectedGeneration:1,expectedActiveSourceSha256:selected.active.sourceSha256,stateSchema:1}),/runtime_binary_changed/);assert.equal(canonical(f.manager.status()),before);
 }finally{f.close();}
});

test('managed claim is fenced by active source and backend in the same transaction',()=>{
 const f=fixture();try{
  const selected=f.manager.upgrade(f.proposal),task=f.ledger.create(f.request);
  assert.throws(()=>f.ledger.claim(task.id,f.identity(f.old)),/runtime_selection_conflict/);assert.throws(()=>f.ledger.claim(task.id),/runtime_selection_conflict/);assert.equal(f.ledger.status(task.id).epoch,0);
  assert.equal(f.ledger.claim(task.id,selected.active.sourceSha256),1);
 }finally{f.close();}
});

test('readonly runtime status does not initialize selection or modify database files',()=>{
 const f=fixture();try{f.ledger.close();const path=join(f.state,'tasks.sqlite'),before=fileDigest(path);const reply=spawnSync(process.execPath,['src/cli.ts','runtime-status','--state-dir',f.state],{encoding:'utf8'});assert.equal(reply.status,0,reply.stdout+reply.stderr);assert.equal(JSON.parse(reply.stdout).generation,0);assert.equal(fileDigest(path),before);f.ledger=new Ledger(f.state);}finally{f.close();}
});

test('bridge selection never silently dispatches a headless task',()=>{
 const f=fixture();try{const selected=f.manager.upgrade({...f.proposal,backend:'bridge'}),task=f.ledger.create(f.request);assert.throws(()=>f.ledger.claim(task.id,selected.active.sourceSha256),/runtime_backend_conflict/);assert.equal(f.ledger.status(task.id).epoch,0);}finally{f.close();}
});

test('actual fixed CLI and owned desktop produce separate readonly lifecycle probes',{skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-runtime-probes-')));const receipts:any[]=[];
 try{for(const backend of ['headless','bridge'] as const){const output=join(root,backend);mkdirSync(output);const result=probeRuntime({skillRoot:process.env.PHOTOCRAFT_SKILL_ROOT??resolve('skills/photocraft-use'),python:process.env.PHOTOCRAFT_PYTHON??'/opt/anaconda3/bin/python3',runtimeHome:join(process.env.HOME!,'.local/share/craft-runtimes')},backend,output);assert.equal(result.editingCalls,0);assert.equal(result.snapshot.backend,backend);receipts.push(result);}
 if(process.env.PHOTOCRAFT_RUNTIME_PROBE_REPORT)writeFileSync(process.env.PHOTOCRAFT_RUNTIME_PROBE_REPORT,JSON.stringify({schema:'photocraft-runtime-probes-native/v1',status:'PASS',receipts,scope:'Actual unchanged craft.1 binary; readonly headless and owned desktop registry discovery. Different-version upgrade and rollback fixed acceptance remain open.'},null,2)+'\n');
 }finally{rmSync(root,{recursive:true,force:true});}
});

import {Runner} from '../src/harness/runner.ts';

test('native lifecycle drains saved tasks, fences old claims and reopens retained projects on upgrade and rollback',{skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-native-upgrade-'))),state=join(root,'state'),ledger=new Ledger(state);const skillRoot=process.env.PHOTOCRAFT_SKILL_ROOT??resolve('skills/photocraft-use'),python=process.env.PHOTOCRAFT_PYTHON??'/opt/anaconda3/bin/python3',options={skillRoot,python,runtimeHome:join(process.env.HOME!,'.local/share/craft-runtimes')};
 try{
  const next=join(root,'candidate');cpSync(skillRoot,next,{recursive:true,filter:path=>!path.split('/').includes('__pycache__')});writeFileSync(join(next,'references/lifecycle-identity.json'),canonical({purpose:'same-binary candidate source identity; not a new runtime version'}));
  const request={idempotencyKey:'baseline',brief:'Keep this editable title through runtime lifecycle',plan:{document:{width:32,height:32,background:'#ffffff'},operations:[{command:'type.create',params:{text:'KEEP',font:'Arial',size:12,x:1,y:16}}],exports:[{format:'png'}]},output:join(root,'baseline'),authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+180000,maxRevisions:0,reserveBytes:0}};
  const task=ledger.create(request),runner=new Runner(ledger,options),created=await runner.run(task.id);assert.equal(created.technical.status,'PASS');const project=join(request.output,'project.pcraft'),original=fileDigest(project);const source=skillIdentity(options).sha256,target=skillIdentity({...options,skillRoot:next}).sha256;
  const manager=new RuntimeManager(ledger,options),proposal={authorizationRef:'user',expectedGeneration:0,expectedActiveSourceSha256:source,candidateSkillRoot:next,candidateSourceSha256:target,backend:'headless',stateSchema:1};
  assert.throws(()=>manager.upgrade(proposal),/runtime_tasks_not_drained/);ledger.stop(task.id);assert.equal((await runner.reconcile(task.id)).state,'cancelled');
  const upgraded=manager.upgrade(proposal);assert.equal(upgraded.active.sourceSha256,target);assert.equal(upgraded.history[0].projects[project],original);assert.equal(fileDigest(project),original);
  const old=ledger.create({...request,idempotencyKey:'old-source',output:join(root,'old-source')});await assert.rejects(()=>runner.run(old.id),/runtime_selection_conflict/);assert.equal(ledger.status(old.id).epoch,0);ledger.stop(old.id);
  const activeRunner=new Runner(ledger,{...options,skillRoot:upgraded.active.skillRoot}),selected=ledger.create({...request,idempotencyKey:'selected',output:join(root,'selected')});assert.equal((await activeRunner.run(selected.id)).technical.status,'PASS');ledger.stop(selected.id);assert.equal((await activeRunner.reconcile(selected.id)).state,'cancelled');
  const interrupted=ledger.create({...request,idempotencyKey:'failed-export',output:join(root,'failed-export'),plan:{document:{width:32,height:32,background:'transparent'},operations:[{command:'layer.new.layer',params:{name:'SAVED'}}],exports:[{format:'jpg'}],flatExport:{colorSpace:'Rgb',transparency:'preserve'}}});const failed=await activeRunner.run(interrupted.id);assert.equal(failed.state,'reconciling');const failure=JSON.parse(readFileSync(join(interrupted.request.output,'failure.json'),'utf8')),failedProject=resolve(interrupted.request.output,failure.stage,'project.pcraft'),failedSha=fileDigest(failedProject);ledger.stop(interrupted.id);assert.equal((await activeRunner.reconcile(interrupted.id)).state,'cancelled');
  const back=manager.rollback({authorizationRef:'user',expectedGeneration:1,expectedActiveSourceSha256:target,stateSchema:1});assert.equal(back.active.sourceSha256,source);assert.equal(back.generation,2);assert.equal(back.history[1].projects[project],original);assert.equal(back.history[1].projects[failedProject],failedSha);assert.equal(fileDigest(failedProject),failedSha);assert.equal(fileDigest(project),original);assert.ok(existsSync(upgraded.active.skillRoot));
  if(process.env.PHOTOCRAFT_RUNTIME_TRANSITION_REPORT)writeFileSync(process.env.PHOTOCRAFT_RUNTIME_TRANSITION_REPORT,JSON.stringify({schema:'photocraft-runtime-transition-native/v1',status:'PASS',initialSourceSha256:source,candidateSourceSha256:target,finalSourceSha256:back.active.sourceSha256,initialProjectSha256:original,retainedProjectSha256:fileDigest(project),generations:[1,2],pendingTaskRefused:true,oldSourceClaimRefused:true,oldSourceEpoch:0,selectedSourceExecutionPassed:true,backupCount:back.history.length,projectsReopened:back.history.map((row:any)=>Object.keys(row.projects).length),probes:back.history.map((row:any)=>row.kind),runtimeVersion:back.active.runtimeVersion,sameBinaryOnly:true,failedSavedStageReopened:true,failedSavedProjectSha256:failedSha,editingDuringProbe:0,scope:'Actual native create/save, drain/cancel, source combination activation and rollback with readonly project checks; same craft.1 binary. Different-version and full PC-RT-002 fixed acceptance remain open.'},null,2)+'\n');
 }finally{ledger.close();rmSync(root,{recursive:true,force:true});}
});

import {spawn} from 'node:child_process';

test('independent process creation waits for the transition transaction and cannot claim the retired source',async()=>{
 const f=fixture();let child:ReturnType<typeof spawn>|undefined;
 try{
  const script=join(f.root,'transition.mjs');writeFileSync(script,`import {Ledger} from ${JSON.stringify(new URL('../src/harness/ledger.ts',import.meta.url).href)};import {RuntimeManager} from ${JSON.stringify(new URL('../src/harness/runtime_manager.ts',import.meta.url).href)};import {canonical,digest} from ${JSON.stringify(new URL('../src/protocol/files.ts',import.meta.url).href)};import {readFileSync} from 'node:fs';const ledger=new Ledger(process.argv[2]);const options=JSON.parse(process.argv[3]),proposal=JSON.parse(process.argv[4]);const manager=new RuntimeManager(ledger,options,(options,backend)=>{process.send('locked');Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,500);const lock=JSON.parse(readFileSync(options.skillRoot+'/scripts/runtime.lock.json','utf8')),snapshot={backend};return {schema:'photocraft-runtime-probe/v1',backend,runtimeVersion:lock.resolvedVersion,runtimeSha256:Object.values(lock.artifacts)[0].binarySha256,snapshot,snapshotSha256:digest(canonical(snapshot)),editingCalls:0};});try{manager.upgrade(proposal);}finally{ledger.close();process.disconnect();}`);
  child=spawn(process.execPath,[script,f.state,JSON.stringify(f.options),JSON.stringify(f.proposal)],{stdio:['ignore','pipe','pipe','ipc']});let diagnostic='';child.stderr?.on('data',data=>diagnostic+=data);const finished=new Promise<number|null>((resolve,reject)=>{child!.once('error',reject);child!.once('exit',resolve);});
  await new Promise<void>((resolve,reject)=>{child!.once('message',message=>message==='locked'?resolve():reject(new Error('unexpected child message')));child!.once('exit',code=>reject(new Error('transition exited before probe '+code+' '+diagnostic)));});
  const task=f.ledger.create(f.request);assert.equal(f.manager.status().generation,1);assert.throws(()=>f.ledger.claim(task.id,f.identity(f.old)),/runtime_selection_conflict/);assert.equal(f.ledger.status(task.id).epoch,0);assert.equal(await finished,0,diagnostic);
 }finally{if(child?.exitCode===null && !child.signalCode)child.kill('SIGKILL');f.close();}
});
