import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,realpathSync,writeFileSync,mkdirSync,readdirSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {strictJson} from '../src/protocol/strict_json.ts';
import {canonical,readJson} from '../src/protocol/files.ts';
import {pythonReply} from '../src/harness/preflight.ts';

const invalid:[string,string][]=[['{"x":"\\ud800"}','$.x'],['{"x":["\\udc00"]}','$.x[0]'],['{"bad\\ud800":1}','$["bad\\ud800"]'],['{"bad expected name":"\\ud800"}','$["bad expected name"]'],['{"x":"a\\ud800b"}','$.x']];
function refusal(error:any,path:string){assert.equal(error.code,'invalid_json_unicode');assert.equal(error.fieldPath,path);assert.equal(error.phase,'validation');assert.equal(error.outcome,'not_executed');assert.equal(error.retryable,false);return true;}

test('strict Harness JSON refuses lone surrogate values and keys with full field paths',()=>{
 for(const [raw,path] of invalid)assert.throws(()=>strictJson(raw),(error:any)=>refusal(error,path));
 assert.deepEqual(strictJson('{"中文":"\\ud83d\\ude00"}'),{'中文':'😀'});
});

test('five public Harness JSON actions refuse invalid Unicode before ledger or runtime creation',()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-unicode-entry-')));
 try {
  const file=join(root,'input.json');
  for(const [action,flag] of [['create','--request'],['revise','--proposal'],['recover','--proposal'],['review-import','--receipt'],['import-judge','--receipt']])for(const [raw,path] of invalid){
   writeFileSync(file,raw);const result=spawnSync(process.execPath,['src/cli.ts',action,'--state-dir',join(root,'state'),'--task','not-used',flag,file,'--skill-root',join(root,'absent-skill'),'--runtime-home',join(root,'runtime')],{encoding:'utf8',timeout:30000});
   assert.equal(result.status,1,result.stdout+result.stderr);refusal(JSON.parse(result.stdout),path);assert.deepEqual(readdirSync(root),['input.json']);
  }
 } finally {rmSync(root,{recursive:true,force:true});}
});

test('canonical in-memory values cannot bypass strict Unicode input semantics',()=>{
 for(const [raw,path] of invalid)assert.throws(()=>canonical(JSON.parse(raw)),(error:any)=>refusal(error,path));
 assert.equal(canonical({'中文':['😀','a']}),'\u007b"中文":["😀","a"]}');
});

test('malformed Unicode subprocess result stays unknown rather than validated',()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-unicode-reply-')));
 try {
  mkdirSync(join(root,'scripts'));writeFileSync(join(root,'scripts/probe.py'),'print(\'{"result":"PASS","probe":"\\\\ud800"}\')\n');
  assert.throws(()=>pythonReply({skillRoot:root,python:process.env.PHOTOCRAFT_PYTHON??'/opt/anaconda3/bin/python3'},'probe.py',[]),(error:any)=>{assert.equal(error.code,'adapter_reply_invalid');assert.equal(error.phase,'reply_received');assert.equal(error.outcome,'unknown');assert.equal(error.recoveryAction,'reconcile');return true;});
 } finally {rmSync(root,{recursive:true,force:true});}
});

test('public Harness JSON files reject invalid UTF-8 bytes instead of replacement decoding',()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-utf8-input-')));
 try {
  const file=join(root,'input.json');writeFileSync(file,Buffer.concat([Buffer.from('{"x":"'),Buffer.from([255]),Buffer.from('"}') ]));
  for(const [action,flag] of [['create','--request'],['revise','--proposal'],['recover','--proposal'],['review-import','--receipt'],['import-judge','--receipt']]){
   const result=spawnSync(process.execPath,['src/cli.ts',action,'--state-dir',join(root,'state'),'--task','not-used',flag,file],{encoding:'utf8',timeout:30000});const reply=JSON.parse(result.stdout);assert.equal(reply.code,'invalid_json_encoding');assert.equal(reply.fieldPath,'$');assert.equal(reply.outcome,'not_executed');assert.deepEqual(readdirSync(root),['input.json']);
  }
  const legal={x:'中文😀�'};writeFileSync(file,JSON.stringify(legal));assert.deepEqual(readJson(file),legal);writeFileSync(file,Buffer.concat([Buffer.from([239,187,191]),Buffer.from('{}')]));assert.throws(()=>readJson(file),/invalid_json_value/);
 } finally {rmSync(root,{recursive:true,force:true});}
});

test('invalid UTF-8 adapter output is unknown even when replacement text would be valid JSON',()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-utf8-adapter-')));
 try {
  mkdirSync(join(root,'scripts'));writeFileSync(join(root,'scripts/probe.py'),'import sys\nsys.stdout.buffer.write(b\'{"probe":"\\xff"}\')\n');
  assert.throws(()=>pythonReply({skillRoot:root,python:process.env.PHOTOCRAFT_PYTHON??'/opt/anaconda3/bin/python3'},'probe.py',[]),(error:any)=>{assert.equal(error.code,'adapter_reply_invalid');assert.equal(error.outcome,'unknown');return true;});
 } finally {rmSync(root,{recursive:true,force:true});}
});

import {Ledger} from '../src/harness/ledger.ts';
import {Runner} from '../src/harness/runner.ts';
import {digest} from '../src/protocol/files.ts';
import {runtimePlatformKey} from '../src/harness/preflight.ts';
import {existsSync} from 'node:fs';

test('worker preserves raw output digest and refuses invalid UTF-8 before verification or replay',async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-utf8-worker-')));const ledger=new Ledger(join(root,'state'));
 try {
  const skill=join(root,'skill'),output=join(root,'delivery');mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(join(skill,'references'));
  writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{[runtimePlatformKey()]:{binarySha256:'a'.repeat(64)}}}));
  const reply=JSON.stringify({schema:'photocraft-delivery/v1',files:{'project.pcraft':'b'.repeat(64),'design.png':'c'.repeat(64)},runtimeSha256:'a'.repeat(64),outputs:[],probe:'BAD'});const [before,after]=reply.split('BAD');const bytes=Buffer.concat([Buffer.from(before),Buffer.from([255]),Buffer.from(after)]);
  writeFileSync(join(skill,'scripts/workflow.py'),'import sys,base64\nfrom pathlib import Path\nif "--check" in sys.argv: print(\'{"result":"PASS"}\')\nelse:\n output=Path(sys.argv[sys.argv.index("--output")+1]);output.mkdir();(output/"executed").write_text("one operation")\n payload=base64.b64decode("'+bytes.toString('base64')+'");(output/"manifest.json").write_bytes(payload);sys.stdout.buffer.write(payload)\n');
  const task=ledger.create({idempotencyKey:'utf8',brief:'preserve unknown output',plan:{document:{width:16,height:16},operations:[]},output,authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+30000,maxRevisions:0,reserveBytes:0}});
  const runner=new Runner(ledger,{skillRoot:skill,python:process.env.PHOTOCRAFT_PYTHON??'/opt/anaconda3/bin/python3'});let verified=false;runner.verify=async()=>{verified=true;return ledger.status(task.id);};
  const result=await runner.run(task.id);assert.equal(result.executionResult.outputSha256,digest(bytes));assert.equal(result.state,'reconciling');assert.equal(result.executionResult.replyFailureCode,'invalid_json_encoding');assert.equal(result.executionResult.outcome,'unknown');assert.equal(result.executionResult.phase,'reply_received');assert.equal(result.replayAllowed,false);assert.equal(verified,false);assert.ok(existsSync(join(output,'executed')));await assert.rejects(()=>runner.run(task.id),/reconcile_required/);
 } finally {ledger.close();rmSync(root,{recursive:true,force:true});}
});

import {chmodSync,readFileSync} from 'node:fs';
test('actual native saved delivery survives invalid UTF-8 outer worker reply without replay',{skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-native-utf8-')));const ledger=new Ledger(join(root,'state'));
 try {
  const realPython=process.env.PHOTOCRAFT_PYTHON??'/opt/anaconda3/bin/python3',skill=process.env.PHOTOCRAFT_SKILL_ROOT!,shim=join(root,'python-shim'),capture=join(root,'raw-reply.bin');
  writeFileSync(shim,'#!'+realPython+'\nimport os,sys,subprocess\nfrom pathlib import Path\nargs=sys.argv[1:]\nif len(args)>2 and args[2].endswith("workflow.py") and "--check" not in args:\n result=subprocess.run(['+JSON.stringify(realPython)+',*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)\n payload=b\'{"probe":"\\xff",\'+result.stdout.lstrip()[1:];Path('+JSON.stringify(capture)+').write_bytes(payload);sys.stdout.buffer.write(payload);sys.stderr.buffer.write(result.stderr);raise SystemExit(result.returncode)\nelse:os.execv('+JSON.stringify(realPython)+',['+JSON.stringify(realPython)+',*args])\n');chmodSync(shim,0o700);
  const task=ledger.create({idempotencyKey:'native-utf8',brief:'保全已保存的原生工程',plan:{document:{width:16,height:16},operations:[{command:'layer.new.layer',params:{name:'Retained'}}]},output:join(root,'delivery'),authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+60000,maxRevisions:0,reserveBytes:0}});
  const runner=new Runner(ledger,{skillRoot:skill,python:shim});const result=await runner.run(task.id);assert.equal(result.state,'reconciling');assert.equal(result.technical.status,'NOT_RUN');assert.equal(result.executionResult.replyFailureCode,'invalid_json_encoding');assert.equal(result.executionResult.outcome,'unknown');assert.equal(result.executionResult.outputSha256,digest(readFileSync(capture)));assert.equal(result.replayAllowed,false);assert.equal(result.worker.processGroupGone,true);
  const project=join(task.request.output,'project.pcraft'),before=digest(readFileSync(project));const inspected=spawnSync(realPython,['-I','-B',join(skill,'scripts/cli.py'),'--','info',project],{encoding:'utf8',timeout:30000});assert.equal(inspected.status,0,inspected.stdout+inspected.stderr);assert.ok(JSON.parse(inspected.stdout).layers.some((layer:any)=>layer.name==='Retained'));assert.equal(digest(readFileSync(project)),before);await assert.rejects(()=>runner.run(task.id),/reconcile_required/);
  if(process.env.PHOTOCRAFT_UTF8_NATIVE_REPORT)writeFileSync(process.env.PHOTOCRAFT_UTF8_NATIVE_REPORT,JSON.stringify({status:'PASS',nativeSavedReopened:true,projectSha256:before,rawOutputSha256:result.executionResult.outputSha256,outcome:'unknown',technical:'NOT_RUN',workerStopped:true,replayAllowed:false,guiLaunches:0},null,2)+'\n');
 } finally {ledger.close();rmSync(root,{recursive:true,force:true});}
});
