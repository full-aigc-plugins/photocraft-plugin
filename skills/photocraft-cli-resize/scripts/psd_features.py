"""按树中位置比较 PSD 实际使用特性；未知指标不升级为保真。"""
def tree(model):
 result={}
 def walk(layers,prefix):
  if not isinstance(layers,list):raise ValueError('psd_feature_tree_invalid')
  for n,layer in enumerate(layers):
   if not isinstance(layer,dict):raise ValueError('psd_feature_tree_invalid')
   key=prefix+str(n);result[key]=layer
   if 'children' in layer:walk(layer['children'],key+'/')
 walk(model.get('layers',[]),'');return result

def verify_reopen(recorded,actual):
 """PSD 重开可重分配 ID；按递归位置比较完整持久属性和画幅。"""
 for key in ('width','height','mode','depth'):
  if recorded.get(key)!=actual.get(key):raise ValueError('psd_reopen_canvas_changed: '+key)
 before=tree(recorded);after=tree(actual)
 if set(before)!=set(after):raise ValueError('psd_reopen_structure_changed: positions')
 for key,old in before.items():
  normalize=lambda row:{name:value for name,value in row.items() if name not in ('id','selected','children')}
  if normalize(old)!=normalize(after[key]):raise ValueError('psd_reopen_structure_changed: '+key)
 return {'status':'PASS','layers':len(before),'scope':'recursive reopened PSD persistent properties; reassigned IDs and temporary selection excluded, external editor fidelity NOT_RUN'}

def assess(native,psd,used_effects=False):
 a=tree(native);b=tree(psd);features={}
 for key,layer in a.items():
  other=b.get(key);same=other is not None and other.get('name')==layer.get('name')
  features[key+':structure']={'status':'retained' if same and other.get('kind')==layer.get('kind') else 'lost','native':{'name':layer.get('name'),'kind':layer.get('kind')},'psd':{'name':other.get('name'),'kind':other.get('kind')} if other is not None else None,'evidence':'native and PSD reopened trees at the same sibling position'}
  used=[]
  if layer.get('kind')=='Type':used.append(('text','text'))
  if layer.get('hasMask') is True:used.append(('mask','hasMask'))
  for field in ('blend','opacity','smartObject','smartSourceKind','smartTransform','adjustment','shape'):
   if field in layer and layer[field] is not None:used.append((field,field))
  for feature,field in used:
   expected=layer.get(field)
   if not same:status='lost';actual=None
   elif field not in other:status='lost' if feature=='text' and other.get('kind')!='Type' else 'unknown';actual=None
   else:
    actual=other[field];status='retained' if actual==expected else 'lost' if actual is None or feature=='mask' and actual is False else 'degraded'
   features[key+':'+feature]={'status':status,'native':expected,'psd':actual,'evidence':'reopened inspection properties; external editor NOT_RUN'}
 if len(b)!=len(a):features['tree-size']={'status':'degraded','native':len(a),'psd':len(b)}
 if used_effects:features['effects']={'status':'unknown','reason':'Inspection does not expose a complete editable filter/effect graph.'}
 return {'schema':'photocraft-psd-features/v1','features':features,'completeFidelity':False,'scope':'used properties observed on reopened native and PSD; complete editability, visual equivalence and external editor acceptance remain unverified'}
