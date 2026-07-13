#!/usr/bin/env python3
"""Generate my/clock.html (Compass + Report Card redesign) from content.json + compass-*.json."""
import json, os
ROOT='/Users/ivanchang/malaysia-property'
SCR='/private/tmp/claude-501/-Users-ivanchang-malaysia-property/52542b53-2f2a-49e2-9a78-6dd7a75141c7/scratchpad'
C=json.load(open(ROOT+'/scripts/compass_assets/content.json'))
DATA={m:open(f'{ROOT}/data/compass-{m}.json').read().strip() for m in ['us','tw','my','jp']}
def esc(s): return s  # copy is trusted (from our own agents); keep as-is
def dual(en,zh): return f'<span class="lang-en">{en}</span><span class="lang-zh" style="display:none">{zh}</span>'
def mkt(m, en, zh): return f'<span class="mkt-{m}">{dual(en,zh)}</span>'

MK={'us':('United States','美國'),'tw':('Taiwan','台灣'),'my':('Malaysia','馬來西亞'),'jp':('Japan','日本')}
SPAN={'us':('US · 1975–2026','美國 · 1975–2026'),'tw':('Taiwan · 2001–2026','台灣 · 2001–2026'),
      'my':('Malaysia · 1988–2026','馬來西亞 · 1988–2026'),'jp':('Japan · 1975–2025','日本 · 1975–2025')}

CSS=open(ROOT+'/my/clock.html').read().split('<style>')[1].split('</style>')[0]
# strip old-only rules we replace; keep base. Add compass/report-card styles.
CSS_EXTRA="""
/* compass + report card */
.jwarn{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;color:#8a2b13;background:#fdf0e7;border:1px solid #f2c9b3;border-radius:999px;padding:5px 12px;margin:0 0 14px}
.jwarn .dot{width:8px;height:8px;border-radius:50%;background:#dc2626;box-shadow:0 0 0 3px rgba(220,38,38,.18)}
.card{display:grid;gap:12px;margin:6px 0 4px}
.crow{display:grid;grid-template-columns:76px 1fr;gap:12px;align-items:center}
.crow .cl{font-size:12px;font-weight:700;color:var(--navy);text-align:right}
.gauge{position:relative;height:34px}
.gtrack{position:absolute;top:13px;left:0;right:0;height:8px;border-radius:6px;background:linear-gradient(90deg,#e9c3c0,#f2ede2 50%,#c3e0cb)}
.gmid{position:absolute;top:8px;bottom:8px;left:50%;width:1px;background:#c9bfa8}
.gpin{position:absolute;top:8px;width:4px;height:18px;border-radius:3px;transform:translateX(-50%);box-shadow:0 1px 3px rgba(0,0,0,.25)}
.gends{position:absolute;top:-2px;left:0;right:0;display:flex;justify-content:space-between;font-size:9.5px;color:var(--muted)}
.cnote{font-size:11.5px;color:var(--text-soft);line-height:1.6;margin:3px 0 0}
.cnote b{color:var(--navy)}
.methnote{font-size:13px;color:var(--text-soft);line-height:1.95;margin:0 0 14px}
.methnote b{color:var(--navy);font-weight:600}
/* versus-the-world panel */
.xcdiv{display:flex;align-items:center;gap:10px;margin:26px 0 10px}
.xcdiv-line{flex:1;height:1px;background:var(--gold-line)}
.xcdiv-h{font-family:'Playfair Display','Noto Serif TC',serif;font-weight:700;color:var(--navy);font-size:15px;margin:0;white-space:nowrap}
.xcbars{display:grid;gap:9px;margin:6px 0 2px}
.xcrow{display:grid;grid-template-columns:88px 1fr 108px;gap:12px;align-items:center}
.xcrow .cl{font-size:11.5px;font-weight:700;color:var(--navy);text-align:right}
.xcbar{position:relative;height:20px}
.xctrack{position:absolute;top:7px;left:0;right:0;height:6px;border-radius:4px;background:linear-gradient(90deg,#e9c3c0,#f2ede2 50%,#c3e0cb)}
.xctrack-carry{background:linear-gradient(90deg,#e9c3c0,#f6ecd8 50%,#e3cfa0);box-shadow:0 0 0 1px rgba(184,146,74,.35) inset}
.xcpin{position:absolute;top:3px;width:3px;height:14px;border-radius:2px;transform:translateX(-50%);box-shadow:0 1px 3px rgba(0,0,0,.25)}
.xcpin-carry{width:5px;height:16px;top:2px;box-shadow:0 1px 5px rgba(184,146,74,.55)}
.xcval{font-family:'IBM Plex Mono',Inter,sans-serif;font-size:10.5px;color:var(--text-soft);text-align:right;white-space:nowrap}
.xcrow-carry{background:rgba(184,146,74,.10);border-radius:8px;padding:6px 8px;margin:2px -8px}
.xcrow-carry .cl{color:var(--gold-deep)}
.xcnote-carry{border-left:2px solid var(--gold);padding-left:10px;margin-top:8px}
@media(max-width:520px){.xcrow{grid-template-columns:70px 1fr 92px;gap:8px}}
"""

def badges():
    b=[f'<span class="kpi-badge badge-blue">{dual("Momentum × Credit","動能 × 信貸")}</span>',
       f'<span class="kpi-badge badge-orange">{dual("+ supply-glut warning · report card","+ 供給警示 · 體檢表")}</span>']
    for m in ['us','tw','my','jp']:
        b.append(f'<span class="kpi-badge badge-green mkt-{m}">{dual(*SPAN[m])}</span>')
    b.append(f'<span class="kpi-badge badge-orange">{dual("Updated Jul 2026","更新至 2026年7月")}</span>')
    return ''.join(b)

def mkt_buttons():
    r=[]
    for m in ['us','tw','my','jp']:
        a=' active' if m=='us' else ''
        r.append(f'<button class="mkt-btn{a}" data-mkt="{m}" type="button">{dual(*MK[m])}</button>')
    return '\n      '.join(r)

def market_block(field):
    return ''.join(mkt(m, C['markets'][m][field+'_en'], C['markets'][m][field+'_zh']) for m in ['us','tw','my','jp'])

HTML=f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Property Compass | Malaysia Property Monitor</title>
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,600&family=IBM+Plex+Mono:wght@500;600;700&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
<link rel="stylesheet" href="../css/kl-theme.css">
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>{CSS}{CSS_EXTRA}</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <a class="brand" href="/kl-check"><span class="brand-mark">K</span><span class="brand-text"><span class="brand-name">KL Property Check</span><span class="brand-by">by InvestMQuest</span></span></a>
    <div class="nav-links">
      <a class="nav-link" href="/kl-check">{dual("Scorecards","評分卡")}</a>
      <a class="nav-link" href="/my/report">{dual("Market Report","市場報告")}</a>
      <a class="nav-link" href="/my/macro">{dual("Macro","總經")}</a>
      <a class="nav-link" href="/my/framework">{dual("Framework","框架回測")}</a>
      <a class="nav-link active" href="/my/clock">{dual("Compass","羅盤")}</a>
      <div class="lang-btns"><button class="lang-btn active" data-lang="en">EN</button><button class="lang-btn" data-lang="zh">中文</button></div>
    </div>
  </div>
</nav>

<main class="wrap">
  <div class="pg-head">
    <h1 class="pg-title">{dual("The Property Compass — Trend, Credit &amp; a Report Card","房產羅盤 — 趨勢、信貸與體檢表")}</h1>
    <div class="mkt-switch" role="tablist" aria-label="market">
      {mkt_buttons()}
    </div>
    <div class="pg-badges">{badges()}</div>
  </div>

  <div class="lede">
    <span class="lk">{dual("Two instruments, one page","兩套儀器，一頁讀")}</span>
    {dual(C['method']['lede_en'], C['method']['lede_zh'])}
  </div>

  <!-- reading panel -->
  <div class="judge">
    <p class="jlab">{dual('The reading right now · <span class="curQtr">—</span>','現在的判讀 · <span class="curQtr">—</span>')}</p>
    <p class="jphase curPhase">—</p>
    <p class="jread">{market_block('judge')}</p>
    <div class="jwarn"><span class="dot"></span><span>{market_block('warn')}</span></div>
    <div class="jrow">
      <span class="jchip">{dual("Momentum: ","動能：")}<b class="jMom">—</b></span>
      <span class="jchip">{dual("Credit: ","信貸：")}<b class="jCred">—</b></span>
      <span class="jchip">{dual("In this cell since ","停留於此自 ")}<b class="jSince">—</b></span>
    </div>
    <p class="jhist">{dual("Historical echo: quarters in this cell saw a <b>3-year forward nominal house-price return with a median of <span class='jpMed'>—</span></b> (n=<span class='jpN'>—</span>).","歷史對照：落在此格的季度，其後 <b>3 年名目房價報酬中位 <span class='jpMed'>—</span></b>（n=<span class='jpN'>—</span>）。")} <span class="apx">{market_block('fwdnote') if False else dual("Descriptive of the past, not a forward promise.","描述過去，非對未來的承諾。")}</span></p>
    <div class="cells4">
      <div class="cell4" data-ph="fuelled" style="border-color:#15803d"><p class="c4n" style="color:#15803d">{dual("Uptrend · Fuelled","上行·有燃料")}<span class="nowtag now-fuelled"></span></p><p class="c4d">{dual("price rising × credit expanding — trend with fuel","房價漲 × 信貸擴張——有燃料的趨勢")}</p><p class="c4s">{dual("3y median ","其後3年中位 ")}<b class="med-fuelled">—</b> · n=<span class="n-fuelled">—</span></p></div>
      <div class="cell4" data-ph="draining" style="border-color:#a16207"><p class="c4n" style="color:#a16207">{dual("Uptrend · Draining","上行·資金退")}<span class="nowtag now-draining"></span></p><p class="c4d">{dual("price rising × credit contracting — rally losing its fuel","房價漲 × 信貸收縮——漲勢在斷奶")}</p><p class="c4s">{dual("3y median ","其後3年中位 ")}<b class="med-draining">—</b> · n=<span class="n-draining">—</span></p></div>
      <div class="cell4" data-ph="reflating" style="border-color:#1d4ed8"><p class="c4n" style="color:#1d4ed8">{dual("Downtrend · Reflating","下行·資金回流")}<span class="nowtag now-reflating"></span></p><p class="c4d">{dual("price falling × credit expanding — money returning, possible bottom","房價跌 × 信貸擴張——資金回流、可能觸底")}</p><p class="c4s">{dual("3y median ","其後3年中位 ")}<b class="med-reflating">—</b> · n=<span class="n-reflating">—</span></p></div>
      <div class="cell4" data-ph="starved" style="border-color:#b91c1c"><p class="c4n" style="color:#b91c1c">{dual("Downtrend · Starved","下行·斷炊")}<span class="nowtag now-starved"></span></p><p class="c4d">{dual("price falling × credit contracting — no fuel, the weakest cell","房價跌 × 信貸收縮——無燃料，最弱的一格")}</p><p class="c4s">{dual("3y median ","其後3年中位 ")}<b class="med-starved">—</b> · n=<span class="n-starved">—</span></p></div>
    </div>
  </div>

  <!-- compass chart -->
  <div class="blk">
    <h2>{dual("The Compass — Momentum × Credit","羅盤 · 動能 × 信貸")}</h2>
    <p class="sub">{dual(C['howto']['compass_howto_en'], C['howto']['compass_howto_zh'])}</p>
    <div class="chartbox"><div id="chartCompass" class="ch" style="height:520px"></div></div>
  </div>

  <!-- report card -->
  <div class="blk">
    <h2>{dual("The Report Card — Health, Not Prediction","體檢表 · 診斷體質，不預測")}</h2>
    <p class="sub">{dual(C['howto']['card_howto_en'], C['howto']['card_howto_zh'])}</p>
    <div class="chartbox" style="padding:18px 20px">
      <div class="card">
        <div class="crow"><div class="cl">{dual("Valuation","估值")}</div><div class="gauge" id="g-val"></div></div>
        <p class="cnote">{market_block('card_val')}</p>
        <div class="crow"><div class="cl">{dual("Population","人口")}</div><div class="gauge" id="g-pop"></div></div>
        <p class="cnote">{market_block('card_pop')}</p>
        <div class="crow"><div class="cl">{dual("Supply","供給")}</div><div class="gauge" id="g-sup"></div></div>
        <p class="cnote">{market_block('card_sup')}</p>
      </div>

      <!-- versus the world -->
      <div class="xcdiv"><span class="xcdiv-line"></span><h3 class="xcdiv-h">{dual("Versus the world · where it sits among 12 markets now","與世界比 · 現在在 12 個市場中的位置")}</h3><span class="xcdiv-line"></span></div>
      <p class="sub" style="margin:0 0 14px">{dual(C['howto']['xc_howto_en'], C['howto']['xc_howto_zh'])}</p>
      <div class="card">
        <div class="crow"><div class="cl">{dual("Valuation","估值")}</div><div class="gauge" id="g-xc-val"></div></div>
        <p class="cnote">{market_block('xc_val')}</p>
      </div>
      <div class="xcbars">
        <div class="xcrow"><div class="cl">{dual("Price/income","房價/所得")}</div><div class="xcbar" id="g-xc-pti"></div><div class="xcval" id="v-xc-pti">—</div></div>
        <div class="xcrow"><div class="cl">{dual("Rental yield","租金收益率")}</div><div class="xcbar" id="g-xc-yield"></div><div class="xcval" id="v-xc-yield">—</div></div>
        <div class="xcrow xcrow-carry"><div class="cl">{dual("Carry spread","持有利差")}</div><div class="xcbar" id="g-xc-carry"></div><div class="xcval" id="v-xc-carry">—</div></div>
        <div class="xcrow"><div class="cl">{dual("Vacancy","空置率")}</div><div class="xcbar" id="g-xc-vac"></div><div class="xcval" id="v-xc-vac">—</div></div>
        <div class="xcrow"><div class="cl">{dual("Population","人口成長")}</div><div class="xcbar" id="g-xc-pop"></div><div class="xcval" id="v-xc-pop">—</div></div>
      </div>
      <p class="cnote xcnote-carry">{market_block('xc_carry')}</p>
    </div>
    <p class="narr-p" style="font-size:12.5px">{dual("Trajectory: ","軌跡：")}{market_block('traj')}</p>
  </div>

  <!-- clock -->
  <div class="blk">
    <h2>{dual("The History Dial — the Path Walked","歷史盤 · 走過的路")}</h2>
    <p class="sub">{dual("The compass wrapped into a dial: press play and the hand sweeps every quarter, angle = which cell, distance = how far from neutral. A trajectory through history, not a forecast.","把羅盤捲成鐘面：按播放，指針逐季掃過，角度＝哪一格、離心＝離中性多遠。這是穿過歷史的軌跡，不是預測。")}</p>
    <div class="chartbox"><div id="chartClock" class="ch" style="height:460px"></div></div>
  </div>

  <!-- forward table -->
  <div class="blk">
    <h2>{dual("Forward Returns by Cell — Read Honestly","各格前向報酬 · 誠實讀")}</h2>
    <p class="sub">{dual(C['howto']['fwd_note_en'], C['howto']['fwd_note_zh'])}</p>
    <div class="mtbl-wrap"><table class="mtbl"><thead><tr>
      <th>{dual("Compass cell","羅盤格")}</th><th>{dual("Quarters (n)","季數 (n)")}</th><th>{dual("3y fwd median","3年前向中位")}</th><th>{dual("Range (worst → best)","範圍（最差 → 最好）")}</th>
    </tr></thead><tbody>
      <tr data-ph="fuelled"><td class="who"><span style="color:#15803d">■</span> {dual("Uptrend · Fuelled","上行·有燃料")}<span class="nowtag now-fuelled"></span></td><td class="n-fuelled">—</td><td><b class="med-fuelled">—</b></td><td class="rng-fuelled">—</td></tr>
      <tr data-ph="draining"><td class="who"><span style="color:#a16207">■</span> {dual("Uptrend · Draining","上行·資金退")}<span class="nowtag now-draining"></span></td><td class="n-draining">—</td><td><b class="med-draining">—</b></td><td class="rng-draining">—</td></tr>
      <tr data-ph="reflating"><td class="who"><span style="color:#1d4ed8">■</span> {dual("Downtrend · Reflating","下行·資金回流")}<span class="nowtag now-reflating"></span></td><td class="n-reflating">—</td><td><b class="med-reflating">—</b></td><td class="rng-reflating">—</td></tr>
      <tr data-ph="starved"><td class="who"><span style="color:#b91c1c">■</span> {dual("Downtrend · Starved","下行·斷炊")}<span class="nowtag now-starved"></span></td><td class="n-starved">—</td><td><b class="med-starved">—</b></td><td class="rng-starved">—</td></tr>
    </tbody></table></div>
  </div>

  <!-- methodology -->
  <div class="sec-rule"><h2>{dual("Why It's Built This Way","為什麼這樣設計")}</h2></div>
  <p class="methnote">{dual(C['method']['why_en'], C['method']['why_zh'])}</p>
  <p class="methnote">{dual(C['method']['frames_en'], C['method']['frames_zh'])}</p>

  <!-- honesty -->
  <div class="blk">
    <h2>{dual("What This Does and Does Not Claim","承諾什麼、不承諾什麼")}</h2>
    <ul class="pt">
      <li class="warn">{dual("<b>In-sample, not a forward test.</b> The compass was built and shown on the same 1975–2026 history; forward-return numbers describe the past. The genuine out-of-sample test is the quarters still to come.","<b>樣本內，不是前向測試。</b>羅盤是在同一段 1975–2026 歷史上建立並展示的；前向報酬數字描述過去。真正的樣本外測試，是還沒到來的季度。")}</li>
      <li>{dual("<b>The compass forecasts, the report card diagnoses.</b> Momentum × credit orders forward outcomes in the US, Malaysia and Japan (the market that actually crashed); Taiwan's short one-sided sample breaks it, disclosed. The report card never predicts — it describes valuation, population and supply health.","<b>羅盤預測、體檢表診斷。</b>動能×信貸在美國、馬來西亞、日本（真正崩過的市場）都能排序前向結果；台灣短且單邊的樣本會破壞它，已揭露。體檢表從不預測——它描述估值、人口、供給的體質。")}</li>
      <li>{dual("<b>Supply is a warning, not an axis.</b> A supply glut (extreme vacancy or completions) flags downside risk beyond momentum, but does not change which compass cell you are in.","<b>供給是警示，不是軸。</b>供給過剩（空置或完工極端）標示動能之外的下檔風險，但不改變你在羅盤的哪一格。")}</li>
    </ul>
  </div>

  <p class="src">{dual("Inputs per market via FRED, BIS, DOSM/OpenDOSM, DGBAS, BNM, BOJ, e-Stat, NAPIC, World Bank and the Sinyi index; assembled and standardised on trailing windows. Momentum = trailing-z of house-price YoY; credit = real credit impulse. Report-card gauges are trailing-z of valuation (price/income), population (absolute growth), and supply (completions/vacancy). Independent analysis, not investment advice.","各市場輸入經 FRED、BIS、DOSM／OpenDOSM、主計總處、央行、日本央行、e-Stat、NAPIC、世界銀行與信義指數；以滾動窗組裝標準化。動能＝房價年增的滾動 z；信貸＝實質信貸脈衝。體檢表為估值（房價／所得）、人口（絕對成長）、供給（完工／空置）的滾動 z。獨立分析，不構成投資建議。")}</p>
</main>

<footer class="footer"><div class="footer-ornament" aria-hidden="true"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
<p class="footer-disclaimer">{dual("<strong>Independent analysis for reference only</strong> — not investment advice. A project by InvestMQuest.","<strong>獨立分析參考</strong>，不構成投資建議。InvestMQuest 製作。")}</p></footer>

<script>
var D_US={DATA['us']};
var D_TW={DATA['tw']};
var D_MY={DATA['my']};
var D_JP={DATA['jp']};
</script>
<script>
{open(ROOT+'/scripts/compass_assets/compass.js').read()}
</script>
</body>
</html>
"""
open(ROOT+'/my/clock.html','w',encoding='utf-8').write(HTML)
print('wrote my/clock.html', len(HTML),'bytes')
