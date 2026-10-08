import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,realpathSync,writeFileSync,readFileSync,rmSync,cpSync,renameSync,symlinkSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {spawnSync} from 'node:child_process';
import {Ledger} from '../src/harness/ledger.ts';
import {Runner} from '../src/harness/runner.ts';
import {Review} from '../src/evaluation/review.ts';
import {exportBundle,verifyBundle} from '../src/protocol/bundle.ts';
import {fileDigest,canonical,digest} from '../src/protocol/files.ts';

// 旧交付仅允许既有文件完整性检查，不能把空对象或缺失工程解释成通过。
test('legacy bundle inspection refuses empty, malformed and incomplete delivery manifests',()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photo-legacy-negative-')));
 try {
  for(const manifest of [{schema:'photocraft-delivery/v1',files:{}}, {}, {schema:'other',files:{}}, {schema:'photocraft-delivery/v1',files:[],outputs:[]}, {schema:'photocraft-delivery/v1',files:{'preview.png':digest('preview')},outputs:[{path:'preview.png'}],assets:{}}]) {
   writeFileSync(join(root,'manifest.json'),canonical(manifest));writeFileSync(join(root,'preview.png'),'preview');
   assert.throws(()=>verifyBundle(root),/legacy_delivery_invalid|legacy_required_file_missing|bundle_files_required/);
  }
 } finally {rmSync(root,{recursive:true,force:true});}
});

test('real native creation revision and moved bundle preserve lineage and refuse mixed identities', {skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photo-lineage-native-')));let ledger:Ledger|undefined;
 const report:any={schema:'photocraft-lineage-acceptance/v1',status:'RUNNING',creativeAcceptance:'NOT_RUN',sourceAuthenticity:'NOT_PROVEN',cases:[]};
 try {
  const skillRoot=process.env.PHOTOCRAFT_SKILL_ROOT!;const python=process.env.PHOTOCRAFT_PYTHON??'python3';ledger=new Ledger(join(root,'state'));const runner=new Runner(ledger,{skillRoot,python});
  const reference=join(root,'reference.txt');writeFileSync(reference,'Lineage acceptance reference; OLD becomes NEW.');
  const parent=ledger.create({idempotencyKey:'lineage-parent',brief:'Change editable OLD to NEW while retaining original package',references:[{path:reference,sha256:fileDigest(reference)}],plan:{document:{width:64,height:64,background:'#ffffff'},operations:[{command:'type.create',params:{text:'OLD',font:'Arial',size:12,x:8,y:20},as:'title'}],exports:[{format:'png'},{format:'psd'}]},output:join(root,'parent'),authorization:{ref:'lineage-fixture',writeRoot:root},budget:{deadline:Date.now()+180000,maxRevisions:1,maxConcurrent:1,reserveBytes:1048576}});
  const created=await runner.run(parent.id);assert.equal(created.technical.status,'PASS',JSON.stringify(created));const parentManifest=JSON.parse(readFileSync(join(root,'parent/manifest.json'),'utf8'));const parentHashes={...parentManifest.files,manifest:fileDigest(join(root,'parent/manifest.json'))};
  const first=exportBundle(created,join(root,'parent-bundle'));assert.equal(first.creativeAcceptance,'NOT_RUN');assert.equal(first.artifact.producerTaskId,parent.id);
  // 回执仅为修订合同fixture，不以模拟评估器证明真实创作验收。
  const review=new Review(ledger);const request=review.request(parent.id);review.import(parent.id,{requestId:request.id,projectSha256:request.projectSha256,previewSha256:request.previewSha256,manifestSha256:request.manifestSha256,referencesSha256:request.referencesSha256,briefSha256:request.briefSha256,rubricVersion:request.rubricVersion,evaluator:{kind:'external',identity:'lineage-contract-fixture',version:'v1',contextIsolation:'fixture-only'},verdict:'FAIL',gaps:[{id:'title',layer:parentManifest.bindings.title.layer,property:'text',reason:'OLD must become NEW'}]});
  const child=await runner.revise(parent.id,{baseProjectSha256:request.projectSha256,baseManifestSha256:request.manifestSha256,authorizationRef:'lineage-fixture',operations:[{command:'type.edit',params:{layer:parentManifest.bindings.title.layer,text:'NEW'}}]});
  const revised=await runner.run(child.id);assert.equal(revised.technical.status,'PASS',JSON.stringify(revised));assert.equal(revised.creative.status,'NOT_RUN');const native=JSON.parse(readFileSync(join(child.request.output,'native.json'),'utf8'));assert.ok(native.layers.some((row:any)=>row.kind==='Type' && row.text?.text==='NEW'));
  const second=exportBundle(revised,join(root,'child-bundle'),created.artifact);assert.equal(second.artifact.assetId,first.artifact.assetId);assert.notEqual(second.artifact.version,first.artifact.version);assert.equal(second.artifact.sourceRefs[0].sha256,first.artifact.sha256);assert.equal(second.artifact.producerTaskId,child.id);
  const task=JSON.parse(readFileSync(join(root,'child-bundle/harness/task.json'),'utf8'));const manifest=JSON.parse(readFileSync(join(root,'child-bundle/manifest.json'),'utf8'));const cap=JSON.parse(readFileSync(join(root,'child-bundle/capabilities.json'),'utf8'));const lock=JSON.parse(readFileSync(join(skillRoot,'scripts/runtime.lock.json'),'utf8'));
  assert.equal(digest(canonical(task.request.plan)),digest(canonical(JSON.parse(readFileSync(join(root,'child-bundle/plan.json'),'utf8')))));assert.equal(task.executionIdentity.sha256,task.technical.sourceSha256);assert.equal(cap.binarySha256,manifest.runtimeSha256);assert.equal(cap.runtimeIdentity.version,lock.resolvedVersion);
  for(const file of ['plan.json','operations.json','capabilities.json','native.json'])assert.ok(second.artifact.evidenceRefs.some((ref:any)=>ref.location===file && ref.sha256===manifest.files[file]));
  assert.ok(second.artifact.evidenceRefs.some((ref:any)=>ref.location==='harness/task.json'));assert.ok(second.artifact.evidenceRefs.some((ref:any)=>ref.location==='harness/parent-artifact.json'));
  for(const [name,sha] of Object.entries(parentHashes))assert.equal(fileDigest(join(root,'parent',name==='manifest'?'manifest.json':name)),sha);
  report.cases.push({id:'PC-AR-001-P',result:'PASS'},{id:'PC-AR-001-LINEAGE',result:'PASS',parentTask:parent.id,childTask:child.id,parentArtifact:first.artifact,childArtifact:second.artifact,planSha256:manifest.files['plan.json'],inputManifestSha256:revised.request.plan.expectedManifestSha256,runtimeSha256:manifest.runtimeSha256,capabilitiesSha256:manifest.files['capabilities.json'],reviewFixtureOnly:true});
  const moved=join(root,'移动 包');renameSync(join(root,'child-bundle'),moved);const snapshot=fileDigest(join(moved,'bundle-manifest.json'));assert.equal(verifyBundle(moved,second.bundleSha256).artifact.version,second.artifact.version);
  function reject(name:string,mutate:(dir:string)=>void,pattern:RegExp,anchored=true) {
   const directory=join(root,'fault-'+name);cpSync(moved,directory,{recursive:true});mutate(directory);
   const command=spawnSync(process.execPath,['src/cli.ts','bundle-check','--bundle',directory,...(anchored?['--expected-sha256',second.bundleSha256]:[])],{cwd:join(import.meta.dirname,'..'),encoding:'utf8',timeout:30000});assert.equal(command.status,1,command.stdout+command.stderr);const reply=JSON.parse(command.stdout);assert.match(reply.error,pattern);assert.equal(fileDigest(join(moved,'bundle-manifest.json')),snapshot);report.cases.push({id:name,result:'PASS',error:reply.code});
  }
  function rehash(directory:string,file:string,value:any) {writeFileSync(join(directory,file),canonical(value));const p=join(directory,'bundle-manifest.json');const v=JSON.parse(readFileSync(p,'utf8'));v.files[file]=fileDigest(join(directory,file));writeFileSync(p,canonical(v));}
  reject('same-name-preview',dir=>writeFileSync(join(dir,'design.png'),'other-round'),/bundle_file_mismatch/);
  reject('missing-file',dir=>rmSync(join(dir,'project.pcraft')),/ENOENT/);
  reject('symlink',dir=>{rmSync(join(dir,'design.png'));symlinkSync(join(moved,'design.png'),join(dir,'design.png'));},/symlink_not_allowed/);
  reject('duplicate-key',dir=>writeFileSync(join(dir,'bundle-manifest.json'),'{"files":{},"files":{}}'),/bundle_anchor_mismatch/);
  reject('duplicate-key-unanchored',dir=>writeFileSync(join(dir,'bundle-manifest.json'),'{"files":{},"files":{}}'),/duplicate_json_key/,false);
  reject('path-escape',dir=>{const p=join(dir,'bundle-manifest.json');const v=JSON.parse(readFileSync(p,'utf8'));v.files['../outside']='0'.repeat(64);writeFileSync(p,canonical(v));},/bundle_path_invalid/,false);
  reject('mixed-review',dir=>{const v=JSON.parse(readFileSync(join(dir,'harness/task.json'),'utf8'));const receipt={requestId:request.id,...request,evaluator:{identity:'fixture',version:'v1',contextIsolation:'fixture'},verdict:'FAIL'};v.reviewRequest=request;v.reviewReceipt=receipt;v.reviewConsumed=true;v.creative={status:'FAIL',requestId:request.id,receiptSha256:digest(canonical(receipt))};rehash(dir,'harness/task.json',v);},/bundle_review_binding_mismatch/,false);
  reject('forged-acceptance',dir=>{const v=JSON.parse(readFileSync(join(dir,'harness/task.json'),'utf8'));v.creative={status:'PASS'};rehash(dir,'harness/task.json',v);},/bundle_review_required/,false);
  reject('wrong-parent',dir=>{const v=JSON.parse(readFileSync(join(dir,'harness/parent-artifact.json'),'utf8'));v.sha256='f'.repeat(64);v.version=v.sha256;rehash(dir,'harness/parent-artifact.json',v);},/parent_version_conflict/,false);
  reject('wrong-plan',dir=>{const v=JSON.parse(readFileSync(join(dir,'harness/task.json'),'utf8'));v.request.plan.operations[0].params.text='OTHER';v.identity=digest(canonical(v.request));rehash(dir,'harness/task.json',v);const p=join(dir,'bundle-manifest.json');const m=JSON.parse(readFileSync(p,'utf8'));m.requestSha256=v.identity;writeFileSync(p,canonical(m));},/bundle_plan_binding_mismatch/,false);
  reject('rehashed-package-old-anchor',dir=>rehash(dir,'harness/task.json',{...task,createdAt:task.createdAt+1}),/bundle_anchor_mismatch/);
  const legacy=verifyBundle(join(root,'parent'));assert.equal(legacy.lineage,'UNKNOWN');assert.equal(legacy.technicalAcceptance,'NOT_RUN');assert.equal(legacy.creativeAcceptance,'NOT_RUN');assert.equal(legacy.acceptance,'NOT_RUN');assert.throws(()=>verifyBundle(join(root,'parent'),first.bundleSha256),/bundle_anchor_missing/);
  report.cases.push({id:'PC-AR-001-MIXED',result:'PASS',legacy},{id:'PC-AR-001-INTEGRITY',result:'PASS',movedAnchor:second.bundleSha256});
  ledger.close();ledger=undefined;rmSync(join(root,'parent'),{recursive:true});rmSync(child.request.output,{recursive:true});rmSync(reference);rmSync(join(root,'state'),{recursive:true});const offline=verifyBundle(moved,second.bundleSha256);assert.equal(offline.lineage,'VERIFIED');assert.equal(offline.sourceAuthenticity,'NOT_PROVEN');assert.equal(offline.creativeAcceptance,'NOT_RUN');assert.equal(offline.acceptance,'NOT_RUN');assert.equal(fileDigest(join(moved,'bundle-manifest.json')),snapshot);
  const reopened=spawnSync(python,['-I','-B',join(skillRoot,'scripts/cli.py'),'--','info',join(moved,'project.pcraft')],{encoding:'utf8',timeout:30000});assert.equal(reopened.status,0,reopened.stdout+reopened.stderr);assert.ok(JSON.parse(reopened.stdout).layers.some((row:any)=>row.text?.text==='NEW'));report.cases.push({id:'moved-without-original-path-or-ledger',result:'PASS',nativeReopened:true});report.cases.push({id:'PC-AR-001-N',result:'PASS',sameNameReplacementRefused:true});report.status='PASS';
 } finally {ledger?.close();if(process.env.PHOTOCRAFT_LINEAGE_REPORT)writeFileSync(process.env.PHOTOCRAFT_LINEAGE_REPORT,JSON.stringify(report,null,2)+'\n');rmSync(root,{recursive:true,force:true});}
});
