import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import {chromium} from 'playwright-core';
import {mkdtemp,writeFile,readFile,stat,readdir} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import assert from 'node:assert/strict';
for(const name of process.argv.slice(2)){
 const workspace=await mkdtemp(join(tmpdir(),name+'-web-smoke-'));
 const client=new Client({name:'web-smoke',version:'1'});let browser;
 try{
  await client.connect(new StdioClientTransport({command:process.execPath,args:[resolve('../../'+name+'-plugin/ui/dist/adapter.mjs')],env:{...process.env,CRAFT_WORKSPACE_ROOT:workspace},stderr:'inherit'}));
  const opened=await client.callTool({name:'open_browser_editor',arguments:{}});assert(!opened.isError,JSON.stringify(opened));
  browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-unsafe-swiftshader','--use-angle=swiftshader']});
  const page=await browser.newPage({viewport:{width:1280,height:1024}});page.on('pageerror',e=>console.error(name,e.message));
  await page.goto(opened.structuredContent.editorUrl);
  await page.waitForFunction(()=>window.__craftWebAdapter?.ready,null,{timeout:120000});
  const inspected=await client.callTool({name:'inspect',arguments:{}},undefined,{timeout:150000});assert(!inspected.isError,JSON.stringify(inspected));
  const catalogue=name==='lightcraft'?null:await client.callTool({name:'command_list',arguments:{}});
  await writeFile(join(workspace,'commands.json'),JSON.stringify(catalogue,null,2));
  await writeFile(join(workspace,'inspect.json'),JSON.stringify(inspected,null,2));
  const call=async(tool,args={})=>{const r=await client.callTool({name:tool,arguments:args},undefined,{timeout:150000});assert(!r.isError,JSON.stringify(r));return r;};
  if(name==='effectcraft'){
   await call('command_run',{id:'file.newProject',params:{}});
   await call('command_run',{id:'comp.new',params:{name:'Bridge test',width:320,height:240,duration:2}});
   await call('command_run',{id:'layer.newText',params:{text:'Bridge roundtrip',size:24}});
   await call('save_project',{path:'roundtrip.ecproj'});
   assert((await stat(join(workspace,'roundtrip.ecproj'))).size>100);
   await call('command_run',{id:'file.newProject',params:{}});
   await call('open_file',{path:'roundtrip.ecproj'});
   await call('save_project',{path:name==='effectcraft'?'reopened.ecproj':'reopened.fcproj'});
   assert.match(await readFile(join(workspace,name==='effectcraft'?'reopened.ecproj':'reopened.fcproj'),'utf8'),/Bridge/);
  }else if(name==='filmcraft'){
   await call('command_run',{id:'file.newProject',params:{name:'Bridge test'}});
   await call('command_run',{id:'file.newSequence',params:{name:'Bridge sequence',width:320,height:240,fps:24}});
   await call('command_run',{id:'graphics.newText',params:{text:'Bridge roundtrip',size:24,seconds:2}});
   await call('save_project',{path:'roundtrip.fcproj'});
   assert((await stat(join(workspace,'roundtrip.fcproj'))).size>100);
   await call('command_run',{id:'file.newProject',params:{name:'Empty'}});
   await call('open_file',{path:'roundtrip.fcproj'});
   await call('save_project',{path:name==='effectcraft'?'reopened.ecproj':'reopened.fcproj'});
   assert.match(await readFile(join(workspace,name==='effectcraft'?'reopened.ecproj':'reopened.fcproj'),'utf8'),/Bridge/);
  }else{
   await call('command_run',{id:'file.backupLibrary',params:{}});
   await page.waitForFunction(()=>window.__craftLastExport || window.__craftExportError,null,{timeout:45000});
   const files=await readdir(join(workspace,'craft-exports'));assert(files.some(f=>f.endsWith('.zip')));
  }
  await page.screenshot({path:join(workspace,'editor.png')});
  console.log(JSON.stringify({name,workspace,editorReady:true,inspect:true,workspaceSave:true}));
 }finally{await browser?.close();await client.close();}
}
