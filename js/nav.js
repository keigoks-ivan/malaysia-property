/* Property Check — shared two-row navbar
   ------------------------------------------------------------------
   Drop <div id="nav-root"></div> near the top of <body> and load this
   script immediately after it (before the page's own <script> block).

   Row 1: brand + market switcher + EN/中文
   Row 2: sub-nav for the active market

   Adding a market = one entry in MARKETS below. Nothing else to touch.

   Language: the navbar labels use the site-wide .lang-en / .lang-zh
   convention, so whichever mechanism a page already uses (body.zh CSS on
   /kl-check, inline display toggling in setLang() elsewhere) keeps working.
   The nav's own buttons call the page's window.setLang() when it exists and
   fall back to a local toggle when it does not (e.g. scorecard pages).
------------------------------------------------------------------ */
(function () {
'use strict';

var MARKETS = [
  { k: 'my', flag: '🇲🇾', en: 'Malaysia', zh: '馬來西亞', home: '/kl-check',
    prefixes: ['/my/', '/kl/', '/kl-check'],
    links: [
      { href: '/kl-check',          en: 'Scorecards',        zh: '評分卡',        also: ['/kl/'] },
      { href: '/my/report',         en: 'Market Report',     zh: '市場報告' },
      { href: '/my/macro',          en: 'Macro',             zh: '總經' },
      { href: '/my/airbnb',         en: 'Airbnb / STRA',     zh: '短租' },
      { href: '/my/reit-vs-direct', en: 'REITs vs Property', zh: 'REIT vs 房產' },
      { href: '/my/framework',      en: 'Framework',         zh: '框架回測' },
      { href: '/my/clock',          en: 'Compass',           zh: '羅盤' }
    ] },
  { k: 'th', flag: '🇹🇭', en: 'Thailand', zh: '泰國', home: '/th/report',
    prefixes: ['/th/'],
    links: [
      { href: '/th/report', en: 'Bangkok Report', zh: '曼谷報告' },
      { href: '/th/macro',  en: 'Macro',          zh: '總經' }
    ] },
  { k: 'ae', flag: '🇦🇪', en: 'UAE', zh: '阿聯', home: '/ae/report',
    prefixes: ['/ae/'],
    links: [
      { href: '/ae/report', en: 'Dubai Report', zh: '杜拜報告' },
      { href: '/ae/macro',  en: 'Macro',        zh: '總經' }
    ] }
];

/* ---------- normalise the current path ---------- */
/* Cloudflare Pages serves /foo for foo.html, so compare on a stripped path. */
var path = location.pathname.replace(/index\.html$/, '').replace(/\.html$/, '');
if (path.length > 1) path = path.replace(/\/$/, '');

function norm(href) {
  var p = href.replace(/index\.html$/, '').replace(/\.html$/, '');
  return p.length > 1 ? p.replace(/\/$/, '') : p;
}

var activeMarket = null;
for (var i = 0; i < MARKETS.length; i++) {
  var m = MARKETS[i];
  for (var j = 0; j < m.prefixes.length; j++) {
    if (path === norm(m.prefixes[j]) || path.indexOf(m.prefixes[j]) === 0) { activeMarket = m; break; }
  }
  if (activeMarket) break;
}

function isCurrent(link) {
  if (path === norm(link.href)) return true;
  var also = link.also || [];
  for (var i = 0; i < also.length; i++) if (path.indexOf(also[i]) === 0) return true;
  return false;
}

/* ---------- markup ---------- */
function bl(en, zh) {
  return '<span class="lang-en">' + en + '</span><span class="lang-zh">' + zh + '</span>';
}

var marketTabs = MARKETS.map(function (m) {
  return '<a class="pc-mk' + (activeMarket === m ? ' on' : '') + '" href="' + m.home + '">' +
           '<span class="pc-flag">' + m.flag + '</span>' + bl(m.en, m.zh) +
         '</a>';
}).join('');

var subRow = '';
if (activeMarket) {
  subRow =
    '<div class="pc-row2">' +
      '<span class="pc-row2-flag">' + activeMarket.flag + '</span>' +
      '<div class="pc-sub">' +
        activeMarket.links.map(function (l) {
          return '<a class="pc-link' + (isCurrent(l) ? ' on' : '') + '" href="' + l.href + '">' + bl(l.en, l.zh) + '</a>';
        }).join('') +
      '</div>' +
    '</div>';
}

var html =
  '<nav class="pc-nav">' +
    '<div class="pc-row1">' +
      '<a class="pc-brand" href="/">' +
        '<span class="pc-mark">P</span>' +
        '<span class="pc-brand-text">' +
          '<span class="pc-brand-name">Property Check</span>' +
          '<span class="pc-brand-by">by InvestMQuest</span>' +
        '</span>' +
      '</a>' +
      '<div class="pc-right">' +
        '<div class="pc-markets">' + marketTabs + '</div>' +
        '<div class="pc-lang lang-btns">' +
          '<button class="pc-lbtn lang-btn" data-lang="en">EN</button>' +
          '<button class="pc-lbtn lang-btn" data-lang="zh">中文</button>' +
        '</div>' +
      '</div>' +
    '</div>' +
    subRow +
  '</nav>';

/* ---------- styles (kl-theme cream / navy / gold) ---------- */
var css = [
'.pc-nav{background:rgba(255,255,255,.94);backdrop-filter:saturate(140%) blur(10px);-webkit-backdrop-filter:saturate(140%) blur(10px);border-bottom:1px solid #e8dfc9;position:sticky;top:0;z-index:120;font-family:Inter,"Noto Sans TC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
'.pc-nav *{box-sizing:border-box}',
'.pc-row1{max-width:1080px;margin:0 auto;padding:11px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px}',
'.pc-brand{display:flex;align-items:center;gap:10px;text-decoration:none!important;flex-shrink:0}',
'.pc-mark{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#0d2244 0%,#173564 100%);display:flex;align-items:center;justify-content:center;font-family:"Playfair Display",serif;font-style:italic;font-weight:700;font-size:16px;color:#d4b576;box-shadow:inset 0 -2px 4px rgba(0,0,0,.2),0 2px 6px rgba(13,34,68,.18);letter-spacing:-.04em}',
'.pc-brand-text{display:flex;flex-direction:column;line-height:1.15}',
'.pc-brand-name{font-size:15px;font-weight:700;letter-spacing:-.01em;color:#0d2244}',
'.pc-brand-by{font-size:10px;color:#6b7a92;font-weight:500;letter-spacing:.08em;text-transform:uppercase;margin-top:1px}',
'.pc-right{display:flex;align-items:center;gap:14px;min-width:0}',
'.pc-markets{display:flex;gap:4px;align-items:center}',
'.pc-mk{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;font-size:13.5px;font-weight:600;color:#41506b!important;text-decoration:none!important;border-radius:999px;border:1px solid transparent;transition:all .15s;white-space:nowrap}',
'.pc-mk:hover{color:#8f6d2c!important;background:#fbf3df;text-decoration:none!important}',
'.pc-mk.on{color:#0d2244!important;background:#e8eef5;border-color:#ccd9e8}',
'.pc-flag{font-size:15px;line-height:1}',
'.pc-lang{display:inline-flex;gap:0;background:#f3efe4;border:1px solid #e8dfc9;border-radius:999px;padding:3px}',
'.pc-lbtn{padding:5px 12px;border:none;border-radius:999px;font-size:11px;font-weight:600;cursor:pointer;background:transparent;color:#6b7a92;font-family:inherit;letter-spacing:.04em;transition:all .2s}',
'.pc-lbtn:hover{color:#0d2244}',
'.pc-lbtn.active{background:#0d2244;color:#fff;box-shadow:0 1px 4px rgba(13,34,68,.18)}',
'.pc-row2{max-width:1080px;margin:0 auto;padding:0 24px 9px;display:flex;align-items:center;gap:10px}',
'.pc-row2-flag{font-size:13px;line-height:1;opacity:.85;flex-shrink:0}',
'.pc-sub{display:flex;align-items:center;gap:2px;flex-wrap:wrap;min-width:0}',
'.pc-link{padding:5px 11px;font-size:12.5px;font-weight:600;color:#41506b!important;text-decoration:none!important;border-radius:7px;transition:all .15s;white-space:nowrap}',
'.pc-link:hover{color:#8f6d2c!important;background:#fbf3df;text-decoration:none!important}',
'.pc-link.on{color:#0d2244!important;background:#f3e5c3}',
/* hide any legacy hardcoded navbar if a page still carries one */
'.pc-nav ~ nav.nav{display:none}',
'@media(max-width:860px){',
  '.pc-row1{padding:7px 14px 6px;gap:7px;flex-wrap:wrap}',
  '.pc-brand-by{display:none}',
  '.pc-mark{width:26px;height:26px;font-size:14px}',
  '.pc-brand-name{font-size:14px}',
  '.pc-right{gap:8px;width:100%;justify-content:space-between}',
  '.pc-mk{padding:5px 10px;font-size:12.5px}',
  '.pc-lbtn{padding:4px 10px}',
  '.pc-row2{padding:0 14px 7px}',
  '.pc-sub{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}',
  '.pc-sub::-webkit-scrollbar{display:none}',
  '.pc-link{font-size:12px;padding:5px 9px}',
'}',
'@media(max-width:400px){.pc-mk .lang-en,.pc-mk .lang-zh{display:none!important}.pc-mk{padding:6px 9px}}'
].join('');

/* ---------- inject ---------- */
var root = document.getElementById('nav-root');
if (!root) return;

var style = document.createElement('style');
style.id = 'pc-nav-style';
style.textContent = css;
document.head.appendChild(style);
root.innerHTML = html;

/* ---------- language ---------- */
function syncButtons(lang) {
  root.querySelectorAll('.pc-lbtn').forEach(function (b) {
    b.classList.toggle('active', b.getAttribute('data-lang') === lang);
  });
}

/* Fallback for pages with no setLang() of their own (e.g. scorecards). */
function fallbackApply(lang) {
  document.body.classList.toggle('zh', lang === 'zh');
  document.documentElement.lang = lang === 'zh' ? 'zh-Hant' : 'en';
  document.querySelectorAll('.lang-en').forEach(function (e) {
    e.style.display = lang === 'en' ? '' : 'none';
  });
  document.querySelectorAll('.lang-zh').forEach(function (e) {
    e.style.display = lang === 'zh' ? '' : 'none';
  });
  try { localStorage.setItem('lang', lang); } catch (e) {}
}

/* These listeners are registered while the page's own scripts are still
   parsing, so they run first. stopImmediatePropagation prevents a page that
   also binds .lang-btn from calling setLang() a second time (which would
   dispose and rebuild every chart twice). */
root.querySelectorAll('.pc-lbtn').forEach(function (btn) {
  btn.addEventListener('click', function (ev) {
    ev.stopImmediatePropagation();
    var lang = btn.getAttribute('data-lang');
    if (typeof window.setLang === 'function') window.setLang(lang);
    else fallbackApply(lang);
    syncButtons(lang);
  });
});

var saved = 'en';
try { saved = localStorage.getItem('lang') || 'en'; } catch (e) {}
syncButtons(saved);

/* Pages with their own setLang() apply the saved language on load. Pages
   without one (scorecards) need it applied here. */
window.addEventListener('load', function () {
  syncButtons(saved);
  if (typeof window.setLang !== 'function' && saved === 'zh') fallbackApply('zh');
});

})();
