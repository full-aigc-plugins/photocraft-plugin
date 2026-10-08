import { statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { fileDigest, readJson, safePath, within } from './files.ts';

const root=join(dirname(fileURLToPath(import.meta.url)),'../..');
function contract() {
 const reference=readJson(join(root,'docs/contracts-reference.json'));const entry=reference.files.artifactSchema;
 const path=join(root,'contracts/artcraft/craft-artifact-v1.json');
 if(fileDigest(path)!==entry.sha256)throw new Error('contract_snapshot_mismatch');
 return readJson(path);
}
/** 校验固定权威 schema 当前使用的约束；未支持的 schema 版本必须显式升级。 */
function validate(value:any,schema:any,path='$') {
 if(schema.anyOf) {for(const child of schema.anyOf)try{validate(value,child,path);return;}catch{}throw new Error('contract_any_of: '+path);}
 if('const'in schema && value!==schema.const)throw new Error('contract_const: '+path);
 if(schema.enum && !schema.enum.includes(value))throw new Error('contract_enum: '+path);
 if(schema.type) {
  const valid=schema.type==='null'?value===null:schema.type==='array'?Array.isArray(value):schema.type==='object'?value!==null && typeof value==='object' && !Array.isArray(value):schema.type==='integer'?Number.isSafeInteger(value):typeof value===schema.type;
  if(!valid)throw new Error('contract_type: '+path);
 }
 if(typeof value==='string' && ((schema.minLength && [...value].length<schema.minLength) || (schema.maxLength && [...value].length>schema.maxLength) || (schema.pattern && !new RegExp(schema.pattern).test(value))))throw new Error('contract_string: '+path);
 if(typeof value==='number' && ((schema.minimum!==undefined && value<schema.minimum) || (schema.maximum!==undefined && value>schema.maximum)))throw new Error('contract_number: '+path);
 if(Array.isArray(value))for(let i=0;i<value.length;i++)validate(value[i],schema.items,path+'['+i+']');
 if(value!==null && typeof value==='object' && !Array.isArray(value)) {
  for(const key of schema.required??[])if(!Object.hasOwn(value,key))throw new Error('contract_required: '+path+'.'+key);
  for(const key of Object.keys(value)) {if(schema.additionalProperties===false && !Object.hasOwn(schema.properties??{},key))throw new Error('contract_unknown_field: '+path+'.'+key);if(Object.hasOwn(schema.properties??{},key))validate(value[key],schema.properties[key],path+'.'+key);}
 }
}
export function validateArtifact(artifact:any) {validate(artifact,contract());return artifact;}

/** 映射已有技术通过候选；位置变化不改变内容版本，旧包血缘不会补造。 */
export function mapArtifact(task:any,parent?:any,location?:string) {
 if(task.technical?.status!=='PASS')throw new Error('technical_verification_required');
 if(task.request.parentTask && (!parent || parent.producerTaskId!==task.request.parentTask))throw new Error('parent_artifact_required');
 if(parent)validateArtifact(parent);
 if(parent && task.request.plan?.expectedProjectSha256!==parent.sha256)throw new Error('parent_version_conflict');
 const directory=safePath(location??task.request.output);const manifestPath=join(directory,'manifest.json');
 if(fileDigest(manifestPath)!==task.technical.manifestSha256)throw new Error('artifact_manifest_mismatch');
 const manifest=readJson(manifestPath);const files=manifest.files;
 if(parent && manifest.sourceProjectSha256!==parent.sha256)throw new Error('parent_version_conflict');
 for(const [name,sha]of Object.entries(files))if(fileDigest(within(join(directory,name),directory))!==sha)throw new Error('artifact_file_mismatch: '+name);
 if(files['project.pcraft']!==task.technical.projectSha256 || files['design.png']!==task.technical.previewSha256)throw new Error('artifact_round_mismatch');
 const assetId=parent?.assetId??'photocraft:'+task.id;const version=files['project.pcraft'];
 const ref=(name:string,id=assetId+':'+name)=>({assetId:id,version:files[name],sha256:files[name],location:name});
 const native=readJson(join(directory,'native.json'));const sources:any[]=[];
 if(parent)sources.push({assetId:parent.assetId,version:parent.version,sha256:parent.sha256});
 const dependencies=Object.entries(manifest.assets??{}).map(([name,entry]:[string,any])=>{
  if(files[entry.path]!==entry.sha256)throw new Error('artifact_dependency_mismatch');
  const assetRef={assetId:'photocraft-input:'+name,version:entry.sha256,sha256:entry.sha256};sources.push(assetRef);return {assetRef,kind:'media',packaged:true,missingReason:null};
 });
 const artifact={protocolVersion:'craft-artifact/v1',assetId,version,sha256:version,bytes:statSync(join(directory,'project.pcraft')).size,mediaType:'application/x-photocraft',producerTaskId:task.id,sourceRefs:sources,nativeProjectRef:{assetId,version,sha256:version,location:'project.pcraft'},renditions:manifest.outputs.map((output:any)=>ref(output.path)),dependencies,technicalMetadata:{width:native.width,height:native.height},lossReportRef:ref('exchange-loss.json'),evidenceRefs:['native.json','plan.json','operations.json','capabilities.json','capability-checks.json','object-preservation.json','object-assertions.json','native-facts.json','native-facts-preservation.json','font-substitutions.json'].filter(name=>files[name]).map(name=>ref(name)),location:'project.pcraft'};
 validateArtifact(artifact);
 for(const [name,sha]of Object.entries(files))if(fileDigest(within(join(directory,name),directory))!==sha)throw new Error('artifact_file_mismatch: '+name);
 if(fileDigest(manifestPath)!==task.technical.manifestSha256)throw new Error('artifact_manifest_mismatch');
 return artifact;
}
