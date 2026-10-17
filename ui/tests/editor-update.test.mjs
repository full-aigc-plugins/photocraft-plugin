import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {selectEditor,unpackZip} from '../editor-update.mjs';
const hash=b=>createHash('sha256').update(b).digest('hex');
function zip(files){let offset=0;const local=[],central=[];for(const [name,text] of Object.entries(files)){const n=Buffer.from(name),b=Buffer.from(text),h=Buffer.alloc(30);h.writeUInt32LE(0x04034b50);h.writeUInt32LE(b.length,18);h.writeUInt32LE(b.length,22);h.writeUInt16LE(n.length,26);local.push(h,n,b);const c=Buffer.alloc(46);c.writeUInt32LE(0x02014b50);c.writeUInt32LE(b.length,20);c.writeUInt32LE(b.length,24);c.writeUInt16LE(n.length,28);c.writeUInt32LE(offset,42);central.push(c,n);offset+=h.length+n.length+b.length;}const cd=Buffer.concat(central),end=Buffer.alloc(22);end.writeUInt32LE(0x06054b50);end.writeUInt16LE(Object.keys(files).length,8);end.writeUInt16LE(Object.keys(files).length,10);end.writeUInt32LE(cd.length,12);end.writeUInt32LE(offset,16);return Buffer.concat([...local,cd,end]);}
async function fixture(){
 const dir=await mkdtemp(join(tmpdir(),'editor-update-')),bundled=join(dir,'bundled');await mkdir(bundled);await writeFile(join(bundled,'tools.json'),'[]');
 const archive=zip({'editor/assets.json':JSON.stringify({name:'photocraft',version:'0.2.3',assets:[{id:'a'.repeat(64)}]}),'editor/server.mjs':'// server','editor/panel.html':'<html/>','editor/tools.json':'[]',['editor/assets/'+'a'.repeat(64)+'.gz']:'asset'});
 const entry={version:'0.2.3',source:{url:'https://github.com/full-aigc-plugins/photocraft-plugin/releases/download/v0.2.3/photocraft-editor-0.2.3.zip',sha256:hash(archive)}};let downloads=0;
 const fetcher=async url=>{if(url.includes('api.github.com'))return new Response(JSON.stringify({tag_name:'v'+entry.version,assets:[{name:'photocraft-editor-'+entry.version+'.zip',browser_download_url:entry.source.url,digest:'sha256:'+entry.source.sha256}]}));downloads++;return new Response(archive);};
 return {options:{name:'photocraft',mode:'enhanced',bundled,bundledVersion:'0.2.2',cacheRoot:join(dir,'cache'),fetcher},entry,archive,downloads:()=>downloads};
}
test('首次打开选择最新完整包，复用缓存且不覆盖内置',async()=>{const f=await fixture();const a=await selectEditor(f.options);assert.equal(a.source,'download');assert.equal(a.version,'0.2.3');assert.equal(await readFile(join(f.options.bundled,'tools.json'),'utf8'),'[]');const b=await selectEditor(f.options);assert.equal(b.source,'cache');assert.equal(f.downloads(),1);});
test('网络失败回退内置并说明原因',async()=>{const f=await fixture();const r=await selectEditor({...f.options,fetcher:async()=>{throw Error('offline');}});assert.equal(r.source,'bundled');assert.match(r.reason,/offline/);});
test('摘要不匹配回退内置',async()=>{const f=await fixture();f.entry.source.sha256='0'.repeat(64);const r=await selectEditor(f.options);assert.equal(r.source,'bundled');assert.match(r.reason,/checksum/);});
test('缓存损坏不能执行',async()=>{const f=await fixture();const a=await selectEditor(f.options);await writeFile(join(a.path,'server.mjs'),'tampered');const b=await selectEditor(f.options);assert.equal(b.source,'bundled');assert.match(b.reason,/cache/);});
test('离线开关不访问网络',async()=>{const f=await fixture();const r=await selectEditor({...f.options,offline:true,fetcher:()=>{throw Error('must not fetch');}});assert.equal(r.source,'bundled');assert.equal(r.reason,'updates disabled');});
test('拒绝压缩包路径逃逸和重复规范化路径',()=>{assert.throws(()=>unpackZip(zip({'../bad':'x'})),/path/);assert.throws(()=>unpackZip(zip({'/bad':'x'})),/path/);});
test('接口发生变化则使用内置',async()=>{const f=await fixture();await writeFile(join(f.options.bundled,'tools.json'),JSON.stringify([{name:'required',inputSchema:{}}]));const r=await selectEditor(f.options);assert.equal(r.source,'bundled');assert.match(r.reason,/tool contract/);});
test('只接受指定官方来源',async()=>{const f=await fixture();f.entry.source.url='https://example.com/attack.zip';const r=await selectEditor(f.options);assert.equal(r.source,'bundled');assert.match(r.reason,/archive/);});

test('官方版本较旧时不降级',async()=>{const f=await fixture();f.entry.version='0.1.0';const r=await selectEditor(f.options);assert.equal(r.source,'bundled');assert.equal(f.downloads(),0);});
test('HTTP 404 和超时均回退',async()=>{const f=await fixture();for(const fetcher of [async()=>new Response('',{status:404}),async(url,options)=>{assert(options.signal instanceof AbortSignal);throw new DOMException('timeout','TimeoutError');}]){const r=await selectEditor({...f.options,fetcher});assert.equal(r.source,'bundled');assert.match(r.reason,/404|timeout/);}});
test('Web 发布包同样校验摘要并完整解包',async()=>{const f=await fixture();const archive=zip({'effectcraft-web/index.html':'<html><head></head></html>','effectcraft-web/app.js':'script','effectcraft-web/app.wasm':'wasm'});const release={tag_name:'v0.10.0',assets:[{name:'effectcraft-web-0.10.0.zip',browser_download_url:'https://github.com/storytold/effectcraft/releases/download/v0.10.0/effectcraft-web-0.10.0.zip',digest:'sha256:'+hash(archive)}]};const fetcher=async url=>new Response(url.includes('api.github.com')?JSON.stringify(release):archive);const r=await selectEditor({...f.options,name:'effectcraft',mode:'web',bundledVersion:'0.9.0',fetcher});assert.equal(r.source,'download');assert.equal(r.version,'0.10.0');assert.match(await readFile(join(r.path,'index.html'),'utf8'),/html/);});
test('缺少摘要不能启用 Web 更新',async()=>{const f=await fixture();const r=await selectEditor({...f.options,name:'effectcraft',mode:'web',fetcher:async()=>new Response(JSON.stringify({tag_name:'v0.10.0',assets:[{name:'effectcraft-web-0.10.0.zip',browser_download_url:'https://github.com/storytold/effectcraft/releases/download/v0.10.0/effectcraft-web-0.10.0.zip'}]}))});assert.equal(r.source,'bundled');assert.match(r.reason,/checksum unavailable/);});
test('自有增强发行包优先，官方原版 Web 不会替换自动化运行时',async()=>{
 const f=await fixture();const files=Object.fromEntries([...unpackZip(f.archive)].map(([p,b])=>[p.replace('photocraft/dist/','editor/'),b]));const archive=zip(files);
 const release={tag_name:'v0.3.0',assets:[{name:'photocraft-editor-0.3.0.zip',browser_download_url:'https://github.com/full-aigc-plugins/photocraft-plugin/releases/download/v0.3.0/photocraft-editor-0.3.0.zip',digest:'sha256:'+hash(archive)}]};
 const requested=[];const fetcher=async url=>{requested.push(url);return new Response(url.includes('api.github.com')?JSON.stringify(release):archive);};
 const r=await selectEditor({...f.options,mode:'enhanced',fetcher});assert.equal(r.source,'download');assert.match(requested[0],/full-aigc-plugins\/photocraft-plugin/);
 release.assets[0].name='photocraft-web-0.3.0.zip';const fallback=await selectEditor({...f.options,mode:'enhanced',fetcher});assert.equal(fallback.source,'bundled');assert.match(fallback.reason,/enhanced/);
});
