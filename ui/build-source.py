#!/usr/bin/env python3
"""从锁定源码构建增强 WASM 到独立目录；不安装工具、不修改原源码、不覆盖内置资源。"""
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,tarfile,urllib.request
p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--target-dir',type=pathlib.Path,required=True);p.add_argument('--jobs',default='4');a=p.parse_args()
ui=pathlib.Path(__file__).resolve().parent;lock=json.loads((ui/'source.lock.json').read_text());out=a.output.resolve()
if out.exists():p.error('output exists; use a fresh directory')
for tool in ['cargo','wasm-bindgen','node']:
 if not shutil.which(tool):p.error('Missing '+tool+'; no automatic installation')
out.mkdir(parents=True);src=out/'source';archive=out/'source.tar.gz'
repository=lock['repository'].removesuffix('.git').removeprefix('https://github.com/')
if not re.fullmatch(r'[\w.-]+/[\w.-]+',repository) or not re.fullmatch('[0-9a-f]{40}',lock['commit']):p.error('invalid source pin')
with urllib.request.urlopen('https://codeload.github.com/'+repository+'/tar.gz/'+lock['commit'],timeout=60) as response:archive.write_bytes(response.read())
with tarfile.open(archive) as t:
 top=t.getmembers()[0].name;t.extractall(out/'unpack',filter='data')
(out/'unpack'/top).rename(src)
for filename in lock.get('patches', []):
 if pathlib.Path(filename).name != filename: p.error('invalid patch filename')
 subprocess.run(['git','apply',str(ui/'runtime/patches'/filename)],cwd=src,check=True)
subprocess.run(['python3',str(ui/'runtime/prepare-automation.py'),str(src),lock['name']],check=True)
env={**os.environ,'CARGO_TARGET_DIR':str(a.target_dir.resolve()),'CARGO_INCREMENTAL':'0'}
fonts=out/'font-input'
subprocess.run(['python3',str(ui/'fetch-fonts.py'),'--output',str(fonts)],check=True)
subprocess.run(['python3',str(ui/'runtime/prepare-fonts.py'),str(src),lock['name']],check=True)
env.update(CRAFT_FONTS_DIR=str(fonts),CRAFT_FONTS_REQUIRED='1',CRAFT_CJK_FONT=str(fonts/'fonts/LXGWWenKai-Regular.ttf'))
html=(src/'apps'/f"{lock['name']}-web"/'index.html').read_text()
match=re.search('data-cargo-profile="([^"]+)"',html);profile=match.group(1) if match else 'release'
subprocess.run(['cargo','build','--target','wasm32-unknown-unknown','--profile',profile,'-p',lock['name']+'-web','-j',a.jobs],cwd=src,env=env,check=True)
subprocess.run(['python3',str(ui/'finalize-source.py'),'--source',str(src),'--target-dir',str(a.target_dir.resolve()),'--output',str(out/'packaged')],env=env,check=True)
