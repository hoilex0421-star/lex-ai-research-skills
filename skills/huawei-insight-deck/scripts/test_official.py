#!/usr/bin/env python3
"""Integration regression fixture for official-shell preservation and failure modes."""
import argparse
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile,ZIP_DEFLATED
import xml.etree.ElementTree as E
from assemble_official import assemble, NS, xml
from check_official import check


def rewrite(source,output,part,transform):
    with ZipFile(source) as src, ZipFile(output,'w',ZIP_DEFLATED) as dst:
        for n in src.namelist():
            b=src.read(n)
            dst.writestr(n,transform(b) if n==part else b)


class OfficialIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out=Path(self.tmp.name)/'deck.pptx'
        self.spec=Path(__file__).resolve().parents[1]/'assets/example-deck.json'

    def build(self):
        assemble(ARGS.template,ARGS.content,self.spec,self.out)

    def test_native_output_and_preserved_shell(self):
        self.build()
        report=check(ARGS.template,self.out)
        self.assertEqual(report['slides'],8)
        self.assertEqual(report['native_tables'],2)
        self.assertGreater(report['native_text_shapes'],30)
        self.assertEqual(report['protected_parts'],34)
        self.assertEqual(report['layouts'],['slideLayout1.xml','slideLayout5.xml']+['slideLayout6.xml']*5+['slideLayout7.xml'])
        with ZipFile(self.out) as z:
            self.assertNotIn('ppt/charts/chart1.xml',z.namelist())
            self.assertIn('非已达成的合作承诺',z.read('ppt/notesSlides/notesSlide7.xml').decode())

    def test_changed_source_rejected(self):
        wrong=Path(self.tmp.name)/'wrong.pptx'
        wrong.write_bytes(Path(ARGS.template).read_bytes()+b'changed')
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):
            assemble(wrong,ARGS.content,self.spec,self.out)
        self.assertFalse(self.out.exists())

    def test_content_overflow_rejected(self):
        bad=Path(self.tmp.name)/'overflow.pptx'
        def shift(raw):
            tree=E.fromstring(raw)
            tree.find('.//p:sp/p:spPr/a:xfrm/a:off',NS).set('x','-1000')
            return xml(tree)
        rewrite(ARGS.content,bad,'ppt/slides/slide1.xml',shift)
        with self.assertRaisesRegex(ValueError,'outside official body'):
            assemble(ARGS.template,bad,self.spec,self.out)
        self.assertFalse(self.out.exists())

    def test_existing_output_is_safe(self):
        self.out.write_bytes(b'user content')
        with self.assertRaisesRegex(ValueError,'never overwritten'):
            self.build()
        self.assertEqual(self.out.read_bytes(),b'user content')

    def test_content_uses_presentation_order(self):
        reordered=Path(self.tmp.name)/'reordered.pptx'
        def reorder(raw):
            tree=E.fromstring(raw)
            slides=tree.find('p:sldIdLst',NS)
            first=slides[0]
            slides.remove(first)
            slides.insert(1,first)
            return xml(tree)
        rewrite(ARGS.content,reordered,'ppt/presentation.xml',reorder)
        assemble(ARGS.template,reordered,self.spec,self.out)
        with ZipFile(self.out) as z:
            self.assertIn('固定输入',z.read('ppt/slides/slide3.xml').decode())
            self.assertNotIn('能力与任务',z.read('ppt/slides/slide3.xml').decode())

    def test_checker_catches_shell_tampering(self):
        self.build()
        bad=Path(self.tmp.name)/'tampered.pptx'
        rewrite(self.out,bad,'ppt/theme/theme1.xml',lambda b:b.replace(b'C7000A',b'0000FF'))
        with self.assertRaisesRegex(AssertionError,'Changed official shell'):
            check(ARGS.template,bad)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--template',required=True)
    p.add_argument('--content',required=True)
    ARGS=p.parse_args()
    unittest.main(argv=['test_official.py'],verbosity=2)
