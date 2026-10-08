import { DatabaseSync } from 'node:sqlite';
import { randomUUID } from 'node:crypto';
import { chmodSync, existsSync, mkdirSync, statfsSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { canonical, digest, fileDigest, safePath, within } from '../protocol/files.ts';
import { strictJson } from '../protocol/strict_json.ts';

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

  constructor(root: string, options: { readOnly?: boolean } = {}) {
    this.root = safePath(root);
    const file = join(this.root, 'tasks.sqlite');
    if (options.readOnly && !existsSync(file)) throw new Error('ledger_missing');
    if (!options.readOnly) mkdirSync(this.root, { recursive: true, mode: 0o700 });
    safePath(file);
    const existed=existsSync(file);
    try {
      this.db = new DatabaseSync(file, { readOnly: !!options.readOnly });
      if(existed && !this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata'").get())throw new Error('unsupported_ledger_schema');
      if (existed && this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata'").get() && (this.db.prepare('SELECT version FROM metadata').get() as any)?.version !== 1)throw new Error('unsupported_ledger_schema');
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
      this.db?.close(); throw new Error('ledger_invalid: ' + String(error));
    }
  }

  close() { this.db.close(); }

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
    return task;
  }

  save(task: any, event: string) {
    task.updatedAt = Date.now();
    this.db.prepare('UPDATE tasks SET data=? WHERE id=?').run(canonical(task), task.id);
    this.db.prepare('INSERT INTO events(task,data) VALUES(?,?)').run(task.id, canonical({ event, epoch: task.epoch, state: task.state, at: task.updatedAt }));
  }

  create(request: any): any {
    const allowed = new Set(['idempotencyKey', 'brief', 'plan', 'output', 'authorization', 'budget', 'source', 'mutableProject', 'expectedProjectSha256', 'parentTask', 'references']);
    if (!request || typeof request !== 'object' || Array.isArray(request) || Object.keys(request).some(key => !allowed.has(key))) throw new Error('invalid_task_request');
    if (typeof request.idempotencyKey !== 'string' || !request.idempotencyKey || typeof request.brief !== 'string' || !request.brief.trim()) throw new Error('task_identity_required');
    if (!request.plan || !Array.isArray(request.plan.operations)) throw new Error('plan_required');
    if (!request.authorization || Object.keys(request.authorization).some(key=>!['ref','writeRoot','objects'].includes(key)) || typeof request.authorization.ref !== 'string' || !request.authorization.ref) throw new Error('authorization_required');
    within(request.output, request.authorization.writeRoot);
    if(request.authorization.objects && (!Array.isArray(request.authorization.objects) || request.authorization.objects.some((id:any)=>!Number.isSafeInteger(id) || id<=0)))throw new Error('invalid_authorization_objects');
    if (request.source) safePath(request.source);
    if (request.mutableProject) {
      safePath(request.mutableProject);
      if (!/^[a-f0-9]{64}$/.test(request.expectedProjectSha256 ?? '')) throw new Error('project_revision_required');
    }
    if(request.references && (!Array.isArray(request.references) || request.references.some((ref:any)=>!ref || Object.keys(ref).some(key=>!['path','sha256'].includes(key)) || !/^[a-f0-9]{64}$/.test(ref.sha256??'') || fileDigest(ref.path)!==ref.sha256)))throw new Error('reference_identity_mismatch');
    const budget = request.budget;
    if (!budget || Object.keys(budget).some(key=>!['deadline','maxRevisions','reserveBytes','maxConcurrent'].includes(key)) || ('maxConcurrent' in budget && (!Number.isSafeInteger(budget.maxConcurrent) || budget.maxConcurrent<1)) || !Number.isSafeInteger(budget.deadline) || !Number.isSafeInteger(budget.maxRevisions) || budget.maxRevisions < 0
        || !Number.isSafeInteger(budget.reserveBytes) || budget.reserveBytes < 0) throw new Error('invalid_budget');
    const normalized = strictJson(canonical(request)); const identity = digest(canonical(normalized));
    return this.transaction(() => {
      const existing = this.db.prepare('SELECT id,identity FROM tasks WHERE key=?').get(request.idempotencyKey) as any;
      if (existing) {
        if (existing.identity !== identity) throw new Error('idempotency_conflict');
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

  claim(id: string): number {
    return this.transaction(() => {
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
