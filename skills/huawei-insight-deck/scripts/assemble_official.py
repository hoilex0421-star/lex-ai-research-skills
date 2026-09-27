#!/usr/bin/env python3
"""Fill official placeholders and graft native content into the untouched official shell.

Input: pinned template, a content-only PPTX, and deck-spec.json. All generated
content must fit the original body region. No automatic shrink-to-fit or flattening.
Uses only Python's standard library; does not reserialize masters or source artwork.
"""
import argparse
import copy
import hashlib
import json
import posixpath
from pathlib import Path
import xml.etree.ElementTree as E
from zipfile import ZipFile, ZIP_DEFLATED

from fetch_official_template import MANIFEST, verify

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
      'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}
for prefix in ('a', 'p', 'r'):
    E.register_namespace(prefix, NS[prefix])
for prefix, uri in {'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
                    'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
                    'a16': 'http://schemas.microsoft.com/office/drawing/2014/main'}.items():
    E.register_namespace(prefix, uri)
REL = NS['r'] + '/'
PROTECTED = ('ppt/slideMasters/', 'ppt/slideLayouts/', 'ppt/theme/', 'ppt/media/')


def q(name):
    prefix, tag = name.split(':')
    return '{' + NS[prefix] + '}' + tag


def xml(root):
    if root.tag in (q('ct:Types'), q('rel:Relationships')):
        E.register_namespace('', root.tag.split('}')[0][1:])
    return E.tostring(root, encoding='utf-8', xml_declaration=True)


def relpath(part):
    return posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')


def resolve(part, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(part), target)) if not target.startswith('/') else target[1:]


def placeholder(slide, kind=None, idx=None):
    for shape in slide.findall('.//p:sp', NS):
        ph = shape.find('p:nvSpPr/p:nvPr/p:ph', NS)
        if ph is not None and (kind is None or ph.get('type') == kind) and (idx is None or ph.get('idx') == str(idx)):
            return shape
    raise ValueError(f'Missing official placeholder {kind}/{idx}')


def fill(shape, lines, active=None):
    """Keep geometry, list styles and inherited font/size; replace only paragraphs."""
    body = shape.find('p:txBody', NS)
    for para in list(body.findall('a:p', NS)):
        body.remove(para)
    for i, line in enumerate(lines):
        para = E.SubElement(body, q('a:p'))
        run = E.SubElement(para, q('a:r'))
        props = E.SubElement(run, q('a:rPr'), lang='zh-CN')
        if active is not None and i == active:
            color = E.SubElement(props, q('a:solidFill'))
            E.SubElement(color, q('a:srgbClr'), val='C7000A')
        E.SubElement(run, q('a:t')).text = str(line)


def notes(text):
    root = E.Element(q('p:notes'))
    cs = E.SubElement(root, q('p:cSld'))
    tree = E.SubElement(cs, q('p:spTree'))
    nv = E.SubElement(tree, q('p:nvGrpSpPr'))
    E.SubElement(nv, q('p:cNvPr'), id='1', name='')
    E.SubElement(nv, q('p:cNvGrpSpPr'))
    E.SubElement(nv, q('p:nvPr'))
    E.SubElement(tree, q('p:grpSpPr'))
    shape = E.SubElement(tree, q('p:sp'))
    nv = E.SubElement(shape, q('p:nvSpPr'))
    E.SubElement(nv, q('p:cNvPr'), id='2', name='Research sources and template provenance')
    E.SubElement(nv, q('p:cNvSpPr'))
    ph = E.SubElement(nv, q('p:nvPr'))
    E.SubElement(ph, q('p:ph'), type='body', idx='1')
    E.SubElement(shape, q('p:spPr'))
    tx = E.SubElement(shape, q('p:txBody'))
    E.SubElement(tx, q('a:bodyPr'))
    E.SubElement(tx, q('a:lstStyle'))
    fill(shape, text.splitlines())
    return xml(root)


def assemble(template, content, spec_path, output):
    verify(template)
    paths = [Path(p).resolve() for p in (template, content, spec_path)]
    output = Path(output)
    if output.exists() or output.resolve() in paths:
        raise ValueError('Use a new output path; inputs and existing outputs are never overwritten.')
    manifest = json.loads(MANIFEST.read_text())
    spec = json.loads(Path(spec_path).read_text())
    with ZipFile(template) as z:
        source = {n: z.read(n) for n in z.namelist()}
    with ZipFile(content) as z:
        donor = {n: z.read(n) for n in z.namelist()}
    donor_presentation = E.fromstring(donor['ppt/presentation.xml'])
    donor_size = donor_presentation.find('p:sldSz', NS)
    if [int(donor_size.get(k)) for k in ('cx', 'cy')] != manifest['slide_size_emu']:
        raise ValueError('Content canvas differs from the exact official slide dimensions.')
    donor_rels = {r.get('Id'): r for r in E.fromstring(donor['ppt/_rels/presentation.xml.rels'])}
    donor_slides = [resolve('ppt/presentation.xml', donor_rels[s.get(q('r:id'))].get('Target'))
                    for s in donor_presentation.find('p:sldIdLst', NS)]
    replaced = ('ppt/slides/', 'ppt/notesSlides/', 'ppt/charts/', 'ppt/embeddings/')
    result = {n: b for n, b in source.items() if not n.startswith(replaced)}
    ct = E.fromstring(source['[Content_Types].xml'])
    for el in list(ct):
        if el.get('PartName', '').lstrip('/').startswith(replaced):
            ct.remove(el)
    donor_ct = E.fromstring(donor['[Content_Types].xml'])

    def add_type(part, content_type):
        if not any(c.get('PartName') == '/' + part for c in ct):
            E.SubElement(ct, q('ct:Override'), PartName='/' + part, ContentType=content_type)

    imported_media = {}

    def import_part(part):
        new = 'ppt/lex-content/' + part
        if new in result:
            return new
        # Repeated image placements keep their own crops but share identical bytes.
        is_image = part.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))
        digest = hashlib.sha256(donor[part]).hexdigest() if is_image else None
        if digest in imported_media:
            return imported_media[digest]
        if is_image:
            imported_media[digest] = new
        result[new] = donor[part]
        override = next((c.get('ContentType') for c in donor_ct if c.get('PartName') == '/' + part), None)
        if override:
            add_type(new, override)
        else:
            ext = part.rsplit('.', 1)[-1]
            default = next((c.get('ContentType') for c in donor_ct if c.get('Extension') == ext), None)
            if default:
                add_type(new, default)
        rp = relpath(part)
        if rp in donor:
            relations = E.fromstring(donor[rp])
            for rel in relations:
                if rel.get('TargetMode') != 'External':
                    dest = import_part(resolve(part, rel.get('Target')))
                    rel.set('Target', posixpath.relpath(dest, posixpath.dirname(new)))
            result[relpath(new)] = xml(relations)
        return new

    presentation = E.fromstring(source['ppt/presentation.xml'])
    slide_ids = presentation.find('p:sldIdLst', NS)
    slide_ids.clear()
    # Original template sections/custom shows would retain stale slide IDs.
    for tag in ('p:custShowLst', 'p:extLst'):
        old = presentation.find(tag, NS)
        if old is not None:
            presentation.remove(old)
    presrels = E.fromstring(source['ppt/_rels/presentation.xml.rels'])
    for rel in list(presrels):
        if rel.get('Type') == REL + 'slide':
            presrels.remove(rel)
    body_x, body_y, body_w, body_h = manifest['body_region_emu']
    for number, page in enumerate(spec['slides'], 1):
        kind = page['kind']
        if kind not in ('cover', 'contents', 'body', 'end'):
            raise ValueError(f'Unsupported official page kind: {kind}')
        ref = manifest['reference_slides'][kind]
        part = f'ppt/slides/slide{number}.xml'
        slide = E.fromstring(source[f'ppt/slides/slide{ref}.xml'])
        rels = E.fromstring(source[f'ppt/slides/_rels/slide{ref}.xml.rels'])
        for rel in list(rels):
            if rel.get('Type') == REL + 'notesSlide':
                rels.remove(rel)
        tree = slide.find('p:cSld/p:spTree', NS)
        if kind == 'cover':
            fill(placeholder(slide, 'ctrTitle'), [page['title']])
            fill(placeholder(slide, idx=10), page['metadata'])
        elif kind == 'contents':
            if len(page['items']) > 5:
                raise ValueError('Split long agendas instead of shrinking the official 22pt font.')
            fill(placeholder(slide, idx=10), page['items'], page.get('active'))
        elif kind == 'body':
            title = placeholder(slide, 'subTitle')
            fill(title, [page['title']])
            # Remove unused content placeholder and the source's empty off-canvas box.
            for item in list(tree):
                if item.tag == q('p:sp') and item is not title:
                    tree.remove(item)
            content_index = page['content_slide']
            if not isinstance(content_index, int) or not 1 <= content_index <= len(donor_slides):
                raise ValueError('content_slide must reference a slide in presentation order.')
            dp = donor_slides[content_index - 1]
            dslide = E.fromstring(donor[dp])
            mapping = {}
            if relpath(dp) in donor:
                for rel in E.fromstring(donor[relpath(dp)]):
                    if rel.get('Type') in (REL + 'slideLayout', REL + 'notesSlide'):
                        continue
                    rid = 'lex' + rel.get('Id')
                    mapping[rel.get('Id')] = rid
                    copied = copy.deepcopy(rel)
                    copied.set('Id', rid)
                    if rel.get('TargetMode') != 'External':
                        dest = import_part(resolve(dp, rel.get('Target')))
                        copied.set('Target', posixpath.relpath(dest, 'ppt/slides'))
                    rels.append(copied)
            imported = []
            for item in dslide.find('p:cSld/p:spTree', NS):
                if item.tag not in [q('p:' + t) for t in ('sp', 'cxnSp', 'graphicFrame', 'pic')]:
                    if item.tag == q('p:grpSp'):
                        raise ValueError('Ungroup content before assembly so bounds can be checked.')
                    continue
                item = copy.deepcopy(item)
                xf = item.find('.//a:xfrm', NS)
                if xf is None:
                    xf = item.find('p:xfrm', NS)
                if xf is None:
                    raise ValueError('Content must have explicit native geometry.')
                off, ext = xf.find('a:off', NS), xf.find('a:ext', NS)
                x, y = int(off.get('x')), int(off.get('y'))
                w, h = int(ext.get('cx')), int(ext.get('cy'))
                if xf.get('rot', '0') != '0':
                    raise ValueError('Rotated content requires explicit bounding-box support.')
                if w < 0 or h < 0 or x < body_x - 10 or y < body_y - 10 or x+w > body_x+body_w+10 or y+h > body_y+body_h+10:
                    raise ValueError(f'Content outside official body region on slide {number}: {(x,y,w,h)}')
                for el in item.iter():
                    for key, value in list(el.attrib.items()):
                        if key.startswith('{' + NS['r'] + '}'):
                            if value not in mapping:
                                raise ValueError(f'Unmapped content relationship: {value}')
                            el.set(key, mapping[value])
                imported.append(item)
            # Remap shape IDs AND connector endpoint IDs.
            ids = {}
            for item in imported:
                for nv in item.findall('.//p:cNvPr', NS):
                    ids[nv.get('id')] = str(100 + len(ids))
                    nv.set('id', ids[nv.get('id')])
            for item in imported:
                for tag in ('a:stCxn', 'a:endCxn'):
                    for conn in item.findall('.//' + tag, NS):
                        conn.set('id', ids[conn.get('id')])
                tree.append(item)
        note_part = f'ppt/notesSlides/notesSlide{number}.xml'
        note_text = page.get('notes', '') + '\n\nTemplate: ' + manifest['source_page'] + '\nSHA256: ' + manifest['sha256']
        result[note_part] = notes(note_text)
        note_rels = E.Element(q('rel:Relationships'))
        E.SubElement(note_rels, q('rel:Relationship'), Id='rId1', Type=REL+'slide', Target=f'../slides/slide{number}.xml')
        E.SubElement(note_rels, q('rel:Relationship'), Id='rId2', Type=REL+'notesMaster', Target='../notesMasters/notesMaster1.xml')
        result[relpath(note_part)] = xml(note_rels)
        E.SubElement(rels, q('rel:Relationship'), Id='lexNotes', Type=REL+'notesSlide', Target=f'../notesSlides/notesSlide{number}.xml')
        result[part], result[relpath(part)] = xml(slide), xml(rels)
        add_type(part, 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml')
        add_type(note_part, 'application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml')
        rid = f'lexSlide{number}'
        E.SubElement(presrels, q('rel:Relationship'), Id=rid, Type=REL+'slide', Target=f'slides/slide{number}.xml')
        E.SubElement(slide_ids, q('p:sldId'), {'id': str(255+number), q('r:id'): rid})
    result['ppt/presentation.xml'] = xml(presentation)
    result['ppt/_rels/presentation.xml.rels'] = xml(presrels)
    result['[Content_Types].xml'] = xml(ct)
    # Remove stale source thumbnail and update the visible slide count metadata.
    for n in list(result):
        if n.startswith('docProps/thumbnail.'):
            del result[n]
    rootrels = E.fromstring(result['_rels/.rels'])
    for rel in list(rootrels):
        if rel.get('Type', '').endswith('/thumbnail'):
            rootrels.remove(rel)
    result['_rels/.rels'] = xml(rootrels)
    ct = E.fromstring(result['[Content_Types].xml'])
    for el in list(ct):
        if el.get('PartName', '').startswith('/docProps/thumbnail.'):
            ct.remove(el)
    result['[Content_Types].xml'] = xml(ct)
    app = E.fromstring(result['docProps/app.xml'])
    for el in app:
        if el.tag.endswith('}Slides'):
            el.text = str(len(spec['slides']))
    result['docProps/app.xml'] = xml(app)
    for name in source:
        if name.startswith(PROTECTED) and result.get(name) != source[name]:
            raise AssertionError(f'Official shell changed: {name}')
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED) as z:
        for name, data in result.items():
            z.writestr(name, data)
    return {'slides': len(spec['slides']), 'protected_parts': sum(n.startswith(PROTECTED) for n in source),
            'source_sha256': manifest['sha256'], 'output': str(output)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', required=True)
    parser.add_argument('--content', required=True)
    parser.add_argument('--spec', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(assemble(args.template, args.content, args.spec, args.output), ensure_ascii=False, indent=2))
