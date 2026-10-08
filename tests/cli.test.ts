import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, realpathSync, rmSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
const run=(args:string[])=>spawnSync(process.execPath,['src/cli.ts',...args],{encoding:'utf8',timeout:10_000});
test('public status is read-only and never initializes a missing ledger',()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photo-cli-')));
 try{const state=join(root,'state');const result=run(['status','--state-dir',state,'--task','missing']);assert.equal(result.status,1);assert.equal(JSON.parse(result.stdout).code,'ledger_missing');assert.equal(existsSync(state),false);}finally{rmSync(root,{recursive:true,force:true});}
});
test('public request rejects duplicate JSON keys before any ledger creation',()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photo-cli-')));
 try{const file=join(root,'task.json');writeFileSync(file,'{"brief":"a","brief":"b"}');const state=join(root,'state');const result=run(['create','--state-dir',state,'--request',file]);assert.equal(result.status,1);assert.equal(JSON.parse(result.stdout).code,'duplicate_json_key');assert.equal(existsSync(state),false);}finally{rmSync(root,{recursive:true,force:true});}
});
