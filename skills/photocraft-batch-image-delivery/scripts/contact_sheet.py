"""用真实 PhotoCraft CLI 制作可编辑联系表；原图只读，失败时保留诊断工程。"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def grid(count, columns=3, rows=2, cell_width=240, cell_height=200):
    if not 1 <= count <= 200 or not 1 <= columns <= 4 or not 1 <= rows <= 3:
        raise ValueError('需要1..200张图片、1..4列、1..3行')
    if not 120 <= cell_width <= 1200 or not 120 <= cell_height <= 1200:
        raise ValueError('单元尺寸必须在120..1200像素')
    return [(i // (columns * rows), (i % columns + .5) * cell_width,
             ((i // columns) % rows + .5) * cell_height - 16) for i in range(count)]


def placement(path, width, height, cx, cy, cell_width, cell_height):
    if width <= 0 or height <= 0:
        raise ValueError('输入尺寸无效')
    scale = min((cell_width-32)/width, (cell_height-64)/height, 1) * 100
    return {'path': str(path), 'scale': scale, 'fit': False,
            'smartObject': True, 'center': [cx, cy]}


def execute(cli, *args):
    process = subprocess.run([str(cli), *args], capture_output=True, text=True,
                             encoding='utf-8', errors='replace')
    if process.returncode:
        raise RuntimeError(process.stderr or process.stdout)
    return process.stdout


def build(cli, images, output, columns=3, rows=2, cell_width=240, cell_height=200):
    locations = grid(len(images), columns, rows, cell_width, cell_height)
    output = Path(output).resolve()
    if output.exists():
        raise ValueError('输出目录必须不存在，禁止覆盖已有交付')
    records = []
    for image in images:
        path = Path(image).resolve(strict=True)
        if output == path or output in path.parents or not path.is_file():
            raise ValueError('输入必须是输出目录以外的文件')
        if len(path.name.encode('utf-8')) > 256 or any(c in path.name for c in '\n\r\t'):
            raise ValueError('文件名不适合单行标签')
        info = json.loads(execute(cli, 'info', str(path)))
        records.append({'path': str(path), 'filename': path.name, 'width': info['width'],
                        'height': info['height'], 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    output.mkdir(parents=True)
    pages = []
    for page in range(locations[-1][0]+1):
        argv = ['run', '--new', json.dumps({'width': columns*cell_width,
                'height': rows*cell_height, 'background': '#ffffff'})]
        selected = []
        for record, (sheet, x, y) in zip(records, locations):
            if sheet != page:
                continue
            selected.append(record)
            argv += ['--cmd', 'file.placeEmbedded', '--params', json.dumps(placement(
                record['path'], record['width'], record['height'], x, y, cell_width, cell_height)),
                '--cmd', 'type.create', '--params', json.dumps({'x': x,
                'y': y+(cell_height-64)/2+24, 'text': record['filename'],
                'name': 'Caption: '+record['filename'], 'size': 12, 'color': '#000000', 'align': 'center'})]
        project = output / ('sheet-%03d.pcraft' % (page+1))
        log = execute(cli, *argv, '--out', str(project))
        (project.with_suffix('.commands.jsonl')).write_text(log, encoding='utf-8')
        results = [json.loads(line) for line in log.splitlines() if line.strip()]
        captions = [v['result']['bounds'] for v in results if v.get('command') == 'type.create']
        if len(captions) != len(selected) or any(b[2]-b[0] > cell_width-24 for b in captions):
            raise ValueError('标签过长，保留草稿；增大单元宽度或显式重命名副本后重试')
        preview = project.with_suffix('.png')
        execute(cli, 'convert', str(project), str(preview))
        reopened = json.loads(execute(cli, 'info', str(project)))
        if len(reopened['layers']) != 1+2*len(selected):
            raise ValueError('重开后的图片及文字图层数量不匹配')
        pages.append({'project': project.name, 'preview': preview.name,
                      'files': [v['filename'] for v in selected]})
    for record in records:
        if hashlib.sha256(Path(record['path']).read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('输入文件在操作期间变化')
    manifest = {'inputOrder': 'explicit argument order', 'images': records, 'pages': pages,
                'quality': '需逐页查看图片内容与标签；未自动验证字体缺字、ICC或打印色彩'}
    (output/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--columns', type=int, default=3)
    parser.add_argument('--rows', type=int, default=2)
    parser.add_argument('--cell-width', type=int, default=240)
    parser.add_argument('--cell-height', type=int, default=200)
    parser.add_argument('images', nargs='+')
    args = parser.parse_args()
    print(json.dumps(build(args.cli, args.images, args.output, args.columns, args.rows,
                           args.cell_width, args.cell_height)))
