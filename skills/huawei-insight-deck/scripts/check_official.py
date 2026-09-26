#!/usr/bin/env python3
"""Structural/template checks. Does not replace rendered visual or evidence review."""
import argparse
import hashlib
import json
import posixpath
from pathlib import Path
import xml.etree.ElementTree as E
from zipfile import ZipFile
from assemble_official import NS, PROTECTED, REL, q, resolve, relpath
from fetch_official_template import MANIFEST, verify


def check(template, deck):
    verify(template)
    manifest = json.loads(MANIFEST.read_text())
    with ZipFile(template) as z:
        src = {n: z.read(n) for n in z.namelist()}
    with ZipFile(deck) as z:
        assert z.testzip() is None, 'ZIP CRC failure'
        assert len(z.namelist()) == len(set(z.namelist())), 'Duplicate ZIP paths'
        data = {n: z.read(n) for n in z.namelist()}
    for n in src:
        if n.startswith(PROTECTED):
            assert src[n] == data.get(n), f'Changed official shell: {n}'
    pres = E.fromstring(data['ppt/presentation.xml'])
    size = pres.find('p:sldSz', NS)
    assert [int(size.get(k)) for k in ('cx','cy')] == manifest['slide_size_emu'], 'Canvas mismatch'
    counts = {'native_tables': 0, 'native_charts': 0, 'native_text_shapes': 0, 'slides': 0}
    for name, raw in data.items():
        if not name.endswith('.rels'):
            continue
        owner = '' if name == '_rels/.rels' else posixpath.join(posixpath.dirname(posixpath.dirname(name)), posixpath.basename(name)[:-5])
        seen = set()
        for rel in E.fromstring(raw):
            assert rel.get('Id') not in seen, f'Duplicate relationship ID: {name}'
            seen.add(rel.get('Id'))
            if rel.get('TargetMode') != 'External':
                target = resolve(owner, rel.get('Target'))
                assert target in data, f'Broken relationship: {name} -> {target}'
    ct = E.fromstring(data['[Content_Types].xml'])
    for el in ct:
        if el.get('PartName'):
            assert el.get('PartName')[1:] in data, 'Stale content-type entry'
    prels = {r.get('Id'): r for r in E.fromstring(data['ppt/_rels/presentation.xml.rels'])}
    bx,by,bw,bh = manifest['body_region_emu']
    layouts=[]
    for sid in pres.find('p:sldIdLst', NS):
        counts['slides'] += 1
        name = resolve('ppt/presentation.xml', prels[sid.get(q('r:id'))].get('Target'))
        slide = E.fromstring(data[name])
        rels = {r.get('Id'):r for r in E.fromstring(data[relpath(name)])}
        layout_rel = next(r for r in rels.values() if r.get('Type') == REL+'slideLayout')
        layout = resolve(name, layout_rel.get('Target'))
        layouts.append(posixpath.basename(layout))
        assert layout in src, 'Unexpected non-official layout'
        ids = [n.get('id') for n in slide.findall('.//p:cNvPr', NS)]
        assert len(ids) == len(set(ids)), f'Duplicate shape ID: {name}'
        for el in slide.iter():
            for key,value in el.attrib.items():
                if key.startswith('{'+NS['r']+'}'):
                    assert value in rels, f'Unresolved shape relationship: {name} {value}'
        for tag in ('a:stCxn','a:endCxn'):
            for conn in slide.findall('.//'+tag,NS):
                assert conn.get('id') in ids, f'Unresolved connector: {name}'
        if layout.endswith('slideLayout6.xml'):
            for item in slide.find('p:cSld/p:spTree', NS):
                xf=item.find('.//a:xfrm',NS)
                if xf is None: xf=item.find('p:xfrm',NS)
                if xf is None or item.tag==q('p:grpSpPr'): continue
                off,ext=xf.find('a:off',NS),xf.find('a:ext',NS)
                x,y,w,h=[int(v) for v in (off.get('x'),off.get('y'),ext.get('cx'),ext.get('cy'))]
                assert x>=bx-10 and y>=by-10 and w>=0 and h>=0 and x+w<=bx+bw+10 and y+h<=by+bh+10, f'Body overflow: {name}'
        # Layout-only ending pages are valid. Their protected inherited artwork is checked above.
        assert slide.findall('.//p:sp',NS) or E.fromstring(data[layout]).findall('.//p:sp',NS), f'Empty visible page: {name}'
        assert any(r.get('Type')==REL+'notesSlide' for r in rels.values()), f'Missing notes: {name}'
        counts['native_tables'] += len(slide.findall('.//a:tbl',NS))
        counts['native_charts'] += len(slide.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}chart'))
        counts['native_text_shapes'] += sum(bool(''.join(s.itertext()).strip()) for s in slide.findall('.//p:txBody',NS))
    return {'status':'pass', **counts, 'layouts':layouts,
            'protected_parts':sum(n.startswith(PROTECTED) for n in src),
            'source_sha256':manifest['sha256'], 'deck_sha256':hashlib.sha256(Path(deck).read_bytes()).hexdigest(),
            'scope':'Package references, native element inventory, exact official shell, body bounds; not text-fit, visual or fact checking.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--template',required=True)
    p.add_argument('--deck',required=True)
    args=p.parse_args()
    print(json.dumps(check(args.template,args.deck),ensure_ascii=False,indent=2))
