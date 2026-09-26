#!/usr/bin/env python3
"""Complete native chart semantics that the sample authoring API cannot express.

H16: convert the second series into a line on a right-hand percent axis.
Doughnuts: place native percent labels inside slices with contrasting text.
Photos: preserve editable native crops of the selected contact-sheet tiles.
Does not modify data values; original literal data will be materialized to XLSX
by the presentation finalizer before the official shell is assembled.
"""
import argparse,copy,posixpath
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import xml.etree.ElementTree as E
C='http://schemas.openxmlformats.org/drawingml/2006/chart'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
N={'c':C,'a':A}
P='http://schemas.openxmlformats.org/presentationml/2006/main'
N['p']=P
E.register_namespace('c',C);E.register_namespace('a',A)
def el(tag,**attrs):return E.Element('{'+C+'}'+tag,attrs)
def put(parent,tag,**attrs):
 old=parent.find('c:'+tag,N)
 if old is None:old=E.SubElement(parent,'{'+C+'}'+tag)
 old.attrib.update(attrs);return old

def prepare(src,dst):
 if Path(dst).exists():raise ValueError('Use a new output path')
 with ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
 for name,raw in list(data.items()):
  if '/charts/' not in name or not name.endswith('.xml'):continue
  root=E.fromstring(raw);plot=root.find('c:chart/c:plotArea',N)
  if plot is None:continue
  bar=plot.find('c:barChart',N)
  if bar is not None:
   series=bar.findall('c:ser',N)
   if len(series)==2 and series[1].find('c:tx/c:v',N).text=='一次通过率（%）':
    line=el('lineChart');line.append(el('grouping',val='standard'))
    ser=series[1];bar.remove(ser)
    sp=ser.find('c:spPr',N);sp.clear()
    ln=E.SubElement(sp,'{'+A+'}ln',w='28575');fill=E.SubElement(ln,'{'+A+'}solidFill');E.SubElement(fill,'{'+A+'}srgbClr',val='C7000A')
    marker=el('marker');marker.append(el('symbol',val='circle'));marker.append(el('size',val='6'));ser.insert(list(ser).index(ser.find('c:cat',N)),marker)
    line.append(ser)
    labs=copy.deepcopy(bar.find('c:dLbls',N));labs.find('c:dLblPos',N).set('val','t');line.append(labs)
    cat_id=bar.findall('c:axId',N)[0].get('val');new_id='48699999'
    line.append(el('axId',val=cat_id));line.append(el('axId',val=new_id));plot.insert(list(plot).index(bar)+1,line)
    axis=copy.deepcopy(plot.find('c:valAx',N));axis.find('c:axId',N).set('val',new_id);axis.find('c:axPos',N).set('val','r');axis.find('c:numFmt',N).set('formatCode','0"%"')
    # Axis child ordering follows CT_ValAx: crosses immediately after crossAx.
    cross=axis.find('c:crossAx',N);axis.insert(list(axis).index(cross)+1,el('crosses',val='max'))
    plot.insert(list(plot).index(plot.find('c:spPr',N)),axis)
  donut=plot.find('c:doughnutChart',N)
  if donut is not None:
   labs=donut.find('c:dLbls',N);pos=labs.find('c:dLblPos',N)
   if pos is None:pos=el('dLblPos',val='ctr');labs.insert(0,pos)
   else:pos.set('val','ctr')
   for tag in ('showLegendKey','showVal','showCatName','showSerName','showLeaderLines'):
    put(labs,tag,val='0')
   put(labs,'showPercent',val='1')
   count=int(donut.find('c:ser/c:val/c:numLit/c:ptCount',N).get('val'))
   for i in range(count):
    label=el('dLbl');label.append(el('idx',val=str(i)))
    tx=copy.deepcopy(labs.find('c:txPr',N))
    for rgb in tx.findall('.//a:srgbClr',N):rgb.set('val','FFFFFF' if i<2 else '1D1D1A')
    label.append(tx)
    for tag in ('showLegendKey','showVal','showCatName','showSerName'):
     label.append(el(tag,val='0'))
    label.append(el('showPercent',val='1'));labs.insert(i,label)
  # Explicit chart/axis/label fonts, including rich axis-title runs.
  for run in root.findall('.//a:r',N):
   if run.find('a:rPr',N) is None:run.insert(0,E.Element('{'+A+'}rPr',{'sz':'1299'}))
  for tag in ('defRPr','rPr','endParaRPr'):
   for props in root.findall('.//a:'+tag,N):
    for kind in ('latin','ea','cs'):
     child=props.find('a:'+kind,N)
     if child is None:child=E.SubElement(props,'{'+A+'}'+kind)
     child.set('typeface','Microsoft YaHei')
  # Remove empty title objects; title formatting belongs to visible titles only.
  ch=root.find('c:chart',N);title=ch.find('c:title',N)
  if title is not None and title.find('c:tx',N) is None:ch.remove(title)
  data[name]=E.tostring(root,encoding='utf-8',xml_declaration=True)
 # The authoring exporter currently drops explicit contact-sheet crop insets.
 # Apply DrawingML srcRect after export; picture pixels remain untouched.
 crops={6:[2,1,10],8:[9],9:[7,0,5,6,12],10:[0,1,2,3],15:[8,9,10],21:[15]}
 for slide_num,tiles in crops.items():
  name=f'ppt/slides/slide{slide_num}.xml';root=E.fromstring(data[name])
  pics=root.findall('p:cSld/p:spTree/p:pic',N)
  if len(pics)!=len(tiles):raise ValueError(f'Unexpected picture count on content slide {slide_num}')
  iw,ih,rows=(2048,768,1) if slide_num==10 else (1672,941,4)
  for pic,tile in zip(pics,tiles):
   ext=pic.find('p:spPr/a:xfrm/a:ext',N)
   ratio=int(ext.get('cx'))/int(ext.get('cy'))
   x0,x1=(tile%4)/4,(tile%4+1)/4
   y0,y1=(tile//4)/rows,(tile//4+1)/rows
   tw,th=iw*(x1-x0),ih*(y1-y0)
   if tw/th>ratio:
    inset=(tw-th*ratio)/(2*iw);x0+=inset;x1-=inset
   else:
    inset=(th-tw/ratio)/(2*ih);y0+=inset;y1-=inset
   fill=pic.find('p:blipFill',N);rect=fill.find('a:srcRect',N)
   if rect is None:rect=E.Element('{'+A+'}srcRect');fill.insert(1,rect)
   rect.attrib.update({k:str(round(v*100000)) for k,v in [('l',x0),('t',y0),('r',1-x1),('b',1-y1)]})
  data[name]=E.tostring(root,encoding='utf-8',xml_declaration=True)
 with ZipFile(dst,'w',ZIP_DEFLATED)as z:
  for n,b in data.items():z.writestr(n,b)
 print(dst)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('output');a=p.parse_args();prepare(a.source,a.output)
