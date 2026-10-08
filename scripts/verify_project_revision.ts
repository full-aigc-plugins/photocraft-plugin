/** 真实桌面观察驱动调用本入口；核对拒绝前后任务、事件、文件和预检次数。 */
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { Ledger } from '../src/harness/ledger.ts';
import { Runner } from '../src/harness/runner.ts';
import { fileDigest } from '../src/protocol/files.ts';
const [requestPath,state,skillRoot,expected]=process.argv.slice(2);
const request=JSON.parse(readFileSync(requestPath,'utf8'));const ledger=new Ledger(state);
try {
 const task=ledger.create(request);const before=JSON.stringify(ledger.status(task.id));const events=JSON.stringify(ledger.db.prepare('SELECT * FROM events ORDER BY sequence').all());const files=readdirSync(state).sort();const projectSha256=fileDigest(task.request.mutableProject);
 const runner=new Runner(ledger,{skillRoot,python:'python3'});let preflightCalls=0;runner.preflight=()=>{preflightCalls++;throw new Error('unexpected_preflight');};
 let failure:any;try {await runner.run(task.id);}catch(error){failure=error;}
 assert.ok(failure);assert.equal(failure.code??failure.message,expected);assert.equal(preflightCalls,0);
 if(expected==='revision_conflict'){assert.equal(failure.phase,'validation');assert.equal(failure.outcome,'not_executed');assert.equal(failure.fieldPath,'$.expectedProjectSha256');}
 assert.equal(JSON.stringify(ledger.status(task.id)),before);assert.equal(JSON.stringify(ledger.db.prepare('SELECT * FROM events ORDER BY sequence').all()),events);assert.deepEqual(readdirSync(state).sort(),files);assert.equal(existsSync(task.request.output),false);assert.equal(fileDigest(task.request.mutableProject),projectSha256);
 console.log(JSON.stringify({result:'PASS',code:failure.code??failure.message,projectSha256,preflightCalls,nativeSessionsStarted:0,taskAndEventsUnchanged:true,outputCreated:false,attempted:ledger.status(task.id).attempted}));
} finally {ledger.close();}
