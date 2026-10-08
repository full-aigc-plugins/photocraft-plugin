import {openSync,closeSync,writeFileSync,readFileSync,fstatSync,fsyncSync,constants} from 'node:fs';
import {canonical,safePath} from '../protocol/files.ts';

/** 认领前固定原任务计划；完全一致的旧文件可复用，截断或外来文件原样保留并拒绝。 */
export function pinPlan(path:string,plan:any):void {
 const target=safePath(path),expected=Buffer.from(canonical(plan));let descriptor:number;
 try {
  descriptor=openSync(target,constants.O_CREAT|constants.O_EXCL|constants.O_WRONLY|constants.O_NOFOLLOW,0o600);
 }catch(error){
  if((error as any).code!=='EEXIST')throw error;
  try {
   descriptor=openSync(safePath(target),constants.O_RDONLY|constants.O_NOFOLLOW);
   try {
    const info=fstatSync(descriptor);
    if(!info.isFile() || info.nlink!==1 || info.size!==expected.length || !readFileSync(descriptor).equals(expected))throw new Error('pinned_plan_conflict');
   }finally{closeSync(descriptor);}
  }catch(error){
   if((error as Error).message==='symlink_not_allowed')throw error;
   throw new Error('pinned_plan_conflict',{cause:error});
  }
  return;
 }
 try{writeFileSync(descriptor,expected);fsyncSync(descriptor);}finally{closeSync(descriptor);}
}
