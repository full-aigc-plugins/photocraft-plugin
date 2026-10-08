import {planDigest} from '../protocol/plan_identity.ts';
import {existsSync,lstatSync} from 'node:fs';
import {dirname,join} from 'node:path';
import {canonical,digest,fileDigest,readJson,within} from '../protocol/files.ts';
import {runtimePlatformKey} from './preflight.ts';
const object=(value:any)=>value!==null && typeof value==='object' && !Array.isArray(value);

/** 只读进度不产生检查点或写入权；来源必须匹配原任务和当前固定执行器。 */
export function observeProgress(task:any,options:any,execute:(script:string,args:string[])=>any) {
 const output=within(task.request.output,task.request.authorization.writeRoot);
 const path=within(join(dirname(output),'.photocraft-progress-'+digest(output)+'.json'),task.request.authorization.writeRoot);
 if(!existsSync(path))return undefined;
 const before=fileDigest(path),reply=execute('progress.py',[output,'--write-root',task.request.authorization.writeRoot]);
 const keys=new Set(['schema','result','recordSha256','record','stage','stageAvailable','replayAllowed','technical','creative','scope']);
 if(!object(reply) || Object.keys(reply).some(key=>!keys.has(key)) || reply.schema!=='photocraft-progress-inspection/v1' || reply.result!=='PASS'
  || reply.recordSha256!==before || fileDigest(path)!==before || reply.replayAllowed!==false || reply.technical!=='NOT_RUN' || reply.creative!=='NOT_RUN'
  || !object(reply.record) || canonical(reply.record)!==canonical(readJson(path)) || typeof reply.stageAvailable!=='boolean')throw new Error('progress_snapshot_unproven');
 const record=reply.record,context=record.context;
 if(record.schema!=='photocraft-progress/v1' || record.targetHash!==digest(output) || record.replayAllowed!==false
  || !Number.isSafeInteger(record.sequence) || record.sequence<1 || !Number.isSafeInteger(record.completedOperations) || record.completedOperations<0
  || !Array.isArray(record.operations) || record.operations.length!==record.completedOperations
  || !['prepared','submitted','reply_validated','publishing','finished'].includes(record.phase)
  || typeof record.stage!=='string' || reply.stage!==within(join(output,record.stage),task.request.authorization.writeRoot)
  || !object(context) || !object(context.executionIdentity))throw new Error('progress_snapshot_unproven');
 if(existsSync(reply.stage)!==reply.stageAvailable)throw new Error('progress_stage_conflict');
 if(reply.stageAvailable){const stage=lstatSync(reply.stage,{bigint:true});if(!stage.isDirectory() || canonical(record.stageIdentity)!==canonical([String(stage.dev),String(stage.ino)]))throw new Error('progress_stage_conflict');}
 const expected={taskId:task.id,taskIdentity:task.identity,epoch:task.epoch,workerToken:task.worker?.token,sourceSha256:task.executionIdentity?.sha256};
 if(!task.worker?.supervisor || !task.worker.token || !object(context.taskBinding) || canonical(context.taskBinding)!==canonical(expected))throw new Error('progress_task_binding_mismatch');
 const runtime=readJson(join(options.skillRoot,'scripts/runtime.lock.json'));
 const identity=context.executionIdentity,project=task.request.source||task.request.checkpoint?task.request.plan.expectedProjectSha256:null;
 if(canonical(context.plan)!==canonical(task.request.plan) || identity.planHash!==planDigest(task.request.plan,identity.planHashAlgorithm) || identity.projectRevision!==project
  || identity.runtimeSha256!==runtime.artifacts?.[runtimePlatformKey()]?.binarySha256 || !object(identity.inputHashes))throw new Error('progress_execution_identity_mismatch');
 for(const [name,entry]of Object.entries(task.request.plan.assets??{}) as [string,any][])if(identity.inputHashes[name]!==entry.sha256)throw new Error('progress_input_identity_mismatch');
 return {status:'OBSERVED',...reply};
}
