// 从真实清单解析入口，在含空格的搬迁目录、无关工作目录启动。
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import {readFile,mkdtemp,writeFile,realpath} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import assert from 'node:assert/strict';
const root=resolve(process.argv[2]),results=[];
assert(root.includes(' '),'test installation must include spaces');
const names='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split(' ');
for(const name of names){
 const plugin=join(root,name+'-plugin');
 for(const [host,file] of [['standard','mcp.json'],['claude','.mcp.json'],['codex','.codex-plugin/mcp.json']]){
  const config=JSON.parse(await readFile(join(plugin,file),'utf8')).mcpServers[name+'-editor'];
  const workspace=await mkdtemp(join(tmpdir(),'craft task '));
  const expand=value=>value.replaceAll('${PLUGIN_ROOT}',plugin).replaceAll('${CLAUDE_PLUGIN_ROOT}',plugin);
  const client=new Client({name:'portable-entry-smoke',version:'1'});
  try{
   await client.connect(new StdioClientTransport({command:config.command,args:config.args.map(expand),cwd:config.cwd?resolve(plugin,config.cwd):workspace,env:{...process.env,...config.env,CRAFT_EDITOR_UPDATE:'off'},stderr:'inherit'}));
   assert((await client.listTools()).tools.some(t=>t.name==='open_browser_editor'));
   const opened=await client.callTool({name:'open_browser_editor',arguments:{workspace}});
   assert(!opened.isError,JSON.stringify(opened));
   assert.equal(await realpath(opened.structuredContent.workspace),await realpath(workspace),'task workspace must not become plugin installation directory');
   const response=await fetch(opened.structuredContent.editorUrl);assert.equal(response.status,200);
   const resources=await client.listResources();assert(resources.resources.some(r=>r.mimeType==='text/html;profile=mcp-app'));
   results.push({plugin:name,host,stdioStartup:true,workspaceProvided:true,mcpAppsResource:true});
  }finally{await client.close();}
 }
}
await writeFile(process.argv[3],JSON.stringify(results,null,2)+'\n');console.log(`${results.length} relocated manifest entry handshakes passed (host path semantics simulated, no installation)`);
