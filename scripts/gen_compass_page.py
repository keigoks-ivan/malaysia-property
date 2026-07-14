#!/usr/bin/env python3
"""Generate my/clock.html (Compass + Report Card redesign) from content.json + compass-*.json."""
import json, os
ROOT='/Users/ivanchang/malaysia-property'
SCR='/private/tmp/claude-501/-Users-ivanchang-malaysia-property/52542b53-2f2a-49e2-9a78-6dd7a75141c7/scratchpad'
C=json.load(open(ROOT+'/scripts/compass_assets/content.json'))
MKTS=['us','tw','my','jp','au']
DATA={m:open(f'{ROOT}/data/compass-{m}.json').read().strip() for m in MKTS}
V3=json.load(open(ROOT+'/data/compass-backtest-v3.json'))
def esc(s): return s  # copy is trusted (from our own agents); keep as-is
def dual(en,zh): return f'<span class="lang-en">{en}</span><span class="lang-zh" style="display:none">{zh}</span>'
def mkt(m, en, zh): return f'<span class="mkt-{m}">{dual(en,zh)}</span>'
def mktwrap(m, html): return f'<span class="mkt-{m}">{html}</span>'

def dedupe_css(css):
    """Drop exact-duplicate non-blank lines, keeping first occurrence and order.
    Needed because CSS is re-extracted from this script's own previous output
    (see below) -- without this, every regeneration re-appends the same
    CSS_EXTRA block and the <style> tag grows without bound (found 7x-duplicated
    rules already baked into the committed file before this fix)."""
    seen=set(); out=[]
    for line in css.split('\n'):
        key=line.strip()
        if key=='':
            continue  # drop blank lines entirely so they can't accumulate across regenerations
        if key in seen: continue
        seen.add(key); out.append(line)
    return '\n'.join(out)

# ---- risk-gauge numbers: every stat below is pulled programmatically from
# data/compass-backtest-v3.json (frozen protocol result), never hand-typed. ----
def fmt1(x): return f'{x:.1f}'
def fmtpct1(x): return f'{x*100:.1f}'

RISKVALS={}
for m in MKTS:
    Dm=json.loads(DATA[m])
    cur_q=Dm['q'][-1]
    on=(Dm['quad'][-1]=='starved' and bool(Dm['warn'][-1]))
    # AU was added after the v3 claim was frozen (Amendment 3) and lives under
    # au_holdout.market_results, not markets.au -- same shape, evaluated as an
    # out-of-sample hold-out rather than folded into the frozen 4-market result.
    mres=V3['au_holdout']['market_results'] if m=='au' else V3['markets'][m]
    rated_abs=mres['rated_abs']
    abs_r=mres['results']['T_ABS']['W_PRIM']
    rel_r=mres['results']['T_REL']['W_PRIM']
    v={'CUR_Q':cur_q,'ON':on,'STATE_EN':'ON' if on else 'OFF','STATE_ZH':'開啟' if on else '關閉'}
    v['OR_REL']=fmt1(rel_r['OR']); v['PREC_REL']=fmtpct1(rel_r['precision'])
    v['RECALL_REL']=fmtpct1(rel_r['recall']); v['BASE_REL']=fmtpct1(rel_r['base_rate'])
    c2,d2=rel_r['cells']['c'],rel_r['cells']['d']; v['PREC_REL_OFF']=fmtpct1(c2/(c2+d2))
    if rated_abs:
        v['OR_ABS']=fmt1(abs_r['OR']); v['PREC_ABS']=fmtpct1(abs_r['precision'])
        c1,d1=abs_r['cells']['c'],abs_r['cells']['d']; v['PREC_ABS_OFF']=fmtpct1(c1/(c1+d1))
    if m=='tw':
        ep=mres['results']['T_ABS']['W_PRIM']['episodes']['details'][0]
        v['EP_START']=ep['start_q']; v['EP_END']=ep['end_q']
    RISKVALS[m]=v
GV={'MH_ABS':fmt1(V3['threshold_evaluation']['ABS']['MH_pooled_OR']),
    'MH_REL':fmt1(V3['threshold_evaluation']['REL']['MH_pooled_OR']),
    'OR_US_ABS':RISKVALS['us']['OR_ABS'],'OR_JP_ABS':RISKVALS['jp']['OR_ABS']}

def risk_light(m):
    v=RISKVALS[m]
    if m=='tw': st,lab='notval',dual('NOT VALIDATED','未通過驗證')
    elif v['ON']: st,lab='on',dual('WARNING ON','警示開啟')
    else: st,lab='off',dual('WARNING OFF','警示關閉')
    return (f'<div class="rglight rg-{st}"><span class="dot"></span><span class="rglabel">{lab}</span>'
            f'<span class="rgqtr">{dual("as of ","截至 ")}{v["CUR_Q"]}</span></div>')

def risk_lights_html():
    return ''.join(mktwrap(m, risk_light(m)) for m in MKTS)

def risk_text_block():
    return ''.join(mkt(m, C['markets'][m]['risk_en'].format(**RISKVALS[m]),
                        C['markets'][m]['risk_zh'].format(**RISKVALS[m]))
                    for m in MKTS)

MK={'us':('United States','美國'),'tw':('Taiwan','台灣'),'my':('Malaysia','馬來西亞'),'jp':('Japan','日本'),'au':('Australia','澳洲')}
SPAN={'us':('US · 1975–2026','美國 · 1975–2026'),'tw':('Taiwan · 2001–2026','台灣 · 2001–2026'),
      'my':('Malaysia · 2000–2026','馬來西亞 · 2000–2026'),'jp':('Japan · 1975–2025','日本 · 1975–2025'),
      'au':('Australia · 1994–2026','澳洲 · 1994–2026')}

CSS=dedupe_css(open(ROOT+'/my/clock.html').read().split('<style>')[1].split('</style>')[0])
# strip old-only rules we replace; keep base. Add compass/report-card styles.
CSS_EXTRA="""
/* market-switch visibility: au (5th market) -- mirrors the tw/my/jp pattern that
   ships baked into the extracted CSS above (self-referential from prior output),
   which only ever covers tw/my/jp, so au needs its own explicit rules here. */
.mkt-au{display:none}
body.mk-au .mkt-us,body.mk-au .mkt-tw,body.mk-au .mkt-my,body.mk-au .mkt-jp{display:none}
body.mk-au .mkt-au{display:revert}
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
/* risk gauge */
.rgbox{border:1px solid var(--gold-soft);border-radius:12px;padding:16px 18px 14px;margin:0 0 4px;background:var(--bg-section)}
.rglight{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;border-radius:999px;padding:6px 14px;margin:0 0 10px}
.rglight .dot{width:9px;height:9px;border-radius:50%;flex:none}
.rglight .rgqtr{font-weight:600;opacity:.7;font-size:11px;margin-left:2px}
.rg-on{color:var(--negative);background:var(--negative-bg);border:1px solid #f2c9b3}
.rg-on .dot{background:var(--negative);box-shadow:0 0 0 3px rgba(185,28,28,.18)}
.rg-off{color:var(--positive);background:var(--positive-bg);border:1px solid #bfe3cc}
.rg-off .dot{background:var(--positive);box-shadow:0 0 0 3px rgba(21,128,61,.18)}
.rg-notval{color:var(--gold-deep);background:var(--gold-bg);border:1px solid var(--gold-soft)}
.rg-notval .dot{background:var(--gold-deep);box-shadow:0 0 0 3px rgba(143,109,44,.18)}
.rgnote{font-size:12.5px;color:var(--text-soft);line-height:1.85;margin:0 0 10px}
.rgcaveat{font-size:11.5px;color:var(--text-soft);line-height:1.75;border-left:2px solid var(--gold);background:rgba(184,146,74,.07);padding:8px 10px;border-radius:0 8px 8px 0;margin:6px 0 0}
"""

def badges():
    b=[f'<span class="kpi-badge badge-blue">{dual("Momentum × Credit","動能 × 信貸")}</span>',
       f'<span class="kpi-badge badge-orange">{dual("+ supply-glut warning · report card","+ 供給警示 · 體檢表")}</span>',
       f'<span class="kpi-badge badge-orange">{dual("Risk gauge · validated on 2 busts","風險警報 · 驗證於兩次崩盤")}</span>']
    for m in MKTS:
        b.append(f'<span class="kpi-badge badge-green mkt-{m}">{dual(*SPAN[m])}</span>')
    b.append(f'<span class="kpi-badge badge-orange">{dual("Updated Jul 2026","更新至 2026年7月")}</span>')
    return ''.join(b)

def mkt_buttons():
    r=[]
    for m in MKTS:
        a=' active' if m=='us' else ''
        r.append(f'<button class="mkt-btn{a}" data-mkt="{m}" type="button">{dual(*MK[m])}</button>')
    return '\n      '.join(r)

def market_block(field):
    return ''.join(mkt(m, C['markets'][m][field+'_en'], C['markets'][m][field+'_zh']) for m in MKTS)

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
<style>{dedupe_css(CSS+CSS_EXTRA)}</style>
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
    <span class="lk">{dual("Three instruments, one page","三套儀器，一頁讀")}</span>
    {dual(C['method']['lede_en'], C['method']['lede_zh'])}
  </div>

  <!-- reading panel -->
  <div class="judge">
    <p class="jlab">{dual('The reading right now · <span class="curQtr">—</span>','現在的判讀 · <span class="curQtr">—</span>')}</p>
    <p class="jphase curPhase">—</p>
    <p class="mkt-tw" style="margin:0 0 10px"><span class="rglight rg-notval" style="margin:0">{dual("cell ordering not validated in Taiwan (ρ=0.08)","四格排序在台灣未通過驗證（ρ=0.08）")}</span></p>
    <p class="mkt-au" style="margin:0 0 10px"><span class="rglight rg-notval" style="margin:0">{dual("cell ordering not validated in Australia (ρ=−0.16 — fuelled trails starved, the same no-crash signature as Taiwan)","四格排序在澳洲未通過驗證（ρ=−0.16——有燃料格報酬低於斷炊格，與台灣同樣的『從未真正崩盤』訊號）")}</span></p>
    <p class="jread">{market_block('judge')}</p>
    <div class="jwarn"><span class="dot"></span><span>{market_block('warn')}</span></div>
    <div class="jrow">
      <span class="jchip">{dual("Momentum: ","動能：")}<b class="jMom">—</b></span>
      <span class="jchip">{dual("Credit: ","信貸：")}<b class="jCred">—</b></span>
      <span class="jchip">{dual("In this cell since ","停留於此自 ")}<b class="jSince">—</b></span>
    </div>
    <p class="jhist">{dual("Historical echo: quarters in this cell saw a <b>3-year forward nominal house-price return with a median of <span class='jpMed'>—</span></b> (n=<span class='jpN'>—</span>).","歷史對照：落在此格的季度，其後 <b>3 年名目房價報酬中位 <span class='jpMed'>—</span></b>（n=<span class='jpN'>—</span>）。")} <span class="apx">{market_block('fwdnote') if False else dual("Descriptive of the past, not a forward promise.","描述過去，非對未來的承諾。")}</span></p>
    <p class="jhist jhistEra">—</p>
    <div class="cells4">
      <div class="cell4" data-ph="fuelled" style="border-color:#15803d"><p class="c4n" style="color:#15803d">{dual("Uptrend · Fuelled","上行·有燃料")}<span class="nowtag now-fuelled"></span></p><p class="c4d">{dual("price rising × credit expanding — trend with fuel","房價漲 × 信貸擴張——有燃料的趨勢")}</p><p class="c4s">{dual("3y median ","其後3年中位 ")}<b class="med-fuelled">—</b> · n=<span class="n-fuelled">—</span></p></div>
      <div class="cell4" data-ph="draining" style="border-color:#a16207"><p class="c4n" style="color:#a16207">{dual("Uptrend · Draining","上行·資金退")}<span class="nowtag now-draining"></span></p><p class="c4d">{dual("price rising × credit contracting — rally losing its fuel","房價漲 × 信貸收縮——漲勢在斷奶")}</p><p class="c4s">{dual("3y median ","其後3年中位 ")}<b class="med-draining">—</b> · n=<span class="n-draining">—</span></p></div>
      <div class="cell4" data-ph="reflating" style="border-color:#1d4ed8"><p class="c4n" style="color:#1d4ed8">{dual("Downtrend · Reflating","下行·資金回流")}<span class="nowtag now-reflating"></span></p><p class="c4d">{dual("price falling × credit expanding — money returning, possible bottom","房價跌 × 信貸擴張——資金回流、可能觸底")}</p><p class="c4s">{dual("3y median ","其後3年中位 ")}<b class="med-reflating">—</b> · n=<span class="n-reflating">—</span></p></div>
      <div class="cell4" data-ph="starved" style="border-color:#b91c1c"><p class="c4n" style="color:#b91c1c">{dual("Downtrend · Starved","下行·斷炊")}<span class="nowtag now-starved"></span></p><p class="c4d">{dual("price falling × credit contracting — no fuel, the weakest cell","房價跌 × 信貸收縮——無燃料，最弱的一格")}</p><p class="c4s">{dual("3y median ","其後3年中位 ")}<b class="med-starved">—</b> · n=<span class="n-starved">—</span></p></div>
    </div>
  </div>

  <!-- risk gauge -->
  <div class="blk">
    <h2>{dual("The Risk Gauge — a Validated Downside Warning","風險警報 · 已驗證的下檔警示")}</h2>
    <p class="sub">{dual(C['howto']['risk_howto_en'].format(**GV), C['howto']['risk_howto_zh'].format(**GV))}</p>
    <div class="chartbox rgbox">
      {risk_lights_html()}
      <p class="rgnote">{risk_text_block()}</p>
      <p class="rgcaveat">{dual(C['howto']['risk_caveat_en'], C['howto']['risk_caveat_zh'])}</p>
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
      <li class="warn">{dual(
        f"<b>The risk gauge is real, but thinly tested.</b> Starved-plus-supply-glut quarters carried elevated odds of a 3-year nominal loss (US OR {GV['OR_US_ABS']}×, Japan OR {GV['OR_JP_ABS']}×, pooled OR {GV['MH_ABS']}×) and of landing in a market's own worst quartile (US, Malaysia, Japan; pooled OR {GV['MH_REL']}×) — validated on frozen, pre-registered thresholds, not fit to the data afterward. But the absolute-loss claim rests on essentially two historical busts in this sample: the US 2006-08 crash and Japan's 1990s-2000s crash. A third crash, whenever it comes, is the real out-of-sample test this page hasn't faced yet.",
        f"<b>風險警報是真實的，但驗證樣本很薄。</b>斷炊疊加供給過剩的季度，三年期名目虧損的勝算明顯偏高（美國勝算比{GV['OR_US_ABS']}倍、日本勝算比{GV['OR_JP_ABS']}倍、合併勝算比{GV['MH_ABS']}倍），落入市場自身最差四分之一表現的勝算也偏高（美國、馬來西亞、日本；合併勝算比{GV['MH_REL']}倍）——這是在凍結、預先設定門檻的條件下驗證出來的，不是事後套進資料調出來的。但絕對虧損這項宣稱，基本上只建立在樣本中僅有的兩次歷史崩盤上：美國2006年至2008年的崩盤，以及日本1990年代至2000年代的崩盤。下一次崩盤，不論何時到來，才是這頁尚未面對過的真正樣本外測試。")}</li>
      <li>{dual('<b>The four-cell return ordering is still descriptive, not a forecast.</b> A separate attempt to validate Fuelled-beats-Starved as a forward-return ranking failed its own pre-registered gates (detail on <a href="/my/framework#v2compass">the framework backtest</a>); the compass panel and the forward-return table above describe the past, they are not a tested prediction of what comes next.',
        '<b>四格報酬排序仍是描述性的，不是預測。</b>另一次想把「助燃格贏過斷炊格」驗證為前向報酬排序的嘗試，未能通過自己預先凍結的門檻（詳情見<a href="/my/framework#v2compass">框架回測</a>）；上方的羅盤面板與前向報酬表描述的是過去，不是經過測試、對未來的預測。')}</li>
      <li>{dual("<b>Taiwan: neither claim validated — read its compass as descriptive only.</b> The risk gauge above never caught Taiwan's one recorded loss episode (2013-2015) and fell short of the pass bar on both the absolute-loss and relative-weakness tests; the return-ordering claim fails there too, for the same reason (a short, almost one-directional history). Treat every reading for Taiwan on this page as a record of the past, not a validated signal.",
        "<b>台灣：兩項宣稱都未通過驗證——它的羅盤讀數請只當描述看待。</b>上方的風險警報從未抓到台灣紀錄中唯一一次虧損事件（2013年至2015年），在絕對虧損與相對弱勢兩項測試上都未達通過門檻；報酬排序的宣稱在台灣也因同樣原因（歷史短、且幾乎單向）而失敗。請把這一頁上所有台灣的讀數，都當作對過去的紀錄，而不是已驗證的訊號。")}</li>
    </ul>
  </div>

  <p class="src">{dual("Inputs per market via FRED, BIS, DOSM/OpenDOSM, DGBAS, BNM, BOJ, e-Stat, NAPIC, World Bank and the Sinyi index. The compass axes are trailing-z: momentum = trailing-z of nominal house-price YoY (rolling window); credit = real (CPI-deflated) credit impulse, also trailing-z. The report card uses a different basis per gauge: valuation and supply are expanding-z against a market's entire history, while population is an absolute growth-direction reading on a fixed scale, not standardised against history. Momentum is nominal while credit is deflated — the trailing window de-trends steady inflation, and the validated downside target (the 3-year forward return) is itself a nominal figure, so the mismatch is by design, not an oversight. Independent analysis, not investment advice.","各市場輸入經 FRED、BIS、DOSM／OpenDOSM、主計總處、央行、日本央行、e-Stat、NAPIC、世界銀行與信義指數。羅盤軸為滾動 z：動能＝名目房價年增的滾動 z（滾動窗）；信貸＝經 CPI 平減的實質信貸脈衝，同樣是滾動 z。體檢表各量表基準不同：估值與供給是相對該市場整段歷史的擴張型 z，人口則是固定尺度的絕對成長方向讀數，不是相對歷史的標準化值。動能採名目、信貸採實質——滾動窗會抵銷穩定的通膨基期，而驗證用的下檔目標（3年前向報酬）本身也是名目數字，因此這個不對稱是刻意設計，不是疏漏。獨立分析，不構成投資建議。")}</p>
</main>

<footer class="footer"><div class="footer-ornament" aria-hidden="true"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
<p class="footer-disclaimer">{dual("<strong>Independent analysis for reference only</strong> — not investment advice. A project by InvestMQuest.","<strong>獨立分析參考</strong>，不構成投資建議。InvestMQuest 製作。")}</p></footer>

<script>
var D_US={DATA['us']};
var D_TW={DATA['tw']};
var D_MY={DATA['my']};
var D_JP={DATA['jp']};
var D_AU={DATA['au']};
</script>
<script>
{open(ROOT+'/scripts/compass_assets/compass.js').read()}
</script>
</body>
</html>
"""
open(ROOT+'/my/clock.html','w',encoding='utf-8').write(HTML)
print('wrote my/clock.html', len(HTML),'bytes')
