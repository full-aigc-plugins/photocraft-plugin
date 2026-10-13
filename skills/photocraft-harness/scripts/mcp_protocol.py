"""固定rmcp 3.5.0初始化类型的只读校验；保留serde忽略字段和扩展元数据。"""
import json
import re


def member(path, key):
    return path + ('.' + key if re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', key) else '[' + json.dumps(key,ensure_ascii=False) + ']')


def reject(code, path):
    error=ValueError(code+': '+path);error.fieldPath=path;raise error


def require(value, kind, path):
    if not isinstance(value,kind) or kind is bool and type(value) is not bool:
        reject('parameter_type',path)
    return value


def field(value, key, kind, path, required=False):
    location=member(path,key)
    if key not in value:
        if required:reject('missing_mcp_initialize_field',location)
        return None
    item=value[key]
    if item is None and not required:return None
    return require(item,kind,location)


def capabilities(value, path):
    """仅校验已知有类型字段；未来能力、扩展名及设置内容保持原生语义。"""
    for key in ['experimental','extensions']:
        settings=field(value,key,dict,path)
        if settings is not None:
            for name,options in settings.items():require(options,dict,member(member(path,key),name))
    roots=field(value,'roots',dict,path)
    if roots is not None:field(roots,'listChanged',bool,member(path,'roots'))
    sampling=field(value,'sampling',dict,path)
    if sampling is not None:
        for key in ['tools','context']:field(sampling,key,dict,member(path,'sampling'))
    elicitation=field(value,'elicitation',dict,path)
    if elicitation is not None:
        form=field(elicitation,'form',dict,member(path,'elicitation'))
        if form is not None:field(form,'schemaValidation',bool,member(member(path,'elicitation'),'form'))
        field(elicitation,'url',dict,member(path,'elicitation'))


def implementation(value, path):
    """检查原生Implementation及图标的必填和可选类型，不引入URI可达性要求。"""
    for key in ['name','version']:field(value,key,str,path,required=True)
    for key in ['title','description','websiteUrl']:field(value,key,str,path)
    icons=field(value,'icons',list,path)
    if icons is not None:
        for index,icon in enumerate(icons):
            location=path+'.icons['+str(index)+']';require(icon,dict,location)
            field(icon,'src',str,location,required=True);field(icon,'mimeType',str,location)
            sizes=field(icon,'sizes',list,location)
            if sizes is not None:
                for size_index,size in enumerate(sizes):require(size,str,location+'.sizes['+str(size_index)+']')
            theme=field(icon,'theme',str,location)
            if theme is not None and theme not in {'light','dark'}:reject('parameter_enum',location+'.theme')


def initialize(message):
    """只处理显式initialize；逐请求元数据协议不被强制改成握手协议。"""
    if 'id' not in message:reject('initialize_requires_id','$.id')
    params=require(message.get('params'),dict,'$.params')
    field(params,'protocolVersion',str,'$.params',required=True)
    client_capabilities=field(params,'capabilities',dict,'$.params',required=True)
    capabilities(client_capabilities,'$.params.capabilities')
    client=field(params,'clientInfo',dict,'$.params',required=True)
    implementation(client,'$.params.clientInfo')
    field(params,'_meta',dict,'$.params')


def number_or_string(value,path,raw=None):
    """固定rmcp的标识只接受字符串或有符号64位整数。"""
    if isinstance(value,str):return
    if type(value) is not int or not -(1<<63)<=value<(1<<63) or raw=='-0':
        reject('invalid_mcp_request_id',path)


def lifecycle(message,fragments):
    """校验已知分页和通知字段；保留原生忽略字段及开放元数据。"""
    if 'id' in message:number_or_string(message['id'],'$.id',fragments.get('$.id'))
    params=message.get('params') or {};method=message['method']
    field(params,'_meta',dict,'$.params')
    if method=='tools/list':field(params,'cursor',str,'$.params')
    if 'id' in message:return
    if method=='notifications/cancelled':
        token=params.get('requestId')
        if token is not None:number_or_string(token,'$.params.requestId',fragments.get('$.params.requestId'))
        field(params,'reason',str,'$.params')
    elif method=='notifications/progress':
        if 'progressToken' not in params:reject('missing_progress_field','$.params.progressToken')
        number_or_string(params['progressToken'],'$.params.progressToken',fragments.get('$.params.progressToken'))
        if 'progress' not in params:reject('missing_progress_field','$.params.progress')
        if type(params['progress']) not in (int,float):reject('parameter_type','$.params.progress')
        if params.get('total') is not None and type(params['total']) not in (int,float):reject('parameter_type','$.params.total')
        field(params,'message',str,'$.params')


class Lifecycle:
    """只镜像固定服务的首请求门禁；不强制等待initialized或改写元数据。"""
    def __init__(self):self.started=False
    def accept(self,message):
        if self.started:return
        if 'id' not in message:reject('expected_initialize_request','$.method')
        if message['method']=='ping':return
        if message['method']=='initialize':self.started=True;return
        meta=field(message.get('params') or {},'_meta',dict,'$.params',required=True)
        path='$.params._meta'
        field(meta,'io.modelcontextprotocol/protocolVersion',str,path,required=True)
        key='io.modelcontextprotocol/clientCapabilities'
        value=field(meta,key,dict,path,required=True);capabilities(value,member(path,key))
        self.started=True
