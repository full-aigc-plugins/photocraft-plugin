import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {runInNewContext} from 'node:vm';

const source=await readFile(new URL('../runtime/client.mjs',import.meta.url),'utf8');
// 执行实际客户端的通知函数，隔离 WASM 与 MCP，不复制通知实现。
const message=source.match(/^function message\(value, error = false\) \{[\s\S]*?^\}/m)?.[0];
assert.ok(message,'client notice function must be available');
function show(value,error,{loaded=false,lastExport=null}={}){
  const context={loaded,lastExport,status:{textContent:'',dataset:{}},notice:{hidden:false},retry:{hidden:true},value,error};
  runInNewContext(message+'\nmessage(value,error);',context);
  return context;
}
test('startup loading does not add a second overlay above the engine loader',()=>{
  assert.equal(show('正在加载编辑器…',false).notice.hidden,true);
});
test('errors remain visible before and after editor readiness',()=>{
  for(const loaded of [false,true]){
    const result=show('编辑器启动失败',true,{loaded});
    assert.equal(result.notice.hidden,false);
    assert.equal(result.status.textContent,'编辑器启动失败');
    assert.equal(result.retry.hidden,true);
  }
});
test('failed exports retain retry while normal messages clear the overlay',()=>{
  const failed=show('保存失败',true,{loaded:true,lastExport:{name:'drawing.dxf'}});
  assert.equal(failed.retry.hidden,false);
  const recovered=show('就绪',false,{loaded:true,lastExport:{name:'drawing.dxf'}});
  assert.equal(recovered.notice.hidden,true);
  assert.equal(recovered.retry.hidden,true);
});

// 使用真实打包器构建最小站点，验证交付 HTML，而不把夹具 WASM 当作引擎实测。
test('source package starts quiet and preserves the engine loader',async t=>{
  const {mkdtemp,mkdir,writeFile,rm,readFile}=await import('node:fs/promises');
  const {tmpdir}=await import('node:os');
  const {join,dirname}=await import('node:path');
  const {fileURLToPath}=await import('node:url');
  const {promisify}=await import('node:util');
  const {execFile}=await import('node:child_process');
  const ui=dirname(fileURLToPath(new URL('../package.json',import.meta.url)));
  const root=await mkdtemp(join(tmpdir(),'craft-notice-package-'));
  t.after(()=>rm(root,{recursive:true,force:true}));
  const site=join(root,'site'),out=join(root,'editor');
  await mkdir(join(site,'licenses'),{recursive:true});
  await writeFile(join(site,'licenses/fixture.txt'),'Test fixture, no third-party engine');
  await writeFile(join(site,'index.html'),'<!doctype html><html><head></head><body><div id="engine-loading">Loading engine fixture...</div><script type="module">import init from "./engine.js"; init();</script></body></html>');
  await writeFile(join(site,'engine.js'),'export default async function init() {}');
  await writeFile(join(site,'engine.wasm'),Buffer.from([0,97,115,109,1,0,0,0]));
  await writeFile(join(site,'tools.json'),'[]');
  await promisify(execFile)(process.execPath,[join(ui,'package-editor.mjs'),site,out],{cwd:ui});
  const panel=await readFile(join(out,'panel.html'),'utf8');
  assert.equal(/<div id="craft-notice" hidden>/.test(panel),true,'notice must be hidden before client initialization');
  assert.equal(panel.includes('<div id="engine-loading">Loading engine fixture...</div>'),true,'preserve engine loader');
  const scripts=[...panel.matchAll(/<script\b[^>]*type=["']module["'][^>]*>([\s\S]*?)<\/script>/gi)];
  assert.equal(scripts.length,1,'bundle one actual client module');
  assert.ok(scripts[0][1].length>1000,'client must actually be bundled');
});
