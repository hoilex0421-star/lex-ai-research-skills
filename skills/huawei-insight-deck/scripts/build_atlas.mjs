// H01–H42 examples: original content arrangements inside the pinned official body.
// New charts/tables/text are native. Synthetic project data are labeled on-page.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const mod=process.env.ARTIFACT_TOOL_MODULE;
const {Presentation,PresentationFile}=await import(mod?pathToFileURL(path.resolve(mod)).href:'@oai/artifact-tool');
const [specPath,output]=process.argv.slice(2);
if(!output)throw Error('Usage: node build_atlas.mjs deck-spec.json content.pptx');
try{await fs.access(output);throw Error('Use a new output filename');}catch(e){if(e.code!=='ENOENT')throw e;}
const spec=JSON.parse(await fs.readFile(specPath,'utf8'));
const base=path.dirname(specPath);
const manifest=JSON.parse(await fs.readFile(new URL('../assets/official-template.json',import.meta.url),'utf8'));
const P=Presentation.create({slideSize:{width:manifest.slide_size_emu[0]/9525,height:720}});
const F='Microsoft YaHei',R='#C7000A',K='#1D1D1A',G='#666666',L='#EBEBEB',W='#FFFFFF',A='#F4A100';
const X=manifest.body_region_emu[0]/9525,Y=manifest.body_region_emu[1]/9525,BW=manifest.body_region_emu[2]/9525;
const assets={};for(const k of ['scenes','people','campus'])assets[k]=new Uint8Array(await fs.readFile(path.join(base,k+'.png')));
let s;
function shape(geometry,x,y,w,h,fill=L,stroke='none',width=0){return s.shapes.add({geometry,position:{left:X+x,top:Y+y,width:w,height:h},fill,line:{fill:stroke,width}});}
function text(value,x,y,w,h=48,{small=false,color=K,bold=false,center=false,size}={}){
 const t=shape('textbox',x,y,w,h,'none');t.text=value;t.text.style={typeface:F,fontSize:size??(small?17.32:24),color,bold,alignment:center?'center':'left',verticalAlignment:'top',autoFit:'none',wrap:'square',insets:{top:0,right:0,bottom:0,left:0}};return t;
}
function label(v,x,y,w=250,color=R){return text(v,x,y,w,36,{color});}
function rule(x,y,w,color=L){shape('rect',x,y,w,1.5,color);}
function arrow(x,y,w=35,h=15,direction='right'){shape(direction+'Arrow',x,y,w,h,R);}
function line(x1,y1,x2,y2,color=G,width=1.5){
 const sh=shape('line',Math.min(x1,x2),Math.min(y1,y2),Math.abs(x2-x1),Math.abs(y2-y1),'none',color,width);
 if((x2-x1)*(y2-y1)<0)sh.position={...sh.position,verticalFlip:true};
 return sh;
}
function para(head,body,x,y,w,h=124){label(head,x,y,w);text(body,x,y+43,w,h-43,{small:true});}
function panel(head,body,x,y,w,h=290){shape('rect',x,y,w,h,'#F7F7F7');shape('rect',x,y,4,h,R);para(head,body,x+20,y+19,w-40,h-35);}
function three(items,y=20,h=330){const gap=26,w=(BW-gap*2)/3;items.forEach((v,i)=>panel(v[0],v[1],i*(w+gap),y,w,h));}
function table(values,x,y,w,h,widths){
 const compact=h/values.length<45;
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:X+x,top:Y+y,width:w,height:h,values,columnWidths:(widths??Array(values[0].length).fill(1/values[0].length)).map(n=>n*w)});
 t.styleOptions={headerRow:false,bandedRows:false};
 t.borders.assign({style:'solid',fill:'#C4C4C4',width:0.6});
 t.cells.block({row:0,column:0,rowCount:values.length,columnCount:values[0].length}).assign({margins:{left:12,right:12,top:compact?3:10,bottom:compact?3:8},anchor:'center'});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
  const cell=t.getCell(r,c);cell.fill=r===0?L:W;cell.text.style={typeface:F,fontSize:r===0&&!compact?24:17.32,color:r>0&&c===0?R:K,bold:false};
 }
 return t;
}
function photo(tile,x,y,w,h,{person=false,circle=false}={}){
 const cols=4,rows=person?1:4,c=tile%cols,r=Math.floor(tile/cols);
 return s.images.add({blob:assets[person?'people':'scenes'],contentType:'image/png',alt:person?'AI生成虚构项目角色':'AI生成机器人场景示意',fit:'cover',geometry:circle?'ellipse':'rect',crop:{left:c/cols,top:r/rows,right:1-(c+1)/cols,bottom:1-(r+1)/rows},position:{left:X+x,top:Y+y,width:w,height:h}});
}
const ctext={typeface:F,fontSize:17.32,fill:K};
function chart(type,categories,series,x,y,w,h,extra={}){
 return s.charts.add(type,{position:{left:X+x,top:Y+y,width:w,height:h},categories,series:series.map((v,i)=>({...v,fill:v.fill??[R,'#919191',A,'#C4C4C4'][i%4]})),hasLegend:false,titleTextStyle:ctext,
 chartFill:'none',plotAreaFill:'none',chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0},
 xAxis:{textStyle:ctext,line:{fill:'#919191',width:0.8},majorGridlines:null},yAxis:{textStyle:ctext,min:0,majorGridlines:{fill:L,width:0.6},line:{fill:'none',width:0}},dataLabels:{showValue:true,position:'outEnd',textStyle:ctext},
 ...extra});
}
function donut(vals,x,y,w=380,h=320){return chart('doughnut',vals.map(v=>v[0]),[{name:'演示占比',values:vals.map(v=>v[1]),points:vals.map((v,i)=>({idx:i,fill:[R,'#666666',A,'#919191','#C4C4C4'][i]}))}],x,y,w,h,{xAxis:{visible:false},yAxis:{visible:false},doughnutOptions:{holeSize:62},dataLabels:{showPercent:true,showValue:false,position:'center',textStyle:{...ctext,fill:W}},hasLegend:false});}
function legendRows(items,x,y,w,step=58){items.forEach((a,i)=>{shape('rect',x,y+i*step+7,12,12,[R,'#666666',A,'#919191','#C4C4C4'][i]);text(a,x+24,y+i*step,w-24,step-7,{small:true});});}
function bottom(page,qualifier='原创分析示例；未对应真实项目承诺或平台实测'){text(`${page.id} · ${page.name}｜${qualifier}`,0,447,BW,43,{small:true,color:G});}
function stepNode(head,body,x,y,w,h=108){shape('rect',x,y,w,h,L);text(head,x+14,y+12,w-28,32,{color:R});text(body,x+14,y+49,w-28,h-55,{small:true});}
function circleNode(head,sub,x,y,d=135){shape('ellipse',x,y,d,d,L);text(head,x+10,y+32,d-20,33,{center:true,color:R});if(sub)text(sub,x+12,y+70,d-24,43,{small:true,center:true});}
for(const page of spec.slides){
 if(page.kind!=='body')continue;
 s=P.slides.add();let qualifier='原创分析示例；未对应真实项目承诺或平台实测';
 switch(page.id){
 case 'H04':
  para('问题：模型能力不等于系统需求','同样是动作生成，输入视角、历史帧、动作块长度和去噪步数不同，计算、显存与时延约束也不同。',0,12,620,126);
  para('分析：沿实际执行链路拆解','先绑定任务质量和实时要求，再测量数据加载、前向计算、后处理与执行等待；避免用参数量单独推导卡数。',0,168,620,132);
  panel('面向决策的输出','负载画像\n模型版本、输入规格、精度与批量\n\n瓶颈定位\n显存峰值、通信占比、等待时间\n\n验证建议\n优先实验、质量门槛、复现材料',685,12,BW-685,380);
  text('交付物：负载表、基线日志、受约束的优化清单。',0,353,630,67);
  break;
 case 'H05':
  three([['数据工程','输入：多视角视频、动作与事件\n\n处理：校准、对齐、切片、质检\n\n输出：版本化数据集与质量报告\n\n边界：保留授权与来源记录'],['训练工程','输入：固定模型、配方与样本集\n\n处理：复现基线、剖析、对照优化\n\n输出：配置、权重与性能记录\n\n边界：以等质量耗时比较'],['评测部署','输入：策略版本与任务清单\n\n处理：回放、仿真、现场回归\n\n输出：评测日志与上线条件\n\n边界：公开结果不代替实测']],10,392);break;
 case 'H06':{
  line(108,25,108,382,R,3);
  const stages=[['W1–2','复现与边界确认','冻结模型、输入与验收口径；保存可重跑的基线。'],['W3–4','负载剖析','分离计算、通信、数据等待；确定优先优化项。'],['W5–8','受控优化','一次改变一个主要变量；保留质量及资源对照。'],['W9–12','复测与交付','多次重复、异常回归；交付复现包与适用限制。']];
  stages.forEach((a,i)=>{const y=10+i*98;shape('ellipse',98,y+14,20,20,R);text(a[0],0,y+8,82,35,{small:true,color:G});label(a[1],147,y,280);text(a[2],147,y+42,900,42,{small:true});});
  qualifier='建议十二周试点节奏；周期与退出条件待双方确认';break;}
 case 'H07':
  chart('bar',['数据等待','前向与反向','通信同步','参数更新'],[{name:'分钟',values:[18,12,6,4]}],0,18,715,350,{barOptions:{direction:'bar',grouping:'clustered',gapWidth:65},xAxis:{...{textStyle:ctext},min:0,max:20,title:{text:'单轮耗时（分钟）',textStyle:ctext}},yAxis:{textStyle:ctext,majorGridlines:null}});
  para('18 / 40 = 45%','演示基线中，数据等待占单轮耗时的45%。首先检查样本解码、存储吞吐和预取队列。',770,30,335,135);
  para('优化假设','若等待缩短6分钟，其他部分保持不变，单轮总耗时从40降为34分钟。',770,207,335,112);
  text('预计耗时下降15%，仍需验证任务质量与运行稳定性。',770,351,335,76,{small:true,color:R});
  qualifier='演示数据：40分钟拆分为18+12+6+4；不是实测加速结论';break;
 case 'H08':{
  const vals=[['采集','多视角、动作、事件'],['质检','时间同步与完整性'],['训练','冻结配方与基线'],['评测','质量与尾延迟'],['部署','回滚与异常记录']];
  const gap=26,w=(BW-4*gap)/5;
  vals.forEach((a,i)=>{stepNode(a[0],a[1],i*(w+gap),34,w,126);if(i<4)arrow(i*(w+gap)+w+5,87,16,13);});
  table([['质量关口','检查项','未通过时的处理'],['数据进入训练','标注一致性、帧与动作对齐','隔离批次，回到采集/处理环节'],['模型进入现场','任务质量、实时预算、失败恢复','保留旧版本，补充回归用例'],['现场反馈回流','样本授权、失败分类、复现条件','补齐记录后再纳入数据集']],0,210,BW,203,[.20,.43,.37]);break;}
 case 'H09':{
  const vals=[['观察证据','检查遮挡、相机位姿、视角变化。','留存：原始帧、时间戳、标定版本'],['动作证据','检查动作语义、夹爪状态与接触。','留存：控制频率、动作序列、事件'],['结果证据','区分完成、失败、人工接管。','留存：任务状态、失败类型、回放']];
  const w=(BW-48)/3;vals.forEach((a,i)=>{photo([2,1,10][i],i*(w+24),12,w,185);label(a[0],i*(w+24),217,w);text(a[1]+'\n\n'+a[2],i*(w+24),262,w,119,{small:true});});qualifier='AI场景示意；文字为建议证据字段，不是真实实验照片';break;}
 case 'H11':
  shape('rect',0,10,BW,390,'#F7F7F7');
  for(const[x,y]of[[0,10],[BW-30,10],[0,370],[BW-30,370]]){shape('rect',x,y,30,3,R);shape('rect',x<1?x:x+27,y,3,30,R);}
  para('研究对象','面向多视角视觉输入、语言指令与连续动作输出的具身策略，讨论其数据管线、训练负载和部署约束。',28,32,BW-56,91);
  para('比较口径','所有性能比较绑定模型与版本、数据集、输入长度、精度、批量、平台与软件栈；训练比较进一步约束目标质量。',28,153,BW-56,91);
  para('结论边界','机制分析用于提出可检验假设。公开论文、厂商自报和目标平台实测分别记录；不从单点吞吐推断端到端收益。',28,274,BW-56,105);break;
 case 'H12':
  photo(9,0,6,BW,193);label('双臂整理：从单次成功转向稳定完成',0,222,800);
  para('任务设置','软物体姿态多变；遮挡与接触影响动作执行。需要连续记录观察、动作、接管与结果。',0,279,345,132);
  para('系统问题','现场变化需要失败样本回流；训练吞吐和数据质量应分别测量，避免把问题都归因于算力。',390,279,345,132);
  para('验证路径','先冻结任务集与基础模型，再对输入策略、数据配方及推理配置做受控对照。',780,279,345,132);
  qualifier='AI场景示意与原创案例设定；非公开产品能力或真实客户项目';break;
 case 'H13':{
  const labels=['设备校准','任务采集','数据处理','仿真回放','现场回归'];const desc=['统一相机与机器人坐标','覆盖变化与失败恢复','切片、去噪与版本化','固定初始条件与任务','跟踪成功率与接管'];const w=(BW-48)/5;
  labels.forEach((a,i)=>{const x=i*(w+12);photo([7,0,5,6,12][i],x,20,w,170);shape('rect',x,203,w,39,R);text(a,x+7,208,w-14,30,{small:true,color:W,center:true});text(desc[i],x,262,w,77,{small:true});text('证据 '+['标定参数','时间戳日志','质检报告','回放脚本','失败清单'][i],x,368,w,55,{small:true,color:G});});
  qualifier='五图为AI生成场景示意；每阶段配一类可追溯交付物';break;}
 case 'H14':{
  const vals=[['技术负责人','模型与验收边界','定义任务集和质量目标\n审批模型与配方变更'],['系统工程师','性能与运行环境','复现基线和剖析瓶颈\n维护配置与优化记录'],['数据负责人','采集与资产质量','设计任务覆盖与质检\n管理授权、版本与分发'],['验证工程师','回归与现场稳定性','执行对照和异常回放\n维护验收与回滚清单']];
  const w=(BW-60)/4;vals.forEach((a,i)=>{const x=i*(w+20);photo(i,x+40,5,w-80,163,{person:true,circle:true});label(a[0],x,190,w);text(a[1],x,232,w,36,{small:true,color:G});rule(x,276,w);text(a[2],x,296,w,84,{small:true});});qualifier='AI生成虚构角色；展示职责分工，不代表真实团队或个人履历';break;}
 case 'H15':
  chart('bar',['第1月','第2月','第3月'],[{name:'验收通过',values:[24,32,40],fill:R},{name:'待补充',values:[6,8,10],fill:'#666666'}],0,18,650,362,{barOptions:{direction:'column',grouping:'stacked',gapWidth:90},hasLegend:true,legend:{position:'bottom',textStyle:ctext},dataLabels:{showValue:true,position:'center',textStyle:{...ctext,fill:W}},yAxis:{textStyle:ctext,min:0,max:60,title:{text:'数据批次',textStyle:ctext}}});
  [['120批','进入验收｜30+40+50'],['96批','验收通过｜24+32+40'],['80%','累计通过率｜96/120']].forEach((a,i)=>{label(a[0],744,24+i*131,300);text(a[1],744,70+i*131,360,48,{small:true});});qualifier='演示数据；通过率按批次计算，不代表样本质量或业务结果';break;
 case 'H16':
  chart('bar',['M1','M2','M3','M4','M5','M6'],[{name:'验收批次',values:[18,25,33,41,48,60],fill:'#919191'},{name:'一次通过率（%）',values:[62,66,71,75,79,82],fill:R}],0,22,748,360,{barOptions:{direction:'column',grouping:'clustered',gapWidth:110},hasLegend:true,legend:{position:'bottom',textStyle:ctext},dataLabels:{showValue:true,position:'outEnd',textStyle:ctext},yAxis:{textStyle:ctext,min:0,max:100}});
  para('规模与质量同时观察','演示期内验收批次从18增至60；一次通过率从62%增至82%，提升20个百分点。',793,20,325,143);
  para('解释需要补充证据','区分任务难度、客户构成和验收规则变化；不要把相关走势直接解读为某项优化的因果结果。',793,207,325,170);
  qualifier='演示数据；柱为批次、线为通过率，右轴单位为%；未归因于真实产品';break;
 case 'H17':{
  const nodes=[['数据资产','来源、授权、版本',10,18],['训练实验','配置、日志、权重',403,0],['评测结果','任务、指标、失败',796,18],['部署包','依赖、接口、回滚',10,255],['运行记录','事件、接管、异常',403,299],['问题闭环','归因、工单、回归',796,255]];
  for(const a of nodes){line(564,209,a[2]+158,a[3]+52,'#919191');}
  shape('ellipse',450,125,222,154,R);text('实验资产中心',470,162,182,40,{color:W,center:true});text('统一标识与血缘',471,217,182,30,{small:true,color:W,center:true});
  nodes.forEach(a=>stepNode(a[0],a[1],a[2],a[3],316,106));break;}
 case 'H18':{
  const vals=[['L1 可复现','冻结配方与环境'],['L2 可定位','找到主要瓶颈'],['L3 可交付','固化验收与回滚'],['L4 可复制','标准包迁移复用']];
  for(let i=0;i<3;i++)line(90+i*288,346-i*78,90+(i+1)*288,346-(i+1)*78,R,3);
  vals.forEach((a,i)=>{const x=i*288,y=327-i*78;shape('ellipse',x+73,y,34,34,R);label(a[0],x,y-72,260);text(a[1],x,y+50,258,59,{small:true});});qualifier='建议成熟度路径；每级以可检查的退出条件判断，而非按时间自动晋级';break;}
 case 'H19':
  photo(8,25,20,230,230,{circle:true});photo(9,430,20,230,230,{circle:true});photo(10,835,20,230,230,{circle:true});
  [['仓储搬运','路径与节拍','测量：尾延迟、阻塞、异常恢复'],['柔性整理','接触与长尾','测量：任务成功率、接管次数'],['包裹分拣','类别与吞吐','测量：错分率、每小时处理量']].forEach((a,i)=>{const x=i*405;label(a[0],x+15,271,300);text(a[1]+'\n\n'+a[2],x+15,316,300,100,{small:true});});qualifier='AI场景示意；候选应用不表示真实客户覆盖或产品已验证能力';break;
 case 'H20':{
  const vals=[['can','数据接入','格式、授权、增量同步'],['flowChartDecision','质量门禁','完整性、一致性、异常'],['cube','训练运行','配方、环境、资源记录'],['hexagon','模型管理','权重、版本、来源关系'],['gear6','推理优化','精度、批量、尾延迟'],['cloud','任务调度','优先级、配额与重试'],['flowChartDocument','评测报告','任务、口径、失败样本'],['homePlate','现场部署','接口、监控、版本回滚']];
  vals.forEach((a,i)=>{const x=(i%4)*288,y=Math.floor(i/4)*207;shape(a[0],x+12,y+18,58,58,L,R,1.5);label(a[1],x+85,y+25,174);text(a[2],x+12,y+104,248,76,{small:true});rule(x+12,y+187,250);});qualifier='建议能力清单；并非对某个现有平台实现状态的声明';break;}
 case 'H21':
  s.images.add({blob:assets.campus,contentType:'image/png',alt:'AI生成虚构园区示意图',fit:'contain',position:{left:X,top:Y+5,width:735,height:415}});
  [[185,125,'A'],[188,306,'B'],[553,106,'C'],[516,241,'D'],[605,336,'E']].forEach(([x,y,n],i)=>{shape('ellipse',x,y,35,35,[R,'#666666',A,'#919191','#C4C4C4'][i]);text(n,x,y+4,35,28,{small:true,color:i<2?W:K,center:true});});
  legendRows(['A 仓储区：移动与搬运采集','B 测试区：操作任务与回归','C 管理区：任务与授权管理','D 数据区：处理、存储与训练','E 交付区：设备维护与出入库'],784,20,337,73);qualifier='AI生成虚构园区地图；点位用于示例，不对应实际客户或真实地理布局';break;
 case 'H22':{
  const vals=[['1个试点','证明任务可完成'],['3类场景','形成验收与回归'],['6个项目','复用数据与工具'],['12个项目','建立交付标准包']];
  vals.forEach((a,i)=>{const x=15+i*277,h=90+i*58,y=390-h;shape('rect',x,y,250,h,i===3?R:L);text(a[0],x+16,y+16,220,38,{color:i===3?W:R});text(a[1],x+16,y+64,218,64,{small:true,color:i===3?W:K});});qualifier='演示规划数；非经营预测，新增项目须先验证客户需求与交付能力';break;}
 case 'H23':
  [[30,65,'数据','失败样本→训练资产'],[402,65,'模型','配方迭代→策略版本'],[774,65,'部署','运行问题→回归用例']].forEach(([x,y,a,b])=>{shape('gear6',x+36,y,250,250,L,R,1.8);text(a,x+82,y+83,158,40,{color:R,center:true});text(b,x,y+278,324,65,{small:true,center:true});});
  arrow(322,180,66,20);arrow(694,180,66,20);line(173,395,932,395,R,2);arrow(163,388,30,14,'left');text('共享条件：样本授权、实验标识、质量阈值、可复现记录',284,399,680,35,{small:true});break;
 case 'H24':{
  arrow(18,195,BW-36,45);
  const vals=[['任务定义','任务边界与质量阈值','产出：验收规格'],['数据就绪','授权、覆盖、同步与质检','产出：数据清单'],['基线冻结','固定模型、配方与环境','产出：复现记录'],['交付验收','回归、回滚与已知限制','产出：交付包']];
  vals.forEach((a,i)=>{const x=i*286;const upper=i%2===0;const y=upper?5:276;para(a[0],a[1]+'\n\n'+a[2],x,y,257,131);line(x+110,upper?148:241,x+110,upper?195:272,R,1.5);});qualifier='建议推进路径；以完成条件推进，不预设合同或已承诺日期';break;}
 case 'H25':
  photo(15,0,5,BW,410);shape('rect',0,223,560,192,R);text('一次成功，还不足以交付',24,248,516,45,{color:W});text('要记录失败发生的条件，\n并验证同类问题能否稳定恢复。',24,305,516,78,{color:W});qualifier='AI场景示意；文字为原创情景表达，不是真实客户引语';break;
 case 'H26':
  para('薄基础：模型演示先行','数据边界不清、测试条件变化，增加模型能力后，仍难解释现场表现。',0,4,505,104);
  para('厚基础：数据与验证先行','固化样本来源、任务集和基线，模型迭代的收益才能被记录和复用。',620,4,505,104);
  [['场景结果',120,135,280],['模型与策略',80,221,360],['数据与验证',140,307,240]].forEach(([a,x,y,w])=>{shape('rect',x,y,w,63,L);text(a,x+10,y+16,w-20,35,{center:true});});
  [['场景结果',762,135,260],['模型与策略',706,221,372],['数据与验证',630,307,514]].forEach(([a,x,y,w])=>{shape('rect',x,y,Math.min(w,BW-x),63,a==='数据与验证'?R:L);text(a,x+10,y+16,Math.min(w,BW-x)-20,35,{center:true,color:a==='数据与验证'?W:K});});
  qualifier='结构隐喻：基础宽度表达依赖关系，不表示资源或性能数值';break;
 case 'H27':
  three([['问题一｜数据不可追溯','表现：样本来源、授权和版本散落\n\n影响：训练结果难定位到数据变化\n\n根因假设：没有统一资产标识\n\n验证：抽查一批数据的完整血缘'],['问题二｜实验不可复现','表现：配方、环境和日志记录缺失\n\n影响：优化收益难被稳定重现\n\n根因假设：交付物不包含运行条件\n\n验证：由另一名工程师独立复跑'],['问题三｜现场反馈断裂','表现：失败只有视频，没有条件\n\n影响：问题难转成回归与训练样本\n\n根因假设：数据与现场工单脱节\n\n验证：抽查失败到回归的闭环记录']],4,405);break;
 case 'H28':
  donut([['SOM',200],['SAM其余',600],['TAM其余',1600]],0,10,455,335);
  legendRows(['SOM：200万元','SAM其余：600万元','TAM其余：1,600万元'],23,343,430,29);
  table([['范围','演算假设','年收入空间'],['TAM','120家 × 20万元/年','2,400万元'],['SAM','40家 × 20万元/年','800万元'],['SOM','10家 × 20万元/年','200万元']],510,21,614,304,[.18,.53,.29]);
  text('SOM ⊂ SAM ⊂ TAM。圆环按互斥区域拆分，三者总量不能直接相加。',510,358,612,63,{small:true,color:R});qualifier='纯演算假设，不是市场调查、收入预测或投资建议；需验证客户数与付费意愿';break;
 case 'H29':
  donut([['采集与质检',240],['训练与算力',150],['工程集成',90],['评测与现场',60],['项目预备',60]],0,26,510,365);
  legendRows(['采集与质检｜240万元 · 40%','训练与算力｜150万元 · 25%','工程集成｜90万元 · 15%','评测与现场｜60万元 · 10%','项目预备｜60万元 · 10%'],590,16,530,66);
  text('演示预算总额：600万元',590,368,520,40,{color:R});qualifier='假设预算，不代表实际融资或资源申请；金额合计600万元，占比合计100%';break;
 case 'H30':{
  const charts=[['仓储场景',[52,28,20]],['柔性操作',[30,45,25]],['工业分拣',[24,36,40]]];const w=(BW-54)/3;
  charts.forEach((a,i)=>{const x=i*(w+27);label(a[0],x,0,w);chart('bar',['方案A','方案B','方案C'],[{name:'占比',values:a[1],points:a[1].map((v,j)=>({idx:j,fill:[R,'#919191',A][j]}))}],x,53,w,284,{barOptions:{direction:'column',gapWidth:100},yAxis:{textStyle:ctext,min:0,max:60,numberFormatCode:'0"%"'},dataLabels:{showValue:true,position:'outEnd',textStyle:ctext}});text(['成熟方案集中，关注替换成本','任务差异大，先固定评测集','多方案并存，比较集成成本'][i],x,356,w,67,{small:true});});qualifier='合成份额数据；每个场景A/B/C合计100%，不代表真实厂商或市场份额';break;}
 case 'H31':
  three([['项目交付','客户入口：明确任务与现场边界\n\n收费对象：一次性集成与验收\n\n核心成本：采集、工程与现场人力\n\n复用资产：测试集、脚本、接口规范'],['持续服务','客户入口：上线后的质量与迭代\n\n收费对象：约定周期的维护服务\n\n核心成本：回归、支持与版本维护\n\n复用资产：监控、回滚、运维工具'],['数据产品','客户入口：有明确授权的标准数据\n\n收费对象：许可范围与更新服务\n\n核心成本：授权、质检与持续更新\n\n边界：不默认客户数据可再销售']],3,405);qualifier='商业模式假设；价格、授权、需求和毛利均需另行验证';break;
 case 'H32':{
  const vals=[['01 覆盖率','80%','已覆盖任务/目标任务',70,8],['02 通过率','85%','质检通过批次/送检批次',693,8],['03 使用率','70%','进入训练样本/合格样本',693,251],['04 闭环率','90%','完成回归问题/有效问题',70,251]];
  vals.forEach(([a,b,c,x,y])=>{shape('rect',x,y,330,150,L);label(a,x+20,y+16,290);text(b,x+20,y+59,150,47,{color:R});text(c,x+20,y+114,290,28,{small:true});});arrow(438,67,202,22);arrow(838,176,22,47,'down');arrow(438,314,202,22,'left');arrow(224,176,22,47,'up');text('反馈推动\n下一轮采集',440,191,200,68,{center:true});qualifier='指标与数值均为示例；四项分母不同，不可相乘得到整体成功率';break;}
 case 'H33':
  table([['交付范围','探索包','试点包','规模包'],['示例价格','10万元/次','30万元/次','60万元起/次'],['任务范围','单任务、单环境','约定任务集、固定现场','多任务与多现场，另定边界'],['核心交付','可行性记录与风险清单','数据/模型/基线与验收记录','标准包、运维与复制手册'],['验收方式','复现流程与问题明确','按约定质量和稳定性验收','按场景分批验收与回归'],['范围外费用','设备、差旅、算力另计','额外采集和变更另计','新增现场与持续服务另计']],0,15,BW,395,[.19,.27,.27,.27]);qualifier='虚构服务报价示例；税费、授权、算力和变更范围须在合同中另行确认';break;
 case 'H34':{
  shape('rect',0,3,BW,421,'#232323');
  const v=[['S｜优势','研究与工程衔接\n能把技术机制转成可复现实验\n\n行动：把验证材料纳入标准交付'],['W｜短板','现场经验和交付带宽有限\n定制任务容易消耗核心人员\n\n行动：限定首批任务与服务范围'],['O｜机会','模型迭代带来复测与迁移需求\n数据治理和质量保证可形成复用\n\n行动：先验证客户付费痛点'],['T｜威胁','客户自建、工具成熟与价格竞争\n数据授权和设备责任增加成本\n\n行动：明确资产边界与责任上限']];
  v.forEach((a,i)=>{const x=24+(i%2)*563,y=18+Math.floor(i/2)*209;text(a[0],x,y,510,35,{color:i<2?'#F4A100':W});text(a[1],x,y+46,510,146,{small:true,color:W});});line(562,25,562,400,'#666666',1);line(25,214,1098,214,'#666666',1);qualifier='针对虚构试点的战略分析示例；深色仅用于正文面板，保留官方白色页壳';break;}
 case 'H35':{
  const left=245,unit=68,top=46;
  for(let i=0;i<12;i++){text(String(i+1),left+i*unit,2,unit,30,{small:true,center:true,color:G});line(left+i*unit,42,left+i*unit,375,L,1);}
  const tasks=[['需求与验收规格',1,2,'负责人'],['采集与数据质检',2,5,'数据组'],['复现基线与剖析',3,6,'系统组'],['优化与受控对照',6,9,'算法/系统'],['现场回归与复测',9,11,'验证组'],['交付与知识移交',11,12,'共同验收']];
  tasks.forEach((a,i)=>{const y=top+i*54;text(a[0],0,y+8,230,30,{small:true});shape('rect',left+(a[1]-1)*unit+3,y+4,(a[2]-a[1]+1)*unit-6,32,i===5?R:'#919191');text(a[3],left+(a[1]-1)*unit+10,y+10,(a[2]-a[1]+1)*unit-20,23,{small:true,color:W,center:true});});
  text('W2：规格冻结',245,387,270,32,{small:true,color:R});text('W6：基线确认',545,387,270,32,{small:true,color:R});text('W12：交付验收',850,387,270,32,{small:true,color:R});qualifier='建议12周排期；依赖为规格→基线→对照→复测，实际资源与周期待确认';break;}
 case 'H36':{
  const vals=[['研发负责人','“希望换一位工程师，也能把同一结果跑出来。”','需求：环境、数据与配方一起交付','验证：独立复跑并比对结果'],['现场负责人','“最需要知道失败后如何恢复，而不只是成功视频。”','需求：异常分类、接管与回滚','验证：固定失败用例现场回归'],['采购负责人','“先说清楚交付范围和变更如何计价。”','需求：边界、验收和额外成本','验证：合同清单与分阶段验收']];
  const w=(BW-48)/3;vals.forEach((a,i)=>{const x=i*(w+24);shape('ellipse',x,3,56,56,L);text(String(i+1),x+13,12,30,32,{color:R});label(a[0],x+77,12,w-77);text(a[1],x,99,w,109);rule(x,232,w);text(a[2]+'\n\n'+a[3],x,265,w,130,{small:true});});qualifier='虚构访谈情景，非真实客户证言或合作背书；用于示范如何把反馈转成验收项';break;}
 case 'H37':
  stepNode('人工治理','目标、预算、工具权限、发布与回滚边界',70,0,1044,77);
  [['任务拆解','读取规格与上下文'],['执行工具','生成候选与实验'],['自动验证','测试、指标与日志']].forEach((a,i)=>{stepNode(a[0],a[1],70+i*372,138,300,104);if(i<2)arrow(390+i*372,181,26,17);});
  arrow(580,95,23,29,'down');arrow(580,259,23,29,'down');
  stepNode('人工门禁','触发：破坏性变更、质量下降、资源越界、解释不足',70,305,1044,104);
  line(30,365,70,365,R,2);arrow(20,48,20,317,'up');line(30,45,70,45,R,2);
  shape('rect',0,174,59,72,W);text('退回\n修正',0,181,59,64,{small:true,color:R,center:true});
  qualifier='建议协作机制：自动验证不通过则回退；关键决策由具名负责人确认';break;
 case 'H38':
  shape('rect',0,8,640,391,'#F7F7F7');
  stepNode('Human On｜治理层','方向、预算、权限、质量策略',22,25,596,84);arrow(305,126,22,33,'down');
  stepNode('自动执行｜运行层','任务编排、工具执行、回归、记录',22,176,365,110);stepNode('Human In','语义与风险裁决',416,176,201,110);arrow(390,217,23,16);
  text('正常路径自动推进；越过预设阈值时暂停并升级。',22,335,595,48,{small:true});
  para('治理决定规则','谁能使用哪些工具，最大消耗多少资源，什么条件可以发布；规则先于任务运行。',695,10,419,123);
  para('裁决处理例外','当性能回归、数据含义不清或方案影响较大时，负责人审查具体问题并给出结论。',695,158,419,123);
  para('统一记录','保留触发原因、证据、裁决人和恢复动作，避免人工处理游离于系统之外。',695,306,419,107);break;
 case 'H39':
  table([['角色','交付责任'],['技术负责人','规格、风险边界与发布决策'],['领域工程师','模型语义与关键技术判断'],['编排工程师','上下文、工具、执行与重试'],['验证工程师','回归、基准、日志与验收']],0,4,459,267,[.30,.70]);
  const flow=[['进入','目标与风险'],['定义','规格与验收'],['执行','工具与实验'],['验证','质量与资源'],['升级','异常与裁决'],['沉淀','日志与资产']];
  flow.forEach((a,i)=>stepNode(a[0],a[1],497+(i%3)*213,5+Math.floor(i/3)*139,197,119));
  table([['触发层','触发条件','动作'],['自动执行','测试通过、资源在限额内','继续执行并记录'],['人工裁决','质量回归、影响不明、风险升级','暂停相关步骤并审查'],['治理决策','发布、路线变化、资源追加','负责人确认后更新规则']],0,306,BW,130,[.17,.52,.31]);break;
 case 'H40':{
  const tasks=['P0 故障恢复｜运行/日志','P1 性能缺口｜算子/通信','P1 数据异常｜格式/时序','P2 文档补齐｜规格/示例'];
  label('任务池',0,3,400);tasks.forEach((a,i)=>{shape('rect',0,57+i*77,390,58,L);text(a,14,73+i*77,365,36,{small:true});});
  stepNode('匹配引擎','优先级\n标签覆盖\n可用负载\n风险等级',447,116,213,210);arrow(403,206,31,20);arrow(673,206,31,20);
  label('能力池',727,3,390);['人｜系统性能与通信','人｜模型语义与配方','人｜质量与现场验收','Agent｜日志分析与回归'].forEach((a,i)=>{shape('rect',727,57+i*77,397,58,L);text(a,742,73+i*77,366,36,{small:true});});break;}
 case 'H41':
  para('类比对象：制造质量管理','原料有批次，工艺有版本，过程有检测，产品有追溯；问题出现时可定位到材料与过程条件。',0,5,505,123);
  para('映射对象：训练交付体系','样本有来源，配方有版本，运行有记录，模型有验收；优化收益需要在受约束条件下复现。',617,5,506,123);
  table([['制造机制','训练交付对应','共同作用'],['原料批次','数据集版本与授权','界定输入边界'],['工艺参数','模型、配方与环境','固化执行条件'],['过程检测','日志、剖析与回归','发现异常变化'],['出厂验收','任务质量与部署门槛','约束交付结果']],0,163,BW,258,[.26,.39,.35]);qualifier='机制类比；不代表制造流程与模型训练在统计性质上完全等同';break;
 case 'H42':
  panel('改造前｜信息分散','配置依赖人工交接，基线环境不完整\n\n问题靠跨组会议推进，定位与复测串行\n\n交付只保留结果截图，后续难以复现',0,2,548,258);
  panel('改造后｜统一记录与门禁','版本化配置、数据与运行环境一起登记\n\n按问题标签组队，独立步骤并行推进\n\n保留对照、回归与风险审查材料',578,2,548,258);
  [['36 → 24小时','单次交付周期下降33.3%'],['12 → 6项','人工交接事项减少50%'],['70% → 100%','关键记录完整率提升30个百分点']].forEach((a,i)=>{const x=i*386;label(a[0],x,310,350);text(a[1],x,364,350,62,{small:true});});qualifier='合成案例；假设任务与质量门槛相同，不是某公司实测或保证收益';break;
 default:throw Error('Missing layout '+page.id);
 }
 bottom(page,qualifier);
 s.speakerNotes.textFrame.setText(page.notes+'\n本页口径：'+qualifier);
 page.notes+='\n本页口径：'+qualifier;
}
await fs.mkdir(path.dirname(output),{recursive:true});
await (await PresentationFile.exportPptx(P)).save(output);
// Persist page-level qualifiers for the official-shell assembler's speaker notes.
await fs.writeFile(path.join(path.dirname(output),'assembled-spec.json'),JSON.stringify(spec,null,2));
console.log(JSON.stringify({bodySlides:P.slides.items.length,output}));
