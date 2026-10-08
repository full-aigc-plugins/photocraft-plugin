import { lstatSync } from 'node:fs';
import { isAbsolute, join, normalize } from 'node:path';
import { canonical, fileDigest, readJson, within } from '../protocol/files.ts';
import { OperationError } from '../protocol/operation_error.ts';

const object=(v:any)=>v!==null && typeof v==='object' && !Array.isArray(v);
const hex=(v:any)=>typeof v==='string' && /^[a-f0-9]{64}$/.test(v);
/** 不可信检查点不能证明原编辑未执行，也不能获得自动重放权限。 */
export function checkpointError() {
 return new OperationError('checkpoint_verification_failed',{code:'checkpoint_verification_failed',phase:'verification',outcome:'unknown',recoveryAction:'inspect'});
}

/** 捕获授权根内原暂存文件；外部写方的变动只拒绝，不覆盖或修复。 */
export function checkpointSnapshot(output:string,writeRoot:string) {
 try {
  output=within(output,writeRoot);
  const recordPath=within(join(output,'failure.json'),output);
  const recordSha256=fileDigest(recordPath),record=readJson(recordPath);
  if(!object(record) || record.schema!=='craft-failed-stage/v1' || record.status!=='failed'
     || record.replayAllowed!==false || !['failed','outcome_unknown'].includes(record.outcome)
     || typeof record.stage!=='string' || isAbsolute(record.stage) || !object(record.files)
     || !Number.isSafeInteger(record.completedOperations) || record.completedOperations<0)throw checkpointError();
  if(record.lastAttempt!=null && (!object(record.lastAttempt) || typeof record.lastAttempt.tool!=='string'
     || !record.lastAttempt.tool || !object(record.lastAttempt.arguments)
     || !['submitted','reply_validated'].includes(record.lastAttempt.phase)))throw checkpointError();
  const stage=within(join(output,record.stage),writeRoot);
  const stageRecord=within(join(stage,'failure.json'),stage);
  if(canonical(readJson(stageRecord))!==canonical(record))throw checkpointError();
  const files:Record<string,{sha256:string;bytes:number}>={};
  for(const [name,value]of Object.entries(record.files) as [string,any][]) {
   if(!name || isAbsolute(name) || normalize(name)!==name || name.split(/[\\/]/).includes('..')
      || name==='failure.json' || !object(value) || Object.keys(value).sort().join(',')!=='bytes,sha256'
      || !hex(value.sha256) || !Number.isSafeInteger(value.bytes) || value.bytes<0)throw checkpointError();
   const path=within(join(stage,name),stage),stat=lstatSync(path);
   if(!stat.isFile() || stat.size!==value.bytes || fileDigest(path)!==value.sha256)throw checkpointError();
   Object.defineProperty(files,name,{value:{sha256:value.sha256,bytes:value.bytes},enumerable:true});
  }
  if(!Object.hasOwn(files,'project.pcraft') || !Object.hasOwn(files,'recovery-operations.json'))throw checkpointError();
  const operations=readJson(join(stage,'recovery-operations.json'));
  if(!Array.isArray(operations) || operations.length!==record.completedOperations)throw checkpointError();
  if(fileDigest(recordPath)!==recordSha256)throw checkpointError();
  return {stage,recordSha256,stageRecordSha256:fileDigest(stageRecord),projectSha256:files['project.pcraft'].sha256,
          files,lastAttempt:record.lastAttempt??null,completedOperations:record.completedOperations};
 }catch {throw checkpointError();}
}

/** 只接受对当前原记录、工程、已验证操作及锁定运行时的部分重开证明。 */
export function validateCheckpointReply(reply:any,before:ReturnType<typeof checkpointSnapshot>,after:ReturnType<typeof checkpointSnapshot>,runtimeSha256:string) {
 if(reply?.result==='FAIL' && typeof reply.error==='string')throw new OperationError(reply.error,{code:'technical_verification_failed',phase:'verification',outcome:'failed',recoveryAction:'inspect'});
 const keys=new Set(['schema','result','stage','recordSha256','projectSha256','files','lastAttempt','completedOperations','nativeReopened','objectCount','runtimeSha256','replayAllowed','technical','creative','scope']);
 if(!object(reply) || Object.keys(reply).some(key=>!keys.has(key)) || (Object.hasOwn(reply,'scope') && typeof reply.scope!=='string')
    || reply.schema!=='photocraft-checkpoint-verification/v1' || reply.result!=='PASS'
    || Object.hasOwn(reply,'error') || reply.replayAllowed!==false || reply.nativeReopened!==true
    || reply.technical!=='NOT_RUN' || reply.creative!=='NOT_RUN'
    || !Number.isSafeInteger(reply.objectCount) || reply.objectCount<0 || !hex(runtimeSha256) || reply.runtimeSha256!==runtimeSha256
    || reply.stage!==before.stage || reply.recordSha256!==before.recordSha256 || reply.projectSha256!==before.projectSha256
    || reply.completedOperations!==before.completedOperations || canonical(reply.lastAttempt??null)!==canonical(before.lastAttempt)
    || !object(reply.files) || canonical(reply.files)!==canonical(before.files) || canonical(before)!==canonical(after))throw checkpointError();
}
