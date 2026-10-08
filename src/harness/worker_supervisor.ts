import { spawn } from 'node:child_process';
import { existsSync, renameSync, writeFileSync } from 'node:fs';
import { canonical, fileDigest, readJson, safePath } from '../protocol/files.ts';

/** 独立持有工作进程，主执行器断连后仍执行原截止时间和停止请求，并留下退出回执。 */
const launchPath=safePath(process.argv[2]);
if(fileDigest(launchPath)!==process.argv[3])throw new Error('worker_launch_changed');
const launch=readJson(launchPath);
const blocked=existsSync(safePath(launch.stopFile)) || Date.now()>=launch.deadline;
const child=blocked?undefined:spawn(launch.python,launch.args,{detached:process.platform!=='win32',stdio:['ignore','pipe','pipe'],env:{...process.env,PYTHONDONTWRITEBYTECODE:'1',CRAFT_STOP_FILE:launch.stopFile,PHOTOCRAFT_TASK_BINDING:JSON.stringify({taskId:launch.taskId,taskIdentity:launch.taskIdentity,epoch:launch.epoch,workerToken:launch.workerToken,sourceSha256:launch.sourceSha256})}});
let closed=blocked;let exitCode:number|null=blocked?1:null;let signal:string|null=null;let stoppedAt:number|null=blocked?Date.now():null;let spawnError='';let bytes=0;let output='';
process.stdout.on('error',()=>{});process.stderr.on('error',()=>{});
child?.stdout.setEncoding('utf8');child?.stdout.on('data',(data:string)=>{bytes+=Buffer.byteLength(data);if(bytes<=2*1024*1024)output+=data;});
child?.stderr.on('data',()=>{});
child?.on('error',error=>{spawnError=error.message;});
child?.once('close',(code,exitSignal)=>{closed=true;exitCode=code;signal=exitSignal;});
let termSent=false;let killSent=false;let signalRequested=false;process.on('SIGTERM',()=>{signalRequested=true;});process.on('SIGINT',()=>{signalRequested=true;});
const groupGone=()=>{
 if(!child?.pid)return closed;
 if(process.platform==='win32')return closed;
 try{process.kill(-child?.pid,0);return false;}catch(error){return (error as any).code==='ESRCH';}
};
const timer=setInterval(()=>{
 const stop=signalRequested || existsSync(safePath(launch.stopFile)) || Date.now()>=launch.deadline;
 if(stop){if(stoppedAt===null)stoppedAt=Date.now();if(!existsSync(launch.stopFile))try{writeFileSync(safePath(launch.stopFile),'supervised stop requested',{flag:'wx',mode:0o600});}catch(error){if((error as any).code!=='EEXIST')throw error;}}
 if(stop && !groupGone()) {
  // 唯一发信号者持有本次创建的 ChildProcess；重启核对只读取回执，绝不按旧 PID 终止进程。
  try{const force=Date.now()-stoppedAt!>=2000;if(force && !killSent || !force && !termSent){const next=force?'SIGKILL':'SIGTERM';if(process.platform!=='win32' && child?.pid)process.kill(-child?.pid,next);else child?.kill(next);if(force)killSent=true;else termSent=true;}}catch{}
 }
 if(!closed || !groupGone())return;
 clearInterval(timer);
 const receipt={schema:'photocraft-worker-exit/v1',taskId:launch.taskId,taskIdentity:launch.taskIdentity,epoch:launch.epoch,workerToken:launch.workerToken,sourceSha256:launch.sourceSha256,launchSha256:process.argv[3],supervisorPid:process.pid,workflowPid:child?.pid??null,processGroupGone:true,exitCode,signal,spawnError,stoppedAt,finishedAt:Date.now(),outputTruncated:bytes>2*1024*1024};
 const temporary=safePath(launch.receipt+'.tmp');writeFileSync(temporary,canonical(receipt),{flag:'wx',mode:0o600});renameSync(temporary,safePath(launch.receipt));
 if(!receipt.outputTruncated)process.stdout.write(output);
 process.exitCode=exitCode??1;
},50);
