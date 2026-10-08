import {copyFileSync,existsSync,mkdirSync,mkdtempSync,renameSync,rmSync,writeFileSync} from 'node:fs';
import {dirname,join} from 'node:path';
import {canonical,digest,fileDigest,readJson,safePath,within} from './files.ts';
import {mapArtifact,validateArtifact} from './artifact.ts';

function pathAt(root:string,name:string) {
 if(typeof name!=='string' || /[\\:\x00]/.test(name) || name.split('/').some(part=>!part || part==='.' || part==='..'))throw new Error('bundle_path_invalid');
 return within(join(root,name),root);
}
function checkFiles(root:string,files:Record<string,string>) {
 if(!files || Array.isArray(files) || typeof files!=='object')throw new Error('bundle_files_required');
 for(const [name,sha]of Object.entries(files))if(!/^[a-f0-9]{64}$/.test(sha) || fileDigest(pathAt(root,name))!==sha)throw new Error('bundle_file_mismatch: '+name);
}
function checkReview(task:any) {
 const request=task.reviewRequest;const receipt=task.reviewReceipt;
 if(!['NOT_RUN','FAIL','PASS'].includes(task.creative?.status) || !['NOT_RUN','PASS'].includes(task.acceptance?.status))throw new Error('bundle_review_status_mismatch');
 if(task.creative.status==='NOT_RUN') {if(receipt || task.acceptance.status!=='NOT_RUN')throw new Error('bundle_review_status_mismatch');return;}
 if(!request || !receipt || !task.reviewConsumed || task.creative.receiptSha256!==digest(canonical(receipt)))throw new Error('bundle_review_required');
 if(request.taskId!==task.id || receipt.requestId!==request.id || task.creative.requestId!==request.id || receipt.verdict!==task.creative.status)throw new Error('bundle_review_binding_mismatch');
 const bindings={projectSha256:task.technical.projectSha256,previewSha256:task.technical.previewSha256,manifestSha256:task.technical.manifestSha256,briefSha256:digest(task.request.brief),referencesSha256:digest(canonical(task.request.references??[]))};
 for(const [key,value]of Object.entries(bindings))if(request[key]!==value || receipt[key]!==value)throw new Error('bundle_review_binding_mismatch: '+key);
 if(receipt.rubricVersion!==request.rubricVersion || !receipt.evaluator?.identity || !receipt.evaluator?.version || !receipt.evaluator?.contextIsolation || receipt.evaluator.identity==='photocraft-harness')throw new Error('bundle_evaluator_missing');
 if(task.acceptance.status==='PASS' && (task.creative.status!=='PASS' || task.acceptance.requestId!==request.id))throw new Error('bundle_acceptance_binding_mismatch');
}

/** 导出额外的本地证据文件，公共 artifact 只使用固定协议既有 evidenceRefs。 */
export function exportBundle(task:any,destination:string,parent?:any) {
 if(['cancel_requested','cancelled','failed','reconciling'].includes(task.state))throw new Error('bundle_task_not_verified');
 if(task.identity!==digest(canonical(task.request)) || !/^[a-f0-9]{64}$/.test(task.executionIdentity?.sha256??'') || task.technical.sourceSha256!==task.executionIdentity?.sha256)throw new Error('bundle_task_identity_mismatch');
 checkReview(task);
 const base=mapArtifact(task,parent);const source=safePath(task.request.output);const target=safePath(destination);
 if(existsSync(target))throw new Error('bundle_output_exists');
 const stage=mkdtempSync(join(dirname(target),'.photocraft-bundle-'));
 try {
  const files:Record<string,string>={};
  const copy=(name:string,path:string)=>{const output=pathAt(stage,name);mkdirSync(dirname(output),{recursive:true});copyFileSync(safePath(path),output);files[name]=fileDigest(output);};
  const save=(name:string,value:any)=>{const path=pathAt(stage,name);mkdirSync(dirname(path),{recursive:true});writeFileSync(path,canonical(value),{flag:'wx',mode:0o600});files[name]=fileDigest(path);};
  const manifest=readJson(join(source,'manifest.json'));
  if(canonical(readJson(join(source,'plan.json')))!==canonical(task.request.plan))throw new Error('bundle_plan_binding_mismatch');
  for(const name of [...Object.keys(manifest.files),'manifest.json'])copy(name,pathAt(source,name));
  save('harness/task.json',task);if(parent)save('harness/parent-artifact.json',parent);
  const references=(task.request.references??[]).map((reference:any,index:number)=>{
   if(fileDigest(reference.path)!==reference.sha256)throw new Error('reference_identity_mismatch');
   const path='harness/references/'+index;copy(path,reference.path);return {index,path,sha256:reference.sha256};
  });
  const evidenceNames=['harness/task.json',...(parent?['harness/parent-artifact.json']:[])];
  const artifact={...base,evidenceRefs:[...base.evidenceRefs,...evidenceNames.map(name=>({assetId:base.assetId+':'+name,version:files[name],sha256:files[name],location:name}))]};
  validateArtifact(artifact);save('harness/artifact.json',artifact);
  save('bundle-manifest.json',{schema:'photocraft-lineage-bundle/v1',taskId:task.id,requestSha256:task.identity,files:{...files},references});
  const anchor=files['bundle-manifest.json'];
  // 重新核对源、复制包和评估；源同时改变不能靠一次 copy 的摘要通过。
  mapArtifact(task,parent);checkReview(task);const result=verifyBundle(stage,anchor);
  renameSync(stage,target);return {...result,directory:target};
 }catch(error){rmSync(stage,{recursive:true,force:true});throw error;}
}

/** 仅消费包内相对位置；外部摘要提供版本锚点，完整性不证明评估器来源真实性。 */
export function verifyBundle(directory:string,expectedSha256?:string):any {
 const root=safePath(directory);const manifestPath=join(root,'bundle-manifest.json');
 if(!existsSync(manifestPath)) {
  if(expectedSha256)throw new Error('bundle_anchor_missing');
  const legacyPath=join(root,'manifest.json');const anchor=fileDigest(legacyPath);const legacy=readJson(legacyPath);
  // 旧版不具备完整血缘，但仍须满足原交付清单的最小文件与引用合同。
  if(!legacy || legacy.schema!=='photocraft-delivery/v1' || !legacy.files || Array.isArray(legacy.files) || typeof legacy.files!=='object' || !Array.isArray(legacy.outputs) || !legacy.assets || Array.isArray(legacy.assets) || typeof legacy.assets!=='object')throw new Error('legacy_delivery_invalid');
  for(const name of ['project.pcraft','native.json','plan.json','operations.json','exchange-loss.json'])if(!Object.hasOwn(legacy.files,name))throw new Error('legacy_required_file_missing');
  checkFiles(root,legacy.files);
  const outputs=new Set();
  for(const output of legacy.outputs) {
   if(!output || typeof output.path!=='string' || !Object.hasOwn(legacy.files,output.path) || outputs.has(output.path))throw new Error('legacy_delivery_invalid');outputs.add(output.path);
  }
  for(const asset of Object.values(legacy.assets) as any[])if(!asset || typeof asset.path!=='string' || !Object.hasOwn(legacy.files,asset.path) || asset.sha256!==legacy.files[asset.path])throw new Error('legacy_delivery_invalid');
  if(fileDigest(legacyPath)!==anchor)throw new Error('bundle_changed_during_verify');
  return {result:'PASS',fileIntegrity:'PASS',lineage:'UNKNOWN',technicalAcceptance:'NOT_RUN',creativeAcceptance:'NOT_RUN',acceptance:'NOT_RUN',missing:['task-lineage','review-binding']};
 }
 const anchor=fileDigest(manifestPath);
 if(expectedSha256 && anchor!==expectedSha256)throw new Error('bundle_anchor_mismatch');
 const manifest=readJson(manifestPath);
 if(manifest.schema!=='photocraft-lineage-bundle/v1' || Object.keys(manifest).some(key=>!['schema','taskId','requestSha256','files','references'].includes(key)))throw new Error('bundle_manifest_invalid');
 checkFiles(root,manifest.files);
 for(const name of ['manifest.json','harness/task.json','harness/artifact.json'])if(!Object.hasOwn(manifest.files,name))throw new Error('bundle_required_file_missing');
 const task=readJson(join(root,'harness/task.json'));
 if(task.id!==manifest.taskId || task.identity!==manifest.requestSha256 || digest(canonical(task.request))!==task.identity || !/^[a-f0-9]{64}$/.test(task.executionIdentity?.sha256??'') || task.technical.sourceSha256!==task.executionIdentity?.sha256)throw new Error('bundle_task_identity_mismatch');
 if(['cancel_requested','cancelled','failed','reconciling'].includes(task.state))throw new Error('bundle_task_not_verified');
 const parent=task.request.parentTask?readJson(pathAt(root,'harness/parent-artifact.json')):undefined;
 if(parent && !Object.hasOwn(manifest.files,'harness/parent-artifact.json'))throw new Error('bundle_required_file_missing');
 const base=mapArtifact(task,parent,root);checkReview(task);
 if(canonical(readJson(join(root,'plan.json')))!==canonical(task.request.plan))throw new Error('bundle_plan_binding_mismatch');
 const references=task.request.references??[];
 if(!Array.isArray(manifest.references) || manifest.references.length!==references.length)throw new Error('bundle_reference_mismatch');
 for(let i=0;i<references.length;i++) {
  const entry=manifest.references[i];if(entry.index!==i || entry.sha256!==references[i].sha256 || manifest.files[entry.path]!==entry.sha256)throw new Error('bundle_reference_mismatch');
 }
 const artifact=validateArtifact(readJson(join(root,'harness/artifact.json')));
 const evidenceNames=['harness/task.json',...(parent?['harness/parent-artifact.json']:[])];
 // 已发布旧包保留原生MIME身份，只读检查不能把其改造成新的已兼容发行。
 const legacyNativeType=artifact.mediaType==='application/x-photocraft';
 const expected={...base,mediaType:legacyNativeType?artifact.mediaType:base.mediaType,evidenceRefs:[...base.evidenceRefs,...evidenceNames.map(name=>({assetId:base.assetId+':'+name,version:manifest.files[name],sha256:manifest.files[name],location:name}))]};
 if(canonical(artifact)!==canonical(expected))throw new Error('bundle_artifact_mismatch');
 checkFiles(root,manifest.files);if(fileDigest(manifestPath)!==anchor)throw new Error('bundle_changed_during_verify');
 return {result:'PASS',fileIntegrity:'PASS',lineage:'VERIFIED',bundleSha256:anchor,externallyAnchored:!!expectedSha256,sourceAuthenticity:'NOT_PROVEN',nativeMediaTypeCompatibility:legacyNativeType?'LEGACY_UNSUPPORTED_BY_PINNED_CONSUMER':'PINNED_CONSUMER_BINARY_CONTRACT',artifact,technicalAcceptance:task.technical.status,creativeAcceptance:task.creative.status,acceptance:task.acceptance.status,evaluatorIsolation:task.reviewReceipt?.evaluator?.contextIsolation??'NOT_RUN'};
}
