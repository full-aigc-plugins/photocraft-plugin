import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync, realpathSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

function fixture() {
  const root = realpathSync(mkdtempSync(join(tmpdir(), 'photocraft-ledger-test-')));
  const request = { idempotencyKey: 'poster-1', brief: 'Make an editable poster',
    plan: { document: { width: 32, height: 32 }, operations: [] },
    output: join(root, 'poster'), authorization: { ref: 'user-request', writeRoot: root },
    budget: { deadline: Date.now() + 60_000, maxRevisions: 2, reserveBytes: 1024 } };
  return { root, request, cleanup: () => rmSync(root, { recursive: true, force: true }) };
}

test('task survives reopening and a key cannot be reused for a different plan', async () => {
  const { Ledger } = await import('../src/harness/ledger.ts');
  const f = fixture();
  try {
    let ledger = new Ledger(join(f.root, 'state'));
    const first = ledger.create(f.request);
    ledger.close();
    ledger = new Ledger(join(f.root, 'state'));
    assert.equal(ledger.create(f.request).id, first.id);
    assert.throws(() => ledger.create({ ...f.request, brief: 'Different brief' }), /idempotency_conflict/);
    assert.equal(ledger.status(first.id).state, 'planned');
    ledger.close();
  } finally { f.cleanup(); }
});

test('shared writable project has one owner and old epochs cannot commit', async () => {
  const { Ledger } = await import('../src/harness/ledger.ts');
  const f = fixture();
  try {
    const ledger = new Ledger(join(f.root, 'state'));
    const resource = join(f.root, 'mutable.pcraft'); writeFileSync(resource, 'native');
    const first = ledger.create({ ...f.request, mutableProject: resource, expectedProjectSha256: createHash('sha256').update('native').digest('hex') });
    const second = ledger.create({ ...f.request, idempotencyKey: 'poster-2', output: join(f.root, 'other'), mutableProject: resource, expectedProjectSha256: createHash('sha256').update('native').digest('hex') });
    const epoch = ledger.claim(first.id);
    assert.throws(() => ledger.claim(second.id), /project_busy/);
    ledger.transition(first.id, epoch, 'reconciling');
    assert.throws(() => ledger.claim(first.id), /reconcile_required/);
    assert.throws(() => ledger.transition(first.id, epoch - 1, 'verifying'), /stale_epoch/);
    assert.equal(ledger.status(first.id).state, 'reconciling');
    ledger.close();
  } finally { f.cleanup(); }
});

test('independent processes race for the same project and only one intent commits',{timeout:10000},async()=>{
 const {Ledger}=await import('../src/harness/ledger.ts');const {spawn}=await import('node:child_process');const f=fixture();
 try{
  const state=join(f.root,'state');const ledger=new Ledger(state);const project=join(f.root,'shared.pcraft');writeFileSync(project,'native');
  const tasks=[1,2].map(index=>ledger.create({...f.request,idempotencyKey:'race-'+index,output:join(f.root,'race-'+index),mutableProject:project,expectedProjectSha256:createHash('sha256').update('native').digest('hex')}));
  const script=join(f.root,'race.mjs');writeFileSync(script,`import {Ledger} from ${JSON.stringify(new URL('../src/harness/ledger.ts',import.meta.url).href)};const ledger=new Ledger(process.argv[2]);process.send('ready');process.once('message',()=>{try{ledger.claim(process.argv[3]);console.log(JSON.stringify({claimed:true}));}catch(error){console.log(JSON.stringify({claimed:false,error:error.message}));}finally{ledger.close();process.disconnect();}});`);
  const workers=tasks.map(task=>spawn(process.execPath,[script,state,task.id],{stdio:['ignore','pipe','pipe','ipc']}));
  const results=workers.map(worker=>new Promise<any>((resolve,reject)=>{let output='';worker.stdout!.on('data',data=>output+=data);worker.on('error',reject);worker.on('close',code=>{try{assert.equal(code,0);resolve(JSON.parse(output));}catch(error){reject(error);}});}));
  await Promise.all(workers.map(worker=>new Promise(resolve=>worker.once('message',resolve))));workers.forEach(worker=>worker.send('claim'));
  const outcomes=await Promise.all(results);assert.equal(outcomes.filter(result=>result.claimed).length,1);assert.equal(outcomes.find(result=>!result.claimed).error,'project_busy');ledger.close();
 }finally{f.cleanup();}
});

test('stop and restart retain deadline and revision budget', async () => {
  const { Ledger } = await import('../src/harness/ledger.ts');
  const f = fixture();
  try {
    let ledger = new Ledger(join(f.root, 'state'));
    const task = ledger.create(f.request); const epoch = ledger.claim(task.id);
    ledger.stop(task.id);
    assert.equal(ledger.status(task.id).state, 'cancel_requested');
    assert.throws(() => ledger.transition(task.id, epoch, 'completed'), /invalid_transition/);
    ledger.close(); ledger = new Ledger(join(f.root, 'state'));
    assert.equal(ledger.status(task.id).request.budget.deadline, f.request.budget.deadline);
    assert.equal(ledger.status(task.id).request.budget.maxRevisions, 2);
    ledger.close();
  } finally { f.cleanup(); }
});

test('expired tasks and output paths outside authorization fail before claiming', async () => {
  const { Ledger } = await import('../src/harness/ledger.ts');
  const f = fixture();
  try {
    const ledger = new Ledger(join(f.root, 'state'));
    assert.throws(() => ledger.create({ ...f.request, output: join(f.root, '..', 'outside') }), /path_outside_authorization/);
    const task = ledger.create({ ...f.request, budget: { ...f.request.budget, deadline: Date.now() - 1 } });
    assert.throws(() => ledger.claim(task.id), /budget_exhausted/);
    assert.equal(ledger.status(task.id).state, 'planned'); ledger.close();
  } finally { f.cleanup(); }
});

test('parent links cannot bypass revision scheduling or revive a cancelled lineage',async()=>{
 const {Ledger}=await import('../src/harness/ledger.ts');const f=fixture();
 try{
  const ledger=new Ledger(join(f.root,'state'));
  assert.throws(()=>ledger.create({...f.request,parentTask:'missing'}),/parent_task_requires_revision/);
  const parent=ledger.create(f.request);const child=ledger.create({...f.request,idempotencyKey:'child',output:join(f.root,'child')});
  // 故障 fixture：模拟已有子调用，不能用孤立的 planned 状态绕过父任务停止。
  const {canonical,digest}=await import('../src/protocol/files.ts');const row=JSON.parse((ledger.db.prepare('SELECT data FROM tasks WHERE id=?').get(child.id) as any).data);row.request.parentTask=parent.id;row.identity=digest(canonical(row.request));ledger.db.prepare('UPDATE tasks SET identity=?,data=? WHERE id=?').run(row.identity,canonical(row),child.id);
  ledger.stop(parent.id);assert.equal(ledger.status(child.id).state,'cancelled');
  assert.throws(()=>ledger.claim(child.id),/reconcile_required/);
  ledger.close();
 }finally{f.cleanup();}
});

test('judge receipts are candidate-bound, consumed once and cannot override technical failure', async () => {
  const { Ledger } = await import('../src/harness/ledger.ts');
  const { Review } = await import('../src/evaluation/review.ts');
  const f = fixture();
  try {
    const ledger = new Ledger(join(f.root, 'state')); const task = ledger.create(f.request);
    const epoch = ledger.claim(task.id);
    ledger.transition(task.id, epoch, 'verifying');
    const review = new Review(ledger);
    assert.throws(() => review.request(task.id), /technical_verification_required/);
    ledger.recordTechnical(task.id, epoch, { status: 'PASS', projectSha256: 'a'.repeat(64), previewSha256: 'b'.repeat(64), manifestSha256: 'c'.repeat(64) });
    const request = review.request(task.id);
    const receipt = { requestId: request.id, projectSha256: request.projectSha256, previewSha256: request.previewSha256,
      manifestSha256:request.manifestSha256,referencesSha256:request.referencesSha256,briefSha256: request.briefSha256, rubricVersion: request.rubricVersion,
      evaluator: { kind: 'human', identity: 'reviewer', version: 'test-fixture/v1', contextIsolation: 'independent-artifact-review' }, verdict: 'PASS', gaps: [] };
    assert.throws(() => review.import(task.id, { ...receipt, previewSha256: 'd'.repeat(64) }), /review_binding_mismatch/);
    review.import(task.id, receipt);
    assert.throws(() => review.import(task.id, receipt), /review_already_consumed/);
    assert.equal(ledger.status(task.id).state, 'review_ready');
    assert.throws(() => review.accept(task.id, 'wrong'), /acceptance_binding_mismatch/);
    review.accept(task.id, request.id);
    assert.equal(ledger.status(task.id).state, 'completed'); ledger.close();
  } finally { f.cleanup(); }
});

test('strict request JSON rejects duplicate keys and numeric overflow', async () => {
  const { strictJson } = await import('../src/protocol/strict_json.ts');
  assert.throws(() => strictJson('{"a":1,"a":2}'), /duplicate_json_key/);
  assert.throws(() => strictJson('{"a":1e999}'), /nonfinite_json_value/);
  assert.deepEqual(strictJson('{"a":{"x":1},"b":{"x":2}}'), { a: { x: 1 }, b: { x: 2 } });
});

test('creative receipts reject executor self-review and missing evaluator version',async()=>{
 const { Ledger }=await import('../src/harness/ledger.ts');const { Review }=await import('../src/evaluation/review.ts');const f=fixture();
 try {
  const ledger=new Ledger(join(f.root,'state'));const task=ledger.create(f.request);const epoch=ledger.claim(task.id);ledger.transition(task.id,epoch,'verifying');ledger.recordTechnical(task.id,epoch,{status:'PASS',projectSha256:'a'.repeat(64),previewSha256:'b'.repeat(64),manifestSha256:'c'.repeat(64)});
  const review=new Review(ledger);const request=review.request(task.id);const receipt={requestId:request.id,projectSha256:request.projectSha256,previewSha256:request.previewSha256,manifestSha256:request.manifestSha256,referencesSha256:request.referencesSha256,briefSha256:request.briefSha256,rubricVersion:request.rubricVersion,evaluator:{kind:'human',identity:'reviewer',contextIsolation:'separate-review'},verdict:'PASS',gaps:[]};
  assert.throws(()=>review.import(task.id,{...receipt,evaluator:{...receipt.evaluator,identity:'photocraft-harness',version:'v1'}}),/executor_self_review_refused/);
  assert.throws(()=>review.import(task.id,receipt),/independent_evaluator_required/);ledger.close();
 }finally{f.cleanup();}
});
