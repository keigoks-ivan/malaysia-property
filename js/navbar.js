/* Property Monitor — shared navbar (dark gradient, two-row with market dropdowns)
   Drop a <div id="nav-root"></div> on any page and load this script.
   Auto-detects active market / tool from location.pathname.
   Row 1: logo + tools (Home, REITs, Markets, Sectors, Screeners) + language.
   Row 2: market flags with hover dropdowns (Overview/Supply/Demand/Valuation/Risk/Report + cities). */
(function(){
'use strict';

/* ---------- market metadata ---------- */
var MARKETS = [
  {k:'my',flag:'🇲🇾',en:'Malaysia',zh:'馬來西亞',base:'/my/',
    cities:[{f:'kl.html',en:'Kuala Lumpur',zh:'吉隆坡'},{f:'penang.html',en:'Penang',zh:'檳城'}]},
  {k:'tw',flag:'🇹🇼',en:'Taiwan',zh:'台灣',base:'/tw/',
    cities:[{f:'taipei.html',en:'Taipei',zh:'台北'},{f:'newtaipei.html',en:'New Taipei',zh:'新北'},{f:'taoyuan.html',en:'Taoyuan',zh:'桃園'},{f:'hsinchu.html',en:'Hsinchu',zh:'新竹'},{f:'taichung.html',en:'Taichung',zh:'台中'},{f:'tainan.html',en:'Tainan',zh:'台南'},{f:'kaohsiung.html',en:'Kaohsiung',zh:'高雄'}]},
  {k:'jp',flag:'🇯🇵',en:'Japan',zh:'日本',base:'/jp/',
    cities:[{f:'tokyo.html',en:'Tokyo',zh:'東京'},{f:'osaka.html',en:'Osaka',zh:'大阪'},{f:'fukuoka.html',en:'Fukuoka',zh:'福岡'}]},
  {k:'au',flag:'🇦🇺',en:'Australia',zh:'澳洲',base:'/au/',
    cities:[{f:'sydney.html',en:'Sydney',zh:'雪梨'},{f:'melbourne.html',en:'Melbourne',zh:'墨爾本'},{f:'brisbane.html',en:'Brisbane',zh:'布里斯本'},{f:'goldcoast.html',en:'Gold Coast',zh:'黃金海岸'}]},
  {k:'nz',flag:'🇳🇿',en:'New Zealand',zh:'紐西蘭',base:'/nz/',
    cities:[{f:'auckland.html',en:'Auckland',zh:'奧克蘭'},{f:'christchurch.html',en:'Christchurch',zh:'基督城'}]},
  {k:'uk',flag:'🇬🇧',en:'UK',zh:'英國',base:'/uk/',
    cities:[{f:'london.html',en:'London',zh:'倫敦'},{f:'manchester.html',en:'Manchester',zh:'曼徹斯特'},{f:'edinburgh.html',en:'Edinburgh',zh:'愛丁堡'},{f:'newcastle.html',en:'Newcastle',zh:'紐卡斯爾'},{f:'birmingham.html',en:'Birmingham',zh:'伯明翰'}]},
  {k:'us',flag:'🇺🇸',en:'US',zh:'美國',base:'/us/',
    cities:[{f:'nyc.html',en:'NYC',zh:'紐約'},{f:'la.html',en:'LA',zh:'洛杉磯'},{f:'sf.html',en:'SF',zh:'舊金山'},{f:'sv.html',en:'Silicon Valley',zh:'矽谷'},{f:'sandiego.html',en:'San Diego',zh:'聖地牙哥'},{f:'miami.html',en:'Miami',zh:'邁阿密'},{f:'austin.html',en:'Austin',zh:'奧斯丁'},{f:'seattle.html',en:'Seattle',zh:'西雅圖'},{f:'chicago.html',en:'Chicago',zh:'芝加哥'},{f:'boston.html',en:'Boston',zh:'波士頓'},{f:'phoenix.html',en:'Phoenix',zh:'鳳凰城'},{f:'denver.html',en:'Denver',zh:'丹佛'}]},
  {k:'th',flag:'🇹🇭',en:'Thailand',zh:'泰國',base:'/th/',
    cities:[{f:'bangkok.html',en:'Bangkok',zh:'曼谷'},{f:'chiangmai.html',en:'Chiang Mai',zh:'清邁'}]},
  {k:'vn',flag:'🇻🇳',en:'Vietnam',zh:'越南',base:'/vn/',
    cities:[{f:'hochiminh.html',en:'Ho Chi Minh',zh:'胡志明'},{f:'hanoi.html',en:'Hanoi',zh:'河內'}]},
  {k:'kr',flag:'🇰🇷',en:'Korea',zh:'韓國',base:'/kr/',
    cities:[{f:'seoul.html',en:'Seoul',zh:'首爾'},{f:'busan.html',en:'Busan',zh:'釜山'}]},
  {k:'ca',flag:'🇨🇦',en:'Canada',zh:'加拿大',base:'/ca/',
    cities:[{f:'toronto.html',en:'Toronto',zh:'多倫多'},{f:'vancouver.html',en:'Vancouver',zh:'溫哥華'}]},
  {k:'ie',flag:'🇮🇪',en:'Ireland',zh:'愛爾蘭',base:'/ie/',
    cities:[{f:'dublin.html',en:'Dublin',zh:'都柏林'},{f:'cork.html',en:'Cork',zh:'科克'}]}
];

var SECTIONS = [
  {f:'index.html',en:'Overview',zh:'市場總覽'},
  {f:'supply.html',en:'Supply',zh:'供給'},
  {f:'demand.html',en:'Demand',zh:'需求'},
  {f:'valuation.html',en:'Valuation',zh:'估值'},
  {f:'risk.html',en:'Risk',zh:'風險'},
  {f:'report.html',en:'Report',zh:'報告'}
];

var TOOLS = [
  {k:'home',href:'/home.html',en:'Home',zh:'首頁'},
  {k:'stress',href:'/tools/stress-test.html',en:'⚡ Stress',zh:'⚡ 壓測'},
  {k:'buy-rent',href:'/tools/buy-vs-rent.html',en:'🔁 Buy/Rent',zh:'🔁 買租'},
  {k:'reits',href:'/reits.html',en:'REITs',zh:'REITs'},
  {k:'markets',href:'/markets.html',en:'Markets',zh:'股市'},
  {k:'sectors',href:'/sectors.html',en:'Sectors',zh:'類股'},
  {k:'screener-us',href:'/screener.html',en:'US Screener',zh:'美股選股'},
  {k:'screener-tw',href:'/screener-tw.html',en:'TW Screener',zh:'台股選股'}
];

/* ---------- detect active ---------- */
var path = location.pathname;
if (path === '' || path === '/') path = '/home.html';
var firstSeg = path.split('/')[1] || '';
var fileSeg = path.split('/').pop() || '';
/* Cloudflare Pages serves /foo for foo.html — normalize so detection still works */
if (fileSeg === '') fileSeg = 'index.html';
else if (fileSeg.indexOf('.') === -1) fileSeg += '.html';

var activeMarket = null, activeTool = null;
var mk = MARKETS.filter(function(m){return m.k===firstSeg;})[0];
if (mk) {
  activeMarket = mk.k;
} else {
  var t = TOOLS.filter(function(x){
    var href=x.href.replace(/^\//,'');
    return href===fileSeg || href===path.replace(/^\//,'') || href===(path.replace(/^\//,'').replace(/\.html$/,'')+'.html');
  })[0];
  if (t) activeTool = t.k;
}

/* ---------- build HTML ---------- */
function spanBL(en,zh){return '<span class="imq-en">'+en+'</span><span class="imq-zh">'+zh+'</span>';}

var toolsHtml = TOOLS.map(function(t){
  var cls = 'imq-tool'+(t.k===activeTool?' on':'');
  return '<a class="'+cls+'" href="'+t.href+'">'+spanBL(t.en,t.zh)+'</a>';
}).join('');

/* Row 2: market flags with hover dropdowns */
var flagsHtml = MARKETS.map(function(m){
  var cls = 'imq-flag'+(m.k===activeMarket?' on':'');
  var sectionsHtml = SECTIONS.map(function(s){
    return '<a class="imq-dd-link" href="'+m.base+s.f+'">'+spanBL(s.en,s.zh)+'</a>';
  }).join('');
  var citiesHtml = m.cities.map(function(ct){
    return '<a class="imq-dd-link imq-dd-city" href="'+m.base+ct.f+'">'+spanBL(ct.en,ct.zh)+'</a>';
  }).join('');
  return '<div class="imq-flag-wrap">'+
    '<a class="'+cls+'" href="'+m.base+'report.html">'+
      '<span class="imq-flag-emoji">'+m.flag+'</span>'+
      '<span class="imq-flag-name">'+spanBL(m.en,m.zh)+'</span>'+
    '</a>'+
    '<div class="imq-dd">'+
      '<div class="imq-dd-section"><div class="imq-dd-title">'+spanBL('Sections','頁面')+'</div>'+sectionsHtml+'</div>'+
      '<div class="imq-dd-section"><div class="imq-dd-title">'+spanBL('Cities','城市')+'</div>'+citiesHtml+'</div>'+
    '</div>'+
  '</div>';
}).join('');

/* Row 3: persistent sub-nav for active country (Sections + Cities) */
var subnavHtml = '';
if (activeMarket) {
  var activeMk = MARKETS.filter(function(m){return m.k===activeMarket;})[0];
  if (activeMk) {
    var activeFile = fileSeg;
    // for Malaysia root, the "base" is "/" so compare just filenames
    var secLinks = SECTIONS.map(function(s){
      var href = activeMk.base + s.f;
      var isOn = (s.f === activeFile);
      return '<a class="imq-sub-link'+(isOn?' on':'')+'" href="'+href+'">'+spanBL(s.en,s.zh)+'</a>';
    }).join('');
    var cityLinks = activeMk.cities.map(function(ct){
      var href = activeMk.base + ct.f;
      var isOn = (ct.f === activeFile);
      return '<a class="imq-sub-link imq-sub-city'+(isOn?' on':'')+'" href="'+href+'">'+spanBL(ct.en,ct.zh)+'</a>';
    }).join('');
    subnavHtml = '<div class="imq-row3">'+
      '<div class="imq-sub-label"><span class="imq-flag-emoji">'+activeMk.flag+'</span><span class="imq-sub-mk">'+spanBL(activeMk.en,activeMk.zh)+'</span></div>'+
      '<div class="imq-sub-links">'+secLinks+'<span class="imq-sub-sep">·</span>'+cityLinks+'</div>'+
    '</div>';
  }
}

var html = ''+
'<nav class="imq-nav">'+
  '<div class="imq-row1">'+
    '<div class="imq-left">'+
      '<a class="imq-logo" href="/home.html">PROPERTY<span class="imq-dot">·</span>MONITOR<span class="imq-sub">investmquest</span></a>'+
      '<div class="imq-tools">'+toolsHtml+'</div>'+
    '</div>'+
    '<div class="imq-right">'+
      '<div class="imq-lang">'+
        '<button class="imq-lbtn" data-lang="en">EN</button>'+
        '<button class="imq-lbtn" data-lang="zh">中文</button>'+
      '</div>'+
      '<button class="imq-burger" aria-label="menu">☰</button>'+
    '</div>'+
  '</div>'+
  '<div class="imq-row2">'+
    '<div class="imq-flags">'+flagsHtml+'</div>'+
  '</div>'+
  subnavHtml+
'</nav>';

/* ---------- CSS ---------- */
var css = ''+
'.imq-nav{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:100;font-family:\'Inter\',\'Noto Sans TC\',-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;font-size:15px;line-height:1.4}'+
'.imq-nav *{box-sizing:border-box}'+
'.imq-row1{display:flex;align-items:center;justify-content:space-between;padding:0 28px;height:56px;gap:14px}'+
'.imq-row2{border-top:1px solid rgba(255,255,255,.08);padding:0 28px;overflow:visible}'+
'.imq-left{display:flex;align-items:center;gap:24px;min-width:0}'+
'.imq-right{display:flex;align-items:center;gap:12px}'+
'.imq-logo{font-size:17px;font-weight:700;color:#fff!important;letter-spacing:-.02em;text-decoration:none!important;white-space:nowrap;display:inline-flex;align-items:baseline}'+
'.imq-logo:hover{color:#fff!important}'+
'.imq-dot{color:#3b82f6;margin:0 1px}'+
'.imq-sub{font-size:11px;color:rgba(255,255,255,.4);margin-left:10px;letter-spacing:.04em;font-weight:400}'+
'.imq-tools{display:flex;gap:3px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}'+
'.imq-tools::-webkit-scrollbar{display:none}'+
'.imq-tool{padding:7px 13px;font-size:14px;font-weight:500;color:rgba(255,255,255,.75)!important;text-decoration:none!important;border-radius:6px;transition:all .15s;white-space:nowrap;letter-spacing:.01em}'+
'.imq-tool:hover{color:#fff!important;background:rgba(255,255,255,.06);text-decoration:none!important}'+
'.imq-tool.on{color:#fff!important;background:rgba(59,130,246,.2);font-weight:600}'+
'.imq-lang{display:flex;gap:4px}'+
'.imq-lbtn{padding:6px 13px;border:1px solid rgba(255,255,255,.15);border-radius:5px;font-size:13px;cursor:pointer;background:transparent;color:rgba(255,255,255,.75);font-family:inherit;font-weight:500;transition:all .15s}'+
'.imq-lbtn:hover{color:#fff;border-color:rgba(255,255,255,.3)}'+
'.imq-lbtn.on{background:#3b82f6;color:#fff;border-color:#3b82f6}'+
'.imq-burger{display:none;background:transparent;border:1px solid rgba(255,255,255,.15);border-radius:5px;color:#fff;font-size:18px;padding:5px 12px;cursor:pointer}'+
/* Row 2 flags */
'.imq-flags{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none;padding:0;min-height:40px;align-items:center}'+
'.imq-flags::-webkit-scrollbar{display:none}'+
'.imq-flag-wrap{position:relative;flex-shrink:0}'+
'.imq-flag{display:inline-flex;align-items:center;gap:6px;padding:8px 11px;font-size:12.5px;font-weight:500;color:rgba(255,255,255,.7)!important;text-decoration:none!important;border-radius:5px;transition:all .15s;white-space:nowrap;border-bottom:2px solid transparent}'+
'.imq-flag:hover{color:#fff!important;background:rgba(255,255,255,.06);text-decoration:none!important}'+
'.imq-flag.on{color:#fff!important;background:rgba(59,130,246,.18);font-weight:600;border-bottom-color:#3b82f6}'+
'.imq-flag-emoji{font-size:15px;line-height:1}'+
'.imq-flag-name{letter-spacing:.01em}'+
/* Dropdown */
'.imq-dd{display:none;position:absolute;top:100%;left:0;min-width:280px;background:#0f172a;border:1px solid rgba(255,255,255,.08);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.4);padding:10px;z-index:200;margin-top:4px;grid-template-columns:1fr 1fr;gap:12px}'+
'.imq-flag-wrap:hover .imq-dd{display:grid}'+
'.imq-dd-section{min-width:0}'+
'.imq-dd-title{font-size:10px;font-weight:600;color:rgba(255,255,255,.45);text-transform:uppercase;letter-spacing:.08em;padding:4px 10px 6px;border-bottom:1px solid rgba(255,255,255,.06);margin-bottom:4px}'+
'.imq-dd-link{display:block;padding:6px 10px;font-size:12.5px;color:rgba(255,255,255,.78)!important;text-decoration:none!important;border-radius:4px;transition:all .12s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'+
'.imq-dd-link:hover{background:rgba(59,130,246,.2);color:#fff!important;text-decoration:none!important}'+
'.imq-dd-city{color:rgba(255,255,255,.65)!important}'+
'.imq-dd-city:hover{color:#fff!important}'+
/* Row 3: persistent sub-nav for active country */
'.imq-row3{display:flex;align-items:center;gap:14px;padding:6px 28px 8px;border-top:1px solid rgba(255,255,255,.06);background:rgba(59,130,246,.08);flex-wrap:wrap}'+
'.imq-sub-label{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:600;color:rgba(255,255,255,.85);white-space:nowrap}'+
'.imq-sub-label .imq-flag-emoji{font-size:14px}'+
'.imq-sub-mk{letter-spacing:.02em}'+
'.imq-sub-links{display:flex;align-items:center;gap:2px;flex-wrap:wrap}'+
'.imq-sub-link{padding:4px 10px;font-size:12.5px;color:rgba(255,255,255,.72)!important;text-decoration:none!important;border-radius:4px;transition:all .12s;white-space:nowrap}'+
'.imq-sub-link:hover{color:#fff!important;background:rgba(255,255,255,.1);text-decoration:none!important}'+
'.imq-sub-link.on{color:#fff!important;background:rgba(59,130,246,.35);font-weight:600}'+
'.imq-sub-city{color:rgba(255,255,255,.58)!important;font-size:12px}'+
'.imq-sub-sep{color:rgba(255,255,255,.25);margin:0 4px;font-size:12px}'+
/* Language toggle */
'.imq-zh{display:none}'+
'html[lang="zh"] .imq-en,body[data-lang="zh"] .imq-en{display:none}'+
'html[lang="zh"] .imq-zh,body[data-lang="zh"] .imq-zh{display:inline}'+
/* Mobile */
'@media(max-width:820px){'+
  '.imq-row1{padding:0 14px;gap:8px;height:52px}'+
  '.imq-row2{padding:0 14px}'+
  '.imq-logo{font-size:15px}'+
  '.imq-sub{display:none}'+
  '.imq-tools{display:none}'+
  '.imq-burger{display:inline-block}'+
  '.imq-flags{overflow-x:auto;padding:4px 0}'+
  '.imq-flag-name{display:none}'+
  '.imq-flag{padding:7px 8px}'+
  '.imq-flag-emoji{font-size:17px}'+
  '.imq-row3{padding:6px 10px;gap:6px}'+
  '.imq-sub-label{font-size:11px}'+
  '.imq-sub-links{overflow-x:auto;flex-wrap:nowrap;scrollbar-width:none}'+
  '.imq-sub-links::-webkit-scrollbar{display:none}'+
  '.imq-sub-link{padding:4px 8px;font-size:11.5px}'+
  '.imq-sub-sep{display:none}'+
  '.imq-tools.open{display:flex!important;flex-direction:column;position:absolute;top:52px;left:0;right:0;background:#0f172a;padding:10px;border-top:1px solid rgba(255,255,255,.1);z-index:150}'+
  '.imq-dd{position:fixed;top:auto;left:8px;right:8px;bottom:8px;min-width:0;max-height:60vh;overflow-y:auto}'+
  '.imq-flag-wrap:hover .imq-dd{display:none}'+
  '.imq-flag-wrap.open .imq-dd{display:grid}'+
'}';

/* ---------- inject ---------- */
var root = document.getElementById('nav-root');
if (!root) return;

var style = document.createElement('style');
style.id = 'imq-nav-style';
style.textContent = css;
document.head.appendChild(style);

root.innerHTML = html;

/* ---------- language switching ---------- */
function applyLang(lang){
  try{localStorage.setItem('lang',lang);}catch(e){}
  document.body.setAttribute('data-lang', lang);
  var en = document.querySelectorAll('.lang-en'), zh = document.querySelectorAll('.lang-zh');
  en.forEach(function(e){e.style.display = (lang==='en')?'':'none';});
  zh.forEach(function(e){e.style.display = (lang==='zh')?'':'none';});
  document.querySelectorAll('.imq-lbtn').forEach(function(b){
    b.classList.toggle('on', b.getAttribute('data-lang')===lang);
  });
  document.querySelectorAll('.lang-btn').forEach(function(b){
    b.classList.toggle('active', b.getAttribute('data-lang')===lang||b.dataset.lang===lang);
  });
}

root.querySelectorAll('.imq-lbtn').forEach(function(btn){
  btn.addEventListener('click', function(){
    var lang = btn.getAttribute('data-lang');
    /* Always update navbar button + body[data-lang] regardless of whether the
       page provides a custom setLang. Page setLang typically only handles
       lang-en/lang-zh visibility + chart re-render, not navbar button state. */
    document.body.setAttribute('data-lang', lang);
    try{localStorage.setItem('lang',lang);}catch(e){}
    document.querySelectorAll('.imq-lbtn').forEach(function(b){
      b.classList.toggle('on', b.getAttribute('data-lang')===lang);
    });
    if (typeof window.setLang === 'function' && window.setLang !== applyLang) {
      window.setLang(lang);
    } else {
      applyLang(lang);
    }
  });
});

if (typeof window.setLang !== 'function') {
  window.setLang = applyLang;
}

var saved = 'en';
try{saved = localStorage.getItem('lang')||'en';}catch(e){}
/* Sync navbar button state on initial load (page setLang doesn't touch .imq-lbtn) */
document.body.setAttribute('data-lang', saved);
document.querySelectorAll('.imq-lbtn').forEach(function(b){
  b.classList.toggle('on', b.getAttribute('data-lang')===saved);
});
if (typeof window.setLang === 'function') window.setLang(saved);

/* ---------- mobile menu ---------- */
var burger = root.querySelector('.imq-burger');
var tools = root.querySelector('.imq-tools');
if (burger && tools) {
  burger.addEventListener('click', function(){ tools.classList.toggle('open'); });
}

/* ---------- mobile flag tap-to-open dropdown ---------- */
root.querySelectorAll('.imq-flag-wrap').forEach(function(wrap){
  var flag = wrap.querySelector('.imq-flag');
  if (!flag) return;
  flag.addEventListener('click', function(e){
    if (window.innerWidth <= 820) {
      var isOpen = wrap.classList.contains('open');
      root.querySelectorAll('.imq-flag-wrap.open').forEach(function(w){ w.classList.remove('open'); });
      if (!isOpen) { e.preventDefault(); wrap.classList.add('open'); }
    }
  });
});
document.addEventListener('click', function(e){
  if (window.innerWidth <= 820 && !e.target.closest('.imq-flag-wrap')) {
    root.querySelectorAll('.imq-flag-wrap.open').forEach(function(w){ w.classList.remove('open'); });
  }
});

})();
