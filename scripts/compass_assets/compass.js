var C = {navy:'#0d2244',green:'#15803d',orange:'#a16207',red:'#b91c1c',blue:'#1d4ed8',muted:'#6b7a92',grid:'#ece5d4',gold:'#b8924a'};
var FF = 'Inter,"Noto Sans TC",sans-serif';
var baseTip = {backgroundColor:'#fff',borderColor:'#e5dfd0',borderWidth:1,textStyle:{color:C.navy,fontSize:12,fontFamily:FF}};
function mkAxis(o){var b={axisLine:{lineStyle:{color:C.grid}},axisTick:{show:false},axisLabel:{color:C.muted,fontFamily:FF,fontSize:11},splitLine:{lineStyle:{color:C.grid}}};var r=Object.assign({},b,o||{});if(o&&o.axisLabel)r.axisLabel=Object.assign({color:C.muted,fontFamily:FF,fontSize:11},o.axisLabel);return r;}

var CELL = {
  fuelled:  {col:C.green,  en:'Uptrend · Fuelled',    zh:'上行·有燃料'},
  draining: {col:C.orange, en:'Uptrend · Draining',   zh:'上行·資金退'},
  reflating:{col:C.blue,   en:'Downtrend · Reflating', zh:'下行·資金回流'},
  starved:  {col:C.red,    en:'Downtrend · Starved',  zh:'下行·斷炊'},
  warmup:   {col:'#9aa7bb',en:'Warm-up',              zh:'暖機'}
};
var MKT='us', D, Q, MOM, CRED, QUAD, WARN, CARD, CUR, LANG='en';
function useMarket(m){MKT=(m==='tw'||m==='my'||m==='jp'||m==='au')?m:'us';
  D=(MKT==='tw'?D_TW:MKT==='my'?D_MY:MKT==='jp'?D_JP:MKT==='au'?D_AU:D_US);
  Q=D.q;MOM=D.mom;CRED=D.cred;QUAD=D.quad;WARN=D.warn;CARD=D.card;CUR=Q.length-1;}
useMarket('us');

function fmtPc(x){return (x>=0?'+':'−')+Math.abs(x).toFixed(1)+'%';}
function hexA(hex,a){var n=parseInt(hex.slice(1),16);return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')';}
function sinceQ(){var c=QUAD[CUR];for(var i=CUR;i>=0;i--){if(QUAD[i]!==c)return Q[i+1];}return Q[0];}

function fillJudge(isZh){
  var L=isZh?'zh':'en', setAll=function(cls,txt){document.querySelectorAll('.'+cls).forEach(function(e){e.textContent=txt;});};
  document.querySelectorAll('.curPhase').forEach(function(e){e.textContent=CELL[QUAD[CUR]][L];e.style.color=CELL[QUAD[CUR]].col;});
  setAll('curQtr',Q[CUR]);
  var mup=MOM[CUR]>=0, cup=CRED[CUR]>=0;
  setAll('jMom',(isZh?(mup?'上漲 ':'下跌 '):(mup?'up ':'down '))+'('+(MOM[CUR]>=0?'+':'−')+Math.abs(MOM[CUR]).toFixed(2)+')');
  setAll('jCred',(isZh?(cup?'擴張 ':'收縮 '):(cup?'expanding ':'contracting '))+'('+(CRED[CUR]>=0?'+':'−')+Math.abs(CRED[CUR]).toFixed(2)+')');
  setAll('jSince',sinceQ());
  var s=D.qstat[QUAD[CUR]];
  if(s&&s.n){setAll('jpMed',fmtPc(s.med));setAll('jpN',s.n);}
  // era-split honesty note: full-history medians can hide a post-2010 shift — see if this
  // market's scored history is effectively all-modern, or split the current cell pre/post-2010.
  var era=D.qstat_era?D.qstat_era[QUAD[CUR]]:null, post=era?era.post:null;
  var eraTxt;
  if(D.all_modern){
    eraTxt=isZh?'這個市場可評分的歷史幾乎全在 2010 年後——上面的數字本身就是現代時代。':
      "This market's scored history is effectively all post-2010 — the number above is already the modern era.";
  } else if(post&&post.n>=8){
    eraTxt=isZh?('僅看 2010 年後：中位 '+fmtPc(post.med)+'（n='+post.n+'）。'):
      ('Post-2010 era alone: median '+fmtPc(post.med)+' (n='+post.n+').');
  } else {
    var pn=post?post.n:0;
    eraTxt=isZh?('2010 年後落在此格的樣本太少，不足以評分（n='+pn+'）。'):
      ('Post-2010 sample in this cell is too thin to score (n='+pn+').');
  }
  setAll('jhistEra',eraTxt);
  ['fuelled','draining','reflating','starved'].forEach(function(p){var f=D.qstat[p]||{n:0};
    setAll('med-'+p,f.n?fmtPc(f.med):'—');setAll('n-'+p,f.n||0);
    setAll('rng-'+p,f.n?(fmtPc(f.mn)+' → '+fmtPc(f.mx)):'—');});
  // now-tag + row highlight
  document.querySelectorAll('.nowtag').forEach(function(e){e.textContent='';});
  document.querySelectorAll('.now-'+QUAD[CUR]).forEach(function(e){e.textContent=isZh?' （現在）':' (now)';});
  document.querySelectorAll('.mtbl tr').forEach(function(t){t.classList.remove('hl');});
  document.querySelectorAll('.mtbl tr[data-ph="'+QUAD[CUR]+'"]').forEach(function(t){t.classList.add('hl');});
  // supply-glut warning bar
  var w=document.querySelector('.jwarn'); if(w) w.style.display=WARN[CUR]?'inline-flex':'none';
}

function gauge(id,z,leftLab,rightLab){
  var el=document.getElementById(id); if(!el)return;
  if(z==null){el.innerHTML='<div class="gtrack"></div><div class="gmid"></div>';return;}
  var pct=Math.max(4,Math.min(96,50+(z/3)*45)), col=z>=0?C.green:C.red;
  el.innerHTML='<div class="gtrack"></div><div class="gmid"></div>'+
    '<div class="gends"><span>'+leftLab+'</span><span>'+rightLab+'</span></div>'+
    '<div class="gpin" style="left:'+pct+'%;background:'+col+'"></div>';
}
function fillCard(isZh){
  gauge('g-val',CARD.valuation[CUR], isZh?'貴':'expensive', isZh?'便宜':'cheap');
  gauge('g-pop',CARD.population[CUR], isZh?'萎縮':'shrinking', isZh?'成長':'growing');
  gauge('g-sup',CARD.supply[CUR], isZh?'過剩':'glut', isZh?'緊':'tight');
}

/* rank bar: pin position = (n-rank)/(n-1) so rank 1 (best) sits at the right */
function xcbar(barId,valId,v,unit,rank,n,isCarry){
  var el=document.getElementById(barId), vel=document.getElementById(valId);
  if(!el)return;
  if(v==null||rank==null||n==null){el.innerHTML='<div class="xctrack"></div>';if(vel)vel.textContent='—';return;}
  var pct=n>1?Math.max(4,Math.min(96,((n-rank)/(n-1))*100)):50;
  var col=isCarry?C.gold:(pct>=50?C.green:C.red);
  el.innerHTML='<div class="xctrack'+(isCarry?' xctrack-carry':'')+'"></div>'+
    '<div class="xcpin'+(isCarry?' xcpin-carry':'')+'" style="left:'+pct+'%;background:'+col+'"></div>';
  if(vel) vel.textContent=(v<0?'−':'')+Math.abs(v).toFixed(1)+unit+' · #'+rank+'/'+n;
}
function fillXC(isZh){
  if(D.xc==null)return;
  var X=D.xc;
  gauge('g-xc-val', X.valcomp, isZh?'貴':'expensive', isZh?'便宜':'cheap');
  xcbar('g-xc-pti','v-xc-pti', X.pti&&X.pti.v, 'x', X.pti&&X.pti.rank, X.n);
  xcbar('g-xc-yield','v-xc-yield', X.yield&&X.yield.v, '%', X.yield&&X.yield.rank, X.n);
  xcbar('g-xc-carry','v-xc-carry', X.carry&&X.carry.v, '%', X.carry&&X.carry.rank, X.n, true);
  xcbar('g-xc-vac','v-xc-vac', X.vac&&X.vac.v, '%', X.vac&&X.vac.rank, X.n);
  xcbar('g-xc-pop','v-xc-pop', X.pop&&X.pop.v, '%', X.pop&&X.pop.rank, X.n);
}

var allCharts=[];
function initCharts(lang){
  allCharts.length=0; var isZh=lang==='zh';
  var cn={}; Object.keys(CELL).forEach(function(k){cn[k]=CELL[k][isZh?'zh':'en'];});
  fillJudge(isZh); fillCard(isZh); fillXC(isZh);

  /* ===== compass scatter: momentum(X) × credit(Y) ===== */
  var cp=echarts.init(document.getElementById('chartCompass')); allCharts.push(cp);
  var LIM=2.6;
  var hist=[]; for(var i=0;i<Q.length;i++){ if(MOM[i]==null||CRED[i]==null||i===CUR)continue;
    hist.push({value:[MOM[i],CRED[i]],itemStyle:{color:hexA(CELL[QUAD[i]].col,0.32)},q:Q[i]});}
  var ts=Math.max(0,CUR-7),trail=[]; for(var t=ts;t<=CUR;t++){if(MOM[t]!=null)trail.push({value:[MOM[t],CRED[t]],symbolSize:4+(t-ts)*1.0});}
  var med=D.qstat;
  var mp=function(p,x,y){var f=med[p]||{};return {value:[x,y],label:{show:true,formatter:f.n?fmtPc(f.med):'—',color:CELL[p].col,fontSize:18,fontWeight:800,fontFamily:'IBM Plex Mono,'+FF}};};
  var medPts=[mp('fuelled',1.55,1.55),mp('draining',1.55,-1.55),mp('reflating',-1.55,1.55),mp('starved',-1.55,-1.55)];
  var cl=function(p,x,y){return {value:[x,y],label:{show:true,formatter:cn[p],color:CELL[p].col,fontSize:12.5,fontWeight:700,fontFamily:FF}};};
  var cornLbl=[cl('fuelled',1.75,2.35),cl('draining',1.75,-2.35),cl('reflating',-1.75,2.35),cl('starved',-1.75,-2.35)];
  var series=[
    {type:'scatter',data:hist,symbolSize:7,z:3,
      markArea:{silent:true,z:1,data:[
        [{coord:[0,0],itemStyle:{color:hexA(C.green,0.05)}},{coord:[LIM,LIM]}],
        [{coord:[0,0],itemStyle:{color:hexA(C.orange,0.05)}},{coord:[LIM,-LIM]}],
        [{coord:[0,0],itemStyle:{color:hexA(C.blue,0.05)}},{coord:[-LIM,LIM]}],
        [{coord:[0,0],itemStyle:{color:hexA(C.red,0.05)}},{coord:[-LIM,-LIM]}]]},
      markLine:{silent:true,symbol:'none',z:2,lineStyle:{color:'#c9bfa8',width:1.2},label:{show:false},data:[{xAxis:0},{yAxis:0}]}},
    {type:'line',data:trail,z:5,symbol:'circle',lineStyle:{color:C.gold,width:2,opacity:0.6},itemStyle:{color:C.gold,opacity:0.75}},
    {type:'scatter',data:[{value:[MOM[CUR],CRED[CUR]]}],z:7,symbolSize:17,
      itemStyle:{color:C.gold,borderColor:'#fff',borderWidth:2.5,shadowBlur:12,shadowColor:hexA(C.gold,0.6)},
      label:{show:true,position:'top',formatter:(isZh?'現在 ':'now ')+Q[CUR],color:C.navy,fontSize:11,fontWeight:700,fontFamily:FF}},
    {type:'scatter',data:medPts,z:6,symbolSize:1,itemStyle:{color:'transparent'},silent:true},
    {type:'scatter',data:cornLbl,z:6,symbolSize:1,itemStyle:{color:'transparent'},silent:true}
  ];
  // supply-glut warning ring on the current point
  if(WARN[CUR]) series.push({type:'scatter',data:[{value:[MOM[CUR],CRED[CUR]]}],z:6,symbolSize:34,
    itemStyle:{color:'transparent',borderColor:C.red,borderWidth:1.6,borderType:'dashed'},silent:true,
    label:{show:true,position:'bottom',formatter:(isZh?'⚠ 供給過剩':'⚠ supply glut'),color:C.red,fontSize:10,fontWeight:700,fontFamily:FF}});
  cp.setOption({grid:{left:52,right:20,top:40,bottom:52},
    tooltip:Object.assign({},baseTip,{trigger:'item',formatter:function(o){
      if(o.data&&o.data.q){var i=Q.indexOf(o.data.q);
        return '<b>'+o.data.q+'</b> · '+cn[QUAD[i]]+'<br/>'+(isZh?'動能 ':'momentum ')+(MOM[i]>=0?'+':'−')+Math.abs(MOM[i]).toFixed(2)+
          ' · '+(isZh?'信貸 ':'credit ')+(CRED[i]>=0?'+':'−')+Math.abs(CRED[i]).toFixed(2)+
          '<br/>'+(isZh?'房價年增 ':'HPI YoY ')+(D.hpi_yoy[i]==null?'–':D.hpi_yoy[i]+'%')+
          (D.fwd12[i]!=null?('<br/>'+(isZh?'其後3年 ':'next 3y ')+fmtPc(D.fwd12[i])):'');}
      return o.name||'';}}),
    xAxis:mkAxis({type:'value',min:-LIM,max:LIM,interval:1.3,axisLabel:{show:false},splitLine:{show:false},axisLine:{show:false},axisTick:{show:false},
      name:isZh?'← 下跌趨勢        動能        上漲趨勢 →':'← downtrend      Momentum      uptrend →',nameLocation:'center',nameGap:26,nameTextStyle:{color:C.navy,fontSize:11.5,fontWeight:700,fontFamily:FF}}),
    yAxis:mkAxis({type:'value',min:-LIM,max:LIM,interval:1.3,axisLabel:{show:false},splitLine:{show:false},axisLine:{show:false},axisTick:{show:false},
      name:isZh?'← 信貸收縮        信貸        信貸擴張 →':'← contracting      Credit      expanding →',nameLocation:'center',nameGap:30,nameRotate:90,nameTextStyle:{color:C.navy,fontSize:11.5,fontWeight:700,fontFamily:FF}}),
    series:series});

  /* ===== history dial (polar animation) ===== */
  var dl=echarts.init(document.getElementById('chartClock')); allCharts.push(dl);
  var RMAX=1.7;
  var angOf=function(i){var a=D.ang[i];return a==null?null:(a<0?a+360:a);};
  var radOf=function(i){return D.rad[i]==null?null:Math.min(RMAX,D.rad[i]);};
  var col={fuelled:CELL.fuelled.col,draining:CELL.draining.col,reflating:CELL.reflating.col,starved:CELL.starved.col};
  var bg=[]; for(var bi=0;bi<Q.length;bi++){if(angOf(bi)==null)continue;bg.push({value:[radOf(bi),angOf(bi)],itemStyle:{color:col[QUAD[bi]],opacity:0.16}});}
  var lbl=[{value:[1.62,45],name:cn.fuelled,label:{color:col.fuelled}},{value:[1.62,315],name:cn.draining,label:{color:col.draining}},
           {value:[1.62,135],name:cn.reflating,label:{color:col.reflating}},{value:[1.62,225],name:cn.starved,label:{color:col.starved}}];
  var frames=[];
  for(var fi=0;fi<Q.length;fi++){var A=angOf(fi),R=radOf(fi),isN=(A==null);
    var hand=isN?[]:[[0,A],[R,A]];var t0=Math.max(0,fi-7),tl=[],td=[];
    for(var tj=t0;tj<=fi;tj++){if(angOf(tj)==null)continue;var pc=[radOf(tj),angOf(tj)];tl.push(pc);
      if(tj<fi){var fr=(tj-t0+1)/(fi-t0+1);td.push({value:pc,itemStyle:{color:C.gold,opacity:0.10+0.5*fr},symbolSize:3+3*fr});}}
    var sub=isN?(isZh?'暖機':'warm-up'):cn[QUAD[fi]];
    sub+=isN?'':'\n'+(isZh?'動能 ':'M ')+(MOM[fi]>=0?'+':'−')+Math.abs(MOM[fi]).toFixed(2)+' · '+(isZh?'信貸 ':'C ')+(CRED[fi]>=0?'+':'−')+Math.abs(CRED[fi]).toFixed(2);
    sub+='\n'+(isZh?'房價年增 ':'HPI YoY ')+(D.hpi_yoy[fi]==null?'–':D.hpi_yoy[fi]+'%');
    frames.push({title:{text:Q[fi],subtext:sub},series:[{},{},{data:hand},{data:tl},{data:td},{data:isN?[]:[{value:[R,A],itemStyle:{color:C.gold}}]}]});}
  dl.setOption({baseOption:{
    timeline:{axisType:'category',data:Q,autoPlay:false,playInterval:200,loop:false,currentIndex:Q.length-1,left:34,right:34,bottom:4,height:34,symbol:'circle',symbolSize:4,
      lineStyle:{color:'#e5dcc8'},itemStyle:{color:'#cdbf9f'},checkpointStyle:{color:C.gold,borderColor:'#fff',borderWidth:2},
      controlStyle:{showPlayBtn:true,showPrevBtn:true,showNextBtn:true,itemSize:15,itemGap:8,color:C.navy,borderColor:C.navy},
      progress:{lineStyle:{color:C.gold},itemStyle:{color:C.gold},label:{show:false}},
      label:{color:C.muted,fontFamily:FF,fontSize:10,interval:0,formatter:function(v){return /[048]Q1$/.test(v)?v.slice(0,4):'';}},
      emphasis:{label:{show:true,color:C.navy}}},
    title:{left:'50%',top:'38%',textAlign:'center',text:'',subtext:'',textStyle:{color:C.navy,fontFamily:'IBM Plex Mono,'+FF,fontSize:19,fontWeight:700},subtextStyle:{color:C.muted,fontFamily:FF,fontSize:11,lineHeight:15,align:'center'}},
    polar:{center:['50%','45%'],radius:'62%'},
    angleAxis:{type:'value',min:0,max:360,interval:90,startAngle:0,clockwise:false,axisLine:{show:true,lineStyle:{color:'#e5dcc8'}},axisTick:{show:false},axisLabel:{show:false},splitLine:{show:true,lineStyle:{color:'#ece3d1'}},splitArea:{show:true,areaStyle:{color:[hexA(C.green,0.05),hexA(C.orange,0.05),hexA(C.starved?C.red:C.red,0.05),hexA(C.blue,0.05)]}}},
    radiusAxis:{type:'value',min:0,max:RMAX+0.02,axisLine:{show:false},axisTick:{show:false},axisLabel:{show:false},splitLine:{show:false}},
    series:[
      {name:'bg',type:'scatter',coordinateSystem:'polar',data:bg,symbolSize:4,z:2,silent:true},
      {name:'labels',type:'scatter',coordinateSystem:'polar',data:lbl,symbolSize:8,z:3,silent:true,itemStyle:{color:'transparent'},label:{show:true,formatter:function(p){return p.name;},fontFamily:FF,fontSize:11,fontWeight:700}},
      {name:'hand',type:'line',coordinateSystem:'polar',data:[],symbol:'none',lineStyle:{color:C.gold,width:2.5,opacity:0.55},z:4,silent:true},
      {name:'tl',type:'line',coordinateSystem:'polar',data:[],symbol:'none',lineStyle:{color:C.gold,width:2,opacity:0.3},z:5,silent:true},
      {name:'td',type:'scatter',coordinateSystem:'polar',data:[],z:6,silent:true},
      {name:'head',type:'scatter',coordinateSystem:'polar',data:[],symbolSize:15,z:7,itemStyle:{color:C.gold,borderColor:'#fff',borderWidth:1.5,shadowBlur:10,shadowColor:hexA(C.gold,0.55)}}
    ]},options:frames});
}

function setLang(lang){LANG=lang;
  document.body.classList.toggle('zh',lang==='zh');
  document.documentElement.lang=lang==='zh'?'zh-Hant':'en';
  document.querySelectorAll('.lang-en').forEach(function(e){e.style.display=lang==='en'?'':'none';});
  document.querySelectorAll('.lang-zh').forEach(function(e){e.style.display=lang==='zh'?'':'none';});
  document.querySelectorAll('.lang-btn').forEach(function(b){b.classList.toggle('active',b.dataset.lang===lang);});
  try{localStorage.setItem('lang',lang);}catch(e){}
  allCharts.forEach(function(c){if(c)c.dispose();});allCharts=[];initCharts(lang);}
function setMarket(m){useMarket(m);
  document.body.classList.toggle('mk-tw',m==='tw');document.body.classList.toggle('mk-my',m==='my');document.body.classList.toggle('mk-jp',m==='jp');document.body.classList.toggle('mk-au',m==='au');
  document.querySelectorAll('.mkt-btn').forEach(function(b){b.classList.toggle('active',b.dataset.mkt===m);});
  try{localStorage.setItem('mkt',m);}catch(e){}try{history.replaceState(null,'','#'+m);}catch(e){}
  allCharts.forEach(function(c){if(c)c.dispose();});allCharts=[];initCharts(LANG);}
window.addEventListener('resize',function(){allCharts.forEach(function(c){if(c)c.resize();});});
window.addEventListener('load',function(){
  document.querySelectorAll('.lang-btn').forEach(function(b){b.addEventListener('click',function(){setLang(b.dataset.lang);});});
  document.querySelectorAll('.mkt-btn').forEach(function(b){b.addEventListener('click',function(){setMarket(b.dataset.mkt);});});
  var lang='en';try{lang=localStorage.getItem('lang')||'en';}catch(e){}
  var mkt='us';try{mkt=localStorage.getItem('mkt')||'us';}catch(e){}
  if(location.hash==='#tw')mkt='tw';if(location.hash==='#us')mkt='us';if(location.hash==='#my')mkt='my';if(location.hash==='#jp')mkt='jp';if(location.hash==='#au')mkt='au';
  useMarket(mkt);document.body.classList.toggle('mk-tw',mkt==='tw');document.body.classList.toggle('mk-my',mkt==='my');document.body.classList.toggle('mk-jp',mkt==='jp');document.body.classList.toggle('mk-au',mkt==='au');
  document.querySelectorAll('.mkt-btn').forEach(function(b){b.classList.toggle('active',b.dataset.mkt===mkt);});
  setLang(lang);
});
