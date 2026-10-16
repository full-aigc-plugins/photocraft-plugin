import {AppBridge,PostMessageTransport} from '@modelcontextprotocol/ext-apps/app-bridge';
const status=document.querySelector('#status');
const pageId=crypto.randomUUID();
const rpc=async(method,params)=>{
 const response=await fetch('rpc',{method:'POST',headers:{'Content-Type':'application/json','X-Craft-Page':pageId},body:JSON.stringify({method,params})});
 const result=await response.json();if(!response.ok)throw Error(result.error);return result;
};
const bridge=new AppBridge(null,{name:'Craft host browser',version:'0.1.0'},
 {serverResources:{},serverTools:{},downloadFile:{}},
 {hostContext:{theme:'dark',locale:'zh-CN',displayMode:'fullscreen'}});
bridge.onreadresource=p=>rpc('readResource',p);
bridge.oncalltool=p=>rpc('callTool',p);
bridge.ondownloadfile=p=>rpc('downloadFile',p);
bridge.onsizechange=()=>{};
bridge.oninitialized=async()=>{
 await bridge.sendToolInput({arguments:{}});
 await bridge.sendToolResult(await rpc('initial',{}));
 status.textContent='已连接 · 工程与工具共享当前会话';
};
const stream=new EventSource('events');
stream.onmessage=async({data})=>{
 const event=JSON.parse(data);
 if(event.type==='tool-result')await bridge.sendToolResult(event.result);
 if(event.type==='saved')status.textContent=`已保存：${event.paths.join('，')}`;
};
stream.onerror=()=>{status.textContent='连接中断；保留页面并检查 MCP 服务，勿重复编辑。';};
const frame=document.querySelector('iframe');
await bridge.connect(new PostMessageTransport(frame.contentWindow,frame.contentWindow));
frame.src='panel?webgl';
window.addEventListener('pagehide',()=>{navigator.sendBeacon('detach',JSON.stringify({pageId}));stream.close();});
