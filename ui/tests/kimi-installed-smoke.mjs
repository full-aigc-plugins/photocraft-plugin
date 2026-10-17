// 对 Kimi 原生安装后的包执行真实 stdio 工具调用；不冒充模型路由测试。
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import {readFile,mkdtemp,writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import assert from 'node:assert/strict';
const [home,binary,output]=process.argv.slice(2),results=[];
for(const name of 'cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split(' ')){
 const root=join(resolve(home),'plugins/managed',name);
 const config=JSON.parse(await readFile(join(root,'kimi.plugin.json'),'utf8')).mcpServers[name+'-editor'];
 const client=new Client({name:'installed-package-acceptance',version:'1'});
 try{
  await client.connect(new StdioClientTransport({command:binary,args:['__plugin_run_node',...config.args],cwd:root,env:{...process.env,KIMI_CODE_HOME:resolve(home),KIMI_PLUGIN_ROOT:root,CRAFT_EDITOR_UPDATE:'off'},stderr:'inherit'}));
  const tools=await client.listTools();assert(tools.tools.some(t=>t.name==='editor_status'));
  const status=await client.callTool({name:'editor_status',arguments:{}});assert(!status.isError);
  const workspace=await mkdtemp(join(tmpdir(),'craft acceptance '));
  const opened=await client.callTool({name:'open_browser_editor',arguments:{workspace}});assert(!opened.isError,JSON.stringify(opened));
  assert.equal((await fetch(opened.structuredContent.editorUrl)).status,200);
  results.push({name,installedManifest:true,kimiNativeNodeFallback:true,toolCount:tools.tools.length,status:true,openBrowserEditor:true,routeAccessible:true,modelRouting:false});
  console.log(name,'passed');
 }finally{await client.close();}
}
await writeFile(output,JSON.stringify(results,null,2)+'\n');
