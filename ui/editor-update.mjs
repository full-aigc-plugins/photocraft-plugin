// 首次打开时获取最新兼容完整编辑器包；失败保留内置版本，绝不热替换活动工程。
import {readFile,writeFile,mkdir,mkdtemp,rename,rm,lstat} from 'node:fs/promises';
import {join,dirname} from 'node:path';
import {homedir} from 'node:os';
import {createHash} from 'node:crypto';
import {inflateRawSync} from 'node:zlib';
const digest=b=>createHash('sha256').update(b).digest('hex');
const MAX_ARCHIVE=160*1024*1024,MAX_EXPANDED=768*1024*1024;

// 仅支持发行包使用的普通 ZIP store/deflate；拒绝 ZIP64、加密、符号链接和路径逃逸。
export function unpackZip(buffer){
 let end=-1;
 for(let i=buffer.length-22;i>=Math.max(0,buffer.length-65557);i--)if(buffer.readUInt32LE(i)===0x06054b50&&i+22+buffer.readUInt16LE(i+20)===buffer.length){end=i;break;}
 if(end<0)throw Error('Invalid ZIP directory');
 const count=buffer.readUInt16LE(end+10);let offset=buffer.readUInt32LE(end+16),total=0;
 if(count===65535||count>20000||buffer.readUInt16LE(end+4)||buffer.readUInt16LE(end+6)||buffer.readUInt16LE(end+8)!==count||offset+buffer.readUInt32LE(end+12)!==end)throw Error('Unsupported ZIP directory');
 const files=new Map(),paths=new Set();
 for(let i=0;i<count;i++){
  if(offset+46>end||buffer.readUInt32LE(offset)!==0x02014b50)throw Error('Invalid ZIP entry');
  const flags=buffer.readUInt16LE(offset+8),method=buffer.readUInt16LE(offset+10),packed=buffer.readUInt32LE(offset+20),size=buffer.readUInt32LE(offset+24),n=buffer.readUInt16LE(offset+28),extra=buffer.readUInt16LE(offset+30),comment=buffer.readUInt16LE(offset+32),mode=buffer.readUInt32LE(offset+38)>>>16,local=buffer.readUInt32LE(offset+42);
  const name=buffer.subarray(offset+46,offset+46+n).toString('utf8');offset+=46+n+extra+comment;
  const parts=name.replace(/\/$/,'').split('/');
  if(offset>end||!name||name.includes('\\')||name.includes('\0')||parts.some(p=>!p||p==='.'||p==='..'||p.includes(':'))||paths.has(name))throw Error('Unsafe ZIP path');paths.add(name);
  if((mode&0xf000)===0xa000||(flags&1)||![0,8].includes(method))throw Error('Unsupported ZIP entry');
  if(name.endsWith('/'))continue;
  total+=size;if(total>MAX_EXPANDED)throw Error('Expanded ZIP too large');
  if(local+30>buffer.length||buffer.readUInt32LE(local)!==0x04034b50)throw Error('Invalid ZIP local header');
  const start=local+30+buffer.readUInt16LE(local+26)+buffer.readUInt16LE(local+28);
  if(start+packed>buffer.readUInt32LE(end+16))throw Error('Truncated ZIP');
  const raw=buffer.subarray(start,start+packed),data=method===0?raw:inflateRawSync(raw,{maxOutputLength:Math.max(1,size)});
  if(data.length!==size)throw Error('ZIP length mismatch');files.set(name,data);
 }
 return files;
}
async function download(url,limit,timeout,fetcher){
 const response=await fetcher(url,{signal:AbortSignal.timeout(timeout),headers:{'User-Agent':'full-aigc-craft-editor','Accept':'application/json, application/octet-stream'}});
 if(!response.ok)throw Error(`Download HTTP ${response.status}`);
 if(Number(response.headers.get('content-length'))>limit)throw Error('Download too large');
 let n=0;const chunks=[];for await(const chunk of response.body){n+=chunk.length;if(n>limit)throw Error('Download too large');chunks.push(chunk);}return Buffer.concat(chunks);
}
async function latest(name,mode,fetcher){
 if(mode==='enhanced'){
  const plugin=name==='pdfcraft'?'printcraft':name;
  const repository=`full-aigc-plugins/${plugin}-plugin`;
  const release=JSON.parse(await download(`https://api.github.com/repos/${repository}/releases/latest`,8*1024*1024,5000,fetcher));
  const version=release.tag_name?.replace(/^v/,'');
  if(release.draft||release.prerelease||!/^\d+\.\d+\.\d+$/.test(version))throw Error('No stable enhanced release');
  const asset=release.assets?.find(a=>a.name===`${name}-editor-${version}.zip`);
  if(!asset?.browser_download_url?.startsWith(`https://github.com/${repository}/releases/download/`))throw Error('Missing compatible enhanced archive');
  return {version,url:asset.browser_download_url,sha256:asset.digest?.replace(/^sha256:/,''),prefix:'editor/'};
 }

 const release=JSON.parse(await download(`https://api.github.com/repos/storytold/${name}/releases/latest`,8*1024*1024,5000,fetcher));
 const version=release.tag_name?.replace(/^v/,'');
 if(release.draft||release.prerelease||!/^\d+\.\d+\.\d+$/.test(version))throw Error('No stable Web release');
 const asset=release.assets?.find(a=>a.name===`${name}-web-${version}.zip`);
 if(!asset?.browser_download_url?.startsWith(`https://github.com/storytold/${name}/releases/download/`))throw Error('Missing official Web archive');
 return {version,url:asset.browser_download_url,sha256:asset.digest?.replace(/^sha256:/,''),prefix:null};
}
const canonical=v=>Array.isArray(v)?v.map(canonical):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):v;
async function validate(files,name,mode,bundled){
 if(mode==='enhanced'){
  for(const file of ['assets.json','server.mjs','panel.html','tools.json'])if(!files.has(file))throw Error('Incomplete editor bundle');
  const info=JSON.parse(files.get('assets.json'));if(info.name!==name)throw Error('Editor identity mismatch');
  if(!info.assets?.length||info.assets.some(a=>!/^\w{64}$/.test(a.id)||!files.has('assets/'+a.id+'.gz')))throw Error('Missing WASM/JS assets');
  const old=JSON.parse(await readFile(join(bundled,'tools.json'),'utf8')),next=JSON.parse(files.get('tools.json'));
  for(const t of old){const found=next.find(x=>x.name===t.name);if(!found||JSON.stringify(canonical(found.inputSchema))!==JSON.stringify(canonical(t.inputSchema)))throw Error('Incompatible tool contract');}
 }else{
  const html=files.get('index.html')?.toString();if(!html||!html.includes('</head>')||![...files.keys()].some(p=>p.endsWith('.wasm'))||![...files.keys()].some(p=>p.endsWith('.js')))throw Error('Incomplete Web/WASM bundle');
 }
}
export async function selectEditor({name,mode,bundled,bundledVersion,cacheRoot=process.env.CRAFT_EDITOR_CACHE_DIR||join(homedir(),'.cache/full-aigc/editors'),offline=process.env.CRAFT_EDITOR_UPDATE==='off',fetcher=fetch}){
 const fallback=reason=>({path:bundled,source:'bundled',version:bundledVersion,reason});
 if(offline)return fallback('updates disabled');
 let staging;
 try{
  const release=await latest(name,mode,fetcher);
  const numbers=v=>v.split('.').slice(0,3).map(x=>parseInt(x,10));
  const a=numbers(release.version),b=numbers(bundledVersion);let older=false;
  for(let i=0;i<3;i++){if(a[i]!==b[i]){older=a[i]<b[i];break;}}
  if(older)return fallback('official release is older than bundled');
  if(!/^[0-9a-f]{64}$/.test(release.sha256))throw Error('Official archive checksum unavailable');
  const dir=join(cacheRoot,name);await mkdir(dir,{recursive:true,mode:0o700});
  const archivePath=join(dir,release.sha256+'.zip');let archive,cached=false;
  try{archive=await readFile(archivePath);if(digest(archive)!==release.sha256)throw Error('cache checksum mismatch');cached=true;}catch(e){if(e.code!=='ENOENT')throw e;}
  if(!archive){archive=await download(release.url,MAX_ARCHIVE,45000,fetcher);if(digest(archive)!==release.sha256)throw Error('Archive checksum mismatch');}
  const all=unpackZip(archive);let prefix=release.prefix;
  if(prefix===null){const entries=[...all.keys()].filter(x=>/^[^/]+\/index\.html$/.test(x));if(entries.length!==1)throw Error('Unexpected Web archive root');prefix=entries[0].slice(0,-'index.html'.length);}
  const files=new Map([...all].filter(([p])=>p.startsWith(prefix)).map(([p,b])=>[p.slice(prefix.length),b]));
  await validate(files,name,mode,bundled);
  const dest=join(dir,release.sha256);
  try{
   if(!(await lstat(dest)).isDirectory()||(await lstat(dest)).isSymbolicLink())throw Error('Invalid cache directory');
   for(const [p,b] of files){const f=join(dest,p);if((await lstat(f)).isSymbolicLink()||digest(await readFile(f))!==digest(b))throw Error('cache file checksum mismatch');}
  }catch(e){
   if(e.code!=='ENOENT')throw e;
   // A missing file inside an existing cache is corruption, not a successful cached release.
   try{await lstat(dest);throw Error('Incomplete cache');}catch(check){if(check.code!=='ENOENT')throw check;}
   staging=await mkdtemp(join(dir,'.download-'));
   for(const [p,b] of files){const out=join(staging,p);await mkdir(dirname(out),{recursive:true});await writeFile(out,b,{flag:'wx'});}
   try{await rename(staging,dest);staging=null;}catch(e){if(!['EEXIST','ENOTEMPTY'].includes(e.code))throw e;throw Error('Concurrent update; retry next session');}
  }
  if(!cached)await writeFile(archivePath,archive,{flag:'wx'}).catch(e=>{if(e.code!=='EEXIST')throw e;});
  return {path:dest,source:cached?'cache':'download',version:release.version,url:release.url,sha256:release.sha256};
 }catch(e){return fallback(e.message);}finally{if(staging)await rm(staging,{recursive:true,force:true});}
}
