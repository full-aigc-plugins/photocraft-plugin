import test from 'node:test';
import assert from 'node:assert/strict';
import {spawn,spawnSync} from 'node:child_process';
import {mkdtempSync,realpathSync,writeFileSync,readFileSync,chmodSync,existsSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {Ledger} from '../src/harness/ledger.ts';
import {Runner} from '../src/harness/runner.ts';
import {digest,fileDigest,readJson} from '../src/protocol/files.ts';

async function waitFor(check:()=>boolean,label:string){const until=Date.now()+30000;while(!check()){if(Date.now()>until)throw new Error(label);await new Promise(resolve=>setTimeout(resolve,20));}}

test('native parent runner SIGKILL and ledger reopen preserve original intent across five interruption windows',{skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const cases:any[]=[];
 for(const mode of ['before_save','after_reply','after_confirmed','publishing','finished']) {
  const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-interrupted-restart-'))),state=join(root,'state');let ledger:Ledger|undefined;let cli:ReturnType<typeof spawn>|undefined;let workflowPid:number|undefined;
  try {
   const skillRoot=process.env.PHOTOCRAFT_SKILL_ROOT!,sourceRoot=process.env.PHOTOCRAFT_SOURCE_ROOT!,python=process.env.PHOTOCRAFT_PYTHON??'/opt/anaconda3/bin/python3',injection=join(sourceRoot,'tests/fixtures/workflow_interruption_pause.py'),marker=join(root,'paused'),shim=join(root,'python');
   writeFileSync(shim,'#!'+python+'\nimport os,sys,runpy\nargs=sys.argv[1:]\nif len(args)>2 and args[2].endswith("workflow.py") and "--check" not in args and "--checkpoint" not in args:\n sys.argv=['+JSON.stringify(injection)+','+JSON.stringify(mode)+','+JSON.stringify(marker)+',*args[2:]]\n runpy.run_path('+JSON.stringify(injection)+',run_name="__main__")\nelse: os.execv('+JSON.stringify(python)+',['+JSON.stringify(python)+',*args])\n');chmodSync(shim,0o700);
   const plan:any={document:{width:64,height:64,background:'#ffffff'},operations:[{command:'type.create',params:{text:'KEEP',font:'Arial',size:12,x:0.000001,y:20},as:'title'}],exports:[{format:'png'}]};
   const asset=join(root,'product.png');
   if(mode==='after_reply'){
    const image=spawnSync(python,['-I','-B','-c','from PIL import Image; import sys; Image.new("RGBA",(16,16),"red").save(sys.argv[1])',asset],{encoding:'utf8'});assert.equal(image.status,0,image.stderr);
    plan.assets={product:{path:asset,sha256:fileDigest(asset)}};plan.operations.unshift({command:'asset.placeSmart',params:{asset:'product',center:[32,32],fit:false,scale:100},as:'product'},{command:'layer.layerMask.revealAll',params:{layer:{$ref:'product.layer'}}});
   }
   ledger=new Ledger(state);const task=ledger.create({idempotencyKey:'original-'+mode,brief:'recover original process after restart',plan,output:join(root,'output'),authorization:{ref:'user',writeRoot:root},budget:{deadline:Date.now()+180000,maxRevisions:1,reserveBytes:0}});ledger.close();ledger=undefined;
   cli=spawn(process.execPath,['src/cli.ts','run','--state-dir',state,'--task',task.id,'--skill-root',skillRoot,'--python',shim],{cwd:join(import.meta.dirname,'..'),stdio:['ignore','pipe','pipe']});cli.stdout?.resume();cli.stderr?.resume();await waitFor(()=>existsSync(marker),'native interruption window missing '+mode);
   const progressPath=join(root,'.photocraft-progress-'+digest(task.request.output)+'.json'),originalProgress=readFileSync(progressPath),progress=readJson(progressPath);workflowPid=progress.ownerPid;
   // 杀死实际父 CLI，随后独立监督层继续持有原 workflow；新账本进程不按旧 PID 发信号。
   const parentExit=new Promise(resolve=>cli!.once('exit',resolve));cli.kill('SIGKILL');await parentExit;
   ledger=new Ledger(state);let runner=new Runner(ledger,{skillRoot,python:shim});const live=runner.status(task.id);assert.equal(live.progressObservation.status,'OBSERVED');assert.equal(live.progressObservation.workerStoppedConfirmed,false);assert.equal(live.epoch,1);const waiting=await runner.reconcile(task.id);assert.equal(waiting.checkpoint,undefined);assert.equal(waiting.recoveryAction,'confirm_owned_workers_stopped');assert.equal(waiting.revisions,0);
   process.kill(workflowPid!,'SIGKILL');await waitFor(()=>existsSync(join(state,task.id+'-worker-exit.json')),'original supervisor receipt missing');ledger.close();ledger=new Ledger(state);runner=new Runner(ledger,{skillRoot,python:shim});
   await waitFor(()=>runner.status(task.id).progressObservation?.workerStoppedConfirmed===true,'original process groups not confirmed stopped');
   const original=runner.status(task.id),stage=original.progressObservation.stage,project=join(stage,'project.pcraft'),sourceSha=existsSync(project)?fileDigest(project):undefined;
   const checked=await runner.reconcile(task.id);assert.equal(checked.epoch,1);assert.equal(checked.revisions,0);assert.equal(checked.replayAllowed,false);await assert.rejects(()=>runner.run(task.id),/reconcile_required/);
   let childSha:string|undefined;
   if(mode==='before_save') {assert.equal(checked.checkpoint,undefined);assert.match(checked.reconcileError,/interrupted_project_missing/);assert.equal(checked.state,'reconciling');assert.equal(checked.technical.status,'NOT_RUN');}
   else if(mode==='finished') {assert.equal(checked.technical.status,'PASS',checked.reconcileError);assert.equal(checked.checkpoint,undefined);assert.equal(checked.creative.status,'NOT_RUN');assert.equal(readJson(join(task.request.output,'native.json')).layers.filter((row:any)=>row.kind==='Type').length,1);}
   else {
    assert.equal(checked.checkpoint?.nativeReopened,true,checked.reconcileError);assert.equal(checked.technical.status,'NOT_RUN');const checkpointBytes=readFileSync(join(checked.checkpoint.output,'checkpoint.json'));
    // 原检查点建立后，新增文件和外部工程修改均拒绝；原样还原后可继续核对。
    const bytes=readFileSync(project);writeFileSync(project,'external edit');const refused=await runner.reconcile(task.id);assert.equal(refused.checkpoint,undefined);assert.equal(refused.technical.status,'NOT_RUN');assert.equal(refused.revisions,0);writeFileSync(project,bytes);
    if(mode==='after_reply'){
     const originalAsset=readFileSync(asset);writeFileSync(asset,'external input change');const inputRefused=await runner.reconcile(task.id);assert.equal(inputRefused.checkpoint,undefined);assert.match(inputRefused.reconcileError,/checkpoint_input_mismatch/);assert.equal(inputRefused.revisions,0);writeFileSync(asset,originalAsset);
     const extra=join(stage,'unregistered.bin');writeFileSync(extra,'external new file');const extraRefused=await runner.reconcile(task.id);assert.equal(extraRefused.checkpoint,undefined);rmSync(extra);assert.equal(extraRefused.revisions,0);
    }
    const restored=await runner.reconcile(task.id);assert.equal(restored.checkpoint.recordSha256,checked.checkpoint.recordSha256);const proposal={baseProjectSha256:sourceSha,checkpointRecordSha256:checked.checkpoint.recordSha256,authorizationRef:'user',reason:'explicit title recovery after parent restart',operations:[{command:'type.edit',params:{layer:progress.context.bindings.title.layer,text:'RECOVERED'}}]};
    const child=await runner.recover(task.id,proposal);assert.equal(child.request.parentTask,task.id);assert.equal(child.request.budget.deadline,task.request.budget.deadline);assert.equal(child.request.budget.maxRevisions,0);assert.equal((await runner.recover(task.id,proposal)).id,child.id);const result=await runner.run(child.id);assert.equal(result.technical.status,'PASS',JSON.stringify(result));assert.equal(result.creative.status,'NOT_RUN');childSha=result.technical.projectSha256;const native=readJson(join(child.request.output,'native.json'));assert.equal(native.layers.filter((row:any)=>row.kind==='Type').length,1);assert.equal(native.layers.find((row:any)=>row.kind==='Type').text.text,'RECOVERED');if(mode==='after_reply'){const smart=native.layers.find((row:any)=>row.id===progress.context.bindings.product.layer);assert.equal(smart.smartSourceKind,'embedded');assert.equal(smart.hasMask,true);assert.equal(native.layers.filter((row:any)=>row.kind.toLowerCase().includes('smart')).length,1);const pixel=spawnSync(python,['-I','-B','-c','from PIL import Image; import sys; assert Image.open(sys.argv[1]).convert("RGB").getpixel((32,32)) == (255,0,0)',join(child.request.output,'design.png')],{encoding:'utf8'});assert.equal(pixel.status,0,pixel.stderr);}assert.equal(fileDigest(project),sourceSha);assert.deepEqual(readFileSync(join(checked.checkpoint.output,'checkpoint.json')),checkpointBytes);assert.equal(ledger.status(task.id).revisions,1);assert.equal(ledger.status(task.id).technical.status,'NOT_RUN');
   }
   assert.deepEqual(readFileSync(progressPath),originalProgress);assert.equal(ledger.status(task.id).epoch,1);assert.equal(ledger.db.prepare("SELECT COUNT(*) AS n FROM events WHERE json_extract(data,'$.event')='intent_persisted'").get().n,mode==='before_save'||mode==='finished'?1:2);assert.equal(existsSync(join(task.request.output,'failure.json')),false);
   cases.push({window:mode,parentRunnerKilled:true,ledgerReopened:true,originalTaskId:task.id,sourceSha256:original.executionIdentity.sha256,planHashAlgorithm:progress.context.executionIdentity.planHashAlgorithm,originalEpoch:1,progressSha256:fileDigest(progressPath),sourceProjectSha256:sourceSha??null,childProjectSha256:childSha??null,originalFilesUnchanged:true,typeLayerCount:mode==='before_save'?null:1,replayCount:0,technical:checked.technical.status,creative:'NOT_RUN',checkpoint:!!checked.checkpoint,maskedSmartAssetPreserved:mode==='after_reply',changedInputRefused:mode==='after_reply'});
  } finally {
   if(cli?.exitCode===null && !cli?.signalCode)cli.kill('SIGKILL');
   if(workflowPid)try{process.kill(workflowPid,'SIGKILL');}catch{}
   // 测试拥有的原监督仍需写出退出回执；不删除活跃工作目录。
   if(ledger){ledger.close();ledger=undefined;}
   rmSync(root,{recursive:true,force:true});
  }
 }
 if(process.env.PHOTOCRAFT_INTERRUPTED_RESTART_REPORT)writeFileSync(process.env.PHOTOCRAFT_INTERRUPTED_RESTART_REPORT,JSON.stringify({schema:'photocraft-interrupted-restart-native/v1',status:'PASS',cases,scope:'Actual parent CLI and workflow SIGKILL; original supervisor proof, five windows, partial checkpoint forks and full delivery reconciliation; creative and complete V1 remain open.'},null,2)+'\n');
});
