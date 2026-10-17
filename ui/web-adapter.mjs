// 官方 Web 发行版的薄适配：命令在可见页面执行，文件仍由工作区边界管理。
import {Server} from '@modelcontextprotocol/sdk/server/index.js';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import {ListToolsRequestSchema,CallToolRequestSchema,ListResourcesRequestSchema,ReadResourceRequestSchema} from '@modelcontextprotocol/sdk/types.js';
import {readFile,writeFile,realpath,mkdir} from 'node:fs/promises';
import {createServer} from 'node:http';
import {randomBytes,randomUUID} from 'node:crypto';
import {dirname,join,resolve,relative,isAbsolute,extname,basename,sep} from 'node:path';
import {fileURLToPath} from 'node:url';
import {authorizeRequest,workspacePath} from './security.mjs';
const here=dirname(fileURLToPath(import.meta.url));
const config=JSON.parse(await readFile(join(here,'config.json'),'utf8'));
let workspace=workspacePath(process.env.CRAFT_WORKSPACE_ROOT||process.cwd());
const token=randomBytes(32).toString('hex'), jobs=new Map(), queue=[];
let origin, attached=0, opened=false, activePage=null;
const ok=value=>({content:[{type:'text',text:JSON.stringify(value??null)}],structuredContent:typeof value==='object'&&value!==null&&!Array.isArray(value)?value:{value:value??null}});
const fail=e=>({isError:true,content:[{type:'text',text:e.message||String(e)}]});
async function scoped(path,writing=false){
 if(typeof path!=='string'||!path||isAbsolute(path))throw Error('Use a workspace-relative path');
 const root=await realpath(workspace), candidate=resolve(root,path), rel=relative(root,candidate);
 if(rel==='..'||rel.startsWith('..'+sep)||isAbsolute(rel))throw Error('Path escapes workspace');
 if(writing) {
  // 逐级校验已有父目录后再创建，不沿外部符号链接写入。
  let current=root;
  for(const part of relative(root,dirname(candidate)).split(sep).filter(Boolean)){
   current=join(current,part);await mkdir(current,{recursive:true});
   const actual=await realpath(current), r=relative(root,actual);
   if(r==='..'||r.startsWith('..'+sep)||isAbsolute(r))throw Error('Symlink escapes workspace');
  }
  return candidate;
 }
 const actual=await realpath(candidate), r=relative(root,actual);
 if(r==='..'||r.startsWith('..'+sep)||isAbsolute(r))throw Error('Symlink escapes workspace');return actual;
}
async function dispatch(action,args={}){
 if(Date.now()-attached>15000)throw Error('Open the editor page and wait for editor_status.ready before executing commands');
 if(jobs.size>=16)throw Error('Editor queue full');
 return new Promise((accept,reject)=>{
  const id=randomUUID();const timer=setTimeout(()=>{jobs.delete(id);const index=queue.findIndex(x=>x.id===id);if(index>=0)queue.splice(index,1);reject(Error('Editor operation timed out; state is uncertain. Inspect before retrying.'));},120000);
  jobs.set(id,{accept,reject,timer});queue.push({id,action,args});
 });
}
const schemas={
 open_editor:{workspace:{type:'string'},path:{type:'string'}},open_browser_editor:{workspace:{type:'string'},path:{type:'string'}},
 editor_status:{},command_list:{},command_run:{id:{type:'string'},params:{type:'object'}},inspect:{},
 open_file:{path:{type:'string'}},save_project:{path:{type:'string'}},
 save_file:{source:{type:'string'},path:{type:'string'}},list_files:{},screenshot:{}
};
const descriptions={open_editor:'Open the real Web editor. Set the absolute workspace before the first open. The page must load before commands work.',open_browser_editor:'Return the same session URL for the host built-in browser.',editor_status:'Check whether the Web editor is alive and ready.',command_list:'List current engine commands. LightCraft does not expose this API; use its pinned command reference.',command_run:'Execute an actual engine command by id and parameters, in the visible editor.',inspect:'Inspect the current visible editor or LightCraft library.',open_file:'Import a workspace-relative file into the visible editor.',save_project:'Save the editable project to a NEW workspace path. LightCraft uses the upstream library backup command instead.',save_file:'Copy an existing browser virtual file to a NEW workspace path.',list_files:'List files held by the actual browser editor.',screenshot:'Capture the actual editor canvas as a PNG.'};
async function call(name,args={}){
 if(name==='open_editor'||name==='open_browser_editor'){
  if(args.workspace && resolve(args.workspace)!==workspace){if(opened)throw Error('Save and close this instance before changing workspace');workspace=await realpath(workspacePath(args.workspace));}
  opened=true;const result={editor:config.name,workspace,editorUrl:`${origin}/${token}/app/`,ready:Date.now()-attached<15000};
  if(args.path)result.openAfterReady={tool:'open_file',arguments:{path:args.path}};return ok(result);
 }
 if(name==='editor_status')return ok({editor:config.name,workspace,ready:Date.now()-attached<15000});
 if(name==='open_file'){
  const data=await readFile(await scoped(args.path));if(data.length>50*1024*1024)throw Error('Input exceeds 50 MiB');
  return ok(await dispatch('open_file',{name:basename(args.path),data:data.toString('base64')}));
 }
 if(name==='save_project'||name==='save_file'){
  const target=await scoped(args.path,true);
  const result=await dispatch(name,args);if(!result?.base64)throw Error('Editor returned no file');
  const bytes=Buffer.from(result.base64,'base64');if(bytes.length>50*1024*1024)throw Error('Output exceeds 50 MiB');
  await writeFile(target,bytes,{flag:'wx'});return ok({path:target,bytes:bytes.length});
 }
 if(!(name in schemas))throw Error('Unknown tool');
 const result=await dispatch(name,args);
 if(name==='screenshot')return {content:[{type:'image',mimeType:'image/png',data:result.base64}]};
 return ok(result);
}
async function body(req){let n=0;const chunks=[];for await(const c of req){n+=c.length;if(n>72*1024*1024)throw Error('Request too large');chunks.push(c);}return JSON.parse(Buffer.concat(chunks).toString());}
const http=createServer(async(req,res)=>{
 try{
  const path=new URL(req.url,'http://127.0.0.1').pathname;const [,provided,...rest]=path.split('/');
  if(!authorizeRequest(req,origin,token,provided)){res.writeHead(403).end();return;}
  const route=rest.join('/');res.setHeader('Cache-Control','no-store');res.setHeader('Referrer-Policy','no-referrer');
  if(req.method==='GET' && route==='poll'){
   const page=req.headers['x-craft-page'];
   if(!page || (activePage && activePage!==page && Date.now()-attached<15000)){res.writeHead(409).end('Editor already has an active page');return;}
   activePage=page;attached=Date.now();res.setHeader('Content-Type','application/json');res.end(JSON.stringify(queue.shift()||null));
  } else if(req.method==='POST' && route==='reply'){
   if(req.headers['x-craft-page']!==activePage)throw Error('Inactive editor page');
   const {id,result,error}=await body(req), pending=jobs.get(id);
   if(pending){jobs.delete(id);clearTimeout(pending.timer);error?pending.reject(Error(error)):pending.accept(result);}
   res.end('{}');
  } else if(req.method==='POST' && route==='download'){
   const {name,data}=await body(req);const bytes=Buffer.from(data,'base64');if(bytes.length>50*1024*1024)throw Error('Export exceeds 50 MiB');
   const target=await scoped(`craft-exports/${randomUUID().slice(0,8)}-${basename(name||'export').replace(/[^\p{L}\p{N}._ -]/gu,'_')}`,true);
   await writeFile(target,bytes,{flag:'wx'});res.setHeader('Content-Type','application/json');res.end(JSON.stringify({path:target}));
  } else if(req.method==='GET'&&route==='connect.js'){
   res.setHeader('Content-Type','text/javascript');res.end(`const application=${JSON.stringify(config.name)};\n`+await readFile(join(here,'web-connect.js'),'utf8'));
  } else if(req.method==='GET'&&route.startsWith('app/')){
   const rel=decodeURIComponent(route.slice(4))||'index.html';const root=resolve(here,'editor'), file=resolve(root,rel);
   if(!file.startsWith(root+sep))throw Error('Invalid asset path');
   const actual=await realpath(file);if(!actual.startsWith(root+sep))throw Error('Invalid asset target');
   if(rel==='sw.js'){res.writeHead(404).end();return;}
   const types={'.html':'text/html','.js':'text/javascript','.wasm':'application/wasm','.svg':'image/svg+xml','.png':'image/png','.otf':'font/otf','.woff2':'font/woff2','.json':'application/json'};
   res.setHeader('Content-Type',types[extname(file)]||'application/octet-stream');
   let data=await readFile(file);
   if(rel==='index.html')data=Buffer.from(data.toString().replace('</head>','<script type="module" src="../connect.js"></script></head>'));
   res.end(data);
  }else{res.writeHead(404).end();}
 }catch(e){res.writeHead(400,{'Content-Type':'application/json'}).end(JSON.stringify({error:e.message}));}
});
await new Promise(r=>http.listen(0,'127.0.0.1',r));origin=`http://127.0.0.1:${http.address().port}`;
const uri=`ui://${config.name}/panel.html`;
const metadata={ui:{resourceUri:uri,visibility:['model','app'],csp:{frameDomains:[origin],resourceDomains:[origin],connectDomains:[origin]}}};
const server=new Server({name:config.name+'-editor',version:'0.1.0'},{capabilities:{tools:{},resources:{}}});
server.setRequestHandler(ListToolsRequestSchema,async()=>({tools:Object.entries(schemas).map(([name,properties])=>({name,description:descriptions[name],inputSchema:{type:'object',properties,...(['command_run'].includes(name)?{required:['id']}:['open_file','save_project'].includes(name)?{required:['path']}:name==='save_file'?{required:['source','path']}:{})},...(name==='open_editor'?{_meta:metadata}:{})}))}));
server.setRequestHandler(CallToolRequestSchema,async({params})=>{try{return await call(params.name,params.arguments);}catch(e){return fail(e);}});
server.setRequestHandler(ListResourcesRequestSchema,async()=>({resources:[{uri,name:'editor',mimeType:'text/html;profile=mcp-app',_meta:metadata}]}));
server.setRequestHandler(ReadResourceRequestSchema,async({params})=>{
 if(params.uri!==uri)throw Error('Unknown resource');
 return {contents:[{uri,mimeType:'text/html;profile=mcp-app',_meta:metadata,text:`<!doctype html><style>html,body,iframe{width:100%;height:100%;margin:0;border:0}</style><iframe src="${origin}/${token}/app/" allow="autoplay; fullscreen"></iframe><script type="module">${await readFile(join(here,'web-panel.js'),'utf8')}</script>`}]};
});
async function close(){for(const p of jobs.values()){clearTimeout(p.timer);p.reject(Error('Editor closed'));}http.closeAllConnections();http.close();process.exit(0);}
process.on('SIGTERM',close);process.on('SIGINT',close);
if(process.argv.includes('--serve'))console.log(JSON.stringify((await call('open_editor')).structuredContent));
else{process.stdin.on('end',close);await server.connect(new StdioServerTransport());}
