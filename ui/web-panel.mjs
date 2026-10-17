import {App,PostMessageTransport} from '@modelcontextprotocol/ext-apps';
const app=new App({name:'Craft editor panel',version:'0.1.0'},{});
await app.connect(new PostMessageTransport(window.parent,window.parent));
