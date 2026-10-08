import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtempSync, realpathSync, existsSync, readFileSync, rmSync, writeFileSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
const installed=process.argv[2];const reportPath=process.argv[3];
const {Ledger}=await import(pathToFileURL(join(installed,'src/harness/ledger.ts')).href);
const {Runner}=await import(pathToFileURL(join(installed,'src/harness/runner.ts')).href);
const {fileDigest,canonical,digest}=await import(pathToFileURL(join(installed,'src/protocol/files.ts')).href);
const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-late-native-')));let outer:any;let paused=false;
const ledger=new Ledger(join(root,'state'));
function tree(directory:string,prefix=''):Record<string,string>{const files:Record<string,string>={};for(const entry of readdirSync(directory,{withFileTypes:true})){const path=join(directory,entry.name);if(entry.isDirectory())Object.assign(files,tree(path,prefix+entry.name+'/'));else files[prefix+entry.name]=createHash('sha256').update(readFileSync(path)).digest('hex');}return files;}
const installedBefore=tree(installed);
async function until(check:()=>boolean){const deadline=Date.now()+30000;while(!check()){if(Date.now()>deadline)throw new Error('condition_timeout');await new Promise(resolve=>setTimeout(resolve,10));}}
try{
 const options={skillRoot:join(installed,'skills/photocraft-use'),python:process.env.PHOTOCRAFT_PYTHON??'python3'};const runner=new Runner(ledger,options);
 const plan={document:{width:64,height:64,background:'#ffffff'},operations:[{command:'type.create',params:{text:'LATE',font:'Arial',size:12,x:8,y:20},as:'title'}],exports:[{format:'png'}]};
 const task=ledger.create({idempotencyKey:'late-native',brief:'controlled late transport response after native save',plan,output:join(root,'delivery'),authorization:{ref:'test-user',writeRoot:root},budget:{deadline:Date.now()+120000,maxRevisions:0,maxConcurrent:1,reserveBytes:1048576}});
 let reply='';outer=spawn(process.execPath,[join(installed,'src/cli.ts'),'run','--state-dir',ledger.root,'--task',task.id,'--python',options.python],{stdio:['ignore','pipe','ignore']});outer.stdout.on('data',(data:Buffer)=>{reply+=data.toString();});
 await until(()=>!!ledger.status(task.id).worker?.childPid);assert.equal(outer.exitCode,null);outer.kill('SIGSTOP');paused=true;
 await until(()=>existsSync(join(task.request.output,'manifest.json')) && existsSync(join(ledger.root,task.id+'-worker-exit.json')));
 const prior=ledger.status(task.id);assert.equal(prior.state,'running');assert.equal(prior.technical.status,'NOT_RUN');const before=tree(task.request.output);
 const stop=ledger.stop(task.id);assert.equal(stop.state,'cancel_requested');const closed=new Promise(resolve=>outer.once('close',resolve));outer.kill('SIGCONT');paused=false;await closed;
 const result=ledger.status(task.id);assert.equal(result.state,'cancelled');assert.equal(result.technical.status,'NOT_RUN');assert.equal(result.creative.status,'NOT_RUN');assert.equal(result.acceptance.status,'NOT_RUN');assert.equal(result.replayAllowed,false);assert.equal(result.stopEvidence.processGroupGone,true);
 const observation=result.lateArtifactObservations.at(-1);assert.equal(observation.taskId,task.id);assert.equal(observation.taskIdentity,task.identity);assert.equal(observation.files['manifest.json'],fileDigest(join(task.request.output,'manifest.json')));assert.equal(observation.files['project.pcraft'],fileDigest(join(task.request.output,'project.pcraft')));
 const native=runner.python('native_verify.py',[task.request.output]);assert.equal(native.result,'PASS');assert.deepEqual(tree(task.request.output),before);assert.deepEqual(tree(installed),installedBefore);
 writeFileSync(reportPath,JSON.stringify({schema:'photocraft-native-late-response/v1',status:'PASS',pluginVersion:JSON.parse(readFileSync(join(installed,'plugin.json'),'utf8')).version,taskId:task.id,taskIdentity:task.identity,planSha256:digest(canonical(plan)),sourceSha256:prior.executionIdentity.sha256,runtimeSha256:native.runtimeSha256,manifestSha256:fileDigest(join(task.request.output,'manifest.json')),projectSha256:fileDigest(join(task.request.output,'project.pcraft')),observationSha256:observation.sha256,observedFiles:Object.keys(observation.files).length,receipt:result.workerExitReceipt,states:{beforeStop:prior.state,stopAccepted:stop.state,afterLateResponse:result.state,technical:result.technical.status,creative:result.creative.status,acceptance:result.acceptance.status},nativeReopen:'PASS_READONLY_EXTERNAL_TO_TASK_ACCEPTANCE',replayAllowed:false,installedTreeUnchanged:true,outputTreeUnchanged:true,scope:'real native workflow runs while owned outer runner is suspended; stop accepted before delayed workflow response is consumed; late native output remains separately observed, never completed; no creative acceptance'},null,2)+'\n');
}finally{if(paused)outer?.kill('SIGCONT');try{for(const row of ledger.db.prepare('SELECT id FROM tasks').all())ledger.stop(row.id);}catch{}outer?.kill();ledger.close();rmSync(root,{recursive:true,force:true});}
