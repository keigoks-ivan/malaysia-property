#!/usr/bin/env python3
"""Generate the Property Compass pages from content.json + compass-*.json.

One generator, several output pages, each carrying a different market subset.
Add a page = add one entry to PAGES below (and make sure data/compass-<m>.json
exists for every market it lists).

Page config keys
  out       output path relative to repo root
  markets   ordered market subset this page carries (data, buttons, badges, copy)
  default   market shown before any hash / localStorage choice; must be in markets
  title     <title> text
  desc      <meta name="description"> text
  h1_en/zh  page headline (optional; falls back to H1_DEFAULT)

The market switcher, the #hash deep-links and the .mkt-XX visibility CSS are all
derived from len(markets): a one-market page renders no switcher at all.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = ROOT + '/scripts/compass_assets'

# ---------------------------------------------------------------- page config
H1_EN = 'The Property Compass — Trend, Credit &amp; a Report Card'
H1_ZH = '房產羅盤 — 趨勢、信貸與體檢表'

PAGES = [
    {'out': 'my/clock.html', 'markets': ['my'], 'default': 'my',
     'title': 'Property Compass | Malaysia · Property Check',
     'desc': 'Malaysia property compass: momentum × credit, a supply-glut risk gauge and a valuation / population / supply report card.'},
    {'out': 'global/compass.html', 'markets': ['us', 'tw', 'jp', 'au'], 'default': 'us',
     'title': 'Other Markets — Property Compass | Cross-market · Property Check',
     'desc': 'The property compass for the United States, Taiwan, Japan and Australia: momentum × credit, a supply-glut risk gauge and a report card per market.',
     'h1_en': 'The Property Compass — Other Markets',
     'h1_zh': '房產羅盤 — 其他市場'},
    # Thailand slots in here once data/compass-th.json exists:
    # {'out': 'th/clock.html', 'markets': ['th'], 'default': 'th',
    #  'title': 'Property Compass | Thailand · Property Check', 'desc': '...'},
]

# Markets whose data/copy must always be loaded, regardless of which page is
# being built: the honesty section and the pooled risk-gauge numbers quote the
# US and Japan odds ratios on every page.
ALL_MKTS = ['us', 'tw', 'my', 'jp', 'au']

C = json.load(open(ASSETS + '/content.json'))
DATA = {m: open(f'{ROOT}/data/compass-{m}.json').read().strip() for m in ALL_MKTS}
V3 = json.load(open(ROOT + '/data/compass-backtest-v3.json'))


def dual(en, zh): return f'<span class="lang-en">{en}</span><span class="lang-zh" style="display:none">{zh}</span>'
def mkt(m, en, zh): return f'<span class="mkt-{m}">{dual(en,zh)}</span>'
def mktwrap(m, html): return f'<span class="mkt-{m}">{html}</span>'


def dedupe_css(css):
    """Drop exact-duplicate non-blank lines, keeping first occurrence and order.

    The CSS now comes from a real asset file (compass_assets/compass.css) rather
    than from this script's own previous output, so it can no longer grow by
    re-appending -- but the per-page market rules are concatenated onto it and
    the guard is cheap, so it stays."""
    seen = set(); out = []
    for line in css.split('\n'):
        key = line.strip()
        if key == '':
            continue
        if key in seen: continue
        seen.add(key); out.append(line)
    return '\n'.join(out)


# ---- risk-gauge numbers: every stat below is pulled programmatically from
# data/compass-backtest-v3.json (frozen protocol result), never hand-typed. ----
def fmt1(x): return f'{x:.1f}'
def fmtpct1(x): return f'{x*100:.1f}'

RISKVALS = {}
for m in ALL_MKTS:
    Dm = json.loads(DATA[m])
    cur_q = Dm['q'][-1]
    on = (Dm['quad'][-1] == 'starved' and bool(Dm['warn'][-1]))
    # AU was added after the v3 claim was frozen (Amendment 3) and lives under
    # au_holdout.market_results, not markets.au -- same shape, evaluated as an
    # out-of-sample hold-out rather than folded into the frozen 4-market result.
    mres = V3['au_holdout']['market_results'] if m == 'au' else V3['markets'][m]
    rated_abs = mres['rated_abs']
    abs_r = mres['results']['T_ABS']['W_PRIM']
    rel_r = mres['results']['T_REL']['W_PRIM']
    v = {'CUR_Q': cur_q, 'ON': on, 'STATE_EN': 'ON' if on else 'OFF', 'STATE_ZH': '開啟' if on else '關閉'}
    v['OR_REL'] = fmt1(rel_r['OR']); v['PREC_REL'] = fmtpct1(rel_r['precision'])
    v['RECALL_REL'] = fmtpct1(rel_r['recall']); v['BASE_REL'] = fmtpct1(rel_r['base_rate'])
    c2, d2 = rel_r['cells']['c'], rel_r['cells']['d']; v['PREC_REL_OFF'] = fmtpct1(c2 / (c2 + d2))
    if rated_abs:
        v['OR_ABS'] = fmt1(abs_r['OR']); v['PREC_ABS'] = fmtpct1(abs_r['precision'])
        c1, d1 = abs_r['cells']['c'], abs_r['cells']['d']; v['PREC_ABS_OFF'] = fmtpct1(c1 / (c1 + d1))
    if m == 'tw':
        ep = mres['results']['T_ABS']['W_PRIM']['episodes']['details'][0]
        v['EP_START'] = ep['start_q']; v['EP_END'] = ep['end_q']
    RISKVALS[m] = v

GV = {'MH_ABS': fmt1(V3['threshold_evaluation']['ABS']['MH_pooled_OR']),
      'MH_REL': fmt1(V3['threshold_evaluation']['REL']['MH_pooled_OR']),
      'OR_US_ABS': RISKVALS['us']['OR_ABS'], 'OR_JP_ABS': RISKVALS['jp']['OR_ABS']}

MK = {'us': ('United States', '美國'), 'tw': ('Taiwan', '台灣'), 'my': ('Malaysia', '馬來西亞'),
      'jp': ('Japan', '日本'), 'au': ('Australia', '澳洲')}
SPAN = {'us': ('US · 1975–2026', '美國 · 1975–2026'), 'tw': ('Taiwan · 2001–2026', '台灣 · 2001–2026'),
        'my': ('Malaysia · 2000–2026', '馬來西亞 · 2000–2026'), 'jp': ('Japan · 1975–2025', '日本 · 1975–2025'),
        'au': ('Australia · 1994–2026', '澳洲 · 1994–2026')}

BASE_CSS = open(ASSETS + '/compass.css', encoding='utf-8').read()


def risk_light(m):
    v = RISKVALS[m]
    if m == 'tw': st, lab = 'notval', dual('NOT VALIDATED', '未通過驗證')
    elif v['ON']: st, lab = 'on', dual('WARNING ON', '警示開啟')
    else: st, lab = 'off', dual('WARNING OFF', '警示關閉')
    return (f'<div class="rglight rg-{st}"><span class="dot"></span><span class="rglabel">{lab}</span>'
            f'<span class="rgqtr">{dual("as of ","截至 ")}{v["CUR_Q"]}</span></div>')


def market_css(markets, default):
    """Per-page .mkt-XX / body.mk-XX visibility rules.

    A single-market page needs none: its only .mkt-XX spans are always visible.
    Multi-market pages hide every non-default subset up front (so the page shows
    the default market before JS runs) and swap on body.mk-XX."""
    if len(markets) < 2:
        return ''
    others = [m for m in markets if m != default]
    rules = [','.join('.mkt-' + m for m in others) + '{display:none}']
    for m in markets:
        rest = [o for o in markets if o != m]
        rules.append(','.join(f'body.mk-{m} .mkt-{o}' for o in rest) + '{display:none}')
        rules.append(f'body.mk-{m} .mkt-{m}{{display:revert}}')
    return '\n'.join(rules)


def build(page):
    MKTS = page['markets']
    DEFAULT = page['default']
    assert DEFAULT in MKTS, f"default {DEFAULT} not in {MKTS}"
    multi = len(MKTS) > 1

    def has(m): return m in MKTS
    def only(m, html): return html if has(m) else ''

    def badges():
        b = [f'<span class="kpi-badge badge-blue">{dual("Momentum × Credit","動能 × 信貸")}</span>',
             f'<span class="kpi-badge badge-orange">{dual("+ supply-glut warning · report card","+ 供給警示 · 體檢表")}</span>',
             f'<span class="kpi-badge badge-orange">{dual("Risk gauge · validated on 2 busts","風險警報 · 驗證於兩次崩盤")}</span>']
        for m in MKTS:
            b.append(f'<span class="kpi-badge badge-green mkt-{m}">{dual(*SPAN[m])}</span>')
        b.append(f'<span class="kpi-badge badge-orange">{dual("Updated Jul 2026","更新至 2026年7月")}</span>')
        return ''.join(b)

    def switcher():
        if not multi:
            return ''
        r = []
        for m in MKTS:
            a = ' active' if m == DEFAULT else ''
            r.append(f'<button class="mkt-btn{a}" data-mkt="{m}" type="button">{dual(*MK[m])}</button>')
        btns = '\n      '.join(r)
        return ('<div class="mkt-switch" role="tablist" aria-label="market">\n      '
                + btns + '\n    </div>')

    def market_block(field):
        return ''.join(mkt(m, C['markets'][m][field + '_en'], C['markets'][m][field + '_zh']) for m in MKTS)

    def risk_lights_html():
        return ''.join(mktwrap(m, risk_light(m)) for m in MKTS)

    def risk_text_block():
        return ''.join(mkt(m, C['markets'][m]['risk_en'].format(**RISKVALS[m]),
                           C['markets'][m]['risk_zh'].format(**RISKVALS[m])) for m in MKTS)

    h1 = dual(page.get('h1_en', H1_EN), page.get('h1_zh', H1_ZH))
    CSS = dedupe_css(BASE_CSS + '\n' + market_css(MKTS, DEFAULT))
    data_js = 'window.COMPASS_DATA={' + ','.join(f'"{m}":{DATA[m]}' for m in MKTS) + '};'
    cfg_js = 'window.COMPASS_CFG=' + json.dumps({'def': DEFAULT, 'markets': MKTS}, separators=(',', ':')) + ';'

    tw_note = only('tw', f'''<p class="mkt-tw" style="margin:0 0 10px"><span class="rglight rg-notval" style="margin:0">{dual("cell ordering not validated in Taiwan (ρ=0.08)","四格排序在台灣未通過驗證（ρ=0.08）")}</span></p>
    ''')
    au_note = only('au', f'''<p class="mkt-au" style="margin:0 0 10px"><span class="rglight rg-notval" style="margin:0">{dual("cell ordering not validated in Australia (ρ=−0.16 — fuelled trails starved, the same no-crash signature as Taiwan)","四格排序在澳洲未通過驗證（ρ=−0.16——有燃料格報酬低於斷炊格，與台灣同樣的『從未真正崩盤』訊號）")}</span></p>
    ''')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,600&family=IBM+Plex+Mono:wght@500;600;700&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
<link rel="stylesheet" href="../css/kl-theme.css">
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>{CSS}</style>
</head>
<body>

<div id="nav-root"></div>
<script src="/js/nav.js"></script>

<main class="wrap">
  <div class="pg-head">
    <h1 class="pg-title">{h1}</h1>
    {switcher()}
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
    {tw_note}{au_note}<p class="jread">{market_block('judge')}</p>
    <div class="jwarn"><span class="dot"></span><span>{market_block('warn')}</span></div>
    <div class="jrow">
      <span class="jchip">{dual("Momentum: ","動能：")}<b class="jMom">—</b></span>
      <span class="jchip">{dual("Credit: ","信貸：")}<b class="jCred">—</b></span>
      <span class="jchip">{dual("In this cell since ","停留於此自 ")}<b class="jSince">—</b></span>
    </div>
    <p class="jhist">{dual("Historical echo: quarters in this cell saw a <b>3-year forward nominal house-price return with a median of <span class='jpMed'>—</span></b> (n=<span class='jpN'>—</span>).","歷史對照：落在此格的季度，其後 <b>3 年名目房價報酬中位 <span class='jpMed'>—</span></b>（n=<span class='jpN'>—</span>）。")} <span class="apx">{dual("Descriptive of the past, not a forward promise.","描述過去，非對未來的承諾。")}</span></p>
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
      <li>{dual('<b>The four-cell return ordering is still descriptive, not a forecast.</b> A separate attempt to validate Fuelled-beats-Starved as a forward-return ranking failed its own pre-registered gates (detail on <a href="/global/framework#v2compass">the framework backtest</a>); the compass panel and the forward-return table above describe the past, they are not a tested prediction of what comes next.',
        '<b>四格報酬排序仍是描述性的，不是預測。</b>另一次想把「助燃格贏過斷炊格」驗證為前向報酬排序的嘗試，未能通過自己預先凍結的門檻（詳情見<a href="/global/framework#v2compass">框架回測</a>）；上方的羅盤面板與前向報酬表描述的是過去，不是經過測試、對未來的預測。')}</li>
      {(f'''<li>{dual("<b>Taiwan: neither claim validated — read its compass as descriptive only.</b> The risk gauge above never caught Taiwan's one recorded loss episode (2013-2015) and fell short of the pass bar on both the absolute-loss and relative-weakness tests; the return-ordering claim fails there too, for the same reason (a short, almost one-directional history). Treat every reading for Taiwan on this page as a record of the past, not a validated signal.",
        "<b>台灣：兩項宣稱都未通過驗證——它的羅盤讀數請只當描述看待。</b>上方的風險警報從未抓到台灣紀錄中唯一一次虧損事件（2013年至2015年），在絕對虧損與相對弱勢兩項測試上都未達通過門檻；報酬排序的宣稱在台灣也因同樣原因（歷史短、且幾乎單向）而失敗。請把這一頁上所有台灣的讀數，都當作對過去的紀錄，而不是已驗證的訊號。")}</li>''') if 'tw' in page['markets'] else ''}
    </ul>
  </div>

  <p class="src">{dual("Inputs per market via FRED, BIS, DOSM/OpenDOSM, DGBAS, BNM, BOJ, e-Stat, NAPIC, World Bank and the Sinyi index. The compass axes are trailing-z: momentum = trailing-z of nominal house-price YoY (rolling window); credit = real (CPI-deflated) credit impulse, also trailing-z. The report card uses a different basis per gauge: valuation and supply are expanding-z against a market's entire history, while population is an absolute growth-direction reading on a fixed scale, not standardised against history. Momentum is nominal while credit is deflated — the trailing window de-trends steady inflation, and the validated downside target (the 3-year forward return) is itself a nominal figure, so the mismatch is by design, not an oversight. Independent analysis, not investment advice.","各市場輸入經 FRED、BIS、DOSM／OpenDOSM、主計總處、央行、日本央行、e-Stat、NAPIC、世界銀行與信義指數。羅盤軸為滾動 z：動能＝名目房價年增的滾動 z（滾動窗）；信貸＝經 CPI 平減的實質信貸脈衝，同樣是滾動 z。體檢表各量表基準不同：估值與供給是相對該市場整段歷史的擴張型 z，人口則是固定尺度的絕對成長方向讀數，不是相對歷史的標準化值。動能採名目、信貸採實質——滾動窗會抵銷穩定的通膨基期，而驗證用的下檔目標（3年前向報酬）本身也是名目數字，因此這個不對稱是刻意設計，不是疏漏。獨立分析，不構成投資建議。")}</p>
</main>

<footer class="footer"><div class="footer-ornament" aria-hidden="true"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
<p class="footer-disclaimer">{dual("<strong>Independent analysis for reference only</strong> — not investment advice. A project by InvestMQuest.","<strong>獨立分析參考</strong>，不構成投資建議。InvestMQuest 製作。")}</p></footer>

<script>
{cfg_js}
{data_js}
</script>
<script>
{open(ASSETS + '/compass.js', encoding='utf-8').read()}
</script>
</body>
</html>
"""


if __name__ == '__main__':
    for page in PAGES:
        html = build(page)
        path = os.path.join(ROOT, page['out'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').write(html)
        print(f"wrote {page['out']}  markets={','.join(page['markets'])}  default={page['default']}  {len(html)} chars")
