// Uses upstream acceptance scenarios; see UPSTREAM-LICENSE.txt.
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import {chromium} from 'playwright-core';
import {automationSmoke} from './upstream-automation-smoke.mjs';
import {mkdtemp,mkdir,writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import assert from 'node:assert/strict';
const results=[];
for(const name of process.argv.slice(2)){
 const pkg=name==='pdfcraft'?'printcraft':name;
 const dir=process.env.CRAFT_TEST_REPOSITORIES?resolve(process.env.CRAFT_TEST_REPOSITORIES,pkg+'-plugin/ui/dist'):resolve('../../'+pkg+'-plugin/ui/dist');
 const workspace=await mkdtemp(join(tmpdir(),name+'-suite-'));await mkdir(join(workspace,'mcp'));
 const client=new Client({name:'suite-smoke',version:'1'});let browser;
 try{
  await client.connect(new StdioClientTransport({command:process.execPath,args:[join(dir,'adapter.mjs')],env:{...process.env,CRAFT_WORKSPACE_ROOT:workspace},stderr:'inherit'}));
  const opened=await client.callTool({name:'open_browser_editor',arguments:{}});assert(!opened.isError,JSON.stringify(opened));
  browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-unsafe-swiftshader','--use-angle=swiftshader']});
  const page=await browser.newPage({viewport:{width:1280,height:1024}});
  await page.goto(opened.structuredContent.editorUrl);await page.waitForTimeout(800);
  const frame=page.frames().find(f=>f.url().includes('/panel'));
  const actual=await automationSmoke({client,frame,name,workspace,catalogPath:join(dir,'editor/tools.json')});
  await page.screenshot({path:join(workspace,'editor.png')});
  results.push({name,workspace,pass:true,...actual});console.log(JSON.stringify(results.at(-1)));
 }catch(e){results.push({name,workspace,pass:false,error:e.message});console.log(JSON.stringify(results.at(-1)));}
 finally{await browser?.close();await client.close();}
}
await writeFile(process.env.CRAFT_TEST_RESULTS||'/tmp/craft-suite-results.json',JSON.stringify(results,null,2));
if(results.some(r=>!r.pass))process.exitCode=1;
