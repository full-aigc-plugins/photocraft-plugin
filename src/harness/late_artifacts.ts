import { closeSync, constants, existsSync, fstatSync, lstatSync, openSync, readSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { canonical, digest, safePath, within } from '../protocol/files.ts';

/** 取消后的文件仅登记观察摘要；不解析交付声明，也不授予验收或重放权限。 */
export function observeLateArtifacts(task:any):any|undefined {
 const files:Record<string,string>={};const errors:{path:string;code:string}[]=[];let count=0;
 const output=task.request.output;
 const walk=(directory:string,prefix:string)=>{
  for(const name of readdirSync(safePath(directory)).sort()) {
   const relative=prefix+name;const path=join(directory,name);
   if(++count>10000){errors.push({path:relative,code:'inventory_limit'});return;}
   try{
    within(path,task.request.authorization.writeRoot);const stat=lstatSync(path);
    if(stat.isDirectory())walk(path,relative+'/');
    else if(stat.isFile()) {
     const fd=openSync(safePath(path),constants.O_RDONLY | constants.O_NOFOLLOW);
     try{
      const before=fstatSync(fd);if(before.ino!==stat.ino || before.dev!==stat.dev)throw new Error('artifact_changed_during_observation');const hash=createHash('sha256');const buffer=Buffer.alloc(1024*1024);let bytes=0;let read=0;
      while(bytes<before.size && (read=readSync(fd,buffer,0,Math.min(buffer.length,before.size-bytes),null))>0){bytes+=read;hash.update(buffer.subarray(0,read));}
      const after=fstatSync(fd);const current=lstatSync(safePath(path));
      if(bytes!==before.size || before.size!==after.size || before.mtimeMs!==after.mtimeMs || before.ctimeMs!==after.ctimeMs || current.ino!==before.ino || current.dev!==before.dev)throw new Error('artifact_changed_during_observation');
      files[relative]=hash.digest('hex');
     }finally{closeSync(fd);}
    }else errors.push({path:relative,code:'unsupported_file_type'});
   }catch(error){errors.push({path:relative,code:error instanceof Error && ['symlink_not_allowed','artifact_changed_during_observation','path_outside_authorization'].includes(error.message)?error.message:'artifact_observation_failed'});}
   if(count>10000)return;
  }
 };
 try{within(output,task.request.authorization.writeRoot);if(!existsSync(output))return undefined;walk(output,'');}
 catch(error){errors.push({path:'.',code:error instanceof Error && error.message==='symlink_not_allowed'?'symlink_not_allowed':'artifact_observation_failed'});}
 if(!Object.keys(files).length && !errors.length)return undefined;
 const observation={schema:'photocraft-late-artifacts/v1',taskId:task.id,taskIdentity:task.identity,workerToken:task.worker?.token??null,output,status:errors.length?'INCOMPLETE':'OBSERVED_UNVERIFIED',files,errors};
 return {...observation,sha256:digest(canonical(observation)),observedAt:Date.now()};
}
