#!/usr/bin/env python3
"""将已编译的锁定源码打包为独立增强编辑器；不替换运行中的候选。"""
import argparse,pathlib,json,re,subprocess,shutil,hashlib
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--target-dir',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
ui=pathlib.Path(__file__).resolve().parent;src=a.source.resolve();out=a.output.resolve();lock=json.loads((ui/'source.lock.json').read_text());name=lock['name']
if out.exists():p.error('output exists; use a fresh directory')
html=(src/'apps'/f'{name}-web/index.html').read_text();match=re.search('data-cargo-profile="([^"]+)"',html);profile=match.group(1) if match else 'release'
wasm=a.target_dir.resolve()/'wasm32-unknown-unknown'/profile/(name+'-web.wasm');site=out/'site';site.mkdir(parents=True)
subprocess.run(['wasm-bindgen','--target','web','--out-dir',str(site),'--out-name',name+'-web',str(wasm)],check=True)
html=re.sub(r'<link\b[^>]*data-trunk[^>]*>', '',html)
html=html.replace('</body>',f'<script type="module">import init, * as bindings from "./{name}-web.js"; await init(); window.wasmBindings=bindings;</script></body>');(site/'index.html').write_text(html)
licenses=site/'licenses';licenses.mkdir()
for f in src.iterdir():
 if f.is_file() and f.name.startswith(('LICENSE','NOTICE','ATTRIBUTION')):shutil.copy2(f,licenses/f.name)
for f in ['LICENSE-UPSTREAM','NOTICE.md']:shutil.copy2(ui/'runtime'/f,licenses/f)
for base in ['assets','docs/brand']:
 for f in (src/base).rglob('*') if (src/base).exists() else []:
  if f.is_file() and re.match(r'^(LICENSE|COPYING|NOTICE|OFL)([-.]|$)',f.name,re.I):
   dest=licenses/f.relative_to(src);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
metadata=json.loads(subprocess.check_output(['cargo','metadata','--locked','--format-version','1','--filter-platform','wasm32-unknown-unknown'],cwd=src))
packages={p['id']:p for p in metadata['packages']};nodes={p['id']:p for p in metadata['resolve']['nodes']};visited=set()
def visit(i):
 if i in visited:return
 visited.add(i)
 for dep in nodes.get(i,{}).get('dependencies',[]):visit(dep)
visit(next(p['id'] for p in metadata['packages'] if p['name']==name+'-web'))
notices=[]
for i in sorted(visited):
 pkg=packages[i];folder=pathlib.Path(pkg['manifest_path']).parent;notices.append(f"{pkg['name']} {pkg['version']}\nLicense: {pkg.get('license')}\n{pkg.get('repository') or pkg.get('source') or lock['repository']}\n")
 paths={f for f in folder.iterdir() if f.is_file() and re.match(r'^(LICENSE|COPYING|NOTICE)([-.]|$)',f.name,re.I)}
 if pkg.get('license_file'):paths.add(folder/pkg['license_file'])
 for f in sorted(paths):
  if f.is_file():notices.append(f'--- {f.name} ---\n'+f.read_text(errors='replace'))
(licenses/'THIRD-PARTY-NOTICES.txt').write_text('\n\n'.join(notices))
subprocess.run(['node',str(ui/'runtime/extract-catalog.mjs'),str(site),str(site/'tools.json')],cwd=ui,check=True)
subprocess.run(['node',str(ui/'package-editor.mjs'),str(site),str(out/'editor')],cwd=ui,check=True)
provenance={**lock,'sourceBuild':True,'overlaySha256':hashlib.sha256((ui/'runtime/prepare-automation.py').read_bytes()).hexdigest(),'rustc':subprocess.check_output(['rustc','--version'],text=True).strip(),'wasmBindgen':subprocess.check_output(['wasm-bindgen','--version'],text=True).strip(),'profile':profile,'runtimeAcceptance':'PENDING'}
(out/'build-source.json').write_text(json.dumps(provenance,indent=2)+'\n');build=out/'editor/BUILD.json';build.write_text(json.dumps({**json.loads(build.read_text()),**provenance},indent=2)+'\n');print(out/'editor')
