"""按固定官方DMG安装桌面应用；与CLI缓存分离，不启动或覆盖用户应用。"""
import argparse,fcntl,hashlib,json,os,platform,plistlib,re,shutil,subprocess,tempfile
from pathlib import Path

def sha(path):
 with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def validate(lock):
 if not isinstance(lock,dict) or lock.get('schema')!='craft-desktop-lock/v1':raise ValueError('invalid_desktop_lock')
 domain=lock.get('domain');version=lock.get('version')
 if domain not in ('filmcraft','effectcraft','photocraft','vectorcraft') or not isinstance(version,str) or not re.fullmatch(r'\d+\.\d+\.\d+',version):raise ValueError('invalid_desktop_identity')
 filename=f'{domain}-{version}-macos-universal.dmg';expected=f'https://github.com/storytold/{domain}/releases/download/v{version}/{filename}'
 if lock.get('url')!=expected or lock.get('filename')!=filename:raise ValueError('untrusted_desktop_url')
 for key in ('archiveSha256','binarySha256'):
  if not isinstance(lock.get(key),str) or not re.fullmatch('[a-f0-9]{64}',lock[key]):raise ValueError('invalid_desktop_digest')
 if type(lock.get('bytes')) is not int or not 0<lock['bytes']<200_000_000:raise ValueError('invalid_desktop_size')
 for key in ('app','executable'):
  if not isinstance(lock.get(key),str) or not lock[key] or '/' in lock[key] or '\\' in lock[key] or lock[key] in ('.','..'):raise ValueError('invalid_desktop_bundle')
 if not lock['app'].endswith('.app') or lock.get('bundleIdentifier')!='ai.storyteller.'+domain:raise ValueError('invalid_desktop_bundle')
 return lock

def tree(app):
 result={}
 for path in sorted(app.rglob('*')):
  name=str(path.relative_to(app))
  if path.is_symlink():
   if not path.resolve().is_relative_to(app.resolve()):raise ValueError('external_desktop_symlink')
   result[name]={'symlink':os.readlink(path)}
  elif path.is_file():result[name]={'sha256':sha(path)}
 return result

def inspect(directory,lock):
 if directory.is_symlink() or not directory.is_dir():raise ValueError('invalid_desktop_install')
 app=directory/lock['app']
 if app.is_symlink() or not app.is_dir():raise ValueError('invalid_desktop_bundle')
 for path in (app/'Contents/Info.plist',app/'Contents/MacOS'/lock['executable']):
  if path.is_symlink() or not path.is_file():raise ValueError('invalid_desktop_payload')
 info=plistlib.loads((app/'Contents/Info.plist').read_bytes());binary=app/'Contents/MacOS'/lock['executable']
 if info.get('CFBundleShortVersionString')!=lock['version'] or info.get('CFBundleIdentifier')!=lock['bundleIdentifier'] or info.get('CFBundleExecutable')!=lock['executable'] or sha(binary)!=lock['binarySha256']:raise ValueError('desktop_identity_mismatch')
 if 'arm64' not in subprocess.check_output(['/usr/bin/lipo','-archs',str(binary)],text=True).split():raise ValueError('desktop_architecture_mismatch')
 subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True,capture_output=True,timeout=60)
 return {'app':str(app),'executable':str(binary),'version':lock['version'],'binarySha256':lock['binarySha256'],'files':tree(app)}

def install(lock,runtime_home,archive=None,platform_key=None):
 validate(lock);key=platform_key or platform.system().lower()+'-'+platform.machine().lower()
 if key!='darwin-arm64':raise ValueError('unsupported_platform: '+key)
 home=Path(runtime_home).expanduser().absolute()
 if home.is_symlink():raise ValueError('desktop_home_symlink')
 home.mkdir(parents=True,exist_ok=True);home=home.resolve();parent=home/(lock['domain']+'-desktop')
 if parent.is_symlink():raise ValueError('desktop_namespace_symlink')
 parent.mkdir(mode=0o700,exist_ok=True);guard=parent/'.install.lock'
 fd=os.open(guard,os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'r+') as stream:
  fcntl.flock(stream,fcntl.LOCK_EX);destination=parent/lock['version']
  if destination.exists() or destination.is_symlink():
   actual=inspect(destination,lock);receipt=destination/'receipt.json'
   if receipt.is_symlink() or not receipt.is_file():raise ValueError('desktop_receipt_missing')
   stored=json.loads(receipt.read_text())
   if stored.get('lock')!=lock or stored.get('files')!=actual['files']:raise ValueError('desktop_install_mutated')
   return {k:v for k,v in actual.items() if k!='files'}|{'reused':True,'scope':'signed app installation only; launch/GUI acceptance separate'}
  with tempfile.TemporaryDirectory(prefix='.desktop-',dir=parent) as td:
   stage=Path(td);source=Path(archive) if archive else stage/lock['filename']
   if archive is None:
    subprocess.run(['/usr/bin/curl','--fail','--location','--proto','=https','--retry','3','--max-time','180','--max-filesize',str(lock['bytes']+1),'--output',str(source),lock['url']],check=True,capture_output=True,timeout=240)
   if source.is_symlink() or not source.is_file() or source.stat().st_size!=lock['bytes'] or sha(source)!=lock['archiveSha256']:raise ValueError('archive_identity_mismatch')
   mount=stage/'mount';mount.mkdir();payload=stage/'payload';payload.mkdir();attached=False
   try:
    subprocess.run(['/usr/bin/hdiutil','attach','-readonly','-nobrowse','-mountpoint',str(mount),str(source.resolve())],check=True,capture_output=True,timeout=60);attached=True;apps=list(mount.glob('*.app'))
    if len(apps)!=1 or apps[0].name!=lock['app'] or apps[0].is_symlink():raise ValueError('desktop_bundle_inventory_mismatch')
    shutil.copytree(apps[0],payload/lock['app'],symlinks=True);actual=inspect(payload,lock)
    (payload/'receipt.json').write_text(json.dumps({'schema':'craft-desktop-install/v1','lock':lock,'files':actual['files']},indent=2)+'\n')
   finally:
    if attached:subprocess.run(['/usr/bin/hdiutil','detach',str(mount)],check=True,capture_output=True,timeout=60)
   os.replace(payload,destination)
  actual=inspect(destination,lock)
  return {k:v for k,v in actual.items() if k!='files'}|{'reused':False,'scope':'signed app installation only; launch/GUI acceptance separate'}

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['install','run']);parser.add_argument('plan',nargs='?',type=Path);parser.add_argument('--output',type=Path);parser.add_argument('--input',action='append',default=[]);parser.add_argument('--runtime-home',type=Path,default=Path.home()/'.local/share/craft-runtimes');parser.add_argument('--archive',type=Path,help='可选固定本地DMG；仍执行全部摘要校验');args=parser.parse_args();lock=json.loads(Path(__file__).with_name('desktop.lock.json').read_text())
 try:
  if args.command=='install':
   if args.plan or args.output or args.input:raise ValueError('unexpected_install_arguments')
   result=install(lock,args.runtime_home,args.archive)
  else:
   if not args.plan or not args.output or args.archive:raise ValueError('run_requires_plan_output_and_pinned_public_install')
   import importlib.util
   spec=importlib.util.spec_from_file_location('craft_owned_desktop',Path(__file__).with_name('desktop_session.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);inputs={}
   for item in args.input:
    name,separator,value=item.partition('=')
    if not separator or name in inputs:raise ValueError('invalid_or_duplicate_input')
    inputs[name]=value
   plan=module.read_plan(args.plan)
   result=module.run(plan,args.output,args.runtime_home,inputs)
  print(json.dumps(result,allow_nan=False))
  if result.get('result','PASS')!='PASS':raise SystemExit(1)
 except KeyboardInterrupt:parser.exit(130,'desktop_workflow_interrupted: outcome receipt preserved; request not replayed\n')
 except (ValueError,OSError,subprocess.SubprocessError) as error:parser.exit(1,'desktop_install_failed: '+type(error).__name__+': '+str(error)+'\n')
if __name__=='__main__':main()
