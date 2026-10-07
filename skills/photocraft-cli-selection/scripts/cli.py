#!/usr/bin/env python3
"""从当前独立技能安装/核验固定 CLI，然后按 argv 调用；不依赖 PATH 或兄弟技能。"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
ALLOWED={'--version', 'batch', 'droplet', 'help', 'info', 'mcp', 'convert', 'commands', 'run', 'serve'}
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--runtime-home',default=os.environ.get('CRAFT_RUNTIME_HOME',str(Path.home()/'.local/share/craft-runtimes')))
 parser.add_argument('--archive',type=Path)
 parser.add_argument('arguments',nargs=argparse.REMAINDER)
 args=parser.parse_args();argv=args.arguments
 if argv[:1]==['--']:argv=argv[1:]
 if not argv or argv[0] not in ALLOWED:parser.error('unsupported_cli_subcommand: put the native subcommand first after --')
 installation_completed=False
 try:
  path=Path(__file__).with_name('bootstrap.py');spec=importlib.util.spec_from_file_location('craft_bootstrap',path)
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  installed=module.install(json.loads(path.with_name('runtime.lock.json').read_text()),args.runtime_home,args.archive)
  installation_completed=True
  result=subprocess.run([installed['executable'],*argv],timeout=600)
  return result.returncode
 except (ValueError,OSError,subprocess.SubprocessError) as error:
  reply={'error':str(error),'result':'unknown' if isinstance(error,subprocess.TimeoutExpired) else 'failed'}
  if not installation_completed and 'module' in locals():reply['dependencySetup']=module.setup_failure(args.runtime_home)
  print(json.dumps(reply));return 1
if __name__=='__main__':raise SystemExit(main())
