import {assertRuntimeBinding} from './runtime_binding.ts';
import { DatabaseSync } from 'node:sqlite';
import { randomUUID } from 'node:crypto';
import { chmodSync, existsSync, mkdirSync, statfsSync, writeFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { canonical, digest, fileDigest, safePath, within } from '../protocol/files.ts';
import { strictJson } from '../protocol/strict_json.ts';
import { OperationError, validationError } from '../protocol/operation_error.ts';
import { readLedgerSnapshot } from './ledger_snapshot.ts';

const transitions: Record<string, string[]> = {
  planned: ['running', 'cancelled'], running: ['verifying', 'reconciling', 'failed', 'cancel_requested'],
  reconciling: ['verifying', 'failed', 'cancel_requested', 'cancelled'], verifying: ['review_ready', 'reconciling', 'failed', 'cancel_requested'],
  review_ready: ['completed', 'cancel_requested'], cancel_requested: ['cancelled', 'reconciling'],
  completed: [], cancelled: [], failed: []
};

/** SQLite 管理任务身份、写入权和轮次；原生副作用通过核对收敛。 */
export class Ledger {
  db: DatabaseSync;
  root: string;
  private snapshotRoot?:string;

  constructor(root: string, options: { readOnly?: boolean } = {}) {
    this.root = safePath(root);
    const file = join(this.root, 'tasks.sqlite');
    if (options.readOnly && !existsSync(file)) throw new Error('ledger_missing');
    if (!options.readOnly) mkdirSync(this.root, { recursive: true, mode: 0o700 });
    safePath(file);
    const existed=existsSync(file);
    try {
      let databaseFile=file;
      if(options.readOnly) {const snapshot=readLedgerSnapshot(this.root);this.snapshotRoot=snapshot.root;databaseFile=snapshot.file;}
      this.db = new DatabaseSync(databaseFile, { readOnly: !!options.readOnly });
      if(existed && !this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata'").get())throw new Error('unsupported_ledger_schema');
      if (existed && this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata'").get() && (this.db.prepare('SELECT version FROM metadata').get() as any)?.version !== 1)throw new Error('unsupported_ledger_schema');
      if(existed) {
        const required:Record<string,string[]>={metadata:['version'],tasks:['id','key','identity','data'],resources:['name','owner','epoch'],events:['sequence','task','data']};
        for(const [table,columns] of Object.entries(required)) {
          const actual=(this.db.prepare('PRAGMA table_info('+table+')').all() as any[]).map(column=>column.name);
          if(columns.some(column=>!actual.includes(column)))throw new Error('ledger_schema_incomplete');
        }
      }
      if (!options.readOnly) {
        chmodSync(file, 0o600);
        this.db.exec(`PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; PRAGMA busy_timeout=5000;
          CREATE TABLE IF NOT EXISTS metadata(version INTEGER NOT NULL);
          CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY, key TEXT UNIQUE NOT NULL, identity TEXT NOT NULL, data TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS resources(name TEXT PRIMARY KEY, owner TEXT NOT NULL, epoch INTEGER NOT NULL);
          CREATE TABLE IF NOT EXISTS events(sequence INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, data TEXT NOT NULL);`);
        if (!this.db.prepare('SELECT version FROM metadata').get()) this.db.exec('INSERT INTO metadata VALUES(1)');
      }
      if ((this.db.prepare('SELECT version FROM metadata').get() as any)?.version !== 1) throw new Error('unsupported_ledger_schema');
    } catch (error) {
      this.db?.close();if(this.snapshotRoot)rmSync(this.snapshotRoot,{recursive:true,force:true});
      if(error instanceof OperationError)throw error;
      throw new Error('ledger_invalid: ' + String(error));
    }
  }

  close() {this.db.close();if(this.snapshotRoot)rmSync(this.snapshotRoot,{recursive:true,force:true});}

  transaction<T>(work: () => T): T {
    this.db.exec('BEGIN IMMEDIATE');
    try { const value = work(); this.db.exec('COMMIT'); return value; }
    catch (error) { this.db.exec('ROLLBACK'); throw error; }
  }

  status(id: string): any {
    const row = this.db.prepare('SELECT id,identity,data FROM tasks WHERE id=?').get(id) as any;
    if (!row) throw new Error('task_missing');
    const task = strictJson(row.data);
    if (task.schema !== 'photocraft-task/v1' || !Object.hasOwn(transitions,task.state) || !Number.isSafeInteger(task.epoch) || task.id!==row.id || task.identity!==row.identity || digest(canonical(task.request))!==row.identity) throw new Error('task_state_invalid');
    // 请求身份正确也不足以恢复写入权；尝试标记必须与持久意图事件一致。
    try {
      const events=(this.db.prepare('SELECT data FROM events WHERE task=? ORDER BY sequence').all(id) as any[]).map(value=>strictJson(value.data));
      const intents=events.filter(event=>event.event==='intent_persisted');
      if(typeof task.attempted!=='boolean' || task.epoch<0 || !events.some(event=>['created','revision_created'].includes(event.event) && event.epoch===0 && event.state==='planned'))throw new Error('task_intent_invalid');
      if(task.attempted) {
        if(task.epoch<1 || task.state==='planned' || !Number.isSafeInteger(task.startedAt) || task.startedAt<task.createdAt || intents.length!==1
          || intents[0].epoch!==task.epoch || intents[0].state!=='running' || intents[0].at<task.startedAt)throw new Error('task_intent_invalid');
      }else if(task.epoch!==0 || task.startedAt!==undefined || intents.length || !['planned','cancelled'].includes(task.state))throw new Error('task_intent_invalid');
    }catch{throw new Error('task_intent_invalid');}
    return task;
  }

  save(task: any, event: string) {
    task.updatedAt = Date.now();
    this.db.prepare('UPDATE tasks SET data=? WHERE id=?').run(canonical(task), task.id);
    this.db.prepare('INSERT INTO events(task,data) VALUES(?,?)').run(task.id, canonical({ event, epoch: task.epoch, state: task.state, at: task.updatedAt }));
  }

  /** 纯读取验证任务元数据，在建立数据库之前复用同一身份规则。 */
  static validateRequest(request: any): {normalized:any;identity:string} {
    const object=(value:any)=>value!==null && typeof value==='object' && !Array.isArray(value);
    const property=(base:string,key:string)=>/^[A-Za-z_][A-Za-z0-9_]*$/.test(key)?base+'.'+key:base+'['+JSON.stringify(key)+']';
    const keys=(value:any,allowed:string[],base:string,code:string)=>{
      const unknown=Object.keys(value).find(key=>!allowed.includes(key));
      if(unknown!==undefined)throw validationError(code,property(base,unknown));
    };
    const pathCheck=(action:()=>any,path:string)=>{
      try {action();} catch(error) {const message=error instanceof Error?error.message:String(error);throw validationError(message.split(':',1)[0],path,message);}
    };
    if(!object(request))throw validationError('invalid_task_request');
    keys(request,['idempotencyKey','brief','plan','output','authorization','budget','source','mutableProject','expectedProjectSha256','parentTask','references','checkpoint'],'$','invalid_task_request');
    if(typeof request.idempotencyKey!=='string' || !request.idempotencyKey)throw validationError('task_identity_required','$.idempotencyKey');
    if(typeof request.brief!=='string' || !request.brief.trim())throw validationError('task_identity_required','$.brief');
    if(!object(request.plan))throw validationError('plan_required','$.plan');
    if(!Array.isArray(request.plan.operations))throw validationError('plan_required','$.plan.operations');
    if(!object(request.authorization))throw validationError('authorization_required','$.authorization');
    keys(request.authorization,['ref','writeRoot','objects'],'$.authorization','authorization_required');
    if(typeof request.authorization.ref!=='string' || !request.authorization.ref)throw validationError('authorization_required','$.authorization.ref');
    pathCheck(()=>safePath(request.authorization.writeRoot),'$.authorization.writeRoot');
    pathCheck(()=>within(request.output,request.authorization.writeRoot),'$.output');
    if(Object.hasOwn(request.authorization,'objects')) {
      if(!Array.isArray(request.authorization.objects))throw validationError('invalid_authorization_objects','$.authorization.objects');
      request.authorization.objects.forEach((id:any,index:number)=>{if(!Number.isSafeInteger(id) || id<=0)throw validationError('invalid_authorization_objects','$.authorization.objects['+index+']');});
    }
    if(Object.hasOwn(request,'source'))pathCheck(()=>safePath(request.source),'$.source');
    if(Object.hasOwn(request,'checkpoint')) {
      const checkpoint=request.checkpoint;
      if(!request.parentTask)throw validationError('checkpoint_requires_revision','$.checkpoint');
      if(!object(checkpoint))throw validationError('invalid_checkpoint_source','$.checkpoint');
      keys(checkpoint,['output','recordSha256','planSha256','projectSha256'],'$.checkpoint','invalid_checkpoint_source');
      pathCheck(()=>within(checkpoint.output,request.authorization.writeRoot),'$.checkpoint.output');
      for(const field of ['recordSha256','planSha256','projectSha256'])if(typeof checkpoint[field]!=='string' || !/^[a-f0-9]{64}$/.test(checkpoint[field]))throw validationError('invalid_checkpoint_source','$.checkpoint.'+field);
      if(request.source)throw validationError('conflicting_source','$.source');
    }
    if(Object.hasOwn(request,'mutableProject')) {
      pathCheck(()=>safePath(request.mutableProject),'$.mutableProject');
      if(typeof request.expectedProjectSha256!=='string' || !/^[a-f0-9]{64}$/.test(request.expectedProjectSha256))throw validationError('project_revision_required','$.expectedProjectSha256');
    }
    if(Object.hasOwn(request,'references')) {
      if(!Array.isArray(request.references))throw validationError('reference_identity_mismatch','$.references');
      request.references.forEach((ref:any,index:number)=>{
        const path='$.references['+index+']';
        if(!object(ref))throw validationError('reference_identity_mismatch',path);
        keys(ref,['path','sha256'],path,'reference_identity_mismatch');
        if(typeof ref.sha256!=='string' || !/^[a-f0-9]{64}$/.test(ref.sha256))throw validationError('reference_identity_mismatch',path+'.sha256');
        pathCheck(()=>{if(fileDigest(ref.path)!==ref.sha256)throw new Error('reference_identity_mismatch');},path+'.path');
      });
    }
    const budget=request.budget;
    if(!object(budget))throw validationError('invalid_budget','$.budget');
    keys(budget,['deadline','maxRevisions','reserveBytes','maxConcurrent'],'$.budget','invalid_budget');
    for(const key of ['deadline','maxRevisions','reserveBytes','maxConcurrent']) {
      if(key==='maxConcurrent' && !Object.hasOwn(budget,key))continue;
      if(!Number.isSafeInteger(budget[key]) || key!=='deadline' && budget[key]<(key==='maxConcurrent'?1:0))throw validationError('invalid_budget','$.budget.'+key);
    }
    const normalized = strictJson(canonical(request)); const identity = digest(canonical(normalized));
    return {normalized,identity};
  }

  /** 查询同键任务；同输入只读返回，冲突绝不成为新的执行。 */
  existing(request:any):any|undefined {
    const {identity}=Ledger.validateRequest(request);
    const row=this.db.prepare('SELECT id,identity FROM tasks WHERE key=?').get(request.idempotencyKey) as any;
    if(!row)return undefined;
    if(row.identity!==identity)throw validationError('idempotency_conflict','$.idempotencyKey');
    return this.status(row.id);
  }

  create(request: any): any {
    const {normalized,identity}=Ledger.validateRequest(request);
    return this.transaction(() => {
      const existing = this.db.prepare('SELECT id,identity FROM tasks WHERE key=?').get(request.idempotencyKey) as any;
      if (existing) {
        if (existing.identity !== identity) throw validationError('idempotency_conflict','$.idempotencyKey');
        return this.status(existing.id);
      }
      if(request.parentTask)throw new Error('parent_task_requires_revision');
      const task = { schema: 'photocraft-task/v1', id: randomUUID(), identity, request: normalized,
        state: 'planned', epoch: 0, createdAt: Date.now(), revisions: 0, attempted: false,
        technical: { status: 'NOT_RUN' }, creative: { status: 'NOT_RUN' }, acceptance: { status: 'NOT_RUN' } };
      this.db.prepare('INSERT INTO tasks VALUES(?,?,?,?)').run(task.id, request.idempotencyKey, identity, canonical(task));
      this.save(task, 'created'); return task;
    });
  }

  claim(id: string, sourceSha256?:string): number {
    return this.transaction(() => {
      assertRuntimeBinding(this,sourceSha256);
      const task = this.status(id);
      if (task.state !== 'planned' || task.attempted) throw new Error('reconcile_required');
      for(const ref of task.request.references??[])if(fileDigest(ref.path)!==ref.sha256)throw new Error('reference_identity_mismatch');
      const budget = task.request.budget;
      const lineage=this.lineage(task);
      if(lineage.some(parent=>['cancel_requested','cancelled','failed'].includes(parent.state) || parent.stopRequestedAt))throw new Error('parent_task_stopped');
      if(lineage.some(parent=>budget.deadline>parent.request.budget.deadline))throw new Error('parent_budget_conflict');
      if (Date.now() >= budget.deadline) throw new Error('budget_exhausted');
      const active=this.db.prepare('SELECT DISTINCT tasks.data FROM tasks JOIN resources ON resources.owner=tasks.id').all().map((row:any)=>strictJson(row.data));
      const processReservations=active.filter(entry=>!entry.worker?.exited || !entry.worker.processGroupGone);
      if(processReservations.length>=(budget.maxConcurrent??4))throw new Error('concurrency_budget_exhausted');
      const reserved=active.reduce((sum:number,entry:any)=>sum+entry.request.budget.reserveBytes,0);
      const disk = statfsSync(task.request.authorization.writeRoot);
      if (disk.bavail * disk.bsize - reserved < budget.reserveBytes) throw new Error('disk_budget_exhausted');
      const resources = ['output:' + safePath(task.request.output)];
      if (task.request.mutableProject) resources.push('project:' + safePath(task.request.mutableProject));
      for (const resource of resources) {
        const owner = this.db.prepare('SELECT owner FROM resources WHERE name=?').get(resource) as any;
        if (owner && owner.owner !== id) throw new Error('project_busy');
      }
      if (task.request.mutableProject && fileDigest(task.request.mutableProject) !== task.request.expectedProjectSha256) throw new Error('revision_conflict');
      task.epoch++; task.state = 'running'; task.attempted = true; task.startedAt=Date.now();
      for (const resource of resources) this.db.prepare('INSERT OR REPLACE INTO resources VALUES(?,?,?)').run(resource, id, task.epoch);
      this.save(task, 'intent_persisted'); return task.epoch;
    });
  }

  update(id: string, epoch: number, action: (task: any) => void): any {
    return this.transaction(() => {
      const task = this.status(id); if (task.epoch !== epoch) throw new Error('stale_epoch');
      action(task); this.save(task, 'updated'); return task;
    });
  }

  /** 返回祖先任务；拒绝损坏循环，不按缺失父记录推测血缘。 */
  lineage(task:any):any[] {
    const result:any[]=[];const seen=new Set([task.id]);let current=task;
    while(current.request.parentTask) {
      if(seen.has(current.request.parentTask))throw new Error('parent_lineage_cycle');
      seen.add(current.request.parentTask);current=this.status(current.request.parentTask);result.push(current);
    }
    return result;
  }

  revisionRoot(task:any):any {return this.lineage(task).at(-1)??task;}

  transition(id: string, epoch: number, next: string): any {
    return this.update(id, epoch, task => {
      if (!transitions[task.state].includes(next)) throw new Error('invalid_transition: ' + task.state + ' -> ' + next);
      if (next === 'completed' && (task.technical.status !== 'PASS' || task.creative.status !== 'PASS' || task.acceptance.status !== 'PASS')) throw new Error('acceptance_required');
      if(next==='cancelled' && task.attempted && !task.stopEvidence?.processGroupGone)throw new Error('stop_confirmation_required');
      if(next==='cancelled' && (this.db.prepare('SELECT data FROM tasks').all() as any[]).some(row=>{const child=strictJson(row.data);return child.request.parentTask===id && !['cancelled','failed','completed'].includes(child.state);}))throw new Error('child_stop_confirmation_required');
      task.state = next;
      if(['verifying','cancelled','failed'].includes(next) && task.startedAt)task.elapsedMs=Date.now()-task.startedAt;
      if (['completed', 'failed', 'cancelled', 'review_ready'].includes(next)) this.db.prepare('DELETE FROM resources WHERE owner=?').run(id);
    });
  }

  recordTechnical(id: string, epoch: number, evidence: any, artifact?: any): any {
    return this.update(id, epoch, task => {
      if (task.state !== 'verifying' || evidence.status !== 'PASS'
          || !['projectSha256', 'previewSha256', 'manifestSha256'].every(key => /^[a-f0-9]{64}$/.test(evidence[key] ?? ''))) throw new Error('invalid_technical_evidence');
      if(artifact)task.artifact=artifact;
      task.technical = evidence; task.creative = { status: 'NOT_RUN' }; task.acceptance = { status: 'NOT_RUN' };
      delete task.reconcileError;delete task.verificationError;task.recoveryAction='request_independent_review';
    });
  }

  stop(id: string): any {
    const task = this.status(id);
    if (['cancelled', 'cancel_requested', 'completed', 'failed'].includes(task.state)) return task;
    for(const row of this.db.prepare('SELECT id,data FROM tasks').all() as any[]) {const child=strictJson(row.data);if(child.request.parentTask===id)this.stop(child.id);}
    const stopPath=safePath(join(this.root,id+'.stop'));
    if(!existsSync(stopPath))writeFileSync(stopPath,'stop requested',{flag:'wx',mode:0o600});
    this.update(id,task.epoch,current=>{current.stopRequestedAt=Date.now();});
    return this.transition(id, task.epoch, task.state === 'planned' ? 'cancelled' : 'cancel_requested');
  }
}
