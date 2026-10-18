#!/usr/bin/env python3
"""按已确认的像素坐标生成局部修复命令；不读取、判断或修改照片。"""
import argparse
import json
import math


def number(value, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not low <= value <= high or not math.isfinite(value):
        raise ValueError('numeric value outside supported bounds')
    return value


def build_plan(data):
    """返回工作层与画笔步骤；拒绝越界、保护区相交及不安全取样路径。"""
    if not isinstance(data, dict):
        raise ValueError('input must be an object')
    width=number(data.get('width'),1,100000);height=number(data.get('height'),1,100000)
    if int(width)!=width or int(height)!=height:
        raise ValueError('image dimensions must be integers')
    def point(p):
        if not isinstance(p,list) or len(p)!=2:
            raise ValueError('point must contain x,y')
        return [number(p[0],0,width),number(p[1],0,height)]
    regions=data.get('protected',[])
    if not isinstance(regions,list) or len(regions)>1000:
        raise ValueError('invalid protected regions')
    for box in regions:
        if not isinstance(box,list) or len(box)!=4:
            raise ValueError('protected rectangle requires x0,y0,x1,y1')
        a=point(box[:2]);b=point(box[2:])
        if a[0]>=b[0] or a[1]>=b[1]:
            raise ValueError('protected rectangle must have positive area')
    strokes=data.get('strokes')
    if not isinstance(strokes,list) or not 1<=len(strokes)<=100:
        raise ValueError('provide 1..100 confirmed strokes')
    steps=[{'command':'layer.duplicate','params':{'name':'Restoration working copy'}}]
    def check_path(points,radius):
        for x,y in points:
            if not radius<=x<=width-radius or not radius<=y<=height-radius:
                raise ValueError('brush footprint extends outside image')
        for a,b in zip(points,points[1:]+points[-1:]):
            left=min(a[0],b[0])-radius;right=max(a[0],b[0])+radius
            top=min(a[1],b[1])-radius;bottom=max(a[1],b[1])+radius
            if any(left<=x1 and right>=x0 and top<=y1 and bottom>=y0 for x0,y0,x1,y1 in regions):
                raise ValueError('conservative stroke envelope touches protected region')
    for stroke in strokes:
        if not isinstance(stroke,dict) or stroke.get('kind') not in ('spot','heal'):
            raise ValueError('stroke kind must be spot or heal')
        size=number(stroke.get('size'),1,5000);raw=stroke.get('points')
        if not isinstance(raw,list) or not 1<=len(raw)<=1000:
            raise ValueError('provide 1..1000 points per stroke')
        points=[point(p) for p in raw];check_path(points,size/2)
        params={'points':points,'size':size}
        if stroke['kind']=='spot':
            if 'source' in stroke:
                raise ValueError('spot stroke has no explicit source')
            command='paint.spotHealing';params['type']='proximityMatch'
        else:
            source=point(stroke.get('source'));offset=[source[i]-points[0][i] for i in range(2)]
            check_path([[p[0]+offset[0],p[1]+offset[1]] for p in points],size/2)
            command='paint.healingBrush';params.update(source=source,hardness=40,sampleLayer='current',opacity=70,aligned=True)
        steps.append({'command':command,'params':params})
    return {'schema':'photocraft-local-repair-plan/v1','countsAsNewScene':False,'imageSize':[width,height],'steps':steps,'checkpoint':'Save a new layered project and PNG; inspect local damage and declared protected regions before any global tone adjustment.','boundary':'Coordinates and protected rectangles must come from actual input inspection; conservative segment envelopes may reject safe diagonal strokes. No automatic damage detection or quality guarantee.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    try:
        with open(a.input,encoding='utf-8') as f:plan=build_plan(json.load(f))
        with open(a.output,'x',encoding='utf-8') as f:json.dump(plan,f,ensure_ascii=True,indent=2);f.write('\n')
    except (ValueError,OSError) as error:p.exit(2,str(error)+'\n')
if __name__=='__main__':main()
