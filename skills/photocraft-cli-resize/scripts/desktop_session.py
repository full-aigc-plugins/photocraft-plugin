"""独立技能拥有桌面和 MCP 生命周期；只关闭本次启动的进程，不重放未知编辑。"""
import importlib.util,json,os,platform,re,secrets,socket,subprocess,tempfile,time
from pathlib import Path

def load(name):
 spec=importlib.util.spec_from_file_location('craft_desktop_'+name,Path(__file__).with_name(name+'.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def owned_listener(process,port):
 result=subprocess.run(['/usr/sbin/lsof','-nP','-a','-p',str(process.pid),'-iTCP:'+str(port),'-sTCP:LISTEN','-Fn'],capture_output=True,text=True,timeout=3)
 return result.returncode==0 and ('n127.0.0.1:'+str(port)) in result.stdout.splitlines()

class OwnedSession:
 def __init__(self,argv,desktop,domain,output,port,token_file=None):
  self.argv=argv;self.desktop=desktop;self.domain=domain;self.output=Path(output);self.port=port;self.token_file=token_file;self.process=None;self.session=None;self.log=None;self.stopped=False;self.listener_verified=False
 def __enter__(self):
  args=[self.desktop['executable'],'--control',str(self.port)];env=dict(os.environ);data=self.output/'.desktop-data';data.mkdir(mode=0o700)
  if self.domain=='filmcraft':args+=['--empty','--no-recover','--data-dir',str(data)]
  elif self.domain=='effectcraft':args+=['--empty'];env['EFFECTCRAFT_CONFIG_DIR']=str(data)
  elif self.domain=='photocraft':
   env['PHOTOCRAFT_CONFIG_DIR']=str(data);args+=['--control-token-file',str(self.token_file),'--automation-read-root',str(self.output),'--automation-write-root',str(self.output)]
  elif self.domain=='vectorcraft':env['VECTORCRAFT_NO_PREFS']='1';env['VECTORCRAFT_NO_NATIVE_MENU']='1'
  else:raise ValueError('unsupported_desktop_domain')
  try:
   self.log=(self.output/'desktop.log').open('w');self.process=subprocess.Popen(args,env=env,stdout=self.log,stderr=subprocess.STDOUT);deadline=time.monotonic()+45
   while time.monotonic()<deadline:
    if self.process.poll() is not None:raise RuntimeError('desktop_start_failed: '+str(self.process.returncode))
    if owned_listener(self.process,self.port):self.listener_verified=True;break
    time.sleep(.2)
   else:raise TimeoutError('desktop_start_timeout: no owned loopback listener')
   self.session=load('mcp_session').Session(self.argv);return self
  except BaseException:
   self.close();raise
 def request(self,*args):return self.session.request(*args)
 def close(self):
  try:
   if self.session:self.session.close()
  finally:
   if self.process and self.process.poll() is None:
    self.process.terminate()
    try:self.process.wait(timeout=15)
    except subprocess.TimeoutExpired:self.process.kill();self.process.wait(timeout=15)
   self.stopped=self.process is None or self.process.poll() is not None
   if self.log:self.log.close()
 def __exit__(self,*args):self.close()

def read_plan(path):
 """计划与原生回复使用相同的严格 JSON 规则，拒绝重复键和非有限值。"""
 return load("commands").reply_json(Path(path).read_text())

def run(plan,output,runtime_home=None,inputs=None):
 commands=load('commands');inputs=inputs or {};commands.validate(plan,inputs)
 if any(not isinstance(k,str) or not re.fullmatch(r'[a-zA-Z][\w-]*',k) or k=='output' for k in inputs):raise ValueError('invalid_input_name')
 for name,path in inputs.items():
  p=Path(path)
  if p.is_symlink() or not p.is_file():raise ValueError('invalid_input_file: '+name)
 output=Path(output).absolute()
 if output.exists() or output.is_symlink():raise ValueError('output_exists')
 if not output.parent.is_dir():raise ValueError('output_parent_missing')
 if platform.system().lower()+'-'+platform.machine().lower()!='darwin-arm64':raise ValueError('unsupported_desktop_platform')
 home=runtime_home or os.environ.get('CRAFT_RUNTIME_HOME',str(Path.home()/'.local/share/craft-runtimes'));desktop={};sessions=[]
 def install(lock,home):
  desktop.update(load('desktop').install(json.loads(Path(__file__).with_name('desktop.lock.json').read_text()),home));return load('bootstrap').install(lock,home)
 with tempfile.TemporaryDirectory(prefix='craft-desktop-session-') as private:
  token=None
  if commands.DOMAIN=='photocraft':
   token=Path(private)/'control-token';token.write_text(secrets.token_hex(32));token.chmod(0o600)
  with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
  def factory(argv):
   session=OwnedSession(argv,desktop,commands.DOMAIN,output,port,token);sessions.append(session);return session
  interrupted=False
  try:
   receipt=commands.execute(plan,output,home,'bridge','127.0.0.1:'+str(port),str(token) if token else None,installer=install,session_factory=factory,inputs=inputs)
  except KeyboardInterrupt:
   if not output.is_dir():raise
   interrupted=True
   try:receipt=commands.reply_json((output/'journal.json').read_text())
   except (OSError,ValueError):receipt={'schema':'craft-command-receipt/v1','steps':[]}
   receipt['result']='unknown';receipt['error']='interrupted: request not replayed'
   if receipt.get('steps') and receipt['steps'][-1].get('state')=='started':receipt['steps'][-1]['state']='unknown'
   commands.write(output/'failure.json',receipt);commands.write(output/'journal.json',receipt)
  proof={'schema':'craft-owned-desktop-session/v1','result':receipt['result'],'domain':commands.DOMAIN,'desktop':desktop,'ownedProcessesStopped':all(s.stopped for s in sessions),'listenerOwnedByPID':bool(sessions) and all(s.listener_verified for s in sessions),'sessionsStarted':len(sessions),'control':'127.0.0.1:'+str(port),'scope':'owned signed desktop and fixed CLI command workflow; no automatic replay','fullCommandAcceptance':'NOT_RUN'}
  commands.write(output/'desktop-session.json',proof)
  if interrupted:raise KeyboardInterrupt()
  return receipt
