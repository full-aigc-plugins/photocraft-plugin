"""滤镜执行目标、选区及蒙版合同；像素烘焙和可编辑能力分别报告。"""
import importlib.util
from pathlib import Path

def load(name):
 s=importlib.util.spec_from_file_location('filter_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def validate(config):
 if not isinstance(config,dict) or set(config)!={'target','method','selection','mask','region'}:raise ValueError('invalid_filter_contract')
 if config['method'] not in ('raster','smart') or type(config['selection']) is not bool or type(config['mask']) is not bool:raise ValueError('invalid_filter_contract')
 target=config['target']
 if not(type(target) is int and target>0 or isinstance(target,dict) and set(target)=={'$ref'} and isinstance(target['$ref'],str)):raise ValueError('invalid_filter_target')
 load('pixel_guard').validate([{'id':'filter-target','rect':config['region']}])

def check(config,model):
 validate(config);rows=load('domain_assertions').index(model);target=rows.get(str(config['target']))
 if target is None or model.get('activeLayer')!=config['target'] or model.get('hasSelection') is not config['selection'] or target.get('hasMask') is not config['mask']:raise ValueError('filter_context_mismatch')
 if config['method']=='smart':raise ValueError('filter_editability_unverified: full editable filter graph is not exposed by this pinned inspection API')
 if target['kind']!='Pixel':raise ValueError('filter_context_mismatch: raster_requires_pixel_layer')
 return {'target':config['target'],'method':'raster','editable':False,'selection':config['selection'],'mask':config['mask'],'scope':'explicit pixel baking; reversible smart-filter editing is not asserted'}

def changed(before,after,rect):
 guard=load('pixel_guard');w,h,a,profile=guard.decode(before);width,height,b,other=guard.decode(after)
 if (w,h)!=(width,height) or profile!=other:raise ValueError('filter_canvas_or_profile_changed')
 x,y,span,rows=rect
 if x+span>w or y+rows>h:raise ValueError('filter_region_outside_canvas')
 total=sum(a[((y+j)*w+x+i)*4:((y+j)*w+x+i+1)*4]!=b[((y+j)*w+x+i)*4:((y+j)*w+x+i+1)*4] for j in range(rows) for i in range(span))
 if total==0:raise ValueError('filter_no_observed_change')
 return {'rect':rect,'changedPixels':total,'scope':'exact pixel change, not perceptual appropriateness'}
