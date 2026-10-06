#!/usr/bin/env python3
"""有界 PNG RGBA 保护区域检查；只验证像素样本，不提升创作验收。"""
import hashlib
from pathlib import Path
import struct
import zlib

MAX_BYTES=64*1024*1024

def validate(regions):
    if not isinstance(regions,list) or not 1<=len(regions)<=128:raise ValueError('protected_regions_invalid')
    ids=set()
    for item in regions:
        if not isinstance(item,dict) or set(item)!={'id','rect'}:raise ValueError('protected_regions_invalid')
        key=item['id'];rect=item['rect']
        if not isinstance(key,str) or not key.strip() or len(key)>64 or key in ids:raise ValueError('protected_regions_invalid')
        if not isinstance(rect,list) or len(rect)!=4 or any(type(n) is not int for n in rect) or any(n<0 or n>16384 for n in rect) or not rect[2] or not rect[3]:raise ValueError('protected_regions_invalid')
        ids.add(key)
    return regions

def paeth(a,b,c):
    p=a+b-c;pa,pb,pc=abs(p-a),abs(p-b),abs(p-c)
    return a if pa<=pb and pa<=pc else b if pb<=pc else c

def decode(path):
    path=Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size>MAX_BYTES:raise ValueError('protected_png_file')
    content=path.read_bytes()
    if len(content)>MAX_BYTES or content[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('protected_png_invalid')
    offset=8;header=None;compressed=[];profiles=[];ended=False;idat_ended=False;seen_idat=False;seen=set()
    while offset<len(content):
        if ended or offset+12>len(content):raise ValueError('protected_png_invalid')
        length=struct.unpack_from('>I',content,offset)[0];kind=content[offset+4:offset+8];end=offset+12+length
        if end>len(content):raise ValueError('protected_png_invalid')
        data=content[offset+8:end-4];crc=struct.unpack_from('>I',content,end-4)[0]
        if zlib.crc32(kind+data)&0xffffffff!=crc:raise ValueError('protected_png_crc')
        if header is None and kind!=b'IHDR':raise ValueError('protected_png_invalid')
        if kind==b'IHDR':
            if header is not None or length!=13:raise ValueError('protected_png_invalid')
            width,height,depth,color,compression,filtering,interlace=struct.unpack('>IIBBBBB',data)
            if not 1<=width<=16384 or not 1<=height<=16384 or width*height*4>MAX_BYTES:raise ValueError('protected_png_limit')
            if depth!=8 or color not in (2,6) or compression or filtering or interlace:raise ValueError('protected_png_unsupported')
            header=(width,height,3 if color==2 else 4)
        elif kind==b'IDAT':
            if idat_ended:raise ValueError('protected_png_invalid')
            seen_idat=True;compressed.append(data)
        elif kind==b'IEND':
            if length or not seen_idat:raise ValueError('protected_png_invalid')
            ended=True
        elif kind in (b'acTL',b'fcTL',b'fdAT',b'tRNS'):
            raise ValueError('protected_png_unsupported')
        elif kind in (b'iCCP',b'sRGB',b'gAMA',b'cHRM'):
            if kind in seen:raise ValueError('protected_png_invalid')
            seen.add(kind);profiles.append((kind,data))
        elif not kind or not (kind[0]&32) and kind!=b'PLTE':
            raise ValueError('protected_png_unsupported')
        if seen_idat and kind!=b'IDAT':idat_ended=True
        offset=end
    if not ended:raise ValueError('protected_png_invalid')
    width,height,channels=header;stride=width*channels;expected=height*(stride+1)
    try:
        inflater=zlib.decompressobj();raw=inflater.decompress(b''.join(compressed),expected+1)
        if len(raw)!=expected or not inflater.eof or inflater.unused_data or inflater.unconsumed_tail:raise ValueError('protected_png_data')
    except zlib.error as error:raise ValueError('protected_png_data') from error
    pixels=bytearray();previous=bytearray(stride)
    for y in range(height):
        start=y*(stride+1);mode=raw[start];row=bytearray(raw[start+1:start+1+stride])
        if mode>4:raise ValueError('protected_png_filter')
        for x in range(stride) if mode else ():
            a=row[x-channels] if x>=channels else 0;b=previous[x];c=previous[x-channels] if x>=channels else 0
            delta=(0,a,b,(a+b)//2,paeth(a,b,c))[mode];row[x]=(row[x]+delta)&255
        if channels==4:pixels.extend(row)
        else:
            for x in range(0,stride,3):pixels.extend(row[x:x+3]);pixels.append(255)
        previous=row
    return width,height,bytes(pixels),sorted(profiles)

def compare(before,after,regions):
    validate(regions);width,height,a,profile=decode(before);w,h,b,other_profile=decode(after)
    if (w,h)!=(width,height):raise ValueError('protected_canvas_changed')
    if profile!=other_profile:raise ValueError('protected_color_profile_changed')
    entries=[]
    for item in regions:
        x,y,span,rows=item['rect']
        if x+span>width or y+rows>height:raise ValueError('protected_region_bounds')
        first=b''.join(a[((y+row)*width+x)*4:((y+row)*width+x+span)*4] for row in range(rows))
        second=b''.join(b[((y+row)*width+x)*4:((y+row)*width+x+span)*4] for row in range(rows))
        changed=sum(first[i:i+4]!=second[i:i+4] for i in range(0,len(first),4))
        if changed:raise ValueError('protected_region_changed: '+item['id']+': '+str(changed)+' pixels')
        entries.append({'id':item['id'],'rect':item['rect'],'pixels':span*rows,'changedPixels':changed,'beforeSha256':hashlib.sha256(first).hexdigest(),'afterSha256':hashlib.sha256(second).hexdigest()})
    return {'schema':'photocraft-pixel-protection/v1','canvas':{'width':width,'height':height},'regions':entries,'scope':'exact 8-bit RGB/RGBA noninterlaced PNG samples and equal color-profile chunks; no visual or creative acceptance'}
