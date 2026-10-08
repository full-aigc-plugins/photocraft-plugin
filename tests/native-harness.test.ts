import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, realpathSync, rmSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Ledger } from '../src/harness/ledger.ts';
import { Runner } from '../src/harness/runner.ts';
import { Review } from '../src/evaluation/review.ts';
import { exportBundle,verifyBundle } from '../src/protocol/bundle.ts';

test('real native task, fresh readonly reopening, bounded title revision, source retention and restart reconcile', {skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-native-harness-')));
 try {
  let ledger=new Ledger(join(root,'state'));
  const options={skillRoot:process.env.PHOTOCRAFT_SKILL_ROOT!,python:process.env.PHOTOCRAFT_PYTHON??'python3'};
  let runner=new Runner(ledger,options);
  const task=ledger.create({idempotencyKey:'poster',brief:'An editable title saying NEW, with the white background preserved',plan:{document:{width:64,height:64,background:'#ffffff'},operations:[{command:'type.create',params:{text:'OLD',font:'Arial',size:12,x:8,y:20},as:'title'}],exports:[{format:'png'},{format:'psd'}],psdPolicy:{requiredFeatures:['structure','text']},flatExport:{colorSpace:'Rgb',transparency:'opaque'}},output:join(root,'delivery'),authorization:{ref:'test-authorization',writeRoot:root},budget:{deadline:Date.now()+120000,maxRevisions:1,maxConcurrent:1,reserveBytes:1048576}});
  const result=await runner.run(task.id);
  assert.equal(result.state,'verifying');assert.equal(result.technical.status,'PASS');assert.equal(result.creative.status,'NOT_RUN');
  const original=readFileSync(join(root,'delivery/project.pcraft'));
  const review=new Review(ledger);const req=review.request(task.id);
  const manifest=JSON.parse(readFileSync(join(root,'delivery/manifest.json'),'utf8'));
  // 合成评估器回执仅测试协调合同，不作为真实独立创作验收。
  review.import(task.id,{requestId:req.id,projectSha256:req.projectSha256,previewSha256:req.previewSha256,manifestSha256:req.manifestSha256,referencesSha256:req.referencesSha256,briefSha256:req.briefSha256,rubricVersion:req.rubricVersion,evaluator:{kind:'external',identity:'test-fixture-not-production-review',version:'test-fixture/v1',contextIsolation:'test-fixture'},verdict:'FAIL',gaps:[{id:'title',layer:manifest.bindings.title.layer,property:'text',reason:'OLD must become NEW'}]});
  assert.throws(()=>review.propose(task.id,{baseProjectSha256:req.projectSha256,baseManifestSha256:req.manifestSha256,authorizationRef:'test-authorization',operations:[{command:'type.edit',params:{layer:manifest.bindings.title.layer,text:'OLD'}}]}),/revision_no_improvement/);
  const child=await runner.revise(task.id,{baseProjectSha256:req.projectSha256,baseManifestSha256:req.manifestSha256,authorizationRef:'test-authorization',operations:[{command:'type.edit',params:{layer:manifest.bindings.title.layer,text:'NEW'}}]});
  assert.deepEqual(child.request.plan.psdPolicy,{requiredFeatures:['structure','text']});
  const revised=await runner.run(child.id);assert.equal(revised.technical.status,'PASS');assert.equal(revised.creative.status,'NOT_RUN');assert.deepEqual(readFileSync(join(root,'delivery/project.pcraft')),original);
  assert.equal(revised.technical.nativeReopen.psdVerification.status,'PASS');
  assert.deepEqual(child.request.plan.flatExport,{colorSpace:'Rgb',transparency:'opaque'});assert.equal(revised.technical.nativeReopen.flatExportVerification.status,'PASS');
  const portable=exportBundle(revised,join(root,'portable-child'),ledger.status(task.id).artifact);
  const {renameSync}=await import('node:fs');renameSync(join(root,'portable-child'),join(root,'relocated-child'));
  const checked=verifyBundle(join(root,'relocated-child'),portable.bundleSha256);assert.equal(checked.lineage,'VERIFIED');assert.equal(checked.artifact.assetId,result.artifact.assetId);assert.equal(checked.artifact.sourceRefs[0].sha256,result.artifact.sha256);assert.equal(checked.creativeAcceptance,'NOT_RUN');
  const copies=[1,2].map(index=>ledger.create({idempotencyKey:'independent-copy-'+index,brief:'Independent immutable source revision',source:revised.request.output,output:join(root,'independent-'+index),plan:{expectedProjectSha256:revised.technical.projectSha256,operations:[{command:'type.edit',params:{layer:manifest.bindings.title.layer,text:'COPY '+index}}],exports:[{format:'png'}]},authorization:{ref:'test-authorization',writeRoot:root},budget:{deadline:Date.now()+120000,maxRevisions:0,maxConcurrent:2,reserveBytes:1048576}}));
  const sourceDigest=readFileSync(join(revised.request.output,'project.pcraft'));const parallel=await Promise.all(copies.map(copy=>runner.run(copy.id)));assert.ok(parallel.every(copy=>copy.technical.status==='PASS'));assert.deepEqual(readFileSync(join(revised.request.output,'project.pcraft')),sourceDigest);
  ledger.transition(child.id,revised.epoch,'reconciling');ledger.close();ledger=new Ledger(join(root,'state'));runner=new Runner(ledger,options);
  const recovered=await runner.reconcile(child.id);assert.equal(recovered.state,'verifying');assert.equal(recovered.attempted,true);assert.equal(recovered.epoch,revised.epoch);assert.equal(recovered.creative.status,'NOT_RUN');ledger.close();
 }finally{rmSync(root,{recursive:true,force:true});}
});

test('real masked local adjustment revision preserves mask tiles and every protected pixel', {skip:process.env.PHOTOCRAFT_NATIVE_TEST!=='1'},async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'photocraft-native-adjustment-')));
 try{
  const options={skillRoot:process.env.PHOTOCRAFT_SKILL_ROOT!,python:process.env.PHOTOCRAFT_PYTHON??'python3'};const plan=JSON.parse(readFileSync(join(options.skillRoot,'examples/adjustment-mask-create.json'),'utf8'));
  plan.assertions=[{layer:{$ref:'adjustment.layer'},kind:'Adjustment',hasMask:true,maskEnabled:true,maskLinked:true}];
  const ledger=new Ledger(join(root,'state'));const runner=new Runner(ledger,options);const task=ledger.create({idempotencyKey:'local-adjustment',brief:'Darken only the masked left half of the product; preserve the control and right half',plan,output:join(root,'delivery'),authorization:{ref:'test-authorization',writeRoot:root},budget:{deadline:Date.now()+120000,maxRevisions:1,maxConcurrent:1,reserveBytes:1048576}});
  const result=await runner.run(task.id);assert.equal(result.technical.status,'PASS');const source=readFileSync(join(root,'delivery/project.pcraft'));const manifest=JSON.parse(readFileSync(join(root,'delivery/manifest.json'),'utf8'));const layer=manifest.bindings.adjustment.layer;
  const review=new Review(ledger);const req=review.request(task.id);review.import(task.id,{requestId:req.id,projectSha256:req.projectSha256,previewSha256:req.previewSha256,manifestSha256:req.manifestSha256,referencesSha256:req.referencesSha256,briefSha256:req.briefSha256,rubricVersion:req.rubricVersion,evaluator:{kind:'external',identity:'fixture-not-independent-creative-proof',version:'v1',contextIsolation:'fixture'},verdict:'FAIL',gaps:[{id:'local-light',layer,property:'brightness',reason:'The masked half must become darker'}]});
  const proposal={baseProjectSha256:req.projectSha256,baseManifestSha256:req.manifestSha256,authorizationRef:'test-authorization',operations:[{command:'layer.setAdjustment',params:{layer,brightness:-30}}],protectedRegions:[{id:'unmasked-product-and-control',rect:[28,0,100,64]}]};
  const child=await runner.revise(task.id,proposal);const revised=await runner.run(child.id);assert.equal(revised.technical.status,'PASS',JSON.stringify(revised));assert.equal(revised.creative.status,'NOT_RUN');assert.deepEqual(readFileSync(join(root,'delivery/project.pcraft')),source);
  const oldFacts=JSON.parse(readFileSync(join(root,'delivery/native-facts.json'),'utf8'));const newFacts=JSON.parse(readFileSync(join(revised.request.output,'native-facts.json'),'utf8'));assert.equal(newFacts.objects[layer].maskSurfaceSha256,oldFacts.objects[layer].maskSurfaceSha256);
  const protection=JSON.parse(readFileSync(join(revised.request.output,'pixel-protection.json'),'utf8'));assert.equal(protection.regions[0].changedPixels,0);
  const model=JSON.parse(readFileSync(join(revised.request.output,'native.json'),'utf8'));assert.equal(model.layers.find((row:any)=>row.id===layer).adjustment.BrightnessContrast.brightness,-30);
  const {spawnSync}=await import('node:child_process');const pixels=spawnSync(options.python,['-I','-B','-c','from PIL import Image;import sys,json;a=Image.open(sys.argv[1]).convert("RGB");b=Image.open(sys.argv[2]).convert("RGB");print(json.dumps({"before":a.getpixel((16,24)),"after":b.getpixel((16,24))}))',join(root,'delivery/design.png'),join(revised.request.output,'design.png')],{encoding:'utf8'});assert.equal(pixels.status,0,pixels.stderr);const value=JSON.parse(pixels.stdout);assert.ok(value.after[0]<value.before[0]);ledger.close();
 }finally{rmSync(root,{recursive:true,force:true});}
});
