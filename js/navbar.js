/* Property Monitor — shared navbar (dark gradient, option B)
   Drop a <div id="nav-root"></div> on any page and load this script.
   Auto-detects active market / tool from location.pathname. */
(function(){
'use strict';

/* ---------- market metadata ---------- */
var MARKETS = [
  {k:'my',flag:'🇲🇾',en:'Malaysia',zh:'馬來西亞',base:'/',
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

var activeMarket = null, activeTool = null;
var mk = MARKETS.filter(function(m){return m.k===firstSeg;})[0];
if (mk) {
  activeMarket = mk.k;
} else {
  var t = TOOLS.filter(function(x){return x.href.replace(/^\//,'')===fileSeg;})[0];
  if (t) activeTool = t.k;
  else {
    var myRoot = ['index.html','kl.html','penang.html','supply.html','demand.html','valuation.html','risk.html','report.html'];
    if (myRoot.indexOf(fileSeg)!==-1) activeMarket = 'my';
  }
}

/* ---------- build HTML ---------- */
function spanBL(en,zh){return '<span class="imq-en">'+en+'</span><span class="imq-zh">'+zh+'</span>';}

var toolsHtml = TOOLS.map(function(t){
  var cls = 'imq-tool'+(t.k===activeTool?' on':'');
  return '<a class="'+cls+'" href="'+t.href+'">'+spanBL(t.en,t.zh)+'</a>';
}).join('');

var flagsHtml = MARKETS.map(function(m){
  var cls = 'imq-flag'+(m.k===activeMarket?' on':'');
  var href = m.base + (m.k==='my'?'report.html':'report.html');
  var sectionsRow = SECTIONS.map(function(s){return '<a href="'+m.base+s.f+'">'+spanBL(s.en,s.zh)+'</a>';}).join('');
  var citiesRow = m.cities.map(function(c){return '<a href="'+m.base+c.f+'">'+spanBL(c.en,c.zh)+'</a>';}).join('');
  return '<div class="imq-flag-wrap">'+
    '<a class="'+cls+'" href="'+href+'"><span class="imq-em">'+m.flag+'</span>'+spanBL(m.en,m.zh)+'</a>'+
    '<div class="imq-drop">'+
      '<div class="imq-drop-title"><span class="imq-em2">'+m.flag+'</span>'+spanBL(m.en,m.zh)+'</div>'+
      '<div class="imq-drop-sec">'+spanBL('Sections','頁面')+'</div>'+
      '<div class="imq-drop-row">'+sectionsRow+'</div>'+
      '<div class="imq-drop-sec">'+spanBL('Cities','城市')+'</div>'+
      '<div class="imq-drop-row">'+citiesRow+'</div>'+
    '</div>'+
  '</div>';
}).join('');

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
'</nav>';

/* ---------- CSS ---------- */
var css = ''+
'.imq-nav{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:100;font-family:\'Inter\',\'Noto Sans TC\',-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;font-size:14px;line-height:1.4}'+
'.imq-nav *{box-sizing:border-box}'+
'.imq-row1{display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:48px;border-bottom:1px solid rgba(255,255,255,.06);gap:12px}'+
'.imq-left{display:flex;align-items:center;gap:20px;min-width:0}'+
'.imq-right{display:flex;align-items:center;gap:10px}'+
'.imq-logo{font-size:15px;font-weight:700;color:#fff!important;letter-spacing:-.02em;text-decoration:none!important;white-space:nowrap;display:inline-flex;align-items:baseline}'+
'.imq-logo:hover{color:#fff!important}'+
'.imq-dot{color:#3b82f6;margin:0 1px}'+
'.imq-sub{font-size:10px;color:rgba(255,255,255,.4);margin-left:8px;letter-spacing:.04em;font-weight:400}'+
'.imq-tools{display:flex;gap:2px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}'+
'.imq-tools::-webkit-scrollbar{display:none}'+
'.imq-tool{padding:6px 11px;font-size:12px;font-weight:500;color:rgba(255,255,255,.7)!important;text-decoration:none!important;border-radius:6px;transition:all .15s;white-space:nowrap;letter-spacing:.01em}'+
'.imq-tool:hover{color:#fff!important;background:rgba(255,255,255,.06);text-decoration:none!important}'+
'.imq-tool.on{color:#fff!important;background:rgba(59,130,246,.2);font-weight:600}'+
'.imq-lang{display:flex;gap:4px}'+
'.imq-lbtn{padding:5px 11px;border:1px solid rgba(255,255,255,.15);border-radius:5px;font-size:11px;cursor:pointer;background:transparent;color:rgba(255,255,255,.7);font-family:inherit;font-weight:500;transition:all .15s}'+
'.imq-lbtn:hover{color:#fff;border-color:rgba(255,255,255,.3)}'+
'.imq-lbtn.on{background:#3b82f6;color:#fff;border-color:#3b82f6}'+
'.imq-burger{display:none;background:transparent;border:1px solid rgba(255,255,255,.15);border-radius:5px;color:#fff;font-size:16px;padding:4px 10px;cursor:pointer}'+
'.imq-row2{padding:0 24px;height:44px;background:rgba(0,0,0,.2);border-top:1px solid rgba(255,255,255,.04);display:flex;align-items:center}'+
'.imq-flags{display:flex;gap:2px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none;width:100%}'+
'.imq-flags::-webkit-scrollbar{display:none}'+
'.imq-flag-wrap{position:relative}'+
'.imq-flag{padding:7px 11px;font-size:12px;font-weight:500;color:rgba(255,255,255,.7)!important;text-decoration:none!important;border-radius:6px;display:inline-flex;align-items:center;gap:6px;cursor:pointer;transition:all .15s;white-space:nowrap;letter-spacing:.01em}'+
'.imq-flag:hover{background:rgba(255,255,255,.08);color:#fff!important;text-decoration:none!important}'+
'.imq-flag.on{background:rgba(59,130,246,.2);color:#fff!important;font-weight:600}'+
'.imq-em{font-size:14px;line-height:1}'+
'.imq-em2{font-size:16px;margin-right:4px}'+
'.imq-drop{position:absolute;top:calc(100% + 8px);left:0;background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px 18px;box-shadow:0 8px 24px rgba(15,23,42,.12);display:none;min-width:300px;z-index:200}'+
'.imq-flag-wrap:hover .imq-drop{display:block}'+
'.imq-flag-wrap:nth-last-child(-n+4) .imq-drop{left:auto;right:0}'+
'.imq-drop-title{font-size:14px;font-weight:700;color:#0f172a;margin-bottom:10px;display:flex;align-items:center}'+
'.imq-drop-sec{font-size:9px;letter-spacing:.14em;color:#2563eb;font-weight:700;margin:10px 0 6px;text-transform:uppercase}'+
'.imq-drop-sec:first-of-type{margin-top:0}'+
'.imq-drop-row{display:flex;flex-wrap:wrap;gap:2px 0}'+
'.imq-drop-row a{font-size:12px;color:#0f172a!important;text-decoration:none!important;padding:4px 10px;border-radius:5px;transition:all .15s;display:inline-block}'+
'.imq-drop-row a:hover{background:#eff6ff;color:#2563eb!important}'+
'.imq-zh{display:none}'+
'html[lang="zh"] .imq-en,body[data-lang="zh"] .imq-en{display:none}'+
'html[lang="zh"] .imq-zh,body[data-lang="zh"] .imq-zh{display:inline}'+
'@media(max-width:820px){'+
  '.imq-row1{padding:0 14px;gap:8px}'+
  '.imq-logo{font-size:13px}'+
  '.imq-sub{display:none}'+
  '.imq-tools{display:none}'+
  '.imq-burger{display:inline-block}'+
  '.imq-row1.open + .imq-row2,.imq-tools.open{display:flex!important;flex-direction:column;position:absolute;top:48px;left:0;right:0;background:#0f172a;padding:10px;border-top:1px solid rgba(255,255,255,.1);z-index:150}'+
  '.imq-row2{padding:0 10px}'+
  '.imq-flag{padding:6px 8px;font-size:11px}'+
  '.imq-drop{min-width:260px;left:0!important;right:auto!important}'+
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
  // toggle both our tokens (imq-en/zh) and the site-wide lang-en/lang-zh
  document.body.setAttribute('data-lang', lang);
  var en = document.querySelectorAll('.lang-en'), zh = document.querySelectorAll('.lang-zh');
  en.forEach(function(e){e.style.display = (lang==='en')?'':'none';});
  zh.forEach(function(e){e.style.display = (lang==='zh')?'':'none';});
  // update buttons
  document.querySelectorAll('.imq-lbtn').forEach(function(b){
    b.classList.toggle('on', b.getAttribute('data-lang')===lang);
  });
  // also toggle legacy .lang-btn buttons elsewhere on the page
  document.querySelectorAll('.lang-btn').forEach(function(b){
    b.classList.toggle('active', b.getAttribute('data-lang')===lang||b.dataset.lang===lang);
  });
}

// hook buttons
root.querySelectorAll('.imq-lbtn').forEach(function(btn){
  btn.addEventListener('click', function(){
    var lang = btn.getAttribute('data-lang');
    // if the page provides its own setLang (e.g. to re-render charts), let it run
    if (typeof window.setLang === 'function' && window.setLang !== applyLang) {
      window.setLang(lang);
    } else {
      applyLang(lang);
    }
  });
});

// expose a default setLang if page didn't define one
if (typeof window.setLang !== 'function') {
  window.setLang = applyLang;
}

// apply saved language on load
var saved = 'en';
try{saved = localStorage.getItem('lang')||'en';}catch(e){}
if (typeof window.setLang === 'function') window.setLang(saved);

/* ---------- mobile menu ---------- */
var burger = root.querySelector('.imq-burger');
var tools = root.querySelector('.imq-tools');
if (burger && tools) {
  burger.addEventListener('click', function(){ tools.classList.toggle('open'); });
}

})();
