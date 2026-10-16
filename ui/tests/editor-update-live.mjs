import {selectEditor} from '../editor-update.mjs';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
const names='photocraft figcraft cadcraft designcraft vectorcraft deckcraft printcraft soundcraft gridcraft wordcraft effectcraft filmcraft lightcraft'.split(' '),results=[];
const cacheRoot=resolve('../../../full-aigc-plugins/.local/editor-update-cache');
async function worker(){for(;;){const pkg=names.shift();if(!pkg)return;const ui=resolve('../../'+pkg+'-plugin/ui');const lock=JSON.parse(await readFile(ui+'/editor.lock.json','utf8'));const start=Date.now();const r=await selectEditor({name:lock.name,mode:lock.mode==='web-api'?'web':'enhanced',bundled:ui+'/dist/editor',bundledVersion:lock.mode==='web-api'||lock.buildKind==='full-aigc-enhanced'?lock.version:'0.0.0',cacheRoot});const result={plugin:pkg,...r,ms:Date.now()-start};results.push(result);console.log(JSON.stringify(result));}}
await Promise.all([worker(),worker(),worker()]);
await writeFile(resolve('../../../full-aigc-plugins/.local/editor-update-live.json'),JSON.stringify(results,null,2)+'\n');
