#!/usr/bin/env python3
"""下载锁定的 OFL 字体作为编译输入；不安装系统字体，不覆盖已有目录。"""
from pathlib import Path
import argparse,json,hashlib,urllib.request
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();ui=Path(__file__).resolve().parent
lock=json.loads((ui/'fonts.lock.json').read_text());out=a.output.resolve()
if out.exists():p.error('output exists; choose a fresh font input directory')
out.mkdir(parents=True)
for entry in lock['files']:
 relative=Path(entry['file'])
 if relative.is_absolute() or '..' in relative.parts:raise ValueError('invalid font path')
 with urllib.request.urlopen(entry['url'],timeout=120) as response:data=response.read(entry['bytes']+1)
 if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:raise ValueError('Font checksum mismatch: '+entry['file'])
 dest=out/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
(out/'fonts/manifest.txt').write_text(lock['manifest']);(out/'fonts/latin-manifest.txt').write_text(lock['latinManifest']);print(out)
