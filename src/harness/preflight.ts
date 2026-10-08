import { spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { canonical, safePath, fileDigest, digest } from '../protocol/files.ts';
import { strictJson } from '../protocol/strict_json.ts';
import { OperationError, validationError } from '../protocol/operation_error.ts';

export type AdapterOptions = {skillRoot:string;python:string;runtimeHome?:string};

/** 指纹绑定参与当前合同的执行器与资源，忽略缓存和展示文档。 */
export function skillIdentity(options:AdapterOptions) {
 const root=safePath(options.skillRoot);const files:Record<string,string>={};
 for(const folder of ['scripts','references'])for(const name of readdirSync(join(root,folder)).sort()) {
  if(name.endsWith('.py') || name.endsWith('.json'))files[folder+'/'+name]=fileDigest(join(root,folder,name));
 }
 return {sha256:digest(canonical(files)),runtimeLockSha256:files['scripts/runtime.lock.json'],files};
}

/** Node 架构名映射到固定运行时使用的 Python 平台键；不声明新平台支持。 */
export function runtimePlatformKey():string {
 return (process.platform==='win32'?'windows':process.platform)+'-'+(process.arch==='x64'?(process.platform==='win32'?'amd64':'x86_64'):process.arch);
}

/** 只消费回复中的稳定恢复字段；未执行必须由执行前验证阶段证明。 */
export function reportedError(reply:any):OperationError|undefined {
 if(reply && typeof reply==='object' && !Array.isArray(reply)
    && typeof reply.error==='string' && typeof reply.code==='string' && /^[a-z][a-z0-9_]*$/.test(reply.code)
    && ['validation','submitted','reply_received','execution','verification'].includes(reply.phase)
    && ['not_executed','failed','unknown'].includes(reply.outcome) && reply.retryable===false
    && ['correct_plan','inspect','reconcile'].includes(reply.recoveryAction)
    && (reply.outcome!=='not_executed' || reply.phase==='validation' && reply.category==='validation_failed' && typeof reply.fieldPath==='string' && reply.fieldPath.startsWith('$'))) {
  return new OperationError(reply.error.slice(0,2048),{code:reply.code,phase:reply.phase,outcome:reply.outcome,recoveryAction:reply.recoveryAction,
   category:typeof reply.category==='string'?reply.category:undefined,fieldPath:typeof reply.fieldPath==='string' && reply.fieldPath.startsWith('$')?reply.fieldPath:undefined});
 }
 return undefined;
}

/** 解析子进程的单个严格 JSON 回复；畸形回复不能宣称原操作未执行。 */
export function pythonReply(options:AdapterOptions,script:string,args:string[]):any {
 const result=spawnSync(options.python,['-I','-B',join(safePath(options.skillRoot),'scripts',script),...args],{encoding:'utf8',timeout:120_000,maxBuffer:2*1024*1024,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
 let reply:any;
 try {reply=strictJson(result.stdout??'');}
 catch {
  throw new OperationError('adapter_reply_invalid',{code:'adapter_reply_invalid',phase:'reply_received',outcome:'unknown',recoveryAction:'reconcile'});
 }
 if(result.error || result.status!==0) {
  // 仅传播已核验的稳定字段，不从本地化错误文字推断恢复动作。
  const failure=reportedError(reply);if(!result.error && failure)throw failure;
  if(!result.error && ['delivery.py','native_verify.py','checkpoint_verify.py'].includes(script) && reply?.result==='FAIL' && typeof reply.error==='string')
   throw new OperationError(reply.error.slice(0,2048),{code:'technical_verification_failed',phase:'verification',outcome:'failed',recoveryAction:'inspect'});
  throw new OperationError('adapter_failed',{code:'adapter_failed',phase:'submitted',outcome:'unknown',recoveryAction:'reconcile'});
 }
 return reply;
}

/** 在私有临时目录复用唯一技能合同；拒绝时不建立账本、输出或恢复记录。 */
export function preflightRequest(request:any,options:AdapterOptions,execute:(script:string,args:string[])=>any=(script,args)=>pythonReply(options,script,args)):void {
 if(options.runtimeHome!==undefined) {
  try {safePath(options.runtimeHome);}catch{throw validationError('invalid_runtime_path','$.runtimeHome');}
 }
 const temporary=mkdtempSync(join(tmpdir(),'photocraft-plan-check-'));
 try {
  const path=join(temporary,'plan.json');writeFileSync(path,canonical(request.plan),{flag:'wx',mode:0o600});
  const args=[path,'--output',request.output,'--check'];if(request.source)args.push('--source',request.source);
  const reply=execute('workflow.py',args);
  if(!reply || typeof reply!=='object' || Array.isArray(reply) || reply.result!=='PASS'
     || Object.keys(reply).some(key=>!['result','scope','nativeExecution'].includes(key))
     || reply.scope!==undefined && typeof reply.scope!=='string'
     || reply.nativeExecution!==undefined && reply.nativeExecution!=='NOT_RUN') {
   throw new OperationError('preflight_reply_invalid',{code:'preflight_reply_invalid',phase:'validation',outcome:'not_executed',category:'validation_failed',fieldPath:'$.plan',recoveryAction:'inspect'});
  }
 } catch(error) {
  if(error instanceof OperationError) {
   if(error.phase==='validation' && error.outcome==='not_executed') {
    // 子进程输入是有效计划；公开任务输入中的计划位于 $.plan。
    if(error.code!=='preflight_reply_invalid' && error.fieldPath?.startsWith('$'))error.fieldPath='$.plan'+error.fieldPath.slice(1);
    throw error;
   }
   throw new OperationError(error.message,{code:'preflight_adapter_failed',phase:'validation',outcome:'not_executed',category:'validation_failed',fieldPath:'$.plan',recoveryAction:'inspect'});
  }
  throw error;
 } finally {rmSync(temporary,{recursive:true,force:true});}
}
