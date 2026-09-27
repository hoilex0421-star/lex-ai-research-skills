// Native editable content only. Official chrome is supplied by assemble_official.py.
// ARTIFACT_TOOL_MODULE can point to the bundled dist/artifact_tool.mjs.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const moduleName = process.env.ARTIFACT_TOOL_MODULE;
const {Presentation, PresentationFile} = await import(moduleName ? pathToFileURL(path.resolve(moduleName)).href : '@oai/artifact-tool');
const [specPath, output] = process.argv.slice(2);
if (!specPath || !output) throw new Error('Usage: node build_content.mjs deck-spec.json content.pptx');
try {await fs.access(output); throw new Error('Output already exists; use a new path.');}
catch (e) {if (e.code !== 'ENOENT') throw e;}
const spec = JSON.parse(await fs.readFile(specPath, 'utf8'));
const manifest = JSON.parse(await fs.readFile(new URL('../assets/official-template.json', import.meta.url), 'utf8'));
const p = Presentation.create({slideSize: {width: manifest.slide_size_emu[0]/9525, height: 720}});
const C = {red:'#C7000A', ink:'#1D1D1A', gray:'#666666', pale:'#EBEBEB', white:'#FFFFFF'};
const X=manifest.body_region_emu[0]/9525, Y=manifest.body_region_emu[1]/9525;
const W=manifest.body_region_emu[2]/9525;
const font='Microsoft YaHei';
function text(slide, value, x, y, w, h, {small=false, color=C.ink, bold=false}={}) {
  const s=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  s.text=value;
  s.text.style={typeface:font,fontSize:(small?12.99:18)*4/3,color,bold,autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};
  return s;
}
function box(slide,x,y,w,h,fill=C.pale) {
  return slide.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});
}
function note(slide,value) {text(slide,value,X,Y+444,W,38,{small:true,color:C.gray});}
function table(slide,values,widths,height=354) {
  const t=slide.tables.add({rows:values.length,columns:values[0].length,left:X,top:Y+8,width:W,height,values,columnWidths:widths.map(n=>n*W)});
  t.styleOptions={headerRow:false,bandedRows:false};
  t.cells.block({row:0,column:0,rowCount:values.length,columnCount:values[0].length}).assign({
    fill:C.white,textStyle:{typeface:font,fontSize:24,color:C.ink},margins:{left:12,right:12,top:12,bottom:10},anchor:'center',
    borders:{fill:'#C4C4C4',width:0.6,style:'solid'}
  });
  for(let r=0;r<values.length;r++) for(let c=0;c<values[0].length;c++) {
    const cell=t.getCell(r,c);
    cell.fill=r===0?C.pale:C.white;
    cell.text.style={typeface:font,fontSize:r===0?24:17.32,color:c===0&&r>0?C.red:C.ink,bold:false};
  }
  return t;
}
let index=0;
for(const page of spec.slides.filter(x=>x.kind==='body')) {
  index++;
  if(page.content_slide!==index) throw new Error('content_slide must follow body-page order starting at 1.');
  const s=p.slides.add(), c=page.content;
  if(c.layout==='architecture') {
    c.layers.forEach((layer,i)=>{
      const y=Y+8+i*93;
      box(s,X,y,194,70,C.pale);
      text(s,layer[0],X+16,y+19,165,34,{color:C.red});
      box(s,X+209,y,W-209,70,'#F7F7F7');
      text(s,layer[1],X+227,y+21,W-247,36);
    });
  } else if(c.layout==='flow') {
    const gap=42, w=(W-3*gap)/4;
    const nodes=c.stages.map((stage,i)=>{
      const x=X+i*(w+gap);
      const n=box(s,x,Y+45,w,82);
      text(s,stage[0],x+14,Y+70,w-28,36,{color:C.red});
      text(s,stage[1],x,Y+155,w,122,{small:true});
      return n;
    });
    for(let i=0;i<nodes.length-1;i++) s.shapes.add({geometry:'rightArrow',position:{left:X+i*(w+gap)+w+10,top:Y+77,width:gap-20,height:17},fill:C.red,line:{fill:'none',width:0}});
    text(s,c.takeaway,X,Y+335,W,62);
  } else if(c.layout==='comparison' || c.layout==='validation') {
    table(s,c.rows,c.widths,c.layout==='validation'?365:354);
  } else if(c.layout==='evidence') {
    const left=W*.58;
    box(s,X,Y+8,left,369,'#F7F7F7');
    text(s,c.evidenceLabel,X+20,Y+25,left-40,38,{color:C.red});
    c.evidence.forEach((line,i)=>text(s,line,X+20,Y+92+i*73,left-40,58));
    text(s,'判断与边界',X+left+34,Y+25,W-left-34,38,{color:C.red});
    c.inferences.forEach((line,i)=>text(s,line,X+left+34,Y+92+i*88,W-left-34,76,{small:true}));
  } else throw new Error(`Unsupported sample layout: ${c.layout}`);
  note(s,c.note);
  s.speakerNotes.textFrame.setText(page.notes);
}
await fs.mkdir(path.dirname(output),{recursive:true});
await (await PresentationFile.exportPptx(p)).save(output);
console.log(JSON.stringify({bodySlides:index,output}));
