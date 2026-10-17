// 首次启动获取固定发行资源；stdout 仅用于 MCP，诊断写入 stderr。
import {readFile,mkdir,writeFile,rename,rm,mkdtemp} from 'node:fs/promises';
import {createHash,randomUUID} from 'node:crypto';
import {gunzipSync} from 'node:zlib';
import {dirname,join,resolve,isAbsolute,relative,sep} from 'node:path';
import {homedir} from 'node:os';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
const digest=b=>createHash('sha256').update(b).digest('hex');
function safePath(root,name){
 if(!name||name.includes('\\')||name.includes(':')||name.includes('\0')||isAbsolute(name)||name.split('/').includes('..'))throw Error('Unsafe runtime path: '+name);
 const p=resolve(root,name),rel=relative(root,p);if(rel==='..'||rel.startsWith('..'+sep)||isAbsolute(rel))throw Error('Runtime escapes cache');return p;
}
/** 只展开普通文件和目录；拒绝链接、特殊条目及逃逸路径。 */
export async function extractRuntime(bytes,root){
 const tar=gunzipSync(bytes,{maxOutputLength:512*1024*1024});let offset=0;
 while(offset+512<=tar.length){
  const h=tar.subarray(offset,offset+512);if(h.every(b=>b===0))return;
  const str=(start,len)=>h.subarray(start,start+len).toString('utf8').split('\0')[0];
  const recorded=parseInt(str(148,8).trim(),8);let actual=0;for(let i=0;i<512;i++)actual+=i>=148&&i<156?32:h[i];if(recorded!==actual)throw Error('Invalid tar checksum');
  const prefix=str(345,155),name=(prefix?prefix+'/':'')+str(0,100),p=safePath(root,name);
  const size=parseInt(str(124,12).trim()||'0',8),type=str(156,1);if(!Number.isSafeInteger(size)||size<0||offset+512+size>tar.length)throw Error('Invalid tar size');
  if(type==='5')await mkdir(p,{recursive:true});
  else if(type==='0'||type===''){await mkdir(dirname(p),{recursive:true});await writeFile(p,tar.subarray(offset+512,offset+512+size),{flag:'wx'});}
  else throw Error('Unsupported tar entry type: '+type);
  offset+=512+Math.ceil(size/512)*512;
 }
 throw Error('Truncated runtime archive');
}
/** 每次启动复核文件哈希，损坏缓存不会被执行。 */
export async function verifyRuntime(root,files){
 try{for(const [name,hash]of Object.entries(files)){if(digest(await readFile(safePath(root,name)))!==hash)return false;}return Object.keys(files).length>0;}catch{return false;}
}
async function download(lock){
 if(!/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+\/releases\/download\//.test(lock.url)||!(/^[a-f0-9]{64}$/.test(lock.sha256)))throw Error('Invalid pinned runtime lock');
 const response=await fetch(lock.url,{signal:AbortSignal.timeout(90000)});if(!response.ok)throw Error('Runtime download HTTP '+response.status);
 const chunks=[];let size=0;for await(const chunk of response.body){size+=chunk.length;if(size>256*1024*1024)throw Error('Runtime archive exceeds 256 MiB');chunks.push(chunk);}
 const bytes=Buffer.concat(chunks);if(digest(bytes)!==lock.sha256)throw Error('Runtime archive SHA-256 mismatch');return bytes;
}
async function main(){
 const here=dirname(fileURLToPath(import.meta.url));const lock=JSON.parse(await readFile(join(here,'runtime.lock.json'),'utf8'));
 let runtime=join(here,'dist');
 if(!(await verifyRuntime(runtime,lock.files))){
  const base=join(process.env.LOCALAPPDATA||join(homedir(),'.cache'),'full-aigc-plugins',lock.name);await mkdir(base,{recursive:true});
  runtime=join(base,lock.sha256);
  if(!(await verifyRuntime(runtime,lock.files))){
   console.error(`[${lock.name}] Downloading pinned editor ${lock.version}; first launch may take up to 90 seconds.`);
   const temp=await mkdtemp(join(base,'download-'));
   try{
    await extractRuntime(await download(lock),temp);if(!(await verifyRuntime(temp,lock.files)))throw Error('Runtime file checksum mismatch');
    try{await rename(temp,runtime);}catch(error){if(!(await verifyRuntime(runtime,lock.files))){throw error;}}
   }finally{await rm(temp,{recursive:true,force:true});}
  }
 }
 const child=spawn(process.execPath,[join(runtime,'adapter.mjs'),...process.argv.slice(2)],{stdio:'inherit',env:process.env,cwd:process.cwd()});
 for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>child.kill(signal));
 child.on('error',error=>{console.error(error.message);process.exitCode=1;});child.on('exit',(code)=>{process.exitCode=code??1;});
}
if(process.argv[1]&&pathToFileURL(resolve(process.argv[1])).href===import.meta.url)main().catch(error=>{console.error('Craft editor setup failed: '+error.message);process.exitCode=1;});
