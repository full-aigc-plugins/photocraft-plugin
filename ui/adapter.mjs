// 同一 MCP 服务连接原生 Apps 面板和宿主浏览器；不复制编辑器命令引擎。
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { ListToolsRequestSchema, CallToolRequestSchema, ListResourcesRequestSchema, ReadResourceRequestSchema, ListResourceTemplatesRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { readFile, realpath, mkdir, writeFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { randomBytes, randomUUID } from 'node:crypto';
import { basename, dirname, join, resolve, relative, isAbsolute, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { authorizeRequest, workspacePath } from './security.mjs';
import {selectEditor} from './editor-update.mjs';
import {withPanelMetadata} from './panel-metadata.mjs';
const panelMetadata = process.env.CRAFT_PANEL_METADATA_FILE
 ? JSON.parse(await readFile(process.env.CRAFT_PANEL_METADATA_FILE, 'utf8')) : {};

const here=dirname(fileURLToPath(import.meta.url));
let config=JSON.parse(await readFile(join(here,'editor/assets.json'),'utf8'));
const bundled=join(here,'editor');
let editorRoot=bundled, runtime={source:'bundled',version:config.version,reason:'not checked'}, selection;
async function prepareEditor(){
 if(used)return;
 if(!selection)selection=(async()=>{
  runtime=await selectEditor({name:config.name,mode:'enhanced',bundled,bundledVersion:config.buildKind==='full-aigc-enhanced'?config.version:'0.0.0'});
  if(runtime.path!==editorRoot){if(connecting)await connecting;if(client)await client.close();client=null;catalog=null;editorRoot=runtime.path;config=JSON.parse(await readFile(join(editorRoot,'assets.json'),'utf8'));}
 })();
 await selection;
}
let workspace=workspacePath(process.env.CRAFT_WORKSPACE_ROOT || process.cwd());
let client, connecting, http, origin, editorAttached=false, used=false, latestResult, catalog, browserOwner, browserToken, lastPoll=0;
const token=randomBytes(32).toString('hex');
const events=new Set();
const notify=(data)=>{for(const res of events) res.write(`data: ${JSON.stringify(data)}\n\n`);};
async function upstream() {
 if (client) return client;
 if (!connecting) connecting=(async()=>{
  const transport=new StdioClientTransport({command:'node',args:[join(editorRoot,'server.mjs')],cwd:workspace,env:{...process.env,CRAFT_WORKSPACE_ROOT:workspace},stderr:'inherit'});
  const next=new Client({name:'craft-editor-adapter',version:'0.1.0'});
  try{await next.connect(transport,{timeout:5000});}catch(e){await next.close().catch(()=>{});throw e;} client=next; return next;
 })().finally(()=>{connecting=null;});
 return connecting;
}
async function selectWorkspace(value) {
 if (!value || resolve(value)===workspace) return;
 if(used || editorAttached) throw Error('当前编辑器已有会话；请保存并结束该 MCP 实例，再连接另一工作区。');
 const selected=await realpath(workspacePath(value));
 if(connecting) await connecting;
 if(client) await client.close();
 client=null; catalog=null; workspace=selected;
}
async function tool(params, fromPage=false, pageId=null) {
 const {workspace:requested,...args}=params.arguments || {};
 if (params.name==='open_editor' || params.name==='open_browser_editor') {
  if(fromPage) throw Error('页面不能切换工作区');
  await selectWorkspace(requested);
  await prepareEditor();
  let result;
  try{result=await (await upstream()).callTool({name:'open_editor',arguments:args},undefined,{timeout:180000});}
  catch(e){
   if(editorRoot===bundled || used)throw e;
   await client?.close();client=null;catalog=null;editorRoot=bundled;config=JSON.parse(await readFile(join(bundled,'assets.json'),'utf8'));
   runtime={source:'bundled',version:config.version,reason:'Downloaded server startup failed: '+e.message};
   result=await (await upstream()).callTool({name:'open_editor',arguments:args},undefined,{timeout:180000});
  }
  if(result.isError) return result;
  runtime={...runtime,upstream:config.upstream,buildKind:config.buildKind||'craft-derived-bundled'};
  used=true; latestResult=result;
  const url=await browserUrl();
  const enriched={...result, content:[...result.content,{type:'text',text:`Editor page: ${url}\nWorkspace: ${workspace}\n页面需要加载完成后才能编辑；请调用 editor_status 检查。`}],structuredContent:{...result.structuredContent,editorUrl:url,workspace,runtime}};
  notify({type:'tool-result',result});
  return enriched;
 }
 if(params.name==='editor_status') return {content:[{type:'text',text:JSON.stringify({editor:config.name,workspace,attached:editorAttached && Date.now()-lastPoll<45000,runtime})}],structuredContent:{editor:config.name,workspace,attached:editorAttached && Date.now()-lastPoll<45000,runtime}};
 used=true;
 const result=await (await upstream()).callTool(params,undefined,{timeout:180000});
 if(params.name==='_editor_attach' && !result.isError) {editorAttached=true;lastPoll=Date.now();if(fromPage){browserOwner=pageId;browserToken=result.structuredContent.token;}}
 if(params.name==='_editor_poll' && !result.isError)lastPoll=Date.now();
 if(params.name==='_editor_detach' && !result.isError) editorAttached=false;
 return result;
}
async function tools() {
 const result=await (await upstream()).listTools(); catalog=new Set(result.tools.map(t=>t.name));
 return {tools:[...result.tools.map(t=>t.name==='open_editor'?{...t,inputSchema:{...t.inputSchema,properties:{...t.inputSchema.properties,workspace:{type:'string',description:'Absolute workspace path; set before opening an editor session.'}}}}:t),
 {name:'open_browser_editor',description:'Open the same editor session in the host built-in browser. Use the returned editorUrl with the host browser tool. Does not itself render the page.',inputSchema:{type:'object',properties:{workspace:{type:'string'},path:{type:'string'}}}},
 {name:'editor_status',description:'Report whether the actual editor has attached to this MCP session.',inputSchema:{type:'object',properties:{}},annotations:{readOnlyHint:true}}]};
}
async function body(req) {
 let size=0; const parts=[];
 for await(const chunk of req) {size+=chunk.length;if(size>72*1024*1024) throw Error('Request exceeds 72 MiB');parts.push(chunk);}
 return JSON.parse(Buffer.concat(parts).toString('utf8'));
}
async function saveDownload(params) {
 const saved=[];
 for(const item of params.contents || []) {
  const r=item.resource;
  if(item.type!=='resource' || typeof r?.blob!=='string') throw Error('Only embedded binary exports are supported');
  const bytes=Buffer.from(r.blob,'base64'); if(bytes.length>50*1024*1024) throw Error('Export exceeds 50 MiB');
  const name=basename(r.name || decodeURIComponent(new URL(r.uri).pathname)).replace(/[^\p{L}\p{N}._ -]/gu,'_') || 'export';
  const folder=join(workspace,'craft-exports'); await mkdir(folder,{recursive:true});
  const actual=await realpath(folder), rel=relative(await realpath(workspace),actual);
  if(isAbsolute(rel)||rel==='..'||rel.startsWith('..'+sep)) throw Error('Export directory escapes workspace');
  const path=join(actual,`${randomUUID().slice(0,8)}-${name}`);
  await writeFile(path,bytes,{flag:'wx'}); saved.push(path);
 }
 if(!saved.length) throw Error('No export received');
 notify({type:'saved',paths:saved}); return {isError:false};
}
async function browserUrl() {
 if(http) return `${origin}/${token}/`;
 http=createServer(async(req,res)=>{
  try {
   const url=new URL(req.url,'http://127.0.0.1');
   const [,provided,...pieces]=url.pathname.split('/');
   if(!authorizeRequest(req,origin,token,provided)){res.writeHead(403).end('Forbidden');return;}
   const route=pieces.join('/');
   res.setHeader('Cache-Control','no-store');res.setHeader('Referrer-Policy','no-referrer');res.setHeader('X-Content-Type-Options','nosniff');
   if(req.method==='GET' && route==='') {
    res.setHeader('Content-Type','text/html; charset=utf-8');
    res.end(`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>${config.title}</title><style>html,body{margin:0;width:100%;height:100%;background:#20242b;color:#ddd;font:13px system-ui}header{height:32px;display:flex;align-items:center;padding:0 12px;gap:18px}iframe{width:100%;height:calc(100% - 32px);border:0}#status{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}</style><header><b>${config.title}</b><span id="status">正在连接编辑器…</span></header><iframe sandbox="allow-scripts allow-same-origin" allow="autoplay; fullscreen"></iframe><script type="module" src="host.js"></script></html>`);
   } else if(req.method==='GET' && route==='host.js') {res.setHeader('Content-Type','text/javascript');res.end(await readFile(join(here,'host.js')));
   } else if(req.method==='GET' && route==='panel') {
    const result=await (await upstream()).readResource({uri:`ui://${config.name}/panel.html`});
    res.setHeader('Content-Type','text/html');
    res.setHeader('Content-Security-Policy',"default-src 'none'; script-src 'self' 'unsafe-inline' blob: data: 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; media-src 'self' data: blob:; worker-src 'self' blob:; connect-src 'none'; frame-src 'none'; base-uri 'self'; form-action 'none'");
    res.end(result.contents[0].text);
   } else if(req.method==='GET' && route==='events') {
    res.writeHead(200,{'Content-Type':'text/event-stream','Connection':'keep-alive'});res.write(': connected\n\n');events.add(res);req.on('close',()=>events.delete(res));
   } else if(req.method==='POST' && route==='detach') {
    const {pageId}=await body(req);
    if(pageId===browserOwner && browserToken){await tool({name:'_editor_detach',arguments:{token:browserToken}},true,pageId);browserOwner=null;browserToken=null;}
    res.end('{}');
   } else if(req.method==='POST' && route==='rpc') {
    const {method,params}=await body(req);let result;
    if(method==='readResource') {
     if(!params?.uri?.startsWith(`ui://${config.name}/`)) throw Error('Resource outside editor');
     result=await (await upstream()).readResource(params);
    } else if(method==='callTool') {
     if(!catalog) await tools();
     if(!catalog.has(params?.name) || params.name==='open_editor') throw Error('Unknown page tool');
     result=await tool(params,true,req.headers['x-craft-page']);
    } else if(method==='downloadFile') result=await saveDownload(params);
    else if(method==='initial') result=latestResult || {content:[],structuredContent:{editor:config.name}};
    else throw Error('Unsupported bridge method');
    res.setHeader('Content-Type','application/json');res.end(JSON.stringify(result));
   } else {res.writeHead(404).end('Not found');}
  } catch(error) {if(!res.headersSent)res.writeHead(400,{'Content-Type':'application/json'});res.end(JSON.stringify({error:error.message}));}
 });
 await new Promise((accept,reject)=>{http.once('error',reject);http.listen(0,'127.0.0.1',accept);});
 origin=`http://127.0.0.1:${http.address().port}`;
 return `${origin}/${token}/`;
}
const server=new Server({name:`${config.name}-editor`,version:'0.1.0'},{capabilities:{tools:{},resources:{}}});
server.setRequestHandler(ListToolsRequestSchema,tools);
server.setRequestHandler(CallToolRequestSchema,async({params})=>{try{return await tool(params);}catch(e){return {isError:true,content:[{type:'text',text:e.message}]};}});
server.setRequestHandler(ListResourcesRequestSchema,async(p)=>withPanelMetadata(await (await upstream()).listResources(p.params), panelMetadata));
server.setRequestHandler(ListResourceTemplatesRequestSchema,async(p)=>(await upstream()).listResourceTemplates(p.params));
server.setRequestHandler(ReadResourceRequestSchema,async(p)=>withPanelMetadata(await (await upstream()).readResource(p.params), panelMetadata));
let closing=false;
async function close(){if(closing)return;closing=true;for(const r of events)r.end();http?.closeAllConnections();http?.close();await client?.close();process.exit(0);}
process.on('SIGINT',close);process.on('SIGTERM',close);
if(process.argv.includes('--serve')) {
 latestResult=await tool({name:'open_editor',arguments:{}});
 console.log(JSON.stringify({editor:config.name,workspace,editorUrl:await browserUrl(),runtime}));
} else {
 process.stdin.on('end',close);
 await server.connect(new StdioServerTransport());
}
