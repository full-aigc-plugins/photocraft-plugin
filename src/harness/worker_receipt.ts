import { join } from 'node:path';
import { existsSync } from 'node:fs';
import { fileDigest, readJson } from '../protocol/files.ts';

/** 退出回执必须匹配持久启动身份，且工作进程组已消失；旧 PID 仅用于保守存活探测。 */
export function confirmedWorkerReceipt(root:string,task:any):any|undefined {
 if(!task.worker?.supervisor)return undefined;
 const path=join(root,task.id+'-worker-exit.json');if(!existsSync(path))return undefined;
 const receipt=readJson(path);const launchPath=join(root,task.id+'-worker-launch.json');
 if(receipt.schema!=='photocraft-worker-exit/v1' || receipt.taskId!==task.id || receipt.taskIdentity!==task.identity || receipt.epoch!==task.epoch
  || receipt.workerToken!==task.worker.token || receipt.sourceSha256!==task.executionIdentity?.sha256 || receipt.launchSha256!==task.worker.launchSha256
  || fileDigest(launchPath)!==task.worker.launchSha256 || (!Number.isSafeInteger(receipt.supervisorPid) || receipt.supervisorPid<=0 || task.worker.childPid!==null && receipt.supervisorPid!==task.worker.childPid) || receipt.processGroupGone!==true
  || !Number.isSafeInteger(receipt.finishedAt) || receipt.finishedAt<task.worker.startedAt
  || !(receipt.workflowPid===null || Number.isSafeInteger(receipt.workflowPid) && receipt.workflowPid>0))throw new Error('worker_receipt_identity_mismatch');
 if(process.platform!=='win32')for(const pid of [receipt.supervisorPid,receipt.workflowPid]) {
  if(pid===null)continue;
  try{process.kill(-pid,0);return undefined;}catch(error){if((error as any).code!=='ESRCH')return undefined;}
 }
 return receipt;
}
