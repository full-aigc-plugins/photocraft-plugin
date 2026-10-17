// 独立解压目录启动，证明运行时不需要源码目录或 node_modules。
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import {mkdtemp,writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import assert from 'node:assert/strict';
const root=resolve(process.argv[2]);const results=[];
for(const name of (process.argv.slice(4).length?process.argv.slice(4):'cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split(' '))) {
 const c=new Client({name:'packed-smoke',version:'1'});
 try{
  const cwd=await mkdtemp(join(tmpdir(),'packed-'+name+'-'));
  await c.connect(new StdioClientTransport({command:process.execPath,args:[join(root,name+'-plugin/ui/dist/adapter.mjs')],cwd,env:{PATH:process.env.PATH,CRAFT_WORKSPACE_ROOT:cwd,CRAFT_EDITOR_UPDATE:'off'},stderr:'inherit'}));
  const listed=await c.listTools();assert(listed.tools.some(t=>t.name==='open_browser_editor'));
  const r=await c.callTool({name:'open_browser_editor',arguments:{}});assert(!r.isError,JSON.stringify(r));
  const resources=await c.listResources();
  const panel=resources.resources.find(x=>x.mimeType==='text/html;profile=mcp-app');assert(panel,'Missing MCP Apps resource');
  const content=await c.readResource({uri:panel.uri});assert(content.contents.some(x=>x.mimeType==='text/html;profile=mcp-app'&&x.text?.includes('<script')));
  const response=await fetch(r.structuredContent.editorUrl);assert.equal(response.status,200);assert.match(await response.text(),/html/i);
  results.push({plugin:name,isolatedMcpStartup:true,tools:listed.tools.length,mcpAppsResource:true,pageServed:true});
 }finally{await c.close();}
}
await writeFile(resolve(process.argv[3]),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results));
