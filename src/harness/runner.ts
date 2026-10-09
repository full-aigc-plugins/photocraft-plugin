import {planDigest} from '../protocol/plan_identity.ts';
import { spawn } from 'node:child_process';
import { existsSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { confirmedWorkerReceipt } from './worker_receipt.ts';
import { pinPlan } from './pinned_plan.ts';
import { observeProgress } from './progress.ts';
import { canonical, digest, fileDigest, readJson, safePath, within } from '../protocol/files.ts';
import { Ledger } from './ledger.ts';
import { observeLateArtifacts } from './late_artifacts.ts';
import { mapArtifact } from '../protocol/artifact.ts';
import { Review } from '../evaluation/review.ts';
import { preflightRequest, pythonReply, reportedError, skillIdentity, runtimePlatformKey } from './preflight.ts';
import { strictJson, decodeUtf8 } from '../protocol/strict_json.ts';
import { OperationError } from '../protocol/operation_error.ts';
import { checkpointSnapshot, validateCheckpointReply } from './checkpoint.ts';

const object=(value:any)=>value!==null && typeof value==='object' && !Array.isArray(value);
const hex=(value:any)=>typeof value==='string' && /^[a-f0-9]{64}$/.test(value);
const invalidVerification=()=>new OperationError('unexpected_verification_result',{code:'unexpected_verification_result',phase:'verification',outcome:'unknown',recoveryAction:'reconcile'});

/** 部分工程或核验失败使旧的当前接受失效，历史通过证据仍保留。 */
function invalidateCurrentAcceptance(task:any,reason:string) {
 if(task.technical?.status==='PASS'){task.invalidatedTechnical??=[];task.invalidatedTechnical.push({technical:task.technical,artifact:task.artifact??null,reason,at:Date.now()});}
 if(task.reviewRequest || task.reviewReceipt){task.invalidatedReviews??=[];task.invalidatedReviews.push({request:task.reviewRequest??null,receipt:task.reviewReceipt??null,reason,at:Date.now()});}
 for(const key of ['reviewRequest','reviewReceipt','reviewConsumed','reviewRevisionReserved'])delete task[key];
 task.technical={status:'NOT_RUN'};task.creative={status:'NOT_RUN'};task.acceptance={status:'NOT_RUN'};delete task.artifact;
}

/** 所有编辑复用独立技能执行器；账本先登记意图，断连后只核对。 */
export class Runner {
 ledger: Ledger;
 options: { skillRoot: string; python: string; runtimeHome?: string };
 constructor(ledger: Ledger, options: { skillRoot: string; python: string; runtimeHome?: string }) { this.ledger=ledger; this.options=options; }

 identity() {
  return skillIdentity(this.options);
 }
 python(script: string,args: string[]) {
  return pythonReply(this.options,script,args);
 }
 /** 创建、执行和修订共用实际技能预检；调用不登记任务意图。 */
 preflight(request:any) {
  const identity=this.identity();
  preflightRequest(request,this.options,(script,args)=>this.python(script,args));
  if(this.identity().sha256!==identity.sha256)throw new OperationError('skill_source_changed',{code:'skill_source_changed',phase:'validation',outcome:'not_executed',category:'validation_failed',fieldPath:'$.skillRoot',recoveryAction:'inspect'});
  return identity;
 }
 /** 状态查询只读取原进度和监督回执，不变更账本、安装运行时或启动会话。 */
 status(id:string) {
  const task=this.ledger.status(id);
  try {
   if(!task.executionIdentity)return task;
   if(this.identity().sha256!==task.executionIdentity.sha256)throw new Error('skill_source_changed');
   const progress=observeProgress(task,this.options,(script,args)=>this.python(script,args));
   if(!progress)return task.progressObservation?{...task,progressObservation:{status:'UNAVAILABLE',code:'progress_record_missing',replayAllowed:false}}:task;
   const receipt=confirmedWorkerReceipt(this.ledger.root,task);
   if(receipt && receipt.workflowPid!==progress.record.ownerPid)throw new Error('progress_worker_identity_mismatch');
   return {...task,progressObservation:{...progress,workerStoppedConfirmed:!!receipt}};
  }catch(error){return {...task,progressObservation:{status:'UNAVAILABLE',code:String(error),replayAllowed:false}};}
 }
 async run(id: string) {
  let task=this.ledger.status(id);
  if(task.state!=='planned' || task.attempted) throw new Error('reconcile_required');
  if(task.request.mutableProject) {
   // 磁盘版本冲突优先报告；摘要相同不证明 GUI 未保存状态安全。
   let current:string;
   try {current=fileDigest(task.request.mutableProject);}
   catch {throw new OperationError('project_revision_unavailable',{code:'project_revision_unavailable',phase:'validation',outcome:'not_executed',category:'validation_failed',fieldPath:'$.mutableProject',recoveryAction:'inspect'});}
   if(current!==task.request.expectedProjectSha256)throw new OperationError('revision_conflict',{code:'revision_conflict',phase:'validation',outcome:'not_executed',category:'validation_failed',fieldPath:'$.expectedProjectSha256',recoveryAction:'correct_plan'});
   throw new Error('mutable_desktop_execution_not_supported');
  }
  if(task.request.checkpoint)this.checkRecoverySource(task);
  const identity=this.preflight(task.request);const planPath=join(this.ledger.root,id+'-plan.json');
  const args=[planPath,'--output',task.request.output];
  if(task.request.source) args.push('--source',task.request.source);
  if(task.request.checkpoint)args.push('--checkpoint',task.request.checkpoint.output,'--write-root',task.request.authorization.writeRoot);
  pinPlan(planPath,task.request.plan);
  const epoch=this.ledger.claim(id,identity.sha256);
  this.ledger.update(id,epoch,current=>{current.executionIdentity=identity;current.preflight={status:'PASS'};});
  if(this.options.runtimeHome) args.push('--runtime-home',safePath(this.options.runtimeHome));
  const workerToken=randomUUID();
  const launchPath=safePath(join(this.ledger.root,id+'-worker-launch.json'));
  const launch={schema:'photocraft-worker-launch/v1',taskId:id,taskIdentity:task.identity,epoch,workerToken,sourceSha256:identity.sha256,python:this.options.python,args:['-I','-B',join(this.options.skillRoot,'scripts/workflow.py'),...args],stopFile:join(this.ledger.root,id+'.stop'),deadline:task.request.budget.deadline,receipt:join(this.ledger.root,id+'-worker-exit.json')};
  writeFileSync(launchPath,canonical(launch),{flag:'wx',mode:0o600});const launchSha256=fileDigest(launchPath);
  this.ledger.update(id,epoch,current=>{current.worker={pid:process.pid,childPid:null,token:workerToken,startedAt:Date.now(),supervisor:true,launchSha256};});
  const child=spawn(process.execPath,[fileURLToPath(new URL('./worker_supervisor.ts',import.meta.url)),launchPath,launchSha256],{detached:process.platform!=='win32',stdio:['ignore','pipe','pipe'],env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
  this.ledger.update(id,epoch,current=>{current.worker.childPid=child.pid??null;});
  let bytes=0;const chunks:Buffer[]=[];let spawnError='';
  child.stdout.on('data',(data:Buffer)=>{bytes+=data.length;if(bytes<=2*1024*1024)chunks.push(data);});
  child.stderr.on('data',()=>{});child.on('error',error=>{spawnError=error.message;});
  // 独立监督进程是唯一停止责任层；父执行器只持久化截止时间触发，不发送第二轮信号。
  const timer=setInterval(()=>{const latest=this.ledger.status(id);if(Date.now()>=latest.request.budget.deadline && !latest.stopRequestedAt)this.ledger.stop(id);},100);
  const exit=await new Promise<number|null>(resolve=>child.once('close',resolve));clearInterval(timer);
  const output=Buffer.concat(chunks);
  task=this.ledger.status(id);let receipt:any;
  try{receipt=confirmedWorkerReceipt(this.ledger.root,task);}catch{}
  const processGroupGone=!!receipt;
  this.ledger.update(id,epoch,current=>{current.worker.exited=true;current.worker.processGroupGone=processGroupGone;current.executionResult={exitCode:exit,outputSha256:digest(output),outputTruncated:bytes>2*1024*1024 || receipt?.outputTruncated===true,spawnError,phase:'submitted',outcome:exit===0?'reply_received':'unknown'};if(receipt)current.workerExitReceipt=receipt;});
  if(receipt?.stoppedAt && !task.stopRequestedAt){this.ledger.stop(id);task=this.ledger.status(id);}
  if(task.stopRequestedAt) {
   this.ledger.update(id,epoch,current=>{current.stopEvidence={processGroupGone,ownedWorkerToken:workerToken,exitCode:receipt?.exitCode??exit,signal:receipt?.signal??child.signalCode,at:Date.now(),lateArtifacts:existsSync(join(current.request.output,'manifest.json'))};});
   if(this.ledger.status(id).state!=='reconciling')this.ledger.transition(id,epoch,'reconciling');
   this.registerLateArtifacts(id);
   const descendants=(this.ledger.db.prepare('SELECT data FROM tasks').all() as any[]).map(row=>JSON.parse(row.data)).filter(value=>value.request.parentTask===id);
   if(processGroupGone && descendants.every(value=>['cancelled','failed','completed'].includes(value.state)))return this.ledger.transition(id,epoch,'cancelled');
   return this.ledger.status(id);
  }
  if(!receipt) {
   this.ledger.transition(id,epoch,'reconciling');
   return this.ledger.update(id,epoch,current=>{current.replayAllowed=false;current.recoveryAction='confirm_owned_workers_stopped';});
  }
  let reply:any;
  try {
   if(spawnError || bytes>2*1024*1024 || receipt.outputTruncated)throw new Error('worker_reply_unavailable');
   reply=strictJson(decodeUtf8(output));
   const failure=reportedError(reply);if(failure)throw failure;
   if(exit!==0)throw new Error('worker_failed_without_contract');
   const manifest=readJson(join(task.request.output,'manifest.json'));
   const runtime=readJson(join(this.options.skillRoot,'scripts/runtime.lock.json'));
   const expectedRuntime=runtime.artifacts?.[runtimePlatformKey()]?.binarySha256;
   if(!object(reply) || reply.schema!=='photocraft-delivery/v1' || !object(reply.files)
      || !hex(reply.files['project.pcraft']) || !hex(reply.files['design.png'])
      || !hex(expectedRuntime) || reply.runtimeSha256!==expectedRuntime
      || !Array.isArray(reply.outputs) || canonical(reply)!==canonical(manifest))throw new Error('invalid_execution_reply');
  } catch(error) {
   // 真实调用已经结束；回复不明确时只保全现场，不自动核验或重放。
   this.ledger.transition(id,epoch,'reconciling');
   return this.ledger.update(id,epoch,current=>{
    const failure=reportedError(reply);
    current.executionResult={...current.executionResult,code:failure?.code??'outcome_unknown',phase:failure?.phase??(spawnError?'submitted':'reply_received'),outcome:failure?.outcome??'unknown',retryable:false,recoveryAction:failure?.recoveryAction??'reconcile',...(failure?.category?{category:failure.category}:{}),...(failure?.fieldPath?{fieldPath:failure.fieldPath}:{}),replyFailureCode:error instanceof OperationError?error.code:'invalid_execution_reply'};
    current.replayAllowed=false;current.recoveryAction='inspect_preserved_artifacts';
   });
  }
  try{
   await this.verify(id);
   return this.ledger.update(id,epoch,current=>{current.executionResult.phase='reply_validated';current.executionResult.outcome='succeeded';});
  }catch(error){
   const current=this.ledger.status(id);if(current.state!=='reconciling')this.ledger.transition(id,epoch,'reconciling');
   return this.ledger.update(id,epoch,value=>{value.replayAllowed=false;value.reconcileError=String(error);value.verificationError={code:error instanceof OperationError?error.code:'technical_verification_unproven',phase:'verification',outcome:error instanceof OperationError?error.outcome:'unknown',retryable:false,recoveryAction:error instanceof OperationError?error.recoveryAction:'reconcile'};value.recoveryAction='inspect_preserved_artifacts';});
  }
 }
 /** 保存取消任务的独立观察记录；相同快照不重复登记，迟到结果不能提升状态。 */
 registerLateArtifacts(id:string) {
  const task=this.ledger.status(id);const observation=observeLateArtifacts(task);
  if(task.replayAllowed===false && (!observation || task.lateArtifactObservations?.at(-1)?.sha256===observation.sha256))return task;
  return this.ledger.update(id,task.epoch,current=>{
   current.replayAllowed=false;
   if(observation && current.lateArtifactObservations?.at(-1)?.sha256!==observation.sha256) {
    current.lateArtifactObservations??=[];current.lateArtifactObservations.push(observation);
   }
  });
 }
 async reconcile(id: string) {
  let task=this.ledger.status(id);
  if(task.state==='cancelled')return this.registerLateArtifacts(id);
  if(['completed','failed','review_ready','planned'].includes(task.state))return task;
  if(task.worker?.supervisor && !task.stopRequestedAt && (existsSync(safePath(join(this.ledger.root,id+'.stop'))) || Date.now()>=task.request.budget.deadline)){this.ledger.stop(id);task=this.ledger.status(id);}
  if(task.state!=='reconciling')task=this.ledger.transition(id,task.epoch,'reconciling');
  if(task.worker?.supervisor && !task.worker.processGroupGone) {
   let receipt:any;
   try{receipt=confirmedWorkerReceipt(this.ledger.root,task);}catch(error){return this.ledger.update(id,task.epoch,current=>{current.replayAllowed=false;current.recoveryAction='inspect_worker_receipt';current.reconcileError=String(error);});}
   if(!receipt)return this.ledger.update(id,task.epoch,current=>{current.replayAllowed=false;current.recoveryAction='confirm_owned_workers_stopped';});
   task=this.ledger.update(id,task.epoch,current=>{current.worker.exited=true;current.worker.processGroupGone=true;current.workerExitReceipt=receipt;});
   if(receipt.stoppedAt && !task.stopRequestedAt){this.ledger.stop(id);task=this.ledger.status(id);}
  }
  // 活跃执行器仍有写入权；状态核对不能与它并行验收。
  if(task.stopRequestedAt) {
   this.registerLateArtifacts(id);
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
   try{return await this.verify(id);}catch(error){return this.ledger.update(id,task.epoch,current=>{invalidateCurrentAcceptance(current,String(error));current.replayAllowed=false;current.reconcileError=String(error);current.verificationError={code:error instanceof OperationError?error.code:'technical_verification_unproven',phase:'verification',outcome:'unknown',retryable:false,recoveryAction:'inspect'};current.recoveryAction='inspect_preserved_artifacts';});}
  }
  if(existsSync(join(task.request.output,'failure.json')) && task.executionIdentity) {
   try {
    if(this.identity().sha256!==task.executionIdentity.sha256)throw new OperationError('skill_source_changed',{code:'skill_source_changed',phase:'verification',outcome:'unknown',recoveryAction:'inspect'});
    const before=checkpointSnapshot(task.request.output,task.request.authorization.writeRoot);
    const runtime=readJson(join(this.options.skillRoot,'scripts/runtime.lock.json'));
    const args=[task.request.output,'--write-root',task.request.authorization.writeRoot];if(this.options.runtimeHome)args.push('--runtime-home',safePath(this.options.runtimeHome));
    const checkpoint=this.python('checkpoint_verify.py',args);
    validateCheckpointReply(checkpoint,before,checkpointSnapshot(task.request.output,task.request.authorization.writeRoot),runtime.artifacts?.[runtimePlatformKey()]?.binarySha256);
    if(before.origin && before.origin.planSha256!==planDigest(task.request.plan,before.origin.planHashAlgorithm))throw new Error('task_checkpoint_plan_mismatch');
    if(before.origin && canonical(before.origin.taskBinding)!==canonical({taskId:task.id,taskIdentity:task.identity,epoch:task.epoch,workerToken:task.worker?.token,sourceSha256:task.executionIdentity.sha256}))throw new Error('checkpoint_task_binding_mismatch');
    if(before.origin && before.origin.projectRevision!==((task.request.source || task.request.checkpoint)?task.request.plan.expectedProjectSha256:null))throw new Error('checkpoint_source_conflict');
    for(const ref of task.request.references??[])if(fileDigest(ref.path)!==ref.sha256)throw new Error('reference_identity_mismatch');
    for(const [name,entry]of Object.entries(task.request.plan.assets??{}) as [string,any][])if(before.origin && before.origin.inputHashes[name]!==entry.sha256)throw new Error('checkpoint_input_mismatch');
    if(this.identity().sha256!==task.executionIdentity.sha256)throw new OperationError('skill_source_changed',{code:'skill_source_changed',phase:'verification',outcome:'unknown',recoveryAction:'inspect'});
    return this.ledger.update(id,task.epoch,current=>{invalidateCurrentAcceptance(current,'partial_checkpoint_only');current.checkpoint=checkpoint;delete current.verificationError;delete current.reconcileError;current.replayAllowed=false;current.recoveryAction='inspect_checkpoint_before_explicit_revision';current.technical={status:'NOT_RUN'};});
   }catch(error){return this.ledger.update(id,task.epoch,current=>{invalidateCurrentAcceptance(current,String(error));delete current.checkpoint;current.replayAllowed=false;current.reconcileError=String(error);current.verificationError={code:error instanceof OperationError?error.code:'checkpoint_verification_failed',phase:'verification',outcome:error instanceof OperationError?error.outcome:'unknown',retryable:false,recoveryAction:'inspect'};current.recoveryAction='inspect_preserved_artifacts';current.technical={status:'NOT_RUN'};});}
  }
  const observed=this.status(id).progressObservation;
  if(observed?.status==='OBSERVED' && observed.workerStoppedConfirmed && task.executionIdentity) {
   try {
    const checkInputs=()=>{
     for(const ref of task.request.references??[])if(fileDigest(ref.path)!==ref.sha256)throw new Error('reference_identity_mismatch');
     for(const entry of Object.values(task.request.plan.assets??{}) as any[])if(fileDigest(entry.path)!==entry.sha256)throw new Error('checkpoint_input_mismatch');
     if(task.request.source && fileDigest(join(task.request.source,'project.pcraft'))!==task.request.plan.expectedProjectSha256)throw new Error('checkpoint_source_conflict');
     if(task.request.checkpoint)this.checkRecoverySource(task);
    };
    checkInputs();
    const output=within(join(dirname(task.request.output),'.photocraft-checkpoint-'+digest(task.request.output)),task.request.authorization.writeRoot);
    const args=[task.request.output,'--write-root',task.request.authorization.writeRoot,'--checkpoint-output',output,'--progress-sha256',observed.recordSha256,'--worker-receipt',join(this.ledger.root,id+'-worker-exit.json'),'--worker-launch',join(this.ledger.root,id+'-worker-launch.json')];
    const capture=this.python('interrupted_checkpoint.py',args),before=checkpointSnapshot(output,task.request.authorization.writeRoot);
    if(!object(capture) || Object.keys(capture).some(key=>!['schema','result','recordSha256','replayAllowed'].includes(key)) || capture.schema!=='photocraft-interrupted-capture/v1' || capture.result!=='PASS' || capture.replayAllowed!==false || capture.recordSha256!==before.recordSha256)throw new Error('interrupted_capture_unproven');
    const record=readJson(join(output,'checkpoint.json'));
    if(record.progressOutput!==task.request.output || record.progressSha256!==observed.recordSha256 || canonical(record.context)!==canonical(observed.record.context))throw new Error('interrupted_origin_conflict');
    const runtime=readJson(join(this.options.skillRoot,'scripts/runtime.lock.json'));
    const verifyArgs=[output,'--write-root',task.request.authorization.writeRoot];if(this.options.runtimeHome)verifyArgs.push('--runtime-home',safePath(this.options.runtimeHome));
    const checkpoint=this.python('checkpoint_verify.py',verifyArgs);
    validateCheckpointReply(checkpoint,before,checkpointSnapshot(output,task.request.authorization.writeRoot),runtime.artifacts?.[runtimePlatformKey()]?.binarySha256);
    if(!confirmedWorkerReceipt(this.ledger.root,task) || this.identity().sha256!==task.executionIdentity.sha256 || this.status(id).progressObservation?.recordSha256!==observed.recordSha256)throw new Error('interrupted_snapshot_changed');
    checkInputs();
    return this.ledger.update(id,task.epoch,current=>{invalidateCurrentAcceptance(current,'partial_interrupted_checkpoint_only');current.progressObservation=observed;current.checkpoint={...checkpoint,output};delete current.reconcileError;delete current.verificationError;current.replayAllowed=false;current.recoveryAction='inspect_checkpoint_before_explicit_revision';});
   }catch(error){return this.ledger.update(id,task.epoch,current=>{invalidateCurrentAcceptance(current,String(error));delete current.checkpoint;current.progressObservation=observed;current.reconcileError=String(error);current.replayAllowed=false;current.recoveryAction='inspect_interrupted_stage';});}
  }
  return this.ledger.update(id,task.epoch,current=>{current.replayAllowed=false;current.recoveryAction=observed?.status==='OBSERVED'?'inspect_interrupted_stage':'inspect_preserved_artifacts';if(observed)current.progressObservation=observed;invalidateCurrentAcceptance(current,'delivery_evidence_missing');});
 }
 async verify(id: string) {
  let task=this.ledger.status(id);
  if(!['running','reconciling','verifying'].includes(task.state))throw new Error('verification_not_ready');
  if(task.stopRequestedAt || Date.now()>=task.request.budget.deadline || existsSync(safePath(join(this.ledger.root,id+'.stop'))))throw new Error('stopped_task_verification_forbidden');
  if(!task.executionIdentity || task.executionIdentity.sha256!==this.identity().sha256)throw new Error('skill_source_changed');
  const output=safePath(task.request.output);
  const integrity=this.python('delivery.py',[output]);
  if(integrity?.result==='FAIL' && typeof integrity.error==='string')throw new OperationError(integrity.error,{code:'technical_verification_failed',phase:'verification',outcome:'failed',recoveryAction:'inspect'});
  if(!object(integrity) || integrity.schema!=='photocraft-delivery-integrity/v1' || integrity.result!=='PASS'
     || Object.hasOwn(integrity,'error') || !hex(integrity.manifestSha256) || !hex(integrity.nativeSha256)
     || !Number.isSafeInteger(integrity.files) || integrity.files<=0)throw invalidVerification();
  const manifest=readJson(join(output,'manifest.json'));const manifestSha256=fileDigest(join(output,'manifest.json'));
  if(!object(manifest) || !object(manifest.files) || integrity.manifestSha256!==manifestSha256
     || integrity.nativeSha256!==manifest.files['project.pcraft'] || integrity.files!==Object.keys(manifest.files).length)throw invalidVerification();
  if(!manifest.files['plan.json'] || canonical(readJson(join(output,'plan.json')))!==canonical(task.request.plan))throw new OperationError('task_delivery_plan_mismatch',{code:'task_delivery_plan_mismatch',phase:'verification',outcome:'unknown',recoveryAction:'inspect'});
  const expectedProducer={taskId:task.id,taskIdentity:task.identity,epoch:task.epoch,workerToken:task.worker?.token,sourceSha256:task.executionIdentity.sha256};
  if(!task.worker?.token || !object(manifest.taskBinding) || canonical(manifest.taskBinding)!==canonical(expectedProducer))throw new OperationError('task_delivery_producer_mismatch',{code:'task_delivery_producer_mismatch',phase:'verification',outcome:'unknown',recoveryAction:'inspect'});
  const expectedSource=task.request.source || task.request.checkpoint?task.request.plan.expectedProjectSha256:null;
  if(manifest.sourceProjectSha256!==expectedSource)throw new OperationError('task_delivery_source_mismatch',{code:'task_delivery_source_mismatch',phase:'verification',outcome:'unknown',recoveryAction:'inspect'});
  for(const ref of task.request.references??[])if(fileDigest(ref.path)!==ref.sha256)throw new OperationError('reference_identity_mismatch',{code:'reference_identity_mismatch',phase:'verification',outcome:'unknown',recoveryAction:'inspect'});
  for(const [name,entry]of Object.entries(task.request.plan.assets??{}) as [string,any][])if(manifest.assets?.[name]?.sha256!==entry.sha256)throw new OperationError('task_delivery_input_mismatch',{code:'task_delivery_input_mismatch',phase:'verification',outcome:'unknown',recoveryAction:'inspect'});
  const nativeArgs=[output];if(this.options.runtimeHome)nativeArgs.push('--runtime-home',safePath(this.options.runtimeHome));
  const reopened=this.python('native_verify.py',nativeArgs);
  if(reopened?.result==='FAIL' && typeof reopened.error==='string')throw new OperationError(reopened.error,{code:'technical_verification_failed',phase:'verification',outcome:'failed',recoveryAction:'inspect'});
  const runtime=readJson(join(this.options.skillRoot,'scripts/runtime.lock.json'));
  const expectedRuntime=runtime.artifacts?.[runtimePlatformKey()]?.binarySha256;
  if(!object(reopened) || reopened.schema!=='photocraft-native-verification/v1' || reopened.result!=='PASS'
     || Object.hasOwn(reopened,'error') || reopened.manifestSha256!==manifestSha256 || reopened.projectSha256!==integrity.nativeSha256
     || !hex(expectedRuntime) || reopened.runtimeSha256!==expectedRuntime || manifest.runtimeSha256!==expectedRuntime
     || fileDigest(join(output,'manifest.json'))!==manifestSha256)throw invalidVerification();
  if(!manifest.files['design.png'])throw new Error('preview_required');
  const files: Record<string,string>={};
  for(const [name,sha]of Object.entries(manifest.files)) {const path=within(join(output,name),output);if(fileDigest(path)!==sha)throw new Error('candidate_changed');files[path]=sha as string;}
  files[join(output,'manifest.json')]=fileDigest(join(output,'manifest.json'));
  if(task.state!=='verifying')task=this.ledger.transition(id,task.epoch,'verifying');
  const evidence={status:'PASS',projectSha256:manifest.files['project.pcraft'],previewSha256:manifest.files['design.png'],manifestSha256:files[join(output,'manifest.json')],files,nativeReopen:reopened,sourceSha256:task.executionIdentity.sha256};
  const parent=task.request.parentTask?this.ledger.status(task.request.parentTask):undefined;
  if(parent && parent.technical.projectSha256===evidence.projectSha256)throw new Error('revision_no_improvement');
  if(task.request.checkpoint)this.checkRecoverySource(task);
  const artifact=mapArtifact({...task,technical:evidence},parent?.artifact);
  return this.ledger.recordTechnical(id,task.epoch,evidence,artifact);
 }
 /** 检查点修订必须绑定原任务、原记录与已停止的原执行者；旧文件不补造父产物。 */
 checkRecoverySource(task:any) {
  const source=task.request.checkpoint,parent=this.ledger.status(task.request.parentTask);
  if(parent.executionIdentity?.sha256!==this.identity().sha256)throw new Error('skill_source_changed');
  if(this.ledger.lineage(parent).some(ancestor=>ancestor.stopRequestedAt || ['cancel_requested','cancelled','failed'].includes(ancestor.state)))throw new Error('parent_task_stopped');
  if(!source || (parent.checkpoint?.output??parent.request.output)!==source.output || parent.checkpoint?.recordSha256!==source.recordSha256 || parent.checkpoint?.projectSha256!==source.projectSha256 || parent.checkpoint?.origin?.planSha256!==source.planSha256)throw new Error('checkpoint_parent_conflict');
  if(parent.stopRequestedAt || ['cancel_requested','cancelled','failed'].includes(parent.state))throw new Error('parent_task_stopped');
  if(!confirmedWorkerReceipt(this.ledger.root,parent))throw new Error('worker_resolution_required');
  const snapshot=checkpointSnapshot(source.output,parent.request.authorization.writeRoot);
  if(snapshot.recordSha256!==source.recordSha256 || snapshot.projectSha256!==source.projectSha256 || snapshot.origin?.planSha256!==source.planSha256 || source.planSha256!==planDigest(parent.request.plan,parent.checkpoint?.origin?.planHashAlgorithm))throw new Error('checkpoint_changed');
  if(task.request.plan.expectedCheckpointSha256!==source.recordSha256 || task.request.plan.expectedCheckpointPlanSha256!==source.planSha256 || task.request.plan.expectedProjectSha256!==source.projectSha256)throw new Error('checkpoint_plan_conflict');
  return snapshot;
 }
 /** 显式新修订从已保存工程开始，不重复原计划；累计预算在调度前保留。 */
 async recover(id:string,proposal:any) {
  let task=this.ledger.status(id);
  if(!confirmedWorkerReceipt(this.ledger.root,task))throw new Error('worker_resolution_required');
  if(!object(proposal) || Object.keys(proposal).some(key=>!['baseProjectSha256','checkpointRecordSha256','authorizationRef','reason','operations'].includes(key)) || typeof proposal.reason!=='string' || !proposal.reason.trim() || !Array.isArray(proposal.operations) || !proposal.operations.length || proposal.operations.length>100)throw new Error('recovery_proposal_invalid');
  const proposalSha256=digest(canonical(proposal));
  if(task.recoveryRevision) {
   if(task.recoveryRevision.proposalSha256!==proposalSha256)throw new Error('recovery_revision_already_reserved');
   return this.ledger.status(task.recoveryRevision.taskId);
  }
  task=await this.reconcile(id);
  const checkpoint=task.checkpoint;
  if(task.state!=='reconciling' || task.stopRequestedAt || !checkpoint?.origin || !checkpoint.nativeDocument)throw new Error('verified_checkpoint_required');
  if(proposal.baseProjectSha256!==checkpoint.projectSha256 || proposal.checkpointRecordSha256!==checkpoint.recordSha256)throw new Error('checkpoint_changed');
  if(proposal.authorizationRef!==task.request.authorization.ref)throw new Error('authorization_scope_changed');
  const allowed:Record<string,string[]>={'type.edit':['text'],'type.setStyle':['font','size'],'layer.renameLayer':['name']};
  const objects=new Map<number,any>();
  const walk=(layers:any[])=>{for(const row of layers){if(!object(row) || !Number.isSafeInteger(row.id) || objects.has(row.id))throw new Error('checkpoint_objects_invalid');objects.set(row.id,row);if(row.children){if(!Array.isArray(row.children))throw new Error('checkpoint_objects_invalid');walk(row.children);}}};walk(checkpoint.nativeDocument.layers);
  const changes:Record<string,string[]>={};
  for(const operation of proposal.operations) {
   const fields=object(operation) && Object.hasOwn(allowed,operation.command)?allowed[operation.command]:undefined,params=operation?.params;
   if(!fields || Object.keys(operation).some(key=>!['command','params'].includes(key)) || !object(params) || !Number.isSafeInteger(params.layer) || !objects.has(params.layer) || Object.keys(params).some(key=>key!=='layer' && !fields.includes(key)))throw new Error('recovery_scope_violation');
   const row=objects.get(params.layer),changed=Object.keys(params).filter(key=>key!=='layer');
   if(!changed.length || operation.command.startsWith('type.') && row.kind!=='Type')throw new Error('recovery_scope_violation');
   if(task.request.authorization.objects && !task.request.authorization.objects.includes(params.layer))throw new Error('authorization_scope_changed');
   if(changed.every(key=>(operation.command.startsWith('type.')?row.text?.[key==='size'?'sizePt':key]:row[key])===params[key]))throw new Error('revision_no_improvement');
   const key=String(params.layer);changes[key]=[...new Set([...(changes[key]??[]),...changed.map(field=>operation.command.startsWith('type.')?'text.'+(field==='size'?'sizePt':field):field),...(operation.command.startsWith('type.')?['bounds']:[])])];
  }
  if(this.ledger.lineage(task).some(ancestor=>ancestor.stopRequestedAt || ['cancel_requested','cancelled','failed'].includes(ancestor.state)))throw new Error('parent_task_stopped');
  const round=task.revisions+1,root=this.ledger.revisionRoot(task),output=join(task.request.authorization.writeRoot,id+'-recovery-'+round);
  if(root.revisions>=root.request.budget.maxRevisions || Date.now()>=root.request.budget.deadline)throw new Error('budget_exhausted');
  const operations=proposal.operations.flatMap((operation:any)=>operation.command==='layer.renameLayer'?[{command:'layer.select',params:{layer:operation.params.layer}},{command:operation.command,params:{name:operation.params.name}}]:[operation]);
  const source={output:checkpoint.output??task.request.output,recordSha256:checkpoint.recordSha256,planSha256:checkpoint.origin.planSha256,projectSha256:checkpoint.projectSha256};
  const plan:any={operations,exports:task.request.plan.exports?.length?task.request.plan.exports:[{format:'png'}],expectedProjectSha256:source.projectSha256,expectedCheckpointSha256:source.recordSha256,expectedCheckpointPlanSha256:source.planSha256,preserveObjects:changes};
  if(task.request.plan.protectedRegions)plan.protectedRegions=task.request.plan.protectedRegions;
  for(const key of ['minimumLayers','acceptedFontSubstitutions','flatExport','assetProvenance'])if(task.request.plan[key]!==undefined)plan[key]=JSON.parse(canonical(task.request.plan[key]));
  if(task.request.plan.psdPolicy){plan.psdPolicy=JSON.parse(canonical(task.request.plan.psdPolicy));if(plan.psdPolicy.acceptedForSourceSha256!==source.projectSha256){delete plan.psdPolicy.acceptedLosses;delete plan.psdPolicy.acceptedForSourceSha256;}}
  const request:any={...task.request,idempotencyKey:task.request.idempotencyKey+':recovery:'+round,parentTask:id,checkpoint:source,output,plan,budget:{...task.request.budget,maxRevisions:root.request.budget.maxRevisions-root.revisions-1}};delete request.source;
  const normalized=Ledger.validateRequest(request).normalized;
  this.preflight(normalized);
  return this.ledger.transaction(()=>{
   const current=this.ledger.status(id),currentRoot=this.ledger.revisionRoot(current);
   if(current.recoveryRevision || current.revisions!==task.revisions || current.stopRequestedAt || current.checkpoint?.recordSha256!==source.recordSha256 || currentRoot.revisions>=currentRoot.request.budget.maxRevisions || Date.now()>=currentRoot.request.budget.deadline)throw new Error('recovery_revision_conflict');
   const next={schema:'photocraft-task/v1',id:randomUUID(),identity:digest(canonical(normalized)),request:normalized,state:'planned',epoch:0,createdAt:Date.now(),revisions:0,attempted:false,technical:{status:'NOT_RUN'},creative:{status:'NOT_RUN'},acceptance:{status:'NOT_RUN'}};
   this.checkRecoverySource(next);
   if(currentRoot.id!==id){currentRoot.revisions++;this.ledger.save(currentRoot,'descendant_recovery_reserved');}
   current.revisions=round;current.recoveryRevision={taskId:next.id,proposalSha256,reason:proposal.reason};current.replayAllowed=false;this.ledger.save(current,'checkpoint_revision_reserved');
   this.ledger.db.prepare('INSERT INTO tasks VALUES(?,?,?,?)').run(next.id,request.idempotencyKey,next.identity,canonical(next));this.ledger.save(next,'revision_created');return next;
  });
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
  if(task.request.plan.flatExport)plan.flatExport=JSON.parse(canonical(task.request.plan.flatExport));
  if(task.request.plan.psdPolicy){
   const policy=JSON.parse(canonical(task.request.plan.psdPolicy));
   // 必要特性继续约束新候选；旧源的损失接受不能授权不同源版本。
   if(policy.acceptedForSourceSha256!==contract.baseProjectSha256){delete policy.acceptedLosses;delete policy.acceptedForSourceSha256;}
   plan.psdPolicy=policy;
  }
  if(contract.protectedRegions.length)plan.protectedRegions=contract.protectedRegions;
  const adjusted=contract.operations.filter((operation:any)=>operation.command==='layer.setAdjustment');
  if(adjusted.length)plan.assertions=adjusted.map((operation:any)=>({layer:operation.params.layer,kind:'Adjustment',hasMask:true,maskEnabled:true}));
  this.preflight({...task.request,source:task.request.output,output,plan});
  return this.ledger.transaction(()=>{
   // 预算在调度前消耗，重启不能撤回；后续失败需用户核对。
   const current=this.ledger.status(id);
   if(current.revisions!==task.revisions || current.creative.receiptSha256!==contract.gapReceiptSha256)throw new Error('revision_conflict');
   if(canonical(new Review(this.ledger).propose(id,proposal))!==canonical(contract))throw new Error('revision_conflict');
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
