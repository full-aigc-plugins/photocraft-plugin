// 只从明确指定的、锁定摘要的编辑器制品导入；不修改来源，不联网安装。
import {readFile, readdir, cp, mkdir, access} from 'node:fs/promises';
import {join,resolve} from 'node:path';
import {createHash} from 'node:crypto';
const source=process.argv[2];
if(!source)throw Error('Usage: node prepare.mjs /absolute/editor/dist');
const lock=JSON.parse(await readFile('editor.lock.json','utf8'));
for(const [path,expected] of Object.entries(lock.files)){
 const data=await readFile(join(resolve(source),path));
 if(createHash('sha256').update(data).digest('hex')!==expected)throw Error(`Editor checksum mismatch: ${path}`);
}
const assets=JSON.parse(await readFile(join(source,'assets.json'),'utf8'));
if(assets.name!==lock.name || assets.upstream.commit!==lock.upstream.commit)throw Error('Editor identity mismatch');
try{await access('dist/editor');throw Error('dist/editor already exists; use a fresh build destination rather than replacing a live editor');}catch(e){if(e.code!=='ENOENT')throw e;}
await mkdir('dist',{recursive:true});
// 仅复制清单文件，避免把不受校验的额外内容带入制品。
for(const path of Object.keys(lock.files)){const dest=join('dist/editor',path);await mkdir(resolve(dest,'..'),{recursive:true});await cp(join(source,path),dest);}
console.log(`Prepared ${lock.name}: ${Object.keys(lock.files).length} verified files`);
