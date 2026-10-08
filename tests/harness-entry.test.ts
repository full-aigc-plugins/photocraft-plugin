import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, realpathSync, rmSync, writeFileSync, existsSync, readdirSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { Ledger } from '../src/harness/ledger.ts';
import { Runner } from '../src/harness/runner.ts';
import { Review } from '../src/evaluation/review.ts';
import { strictJson } from '../src/protocol/strict_json.ts';
import { fileDigest } from '../src/protocol/files.ts';
const skillRoot=resolve('skills/photocraft-use');
const python=process.env.PHOTOCRAFT_PYTHON??'python3';
function fixture(){
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-entry-')));
 const request={idempotencyKey:'title',brief:'An editable title',plan:{document:{width:32,height:32},operations:[] as any[]},output:join(root,'delivery'),authorization:{ref:'fixture',writeRoot:root},budget:{deadline:Date.now()+60000,maxRevisions:2,reserveBytes:1024}};
 return {root,request,close:()=>rmSync(root,{recursive:true,force:true})};
}
function cli(f:any,action:string,extra:string[]=[]){return spawnSync(process.execPath,['src/cli.ts',action,'--state-dir',join(f.root,'state'),'--skill-root',skillRoot,'--python',python,'--runtime-home',join(f.root,'runtime'),...extra],{encoding:'utf8',timeout:30000});}
function snapshot(ledger:Ledger){return JSON.stringify({tasks:ledger.db.prepare('SELECT * FROM tasks ORDER BY id').all(),events:ledger.db.prepare('SELECT * FROM events ORDER BY sequence').all(),files:readdirSync(ledger.root).sort()});}
function refusal(reply:any,path:string){assert.equal(reply.phase,'validation');assert.equal(reply.category,'validation_failed');assert.equal(reply.outcome,'not_executed');assert.equal(reply.retryable,false);assert.equal(reply.recoveryAction,'correct_plan');assert.equal(reply.fieldPath,path);}
test('public create rejects semantic errors before initializing ledger, runtime or delivery',()=>{
 const cases:[any,string][]=[
  [{command:'layer.select',params:{layer:true}},'$.plan.operations[0].params.layer'],
  [{command:'layer.new.layer',params:{typo:1}},'$.plan.operations[0].params.typo'],
  [{command:[],params:{}},'$.plan.operations[0].command'],
  [{command:'layer.select',params:{layer:{$ref:'future.layer'}}},'$.plan.operations[0].params.layer'],
  [{command:'asset.place',params:{asset:'missing'}},'$.plan.operations[0].params.asset'],
 ];
 for(const [operation,path] of cases){const f=fixture();try{
  const file=join(f.root,'request.json');writeFileSync(file,JSON.stringify({...f.request,plan:{...f.request.plan,operations:[operation]}}));const result=cli(f,'create',['--request',file]);
  assert.equal(result.status,1,result.stdout+result.stderr);refusal(JSON.parse(result.stdout),path);assert.deepEqual(readdirSync(f.root),['request.json']);
 }finally{f.close();}}
});
test('nested duplicate keys and numeric overflow expose request field paths without side effects',()=>{
 for(const value of ['{"layer":1,"layer":2}','{"layer":1e999}','{"layer":NaN}']){const f=fixture();try{
  const file=join(f.root,'request.json');const request={...f.request,plan:{...f.request.plan,operations:[{command:'layer.select',params:'REPLACE'}]}};
  writeFileSync(file,JSON.stringify(request).replace('"REPLACE"',value));const result=cli(f,'create',['--request',file]);assert.equal(result.status,1,result.stdout);refusal(JSON.parse(result.stdout),'$.plan.operations[0].params.layer');assert.deepEqual(readdirSync(f.root),['request.json']);
 }finally{f.close();}}
});
test('public run propagates structured validation and preserves all ledger records and files',()=>{
 const f=fixture();try{const ledger=new Ledger(join(f.root,'state'));const task=ledger.create({...f.request,plan:{...f.request.plan,operations:[{command:'layer.select',params:{layer:true}}]}});const before=snapshot(ledger);
 const result=cli(f,'run',['--task',task.id]);assert.equal(result.status,1,result.stdout);refusal(JSON.parse(result.stdout),'$.plan.operations[0].params.layer');assert.equal(snapshot(ledger),before);assert.equal(existsSync(f.request.output),false);assert.equal(existsSync(join(f.root,'runtime')),false);ledger.close();
 }finally{f.close();}
});
test('public create idempotency returns the same task after output exists and refuses conflicting input',()=>{
 const f=fixture();try{const file=join(f.root,'request.json');writeFileSync(file,JSON.stringify(f.request));const first=cli(f,'create',['--request',file]);assert.equal(first.status,0,first.stdout+first.stderr);const task=JSON.parse(first.stdout);mkdirSync(f.request.output);writeFileSync(join(f.request.output,'retained'),'unchanged');
 const ledger=new Ledger(join(f.root,'state'));const before=snapshot(ledger);const second=cli(f,'create',['--request',file]);assert.equal(second.status,0,second.stdout);assert.equal(JSON.parse(second.stdout).id,task.id);assert.equal(snapshot(ledger),before);
 writeFileSync(file,JSON.stringify({...f.request,brief:'conflicting'}));const conflict=cli(f,'create',['--request',file]);assert.equal(conflict.status,1);assert.equal(JSON.parse(conflict.stdout).code,'idempotency_conflict');assert.equal(snapshot(ledger),before);assert.equal(existsSync(join(f.root,'runtime')),false);ledger.close();
 }finally{f.close();}
});
test('invalid revision is rejected before reserving budgets, inserting a child or writing persistent plans',async()=>{
 const f=fixture();try{const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const epoch=ledger.claim(task.id);ledger.transition(task.id,epoch,'verifying');ledger.recordTechnical(task.id,epoch,{status:'PASS',projectSha256:'a'.repeat(64),previewSha256:'b'.repeat(64),manifestSha256:'c'.repeat(64)});
 const review=new Review(ledger);const request=review.request(task.id);review.import(task.id,{requestId:request.id,projectSha256:request.projectSha256,previewSha256:request.previewSha256,manifestSha256:request.manifestSha256,referencesSha256:request.referencesSha256,briefSha256:request.briefSha256,rubricVersion:request.rubricVersion,evaluator:{kind:'human',identity:'fixture',version:'v1',contextIsolation:'fixture'},verdict:'FAIL',gaps:[{id:'title',layer:2,property:'text',reason:'Change title'}]});
 const runner=new Runner(ledger,{skillRoot,python,runtimeHome:join(f.root,'runtime')});const before=snapshot(ledger);await assert.rejects(()=>runner.revise(task.id,{baseProjectSha256:request.projectSha256,baseManifestSha256:request.manifestSha256,authorizationRef:'fixture',operations:[{command:'type.edit',params:{layer:2,text:123}}]}),(error:any)=>{refusal(error,'$.plan.operations[0].params.text');return true;});assert.equal(snapshot(ledger),before);assert.equal(existsSync(join(f.root,'runtime')),false);assert.equal(existsSync(f.request.output),false);ledger.close();
 }finally{f.close();}
});
test('strict JSON parser reports nested and escaped property locations',()=>{
 for(const [text,path] of [['{"a":[{"b":1,"b":2}]}','$.a[0].b'],['{"odd.key":{"x":1e999}}','$["odd.key"].x'],['{"a":[NaN]}','$.a[0]']])assert.throws(()=>strictJson(text),(error:any)=>{refusal(error,path);return true;});
});

test('ambiguous or malformed preflight replies cannot dispatch a worker or mutate the ledger',async()=>{
 for(const reply of ['null','{"result":"FAIL"}','{"result":"PASS","error":"contradictory"}','{"result":"PASS","result":"PASS"}','{"result":"PASS","x":1e999}']){
  const f=fixture();try{
   const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));writeFileSync(join(skill,'scripts/runtime.lock.json'),'{}');
   const marker=join(f.root,'executed');writeFileSync(join(skill,'scripts/workflow.py'),'import sys\nfrom pathlib import Path\nif "--check" in sys.argv: print('+JSON.stringify(reply)+')\nelse: Path('+JSON.stringify(marker)+').write_text("editing dispatched");print("{}")\n');
   const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const before=snapshot(ledger);const runner=new Runner(ledger,{skillRoot:skill,python});
   await assert.rejects(()=>runner.run(task.id),(error:any)=>{assert.equal(error.phase,'validation');assert.equal(error.outcome,'not_executed');assert.equal(error.fieldPath,'$.plan');assert.equal(error.recoveryAction,'inspect');return true;});assert.equal(snapshot(ledger),before);assert.equal(existsSync(marker),false);assert.equal(existsSync(f.request.output),false);ledger.close();
  }finally{f.close();}
 }
});
test('malformed subprocess JSON is unknown rather than an unexecuted validation failure',()=>{
 for(const reply of ['{"x":1,"x":2}','{"x":1e999}','']){
  const f=fixture();try{const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});writeFileSync(join(skill,'scripts/probe.py'),'print('+JSON.stringify(reply)+')');const ledger=new Ledger(join(f.root,'state'));const runner=new Runner(ledger,{skillRoot:skill,python});assert.throws(()=>runner.python('probe.py',[]),(error:any)=>{assert.equal(error.code,'adapter_reply_invalid');assert.equal(error.outcome,'unknown');assert.equal(error.phase,'reply_received');assert.equal(error.recoveryAction,'reconcile');return true;});ledger.close();}finally{f.close();}
 }
});

test('task metadata containers and unknown fields are located before writable ledger initialization',()=>{
 for(const [change,path] of [[{budget:{deadline:1,maxRevisions:0,reserveBytes:'bad'}},'$.budget.reserveBytes'],[{authorization:[]},'$.authorization'],[{references:{}},'$.references'],[{unexpected:true},'$.unexpected'],[{mutableProject:'/not-used.pcraft',expectedProjectSha256:['a'.repeat(64)]},'$.expectedProjectSha256'] ] as [any,string][]){const f=fixture();try{
  const file=join(f.root,'request.json');writeFileSync(file,JSON.stringify({...f.request,...change}));const result=cli(f,'create',['--request',file]);assert.equal(result.status,1);refusal(JSON.parse(result.stdout),path);assert.deepEqual(readdirSync(f.root),['request.json']);
 }finally{f.close();}}
});

test('malformed execution replies remain unknown and never trigger automatic verification or replay',async()=>{
 for(const reply of ['null','{"schema":"photocraft-delivery/v1","files":{}}','{"x":1,"x":2}','{"x":1e999}']){
  const f=fixture();try{
   const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));writeFileSync(join(skill,'scripts/runtime.lock.json'),'{}');
   const marker=join(f.root,'executed');writeFileSync(join(skill,'scripts/workflow.py'),'import sys\nfrom pathlib import Path\nif "--check" in sys.argv: print("{\\"result\\":\\"PASS\\"}")\nelse:\n Path('+JSON.stringify(marker)+').write_text("one execution")\n output=Path(sys.argv[sys.argv.index("--output")+1]);output.mkdir();(output/"manifest.json").write_text("{}")\n print('+JSON.stringify(reply)+')\n');
   const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const runner=new Runner(ledger,{skillRoot:skill,python});let verifications=0;runner.verify=async()=>{verifications++;return {state:'verifying',technical:{status:'PASS'}};};
   const result=await runner.run(task.id);assert.equal(verifications,0);assert.equal(result.state,'reconciling');assert.equal(result.executionResult.outcome,'unknown');assert.equal(result.executionResult.phase,'reply_received');assert.equal(result.executionResult.code,'outcome_unknown');assert.equal(result.replayAllowed,false);assert.equal(result.technical.status,'NOT_RUN');assert.equal(existsSync(marker),true);await assert.rejects(()=>runner.run(task.id),/reconcile_required/);ledger.close();
  }finally{f.close();}
 }
});
test('verification refuses ambiguous integrity replies before native reopening',async()=>{
 const f=fixture();try{
  const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));writeFileSync(join(skill,'scripts/runtime.lock.json'),'{}');
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const runner=new Runner(ledger,{skillRoot:skill,python});const epoch=ledger.claim(task.id);ledger.update(task.id,epoch,current=>{current.executionIdentity=runner.identity();});mkdirSync(f.request.output);writeFileSync(join(f.request.output,'manifest.json'),'{"schema":"photocraft-delivery/v1","files":{}}');let calls:string[]=[];runner.python=(script)=>{calls.push(script);return {result:'PASS'};};
  await assert.rejects(()=>runner.verify(task.id),(error:any)=>{assert.equal(error.code,'unexpected_verification_result');assert.equal(error.outcome,'unknown');return true;});assert.deepEqual(calls,['delivery.py']);assert.equal(ledger.status(task.id).technical.status,'NOT_RUN');ledger.close();
 }finally{f.close();}
});

test('nonzero native completion preserves structured failure without automatic verification',async()=>{
 for(const [reply,expected] of [
  ['not JSON',{code:'outcome_unknown',phase:'reply_received',outcome:'unknown',recoveryAction:'reconcile'}],
  [JSON.stringify({error:'uncertain checkpoint',code:'outcome_unknown',phase:'submitted',outcome:'unknown',retryable:false,recoveryAction:'reconcile'}),{code:'outcome_unknown',phase:'submitted',outcome:'unknown',recoveryAction:'reconcile'}],
  [JSON.stringify({error:'native refused',code:'native_command_failed',phase:'submitted',outcome:'failed',retryable:false,recoveryAction:'inspect'}),{code:'native_command_failed',phase:'submitted',outcome:'failed',recoveryAction:'inspect'}],
 ] as [string,any][]){const f=fixture();try{
  const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));writeFileSync(join(skill,'scripts/runtime.lock.json'),'{}');
  writeFileSync(join(skill,'scripts/workflow.py'),'import sys\nfrom pathlib import Path\nif "--check" in sys.argv: print("{\\"result\\":\\"PASS\\"}")\nelse:\n output=Path(sys.argv[sys.argv.index("--output")+1]);output.mkdir();(output/"manifest.json").write_text("{}")\n print('+JSON.stringify(reply)+');sys.exit(1)\n');
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const runner=new Runner(ledger,{skillRoot:skill,python});let verifications=0;runner.verify=async()=>{verifications++;return {state:'verifying'};};const result=await runner.run(task.id);assert.equal(verifications,0);assert.equal(result.state,'reconciling');for(const [key,value] of Object.entries(expected))assert.equal(result.executionResult[key],value);assert.equal(result.technical.status,'NOT_RUN');assert.equal(result.replayAllowed,false);ledger.close();
 }finally{f.close();}}
});

test('valid Unicode replies survive UTF-8 characters split across pipe chunks',async()=>{
 const f=fixture();try{
  const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));
  const key=(process.platform==='win32'?'windows':process.platform)+'-'+(process.arch==='x64'?(process.platform==='win32'?'amd64':'x86_64'):process.arch);writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{[key]:{binarySha256:'a'.repeat(64)}}}));
  const manifest={schema:'photocraft-delivery/v1',runtimeSha256:'a'.repeat(64),files:{'project.pcraft':'b'.repeat(64),'design.png':'c'.repeat(64)},outputs:[],bindings:{'标题':'项目'}};
  writeFileSync(join(skill,'scripts/workflow.py'),'import sys,time\nfrom pathlib import Path\nif "--check" in sys.argv: print("{\\"result\\":\\"PASS\\"}")\nelse:\n text='+JSON.stringify(JSON.stringify(manifest))+'\n output=Path(sys.argv[sys.argv.index("--output")+1]);output.mkdir();(output/"manifest.json").write_text(text)\n data=text.encode();cut=data.find("标题".encode())+1\n sys.stdout.buffer.write(data[:cut]);sys.stdout.buffer.flush();time.sleep(.05);sys.stdout.buffer.write(data[cut:]);sys.stdout.buffer.flush()\n');
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const runner=new Runner(ledger,{skillRoot:skill,python});let calls=0;runner.verify=async(id)=>{calls++;return ledger.status(id);};const result=await runner.run(task.id);assert.equal(calls,1);assert.equal(result.executionResult.phase,'reply_validated');assert.equal(result.executionResult.outcome,'succeeded');ledger.close();
 }finally{f.close();}
});

test('public create refuses invalid runtime paths before establishing any task state',()=>{
 const f=fixture();try{
  const file=join(f.root,'request.json');writeFileSync(file,JSON.stringify(f.request));const result=spawnSync(process.execPath,['src/cli.ts','create','--state-dir',join(f.root,'state'),'--request',file,'--skill-root',skillRoot,'--python',python,'--runtime-home','relative/runtime'],{encoding:'utf8',timeout:30000});assert.equal(result.status,1,result.stdout);refusal(JSON.parse(result.stdout),'$.runtimeHome');assert.deepEqual(readdirSync(f.root),['request.json']);
 }finally{f.close();}
});
test('public create detects checker source drift before writable ledger initialization',()=>{
 const f=fixture();try{
  const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));writeFileSync(join(skill,'scripts/runtime.lock.json'),'{}');writeFileSync(join(skill,'scripts/workflow.py'),'from pathlib import Path\nPath(__file__).parent.parent.joinpath("references","changed.json").write_text("{}")\nprint(\'{"result":"PASS"}\')\n');
  const file=join(f.root,'request.json');writeFileSync(file,JSON.stringify(f.request));const result=spawnSync(process.execPath,['src/cli.ts','create','--state-dir',join(f.root,'state'),'--request',file,'--skill-root',skill,'--python',python],{encoding:'utf8',timeout:30000});assert.equal(result.status,1,result.stdout);const reply=JSON.parse(result.stdout);assert.equal(reply.code,'skill_source_changed');assert.equal(reply.phase,'validation');assert.equal(reply.outcome,'not_executed');assert.equal(reply.fieldPath,'$.skillRoot');assert.equal(existsSync(join(f.root,'state')),false);assert.equal(existsSync(f.request.output),false);
 }finally{f.close();}
});

test('execution reply is not marked validated before technical reply validation completes',async()=>{
 const f=fixture();try{
  const skill=join(f.root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));const key=(process.platform==='win32'?'windows':process.platform)+'-'+(process.arch==='x64'?(process.platform==='win32'?'amd64':'x86_64'):process.arch);writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{[key]:{binarySha256:'a'.repeat(64)}}}));
  const manifest={schema:'photocraft-delivery/v1',runtimeSha256:'a'.repeat(64),files:{'project.pcraft':'b'.repeat(64),'design.png':'c'.repeat(64)},outputs:[]};writeFileSync(join(skill,'scripts/workflow.py'),'import sys\nfrom pathlib import Path\nif "--check" in sys.argv: print("{\\"result\\":\\"PASS\\"}")\nelse:\n text='+JSON.stringify(JSON.stringify(manifest))+'\n output=Path(sys.argv[sys.argv.index("--output")+1]);output.mkdir();(output/"manifest.json").write_text(text);print(text)\n');
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const runner=new Runner(ledger,{skillRoot:skill,python});runner.verify=async()=>{throw new Error('verification fixture refuses unproven content');};const result=await runner.run(task.id);assert.equal(result.state,'reconciling');assert.equal(result.executionResult.phase,'submitted');assert.notEqual(result.executionResult.outcome,'succeeded');assert.equal(result.technical.status,'NOT_RUN');assert.equal(result.verificationError.outcome,'unknown');assert.equal(result.replayAllowed,false);ledger.close();
 }finally{f.close();}
});

test('closed-ledger idempotency and status do not leave WAL or shared-memory files beside the source',()=>{
 const f=fixture();try{
  const file=join(f.root,'request.json');writeFileSync(file,JSON.stringify(f.request));const first=cli(f,'create',['--request',file]);assert.equal(first.status,0,first.stdout);const task=JSON.parse(first.stdout);const state=join(f.root,'state');const files=()=>Object.fromEntries(readdirSync(state).sort().map(name=>[name,fileDigest(join(state,name))]));const before=files();assert.deepEqual(Object.keys(before),['tasks.sqlite']);
  const second=cli(f,'create',['--request',file]);assert.equal(second.status,0,second.stdout);assert.equal(JSON.parse(second.stdout).id,task.id);assert.deepEqual(files(),before);const status=cli(f,'status',['--task',task.id]);assert.equal(status.status,0,status.stdout);assert.deepEqual(files(),before);
 }finally{f.close();}
});
test('readonly ledger sees committed live WAL rows without touching original database or shared memory',()=>{
 const f=fixture();try{
  const writer=new Ledger(join(f.root,'state'));const task=writer.create(f.request);const files=()=>Object.fromEntries(readdirSync(writer.root).sort().map(name=>[name,fileDigest(join(writer.root,name))]));const before=files();assert.ok(Object.hasOwn(before,'tasks.sqlite-wal'));
  const reader=new Ledger(writer.root,{readOnly:true});assert.equal(reader.status(task.id).id,task.id);reader.close();assert.deepEqual(files(),before);writer.close();
 }finally{f.close();}
});

test('readonly snapshot refuses a commit racing its copy and preserves the writer commit',async()=>{
 const {default:fs}=await import('node:fs');const {syncBuiltinESMExports}=await import('node:module');const original=fs.copyFileSync;const f=fixture();let writer:Ledger|undefined;
 try{
  writer=new Ledger(join(f.root,'state'));writer.create(f.request);let raced=false;let committed:any;
  fs.copyFileSync=((source:any,target:any,mode:any)=>{original(source,target,mode);if(!raced && source===join(writer!.root,'tasks.sqlite')){raced=true;committed=writer!.create({...f.request,idempotencyKey:'concurrent',output:join(f.root,'second')});}}) as typeof fs.copyFileSync;syncBuiltinESMExports();
  assert.throws(()=>new Ledger(writer!.root,{readOnly:true}),(error:any)=>{assert.equal(error.code,'ledger_read_conflict');assert.equal(error.outcome,'not_executed');assert.equal(error.category,'state_conflict');assert.equal(error.recoveryAction,'inspect');return true;});assert.equal(raced,true);assert.equal(writer.status(committed.id).request.idempotencyKey,'concurrent');assert.equal(writer.db.prepare('SELECT count(*) AS count FROM tasks').get()!.count,2);
 }finally{fs.copyFileSync=original;syncBuiltinESMExports();writer?.close();f.close();}
});
