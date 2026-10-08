import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,realpathSync,mkdirSync,writeFileSync,rmSync,renameSync,readFileSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {digest,canonical} from '../src/protocol/files.ts';
test('portable lineage binds task, input, capability and review without live ledger or old path',async()=>{
 const {exportBundle,verifyBundle}=await import('../src/protocol/bundle.ts');
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photo-bundle-')));
 try{
  const delivery=join(root,'delivery');mkdirSync(delivery);const files:Record<string,string>={};
  for(const [name,text] of Object.entries({'project.pcraft':'native','design.png':'preview','native.json':'{"width":32,"height":32}', 'exchange-loss.json':'{}','operations.json':'[]','plan.json':'{"operations":[]}','capabilities.json':'{}'})){writeFileSync(join(delivery,name),text);files[name]=digest(text);}
  const manifest={schema:'photocraft-delivery/v1',files,outputs:[{path:'design.png'}],assets:{},runtimeSha256:'a'.repeat(64)};writeFileSync(join(delivery,'manifest.json'),canonical(manifest));
  const reference=join(root,'reference.png');writeFileSync(reference,'reference');
  const request={brief:'Title',plan:{operations:[]},output:delivery,references:[{path:reference,sha256:digest('reference')}]};
  const task:any={schema:'photocraft-task/v1',id:'task',request,identity:digest(canonical(request)),executionIdentity:{sha256:'b'.repeat(64)},state:'verifying',technical:{status:'PASS',manifestSha256:digest(canonical(manifest)),projectSha256:files['project.pcraft'],previewSha256:files['design.png'],sourceSha256:'b'.repeat(64)},creative:{status:'NOT_RUN'},acceptance:{status:'NOT_RUN'}};
  const exported=exportBundle(task,join(root,'exported'));assert.equal(exported.lineage,'VERIFIED');assert.equal(exported.creativeAcceptance,'NOT_RUN');
  assert.equal(verifyBundle(delivery).lineage,'UNKNOWN');
  assert.throws(()=>exportBundle({...task,creative:{status:'PASS'}},join(root,'forged')),/bundle_review_required/);
  assert.throws(()=>exportBundle({...task,state:'cancelled'},join(root,'cancelled')),/bundle_task_not_verified/);
  assert.throws(()=>verifyBundle(join(root,'exported'),'f'.repeat(64)),/bundle_anchor_mismatch/);
  const reviewRequest={id:'review-old',taskId:task.id,projectSha256:files['project.pcraft'],previewSha256:'f'.repeat(64),manifestSha256:task.technical.manifestSha256,briefSha256:digest(request.brief),referencesSha256:digest(canonical(request.references)),rubricVersion:'v1'};
  const receipt={...reviewRequest,requestId:reviewRequest.id,evaluator:{identity:'fixture',version:'v1',contextIsolation:'fixture'},verdict:'FAIL'};
  assert.throws(()=>exportBundle({...task,reviewRequest,reviewReceipt:receipt,reviewConsumed:true,creative:{status:'FAIL',receiptSha256:digest(canonical(receipt)),requestId:reviewRequest.id}},join(root,'old-review')),/bundle_review_binding_mismatch/);
  renameSync(join(root,'exported'),join(root,'moved'));rmSync(delivery,{recursive:true});rmSync(reference);
  assert.equal(verifyBundle(join(root,'moved'),exported.bundleSha256).artifact.sha256,files['project.pcraft']);
  const metadataPath=join(root,'moved/harness/task.json');const changed=JSON.parse(readFileSync(metadataPath,'utf8'));changed.creative={status:'PASS'};writeFileSync(metadataPath,canonical(changed));
  assert.throws(()=>verifyBundle(join(root,'moved'),exported.bundleSha256),/bundle_file_mismatch/);
 }finally{rmSync(root,{recursive:true,force:true});}
});
