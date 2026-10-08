import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, realpathSync, rmSync, writeFileSync, mkdirSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
test('artifact mapping binds files and parent, survives relocation, rejects mixed preview',async()=>{
 const { mapArtifact }=await import('../src/protocol/artifact.ts');const root=realpathSync(mkdtempSync(join(tmpdir(),'photo-artifact-')));
 const sha=(text:string)=>createHash('sha256').update(text).digest('hex');
 try {
  const dir=join(root,'bundle');mkdirSync(dir);const contents={'project.pcraft':'native','design.png':'preview','exchange-loss.json':'{}','native.json':'{"width":32,"height":32,"layers":[]}', 'plan.json':'{}','capabilities.json':'{}','operations.json':'[]'};
  const files:Record<string,string>={};for(const [name,body]of Object.entries(contents)){writeFileSync(join(dir,name),body);files[name]=sha(body);}
  const manifest=JSON.stringify({schema:'photocraft-delivery/v1',files,outputs:[{path:'design.png'}],assets:{},runtimeSha256:'a'.repeat(64)});writeFileSync(join(dir,'manifest.json'),manifest);
  const task={id:'task-one',request:{output:dir,plan:{}},technical:{status:'PASS',manifestSha256:sha(manifest),projectSha256:files['project.pcraft'],previewSha256:files['design.png']}};
  const artifact=mapArtifact(task);assert.equal(artifact.producerTaskId,task.id);assert.equal(artifact.version,files['project.pcraft']);assert.equal(artifact.renditions[0].sha256,files['design.png']);
  const {validateArtifact}=await import('../src/protocol/artifact.ts');
  for(const name of ['constructor','toString','__proto__'])assert.throws(()=>validateArtifact(JSON.parse(JSON.stringify(artifact).slice(0,-1)+',"'+name+'":1}')),/contract_unknown_field/);
  const inherited=Object.create(artifact);assert.throws(()=>validateArtifact(inherited),/contract_required/);
  const moved=join(root,'moved');const { cpSync }=await import('node:fs');cpSync(dir,moved,{recursive:true});assert.deepEqual(mapArtifact(task,undefined,moved),artifact);
  writeFileSync(join(moved,'design.png'),'other-round');assert.throws(()=>mapArtifact(task,undefined,moved),/artifact_file_mismatch/);
  assert.throws(()=>mapArtifact({...task,request:{...task.request,parentTask:'missing'}}),/parent_artifact_required/);
  assert.throws(()=>mapArtifact({...task,id:'child',request:{...task.request,parentTask:task.id,plan:{expectedProjectSha256:'f'.repeat(64)}}},artifact),/parent_version_conflict/);
 }finally{rmSync(root,{recursive:true,force:true});}
});
test('fixed public contract rejects unknown keys rather than adding competing schema',async()=>{
 const { validateArtifact }=await import('../src/protocol/artifact.ts');assert.throws(()=>validateArtifact({protocolVersion:'craft-artifact/v1',newField:1}),/contract_required|contract_unknown_field/);
});
