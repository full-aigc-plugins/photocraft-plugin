import {spawnSync} from 'node:child_process';
import {checkpointSnapshot} from './checkpoint.ts';
import {copyFileSync,cpSync,existsSync,lstatSync,mkdirSync,mkdtempSync,readdirSync,renameSync,rmSync,writeFileSync} from 'node:fs';
import {join,dirname} from 'node:path';
import {homedir} from 'node:os';
import {canonical,digest,fileDigest,readJson,safePath,within} from '../protocol/files.ts';
import {Ledger} from './ledger.ts';
import {runtimeBinding} from './runtime_binding.ts';
import {confirmedWorkerReceipt} from './worker_receipt.ts';
import {readLedgerSnapshot} from './ledger_snapshot.ts';
import {skillIdentity,pythonReply,runtimePlatformKey} from './preflight.ts';
import type {AdapterOptions} from './preflight.ts';

type Backend='headless'|'bridge';
type Probe=(options:AdapterOptions,backend:Backend,root:string)=>any;

/** 仅用已发布入口执行只读目录发现；禁止把目录清单当成启动或跨后端验证。 */
export function probeRuntime(options:AdapterOptions,backend:Backend,root:string) {
 const plan=join(root,'probe-plan.json'),output=join(root,'probe');writeFileSync(plan,canonical({schema:'craft-command-plan/v1',operations:[{tool:'command_list',params:{}}]}),{flag:'wx',mode:0o600});
 const reply=pythonReply(options,backend==='headless'?'commands.py':'desktop.py',['run',plan,'--output',output,'--runtime-home',options.runtimeHome!]);
 const lock=readJson(join(options.skillRoot,'scripts/runtime.lock.json')),expected=lock.artifacts?.[runtimePlatformKey()],snapshot=reply?.capabilitySnapshot;
 if(reply?.result!=='PASS' || reply?.steps?.length!==1 || reply.steps[0].tool!=='command_list' || reply.steps[0].state!=='succeeded' || canonical(reply.steps[0].params)!=='{}' || !snapshot || snapshot.backend!==backend || snapshot.binarySha256!==expected?.binarySha256
  || snapshot.runtimeIdentity?.version!==lock.resolvedVersion || snapshot.runtimeIdentity?.platform!==runtimePlatformKey()
  || !/^[a-f0-9]{64}$/.test(snapshot.commandsSha256) || !/^[a-f0-9]{64}$/.test(snapshot.toolsSha256) || snapshot.commandCount<1 || snapshot.toolCount<1)throw new Error('runtime_probe_unproven');
 const executable=join(options.runtimeHome!,'photocraft',lock.resolvedVersion,'photocraft-cli');
 if(fileDigest(executable)!==expected.binarySha256)throw new Error('runtime_binary_changed');
 const version=spawnSync(executable,['--version'],{encoding:'utf8',timeout:20000,maxBuffer:65536});
 if(version.error || version.status!==0 || version.stdout.trim()!==(expected.versionOutput??'photocraft-cli '+lock.resolvedVersion) || fileDigest(executable)!==expected.binarySha256)throw new Error('runtime_version_mismatch');
 if(backend==='bridge') {const lifecycle=readJson(join(output,'desktop-session.json'));if(lifecycle.result!=='PASS' || !lifecycle.ownedProcessesStopped || !lifecycle.listenerOwnedByPID)throw new Error('runtime_probe_unproven');}
 return {schema:'photocraft-runtime-probe/v1',backend,runtimeVersion:lock.resolvedVersion,runtimeSha256:expected.binarySha256,versionOutput:version.stdout.trim(),snapshot,snapshotSha256:digest(canonical(snapshot)),editingCalls:0};
}

/** 单账本显式升级与回退；排空、备份、探测和发布共用认领事务的写锁。 */
export class RuntimeManager {
 ledger:Ledger;options:AdapterOptions;probe:Probe;
 constructor(ledger:Ledger,options:AdapterOptions,probe:Probe=probeRuntime){this.ledger=ledger;this.options={...options,runtimeHome:safePath(options.runtimeHome??join(homedir(),'.local/share/craft-runtimes'))};this.probe=probe;}
 status(){return runtimeBinding(this.ledger)??{schema:'photocraft-runtime-selection/v1',generation:0,managed:false};}
 private drained() {
  const rows=this.ledger.db.prepare('SELECT id FROM tasks').all() as any[];
  for(const row of rows){const task=this.ledger.status(row.id);if(!['completed','failed','cancelled'].includes(task.state))throw new Error('runtime_tasks_not_drained');
   if(task.worker && (!task.worker.supervisor || !confirmedWorkerReceipt(this.ledger.root,task)))throw new Error('runtime_workers_not_drained');}
  if(this.ledger.db.prepare('SELECT name FROM resources LIMIT 1').get())throw new Error('runtime_resources_not_drained');
 }
 private retain(root:string,sha:string) {
  root=safePath(root);if(skillIdentity({...this.options,skillRoot:root}).sha256!==sha)throw new Error('runtime_source_changed');
  const parent=join(this.ledger.root,'runtime-combinations');mkdirSync(parent,{recursive:true,mode:0o700});const target=join(parent,sha);
  if(!existsSync(target)) {
   const temporary=mkdtempSync(join(parent,'.retain-'));
   try{cpSync(root,join(temporary,'skill'),{recursive:true,filter:path=>{if(path.split('/').includes('__pycache__'))return false;if(lstatSync(path).isSymbolicLink())throw new Error('runtime_source_unsafe');return true;}});
    if(skillIdentity({...this.options,skillRoot:join(temporary,'skill')}).sha256!==sha || skillIdentity({...this.options,skillRoot:root}).sha256!==sha)throw new Error('runtime_source_changed');renameSync(join(temporary,'skill'),target);
   }finally{rmSync(temporary,{recursive:true,force:true});}
  }
  if(skillIdentity({...this.options,skillRoot:target}).sha256!==sha)throw new Error('runtime_retained_source_changed');return target;
 }
 private retainedProjects() {
  const projects=new Set<string>();const add=(path:string)=>{path=safePath(path);if(existsSync(path))projects.add(path);};
  for(const row of this.ledger.db.prepare('SELECT id FROM tasks').all() as any[]) {
   const task=this.ledger.status(row.id);add(join(task.request.output,'project.pcraft'));
   if(task.request.source)add(join(task.request.source,'project.pcraft'));
   const checkpoints=[task.checkpoint?.output,task.request.checkpoint?.output,...(existsSync(join(task.request.output,'failure.json'))?[task.request.output]:[])].filter(Boolean);
   for(const output of new Set<string>(checkpoints)) {const snapshot=checkpointSnapshot(output,task.request.authorization.writeRoot);add(join(snapshot.stage,'project.pcraft'));}
   const progressPath=join(dirname(task.request.output),'.photocraft-progress-'+digest(task.request.output)+'.json');
   if(!existsSync(progressPath))continue;const progress=readJson(progressPath),binding=progress?.context?.taskBinding;
   if(progress?.schema!=='photocraft-progress/v1' || typeof progress.stage!=='string' || progress.targetHash!==digest(task.request.output) || canonical(binding)!==canonical({taskId:task.id,taskIdentity:task.identity,epoch:task.epoch,workerToken:task.worker?.token,sourceSha256:task.executionIdentity?.sha256}))throw new Error('runtime_retained_project_unproven');
   const stage=within(join(task.request.output,progress.stage),task.request.authorization.writeRoot);
   if(existsSync(stage)){const info=lstatSync(stage,{bigint:true});if(!info.isDirectory() || canonical(progress.stageIdentity)!==canonical([String(info.dev),String(info.ino)]))throw new Error('runtime_retained_project_unproven');add(join(stage,'project.pcraft'));}
  }
  return [...projects];
 }
 private checkedProbe(options:AdapterOptions,backend:Backend,root:string) {
  const proof=this.probe(options,backend,root),lock=readJson(join(options.skillRoot,'scripts/runtime.lock.json'));
  if(proof?.schema!=='photocraft-runtime-probe/v1' || proof.backend!==backend || proof.runtimeVersion!==lock.resolvedVersion || proof.runtimeSha256!==lock.artifacts?.[runtimePlatformKey()]?.binarySha256 || proof.editingCalls!==0 || proof.snapshotSha256!==digest(canonical(proof.snapshot)))throw new Error('runtime_probe_unproven');
  return proof;
 }
 private backup(root:string) {
  const snapshot=readLedgerSnapshot(this.ledger.root);const target=join(root,'state-backup');mkdirSync(target,{mode:0o700});const files:Record<string,string>={};
  try{for(const name of readdirSync(snapshot.root)){copyFileSync(join(snapshot.root,name),join(target,name));files[name]=fileDigest(join(target,name));}}finally{rmSync(snapshot.root,{recursive:true,force:true});}
  writeFileSync(join(target,'backup.json'),canonical({schema:'photocraft-runtime-state-backup/v1',stateSchema:1,files}),{flag:'wx',mode:0o600});return {path:target,files};
 }
 upgrade(proposal:any){return this.switch(proposal,false);}
 rollback(proposal:any){return this.switch(proposal,true);}
 private switch(proposal:any,rollback:boolean) {
  const allowed=['authorizationRef','expectedGeneration','expectedActiveSourceSha256','stateSchema',...(rollback?[]:['candidateSkillRoot','candidateSourceSha256','backend'])];
  if(!proposal || typeof proposal!=='object' || Array.isArray(proposal) || Object.keys(proposal).some(key=>!allowed.includes(key)) || typeof proposal.authorizationRef!=='string' || !proposal.authorizationRef.trim()
   || !Number.isSafeInteger(proposal.expectedGeneration) || proposal.expectedGeneration<0 || !/^[a-f0-9]{64}$/.test(proposal.expectedActiveSourceSha256))throw new Error('runtime_transition_invalid');
  if(proposal.stateSchema!==1)throw new Error('runtime_state_schema_incompatible');
  return this.ledger.transaction(()=>{
   const current=runtimeBinding(this.ledger),generation=current?.generation??0;
   const baselineIdentity=skillIdentity(this.options),baseline=current?.active??{skillRoot:this.options.skillRoot,sourceSha256:baselineIdentity.sha256,runtimeLockSha256:baselineIdentity.runtimeLockSha256,runtimeVersion:readJson(join(this.options.skillRoot,'scripts/runtime.lock.json')).resolvedVersion,runtimeHome:this.options.runtimeHome,backend:'headless',stateSchema:1};
   if(generation!==proposal.expectedGeneration || baseline.sourceSha256!==proposal.expectedActiveSourceSha256)throw new Error('runtime_generation_conflict');
   if((this.ledger.db.prepare('SELECT version FROM metadata').get() as any)?.version!==1)throw new Error('runtime_state_schema_incompatible');
   this.drained();
   const previous=current?.previous??[];const candidate=rollback?previous.at(-1):{skillRoot:proposal.candidateSkillRoot,sourceSha256:proposal.candidateSourceSha256,backend:proposal.backend,stateSchema:proposal.stateSchema,runtimeHome:this.options.runtimeHome};
   if(!candidate)throw new Error('runtime_rollback_unavailable');
   if(candidate.stateSchema!==1 || !['headless','bridge'].includes(candidate.backend) || !/^[a-f0-9]{64}$/.test(candidate.sourceSha256))throw new Error('runtime_transition_invalid');
   const retained=this.retain(candidate.skillRoot,candidate.sourceSha256),oldRoot=this.retain(baseline.skillRoot,baseline.sourceSha256);const old={...baseline,skillRoot:oldRoot};
   const parent=join(this.ledger.root,'runtime-transitions');mkdirSync(parent,{recursive:true,mode:0o700});const root=mkdtempSync(join(parent,'transition-'));const backup=this.backup(root);
   const options={...this.options,skillRoot:retained,runtimeHome:candidate.runtimeHome};const identity=skillIdentity(options);
   const oldProbeRoot=join(root,'previous-probe');mkdirSync(oldProbeRoot,{mode:0o700});
   const previousProbe=this.checkedProbe({...this.options,skillRoot:oldRoot,runtimeHome:old.runtimeHome},old.backend,oldProbeRoot);
   const probe=this.checkedProbe(options,candidate.backend,root);const lock=readJson(join(retained,'scripts/runtime.lock.json'));
   const projects:Record<string,string>={};
   for(const project of this.retainedProjects()) {
    const before=fileDigest(project);const info=pythonReply(options,'cli.py',['--runtime-home',options.runtimeHome!,'--','info',safePath(project)]);
    if(!Array.isArray(info?.layers) || fileDigest(project)!==before)throw new Error('runtime_project_schema_incompatible');projects[project]=before;
   }
   if(skillIdentity(options).sha256!==candidate.sourceSha256 || skillIdentity({...this.options,skillRoot:oldRoot}).sha256!==old.sourceSha256)throw new Error('runtime_source_changed');
   for(const entry of [{skillRoot:oldRoot,runtimeHome:old.runtimeHome},{skillRoot:retained,runtimeHome:options.runtimeHome}]) {
    const currentLock=readJson(join(entry.skillRoot,'scripts/runtime.lock.json'));
    if(fileDigest(join(entry.runtimeHome!,'photocraft',currentLock.resolvedVersion,'photocraft-cli'))!==currentLock.artifacts?.[runtimePlatformKey()]?.binarySha256)throw new Error('runtime_binary_changed');
   }
   for(const [project,sha]of Object.entries(projects))if(fileDigest(project)!==sha)throw new Error('runtime_project_changed');
   const active={skillRoot:retained,sourceSha256:identity.sha256,runtimeLockSha256:identity.runtimeLockSha256,runtimeVersion:lock.resolvedVersion,runtimeHome:options.runtimeHome,backend:candidate.backend,stateSchema:1,probe};
   const event={generation:generation+1,kind:rollback?'rollback':'upgrade',at:Date.now(),authorizationRef:proposal.authorizationRef,fromSourceSha256:old.sourceSha256,toSourceSha256:identity.sha256,backup,projects,previousProbe};
   const next={schema:'photocraft-runtime-selection/v1',generation:generation+1,active,previous:rollback?previous.slice(0,-1):[...previous,old],history:[...(current?.history??[]),event]};
   this.ledger.db.exec('CREATE TABLE IF NOT EXISTS runtime_selection(singleton INTEGER PRIMARY KEY CHECK(singleton=1),data TEXT NOT NULL)');this.ledger.db.prepare('INSERT OR REPLACE INTO runtime_selection VALUES(1,?)').run(canonical(next));
   writeFileSync(join(root,'transition.json'),canonical({schema:'photocraft-runtime-transition/v1',...event,probe}),{flag:'wx',mode:0o600});return next;
  });
 }
}
