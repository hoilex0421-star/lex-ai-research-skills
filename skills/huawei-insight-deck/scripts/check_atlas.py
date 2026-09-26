#!/usr/bin/env python3
"""Check atlas coverage, native chart/workbook links, photo crops and media reuse."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
from check_official import check
from assemble_official import NS, q, resolve, relpath

C = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
N = {**NS, 'c': C}


def check_atlas(template, deck, spec_path):
    spec = json.loads(Path(spec_path).read_text())
    assert [s['id'] for s in spec['slides']] == [f'H{i:02}' for i in range(1, 43)]
    report = check(template, deck)
    assert report['slides'] == 42 and report['native_charts'] == 8 and report['native_tables'] == 6
    with ZipFile(deck) as z:
        chart_owners = {}
        image_parts = set()
        photo_count = 0
        for i in range(1, 43):
            part = f'ppt/slides/slide{i}.xml'
            slide = E.fromstring(z.read(part))
            notes = E.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
            assert f'H{i:02}' in ''.join(notes.itertext()), f'Wrong atlas page identity at {i}'
            rels = {r.get('Id'): r for r in E.fromstring(z.read(relpath(part)))}
            charts = slide.findall('.//c:chart', N)
            if charts:
                chart_owners[i] = [resolve(part, rels[c.get(q('r:id'))].get('Target')) for c in charts]
            for pic in slide.findall('p:cSld/p:spTree/p:pic', N):
                photo_count += 1
                blip = pic.find('p:blipFill/a:blip', N)
                image_parts.add(resolve(part, rels[blip.get(q('r:embed'))].get('Target')))
                if i != 21:
                    crop = pic.find('p:blipFill/a:srcRect', N)
                    assert crop is not None, f'Missing native crop on H{i:02}'
                    l, t, r, b = [int(crop.get(k, '0')) for k in ('l', 't', 'r', 'b')]
                    assert l+r >= 75000 and l+r < 100000 and t+b < 100000
        assert set(chart_owners) == {7, 15, 16, 28, 29, 30}
        assert photo_count == 18 and len(image_parts) == 3, 'Contact-sheet media were duplicated or omitted'
        workbook_parts = set()
        for owner, charts in chart_owners.items():
            for part in charts:
                chart = E.fromstring(z.read(part))
                rels = {r.get('Id'): r for r in E.fromstring(z.read(relpath(part)))}
                external = chart.find('c:externalData', N)
                assert external is not None, f'Chart without editable data on H{owner:02}'
                book = resolve(part, rels[external.get(q('r:id'))].get('Target'))
                assert book.endswith('.xlsx') and book in z.namelist()
                workbook_parts.add(book)
                if owner == 16:
                    plot = chart.find('c:chart/c:plotArea', N)
                    assert plot.find('c:barChart', N) is not None and plot.find('c:lineChart', N) is not None
                    assert len(plot.findall('c:valAx', N)) == 2
                if owner in (28, 29):
                    labs = chart.find('.//c:doughnutChart/c:dLbls', N)
                    assert labs.find('c:showPercent', N).get('val') == '1'
                    assert labs.find('c:showVal', N).get('val') == '0'
                    assert labs.find('c:showCatName', N).get('val') == '0'
        assert len(workbook_parts) == 8
    return {**report, 'coverage': 'H01–H42', 'pictures': photo_count,
            'unique_content_images': len(image_parts), 'embedded_chart_workbooks': len(workbook_parts)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', required=True)
    parser.add_argument('--deck', required=True)
    parser.add_argument('--spec', default=str(Path(__file__).resolve().parents[1] / 'assets/atlas/deck-spec.json'))
    args = parser.parse_args()
    print(json.dumps(check_atlas(args.template, args.deck, args.spec), ensure_ascii=False, indent=2))
