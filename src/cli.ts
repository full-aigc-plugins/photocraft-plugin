#!/usr/bin/env node
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync } from 'node:fs';
import { Ledger } from './harness/ledger.ts';
import { Runner } from './harness/runner.ts';
import { mapArtifact } from './protocol/artifact.ts';
import { exportBundle,verifyBundle } from './protocol/bundle.ts';
import { Review } from './evaluation/review.ts';
import { readJson, safePath } from './protocol/files.ts';
import { preflightRequest, skillIdentity } from './harness/preflight.ts';
import { OperationError, validationError } from './protocol/operation_error.ts';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const actions=['create','run','status','reconcile','verify','judge','review-import','import-judge','revise','recover','stop','accept','artifact','bundle-export','bundle-check'];
let ledger:Ledger|undefined;
try {
 const [action,...args]=process.argv.slice(2);
 if(action==='--help') {
  console.log(JSON.stringify({actions,required:['--state-dir ABSOLUTE'],runtime:'Node 24, Python 3; native platform must be present in skill runtime lock',source:'--skill-root explicitly selects a candidate; default is immutable plugin skill snapshot'}));
 } else {
  if(!actions.includes(action))throw new Error('unknown_action');
  const options:Record<string,string>={};const allowed=new Set(['--state-dir','--task','--request','--receipt','--proposal','--review-id','--skill-root','--python','--runtime-home','--delivery','--bundle','--expected-sha256']);
  for(let i=0;i<args.length;i+=2) {
   if(!allowed.has(args[i]) || !args[i+1] || args[i+1].startsWith('--') || options[args[i]])throw new Error('invalid_cli_option');
   options[args[i]]=args[i+1];
  }
  if(action==='bundle-check') {console.log(JSON.stringify(verifyBundle(options['--bundle'],options['--expected-sha256'])));}
  else {
  if(!options['--state-dir'])throw new Error('state_directory_required');
  const input=action==='create'?readJson(options['--request']):['review-import','import-judge'].includes(action)?readJson(options['--receipt']):['revise','recover'].includes(action)?readJson(options['--proposal']):undefined;
  const state=safePath(options['--state-dir']);
  if(action!=='create' && !options['--task'])throw validationError('task_id_required','$.task');
  if(action!=='create' && !existsSync(join(state,'tasks.sqlite')))throw new Error('ledger_missing');
  const adapterOptions={skillRoot:options['--skill-root']??join(root,'skills/photocraft-use'),python:options['--python']??'python3',runtimeHome:options['--runtime-home']};
  let existing:any;
  if(action==='create') {
   try {Ledger.validateRequest(input);}
   catch(error){if(error instanceof OperationError)throw error;const message=error instanceof Error?error.message:String(error);throw validationError(message.split(':',1)[0],'$',message);}
   // 已有同身份任务不重新预检其已存在输出，也不打开可写账本。
   if(existsSync(join(state,'tasks.sqlite'))) {
    const prior=new Ledger(state,{readOnly:true});
    try{existing=prior.existing(input);}finally{prior.close();}
   }
   if(!existing) {
    if(input.parentTask)throw validationError('parent_task_requires_revision','$.parentTask');
    const identity=skillIdentity(adapterOptions);preflightRequest(input,adapterOptions);
    if(skillIdentity(adapterOptions).sha256!==identity.sha256)throw new OperationError('skill_source_changed',{code:'skill_source_changed',phase:'validation',outcome:'not_executed',category:'validation_failed',fieldPath:'$.skillRoot',recoveryAction:'inspect'});
    Ledger.validateRequest(input);
   }
  }
  if(existing) {console.log(JSON.stringify(existing));}
  else {
  const readOnly=['status','artifact','bundle-export'].includes(action);
  ledger=new Ledger(state,{readOnly});
  const runner=new Runner(ledger,adapterOptions);
  const id=options['--task'];if(action!=='create' && !id)throw new Error('task_id_required');
  let result:any;
  switch(action) {
   case 'create':result=ledger.create(input);break;
   case 'status':result=runner.status(id);break;
   case 'artifact':{const task=ledger.status(id);result=mapArtifact(task,task.request.parentTask?ledger.status(task.request.parentTask).artifact:undefined,options['--delivery']);break;}
   case 'bundle-export':{const task=ledger.status(id);result=exportBundle(task,options['--bundle'],task.request.parentTask?ledger.status(task.request.parentTask).artifact:undefined);break;}
   case 'run':result=await runner.run(id);break;
   case 'reconcile':result=await runner.reconcile(id);break;
   case 'verify':result=await runner.verify(id);break;
   case 'judge':result=new Review(ledger).request(id);break;
   case 'import-judge':
   case 'review-import':result=new Review(ledger).import(id,input);break;
   case 'accept':result=new Review(ledger).accept(id,options['--review-id']);break;
   case 'recover':result=await runner.recover(id,input);break;
   case 'revise':result=await runner.revise(id,input);break;
   case 'stop':result=ledger.stop(id);break;
  }
  console.log(JSON.stringify(result));
  }
  }
 }
} catch(error) {
 const message=error instanceof Error?error.message:String(error);const code=message.split(':',1)[0];
 const detail=error instanceof OperationError?{code:error.code,phase:error.phase,outcome:error.outcome,retryable:error.retryable,recoveryAction:error.recoveryAction,category:error.category,fieldPath:error.fieldPath}:{};
 console.log(JSON.stringify({result:'FAIL',code,error:message,retryable:false,recoveryAction:['reconcile_required','adapter_failed'].includes(code)?'reconcile':'inspect',...detail}));process.exitCode=1;
} finally {ledger?.close();}
