// 首次启动获取固定发行资源；stdout 仅用于 MCP，诊断写入 stderr。
import {readFile,mkdir,writeFile,rename,rm,mkdtemp,realpath} from 'node:fs/promises';
import {createHash,randomUUID} from 'node:crypto';
import {gunzipSync} from 'node:zlib';
import {dirname,join,resolve,isAbsolute,relative,sep} from 'node:path';
import {homedir} from 'node:os';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
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
async function locateRuntime(){
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
 return runtime;
}
async function main(){
 const here=dirname(fileURLToPath(import.meta.url)),lock=JSON.parse(await readFile(join(here,'runtime.lock.json'),'utf8'));
 if(process.argv.includes('--serve')){
  const runtime=await locateRuntime(),child=spawn(process.execPath,[join(runtime,'adapter.mjs'),...process.argv.slice(2)],{stdio:'inherit'});
  for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>child.kill(signal));
  child.on('exit',code=>{process.exitCode=code??1;});return;
 }
 const catalogBytes=await readFile(join(here,'catalog.lock.json'));if(lock.catalogSha256&&digest(catalogBytes)!==lock.catalogSha256)throw Error('MCP catalog checksum mismatch');
 const catalog=JSON.parse(catalogBytes);
 let child,preparing,initParams,sequence=0;const pending=new Map();
 const emit=value=>process.stdout.write(JSON.stringify({jsonrpc:'2.0',...value})+'\n');
 const send=(method,params)=>new Promise((resolve,reject)=>{
  const id='craft-bootstrap:'+randomUUID()+':'+(++sequence);
  const timer=setTimeout(()=>{pending.delete(id);reject(Error('Editor request timed out'));},180000);
  pending.set(id,{resolve,reject,timer});child.stdin.write(JSON.stringify({jsonrpc:'2.0',id,method,params})+'\n');
 });
 async function engine(){
  if(!preparing)preparing=(async()=>{
   const runtime=await locateRuntime();child=spawn(process.execPath,[join(runtime,'adapter.mjs')],{stdio:['pipe','pipe','inherit'],env:process.env,cwd:process.cwd()});
   child.on('error',error=>{for(const p of pending.values()){clearTimeout(p.timer);p.reject(error);}pending.clear();});
   child.on('exit',()=>{for(const p of pending.values()){clearTimeout(p.timer);p.reject(Error('Editor process exited'));}pending.clear();});
   createInterface({input:child.stdout}).on('line',line=>{
    try{const value=JSON.parse(line),p=pending.get(value.id);if(p&&!value.method){pending.delete(value.id);clearTimeout(p.timer);if(value.error)p.reject(Object.assign(Error(value.error.message),{rpcError:value.error}));else p.resolve(value.result);}else emit(value);}
    catch(error){console.error('Invalid editor protocol output: '+error.message);}
   });
   await send('initialize',initParams);child.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})+'\n');
  })();
  try{await preparing;}catch(error){preparing=null;child?.kill();child=null;throw error;}
 }
 createInterface({input:process.stdin}).on('line',async line=>{
  let request;
  try{
   request=JSON.parse(line);
   if(!request.method){if(child)child.stdin.write(line+'\n');return;}
   if(request.id===undefined){if(child&&request.method!=='notifications/initialized')child.stdin.write(line+'\n');return;}
   const {id,method,params}=request;
   if(method==='initialize'){
    const supported=['2025-11-25','2025-06-18','2025-03-26','2024-11-05'];
    initParams={...params,protocolVersion:supported.includes(params?.protocolVersion)?params.protocolVersion:'2025-03-26'};
    emit({id,result:{protocolVersion:initParams.protocolVersion,serverInfo:{name:lock.name+'-editor',version:lock.version},capabilities:{tools:{},resources:{}}}});return;
   }
   if(!initParams)throw Error('MCP initialization required');
   if(method==='ping'){emit({id,result:{}});return;}
   if(method==='tools/list'){emit({id,result:{tools:catalog.tools}});return;}
   if(method==='resources/list'){emit({id,result:{resources:catalog.resources||[]}});return;}
   if(method==='resources/templates/list'){emit({id,result:{resourceTemplates:catalog.resourceTemplates||[]}});return;}
   await engine();emit({id,result:await send(method,params)});
  }catch(error){emit({id:request?.id??null,error:error.rpcError||{code:-32603,message:error.message}});}
 });
 const close=()=>{child?.kill();process.exit(0);};process.stdin.on('end',close);process.on('SIGINT',close);process.on('SIGTERM',close);
}
if(process.argv[1]&&pathToFileURL(await realpath(process.argv[1])).href===import.meta.url)main().catch(error=>{console.error('Craft editor setup failed: '+error.message);process.exitCode=1;});
