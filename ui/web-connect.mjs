// 在官方页面中调用其公开 API；不执行模型提供的 JavaScript。
const base=new URL('../',location.href);
const pageId=crypto.randomUUID();
const encode=bytes=>{let s='';for(let i=0;i<bytes.length;i+=32768)s+=String.fromCharCode(...bytes.subarray(i,i+32768));return btoa(s);};
const decode=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const post=async(route,data)=>{const r=await fetch(new URL(route,base),{method:'POST',headers:{'Content-Type':'application/json','X-Craft-Page':pageId},body:JSON.stringify(data)});const value=await r.json();if(!r.ok)throw Error(value.error);return value;};
const blobs=new Map(),create=URL.createObjectURL.bind(URL),revoke=URL.revokeObjectURL.bind(URL);
URL.createObjectURL=b=>{const u=create(b);if(b instanceof Blob)blobs.set(u,b);return u;};
URL.revokeObjectURL=u=>{blobs.delete(u);revoke(u);};
const click=HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click=function(){
 const blob=blobs.get(this.href);
 if(this.hasAttribute('download')&&blob){
  void blob.arrayBuffer().then(b=>post('download',{name:this.download,data:encode(new Uint8Array(b))})).then(r=>{window.__craftLastExport=r;}).catch(e=>{window.__craftExportError=e.message;console.error(e);});
 }else click.call(this);
};
const delay=ms=>new Promise(r=>setTimeout(r,ms));
let api;
while(!(api=globalThis[application]))await delay(100);
while(document.getElementById('loading') && !document.getElementById('loading').hidden && getComputedStyle(document.getElementById('loading')).display!=='none')await delay(100);
await delay(500);
async function execute(action,args){
 if(action==='command_run')return application==='lightcraft'?JSON.parse(await api.command(args.id,JSON.stringify(args.params||{}))):api.execute(args.id,args.params||{});
 if(action==='command_list'){if(!api.commands)throw Error('This Web build has no live command-list API. Use its versioned command reference.');return api.commands();}
 if(action==='inspect')return application==='lightcraft'?JSON.parse(await api.command('library.info','{}')):api.inspect();
 if(action==='list_files'){if(!api.files)throw Error('No virtual-file listing API in this Web build');return api.files();}
 if(action==='open_file'){
  const f=new File([decode(args.data)],args.name);
  if(application==='effectcraft')return api.addFile(f);
  if(application==='filmcraft')return args.name.endsWith('.fcproj')?api.openProject(f):api.importFiles([f]);
  const transfer=new DataTransfer();transfer.items.add(f);document.querySelector('canvas').dispatchEvent(new DragEvent('drop',{dataTransfer:transfer,bubbles:true,cancelable:true}));return {requested:args.name,inspectRequired:true};
 }
 if(action==='save_project'){
  if(application==='lightcraft')throw Error('Use file.backupLibrary to export the complete LightCraft library; a single project file is not supported');
  const path='/'+args.path.split('/').pop();
  if(application==='effectcraft')await api.saveToBrowser(path);
  else await api.execute('file.saveAs',{path});
  const data=await api.readFile(path);if(!data)throw Error('Saved project absent from virtual files');return {base64:encode(data)};
 }
 if(action==='save_file'){const data=await api.readFile?.(args.source);if(!data)throw Error('Virtual file not found');return {base64:encode(data)};}
 if(action==='screenshot')return {base64:document.querySelector('canvas').toDataURL('image/png').split(',')[1]};
 throw Error('Unsupported action');
}
window.__craftWebAdapter={ready:true};
for(;;){
 try{
  const r=await fetch(new URL('poll',base),{headers:{'X-Craft-Page':pageId}});if(!r.ok){window.__craftWebAdapter.error='Editor already active in another page';window.__craftWebAdapter.ready=false;break;}const job=await r.json();
  if(job){try{await post('reply',{id:job.id,result:await execute(job.action,job.args)});}catch(e){await post('reply',{id:job.id,error:e?.message||String(e)});}}
  await delay(200);
 }catch(e){window.__craftWebAdapter.error=e.message;await delay(1000);}
}
