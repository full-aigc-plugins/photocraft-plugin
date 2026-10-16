import {build} from 'esbuild';
import {mkdir} from 'node:fs/promises';
await mkdir('dist',{recursive:true});
await build({entryPoints:['adapter.mjs'],outfile:'dist/adapter.mjs',bundle:true,platform:'node',format:'esm',target:'node24',banner:{js:'import {createRequire as __createRequire} from "node:module"; const require=__createRequire(import.meta.url);'},legalComments:'linked'});
await build({entryPoints:['host.mjs'],outfile:'dist/host.js',bundle:true,platform:'browser',format:'esm',target:'chrome120',legalComments:'linked'});
