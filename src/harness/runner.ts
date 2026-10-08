import { spawn, spawnSync } from 'node:child_process';
import { existsSync, writeFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { canonical, digest, fileDigest, readJson, safePath } from '../protocol/files.ts';
import { Ledger } from './ledger.ts';
import { mapArtifact } from '../protocol/artifact.ts';
import { Review } from '../evaluation/review.ts';

/** 所有编辑复用独立技能执行器；账本先登记意图，断连后只核对。 */
export class Runner {
 ledger: Ledger;
 options: { skillRoot: string; python: string; runtimeHome?: string };
 constructor(ledger: Ledger, options: { skillRoot: string; python: string; runtimeHome?: string }) { this.ledger=ledger; this.options=options; }

 identity() {
  const root=safePath(this.options.skillRoot);const files: Record<string,string>={};
  for (const folder of ['scripts','references']) for (const name of readdirSync(join(root,folder)).sort()) {
   if (name.endsWith('.py') || name.endsWith('.json')) files[folder+'/'+name]=fileDigest(join(root,folder,name));
  }
  return { sha256:digest(canonical(files)), runtimeLockSha256:files['scripts/runtime.lock.json'], files };
 }
 python(script: string,args: string[]) {
  const result=spawnSync(this.options.python,['-I','-B',join(safePath(this.options.skillRoot),'scripts',script),...args],{encoding:'utf8',timeout:120_000,maxBuffer:2*1024*1024,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
  if(result.error || result.status!==0) throw new Error('adapter_failed: '+(result.stdout || result.error?.message || result.stderr).slice(0,2048));
  return JSON.parse(result.stdout);
 }
 async run(id: string) {
  let task=this.ledger.status(id);
  if(task.state!=='planned' || task.attempted) throw new Error('reconcile_required');
  if(task.request.mutableProject) throw new Error('mutable_desktop_execution_not_supported');
  const identity=this.identity();const planPath=join(this.ledger.root,id+'-plan.json');
  writeFileSync(planPath,canonical(task.request.plan),{flag:'wx',mode:0o600});
  const args=[planPath,'--output',task.request.output];
  if(task.request.source) args.push('--source',task.request.source);
  // --check 必须在 claim、下载和原生进程之前完成。
  try { this.python('workflow.py',[...args,'--check']); }
  catch(error) { this.ledger.update(id,task.epoch,current=>{current.preflight={status:'FAIL',code:'preflight_failed',outcome:'not_executed'};}); throw error; }
  if(this.identity().sha256!==identity.sha256) throw new Error('skill_source_changed');
  const epoch=this.ledger.claim(id);
  this.ledger.update(id,epoch,current=>{current.executionIdentity=identity;current.preflight={status:'PASS'};});
  if(this.options.runtimeHome) args.push('--runtime-home',safePath(this.options.runtimeHome));
  const workerToken=randomUUID();
  const child=spawn(this.options.python,['-I','-B',join(this.options.skillRoot,'scripts/workflow.py'),...args],{detached:process.platform!=='win32',stdio:['ignore','pipe','pipe'],env:{...process.env,PYTHONDONTWRITEBYTECODE:'1',CRAFT_STOP_FILE:join(this.ledger.root,id+'.stop')}});
  this.ledger.update(id,epoch,current=>{current.worker={pid:process.pid,childPid:child.pid,token:workerToken,startedAt:Date.now()};});
  let bytes=0;let output='';let cancelled=false;let stopStarted=0;let spawnError='';
  child.stdout.on('data',data=>{bytes+=data.length;if(bytes<=2*1024*1024)output+=data.toString();});
  child.stderr.on('data',()=>{});
  child.on('error',error=>{spawnError=error.message;});
  const timer=setInterval(()=>{
   const latest=this.ledger.status(id);
   if(latest.state==='cancel_requested' || Date.now()>=latest.request.budget.deadline) {
    if(!cancelled) {
     cancelled=true;
     stopStarted=Date.now();
     if(latest.state!=='cancel_requested')this.ledger.stop(id);
     // 只向本进程持有的 ChildProcess 发信号；重启核对绝不按账本 PID 杀进程。
     try { if(process.platform!=='win32' && child.pid)process.kill(-child.pid,'SIGTERM');else child.kill('SIGTERM'); }catch{}
    }
    else if(Date.now()-stopStarted>=2000) {
     // 宽限期后仍只终止本次持有的进程组；重启后的核对没有此权限。
     try {if(process.platform!=='win32' && child.pid)process.kill(-child.pid,'SIGKILL');else child.kill('SIGKILL');}catch{}
    }
   }
  },100);
  const exit=await new Promise<number|null>(resolve=>child.once('close',resolve));clearInterval(timer);
  task=this.ledger.status(id);
  let processGroupGone=false;try{if(child.pid && process.platform!=='win32')process.kill(-child.pid,0);else processGroupGone=child.exitCode!==null || child.signalCode!==null;}catch(error){processGroupGone=(error as any).code==='ESRCH';}
  this.ledger.update(id,epoch,current=>{current.worker.exited=true;current.worker.processGroupGone=processGroupGone;current.executionResult={exitCode:exit,outputSha256:digest(output),outputTruncated:bytes>2*1024*1024,spawnError,phase:'submitted',outcome:exit===0?'reply_received':'unknown'};});
  if(cancelled) {
   let groupGone=false;try{if(child.pid && process.platform!=='win32')process.kill(-child.pid,0);else groupGone=child.exitCode!==null || child.signalCode!==null;}catch(error){groupGone=(error as any).code==='ESRCH';}
   this.ledger.update(id,epoch,current=>{current.stopEvidence={processGroupGone:groupGone,ownedWorkerToken:workerToken,exitCode:exit,signal:child.signalCode,at:Date.now(),lateArtifacts:existsSync(join(current.request.output,'manifest.json'))};});
   this.ledger.transition(id,epoch,'reconciling');
   if(groupGone)return this.ledger.transition(id,epoch,'cancelled');
   return this.ledger.status(id);
  }
  if(cancelled || exit!==0 || spawnError || bytes>2*1024*1024) {
   if(task.state!=='reconciling')this.ledger.transition(id,epoch,'reconciling');
   return this.reconcile(id);
  }
  try{return await this.verify(id);}catch(error){
   const current=this.ledger.status(id);if(current.state!=='reconciling')this.ledger.transition(id,epoch,'reconciling');
   return this.ledger.update(id,epoch,value=>{value.replayAllowed=false;value.reconcileError=String(error);value.recoveryAction='inspect_preserved_artifacts';});
  }
 }
 async reconcile(id: string) {
  let task=this.ledger.status(id);
  if(['completed','cancelled','failed','review_ready','planned'].includes(task.state))return task;
  if(task.state!=='reconciling')task=this.ledger.transition(id,task.epoch,'reconciling');
  // 活跃执行器仍有写入权；状态核对不能与它并行验收。
  if(task.stopRequestedAt) {
   const descendants=(this.ledger.db.prepare('SELECT data FROM tasks').all() as any[]).map(row=>JSON.parse(row.data)).filter(child=>child.request.parentTask===id);
   if(task.worker?.exited && task.worker.processGroupGone && descendants.every(child=>['cancelled','failed','completed'].includes(child.state))) {
    this.ledger.update(id,task.epoch,current=>{current.stopEvidence={processGroupGone:true,ownedWorkerToken:current.worker.token,at:Date.now(),lateArtifacts:existsSync(join(current.request.output,'manifest.json'))};});
    return this.ledger.transition(id,task.epoch,'cancelled');
   }
   return this.ledger.update(id,task.epoch,current=>{current.replayAllowed=false;current.recoveryAction='confirm_owned_workers_stopped';});
  }
  if(task.worker && !task.worker.exited) {
   let alive=false;try{process.kill(task.worker.pid,0);alive=true;}catch{}
   if(alive)return this.ledger.update(id,task.epoch,current=>{current.replayAllowed=false;current.recoveryAction='wait_for_owned_worker_or_inspect';});
  }
  if(existsSync(join(task.request.output,'manifest.json')) && task.executionIdentity) {
   try{return await this.verify(id);}catch(error){return this.ledger.update(id,task.epoch,current=>{current.replayAllowed=false;current.reconcileError=String(error);current.recoveryAction='inspect_preserved_artifacts';});}
  }
  if(existsSync(join(task.request.output,'failure.json')) && task.executionIdentity) {
   try {
    const args=[task.request.output,'--write-root',task.request.authorization.writeRoot];if(this.options.runtimeHome)args.push('--runtime-home',safePath(this.options.runtimeHome));
    const checkpoint=this.python('checkpoint_verify.py',args);
    if(checkpoint.result!=='PASS' || checkpoint.replayAllowed!==false)throw new Error('checkpoint_verification_failed');
    return this.ledger.update(id,task.epoch,current=>{current.checkpoint=checkpoint;current.replayAllowed=false;current.recoveryAction='inspect_checkpoint_before_explicit_revision';current.technical={status:'NOT_RUN'};});
   }catch(error){return this.ledger.update(id,task.epoch,current=>{current.replayAllowed=false;current.reconcileError=String(error);current.recoveryAction='inspect_preserved_artifacts';current.technical={status:'NOT_RUN'};});}
  }
  return this.ledger.update(id,task.epoch,current=>{current.replayAllowed=false;current.recoveryAction='inspect_preserved_artifacts';current.technical={status:'NOT_RUN'};});
 }
 async verify(id: string) {
  let task=this.ledger.status(id);
  if(!['running','reconciling','verifying'].includes(task.state))throw new Error('verification_not_ready');
  if(!task.executionIdentity || task.executionIdentity.sha256!==this.identity().sha256)throw new Error('skill_source_changed');
  const output=safePath(task.request.output);
  this.python('delivery.py',[output]);
  const nativeArgs=[output];if(this.options.runtimeHome)nativeArgs.push('--runtime-home',safePath(this.options.runtimeHome));
  const reopened=this.python('native_verify.py',nativeArgs);
  if(reopened.result!=='PASS')throw new Error('native_reopen_failed');
  const manifest=readJson(join(output,'manifest.json'));
  if(!manifest.files['design.png'])throw new Error('preview_required');
  const files: Record<string,string>={};
  for(const [name,sha]of Object.entries(manifest.files)) {const path=safePath(join(output,name));if(fileDigest(path)!==sha)throw new Error('candidate_changed');files[path]=sha as string;}
  files[join(output,'manifest.json')]=fileDigest(join(output,'manifest.json'));
  if(task.state!=='verifying')task=this.ledger.transition(id,task.epoch,'verifying');
  const evidence={status:'PASS',projectSha256:manifest.files['project.pcraft'],previewSha256:manifest.files['design.png'],manifestSha256:files[join(output,'manifest.json')],files,nativeReopen:reopened,sourceSha256:task.executionIdentity.sha256};
  const parent=task.request.parentTask?this.ledger.status(task.request.parentTask):undefined;
  if(parent && parent.technical.projectSha256===evidence.projectSha256)throw new Error('revision_no_improvement');
  const artifact=mapArtifact({...task,technical:evidence},parent?.artifact);
  return this.ledger.recordTechnical(id,task.epoch,evidence,artifact);
 }
 async revise(id: string,proposal: any) {
  const task=this.ledger.status(id);const contract=new Review(this.ledger).propose(id,proposal);
  const round=task.revisions+1;const output=join(task.request.authorization.writeRoot,id+'-revision-'+round);
  const allowedChanges: Record<string,string[]>={};
  for(const operation of contract.operations) {
   const key=String(operation.params.layer);const fields=Object.keys(operation.params).filter(k=>k!=='layer').map(k=>operation.command.startsWith('type.')?'text.'+(k==='size'?'sizePt':k):operation.command==='layer.setAdjustment'?'adjustment.BrightnessContrast.'+k:k==='visible'?'visible':k);
   allowedChanges[key]=[...new Set([...(allowedChanges[key]??[]),...fields])];
   if(operation.command.startsWith('type.'))allowedChanges[key].push('bounds');
  }
  const operations=contract.operations.flatMap((operation:any)=>operation.command==='layer.renameLayer'?[{command:'layer.select',params:{layer:operation.params.layer}},{command:operation.command,params:{name:operation.params.name}}]:operation.command==='layer.setAdjustment'?[{command:'layer.select',params:{layer:operation.params.layer}},{command:'native.command',params:{command:operation.command,params:operation.params}}]:[operation]);
  const plan:any={operations,exports:task.request.plan.exports??[{format:'png'}],expectedProjectSha256:contract.baseProjectSha256,expectedManifestSha256:contract.baseManifestSha256,preserveObjects:allowedChanges};
  if(task.request.plan.psdPolicy){
   const policy=JSON.parse(canonical(task.request.plan.psdPolicy));
   // 必要特性继续约束新候选；旧源的损失接受不能授权不同源版本。
   if(policy.acceptedForSourceSha256!==contract.baseProjectSha256){delete policy.acceptedLosses;delete policy.acceptedForSourceSha256;}
   plan.psdPolicy=policy;
  }
  if(contract.protectedRegions.length)plan.protectedRegions=contract.protectedRegions;
  const adjusted=contract.operations.filter((operation:any)=>operation.command==='layer.setAdjustment');
  if(adjusted.length)plan.assertions=adjusted.map((operation:any)=>({layer:operation.params.layer,kind:'Adjustment',hasMask:true,maskEnabled:true}));
  return this.ledger.transaction(()=>{
   // 预算在调度前消耗，重启不能撤回；后续失败需用户核对。
   const current=this.ledger.status(id);
   if(current.revisions!==task.revisions || current.creative.receiptSha256!==contract.gapReceiptSha256)throw new Error('revision_conflict');
   const root=this.ledger.revisionRoot(current);
   if(root.revisions>=root.request.budget.maxRevisions || Date.now()>=root.request.budget.deadline)throw new Error('budget_exhausted');
   if(root.id!==current.id){root.revisions++;this.ledger.save(root,'descendant_revision_reserved');}
   current.revisions=round;current.reviewRevisionReserved=true;current.revisionProposal=contract;this.ledger.save(current,'revision_reserved');
   // 新候选使用独立任务身份和不可变输出，累计预算继承剩余轮次。
   const remaining=root.request.budget.maxRevisions-(root.id===current.id?round:root.revisions);
   const request={...task.request,idempotencyKey:task.request.idempotencyKey+':revision:'+round,parentTask:id,source:task.request.output,output,plan,budget:{...task.request.budget,maxRevisions:remaining}};
   const normalized=JSON.parse(canonical(request));const identity=digest(canonical(normalized));
   const next={schema:'photocraft-task/v1',id:randomUUID(),identity,request:normalized,state:'planned',epoch:0,createdAt:Date.now(),revisions:0,attempted:false,technical:{status:'NOT_RUN'},creative:{status:'NOT_RUN'},acceptance:{status:'NOT_RUN'}};
   this.ledger.db.prepare('INSERT INTO tasks VALUES(?,?,?,?)').run(next.id,request.idempotencyKey,identity,canonical(next));this.ledger.save(next,'revision_created');return next;
  });
 }
}
