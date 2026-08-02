#!/usr/bin/env python3
"""
Compass + Report Card engine (v2 of the property clock).

Reasoning (from the empirical audit):
  - MOMENTUM (house-price trend) is the only factor with consistent forward
    predictive power across all four markets.
  - CREDIT direction adds cleanly (momentum × credit ordered best→worst in all 4).
  - VALUATION is unstable (mean-reverts in cyclical markets, reverses in Japan) →
    it does NOT belong on the predictive axis; it belongs on a descriptive card.
  - SUPPLY glut gives an extra downside warning beyond momentum (TW/MY/JP).

So v2 splits into two instruments:
  COMPASS  (predictive, trend-following): X = momentum, Y = credit → four cells,
           plus a SUPPLY-GLUT warning overlay.
  REPORT CARD (descriptive, not predictive): valuation / demand / population /
           supply shown as transparent per-force gauges — never averaged into an
           axis, never used to predict returns.

Reads the existing clock-<mkt>.json (which already carries hpi_yoy, comps_flow,
comps_struct, fwd12) so nothing needs re-fetching. Writes compass-<mkt>.json.

SUPPLY HAS THREE STATES, NOT TWO (added 2026-07-31 with Thailand)
-----------------------------------------------------------------
The supply-glut overlay used to be binary: warn[i] True = glut, False = no glut.
That is wrong for a market with NO supply series at all — loose() would be False
in every quarter and the market would silently publish "no supply-glut warning",
a false negative. Thailand is exactly that case (months and vacancy are 141/141
null; no official Thai inventory/absorption/vacancy series exists) and it is also
the most oversupplied market on this site, so the silent-false rendering would
directly contradict our own /th/report. The contract is now:

    warn[i] == true   -> supply glut flagged in that quarter
    warn[i] == false  -> supply measured, no glut in that quarter
    warn[i] == null   -> SUPPLY NOT MEASURABLE for this market (no data at all)

and, only for markets in the null case, the output carries a market-level flag:

    "supply_available": false

The flag is emitted ONLY when it is false. Its ABSENCE means supply data exists
(us/tw/my/jp/au), which keeps those five files byte-identical to before this
change. Renderers must therefore read it as: `d.supply_available === false` =>
show "no data" for the supply gauge and for the glut overlay; key missing =>
behave exactly as before. Note bool(null) is false in both Python and JS, so any
renderer that does `if (warn[i])` will silently get the WRONG state — the null
must be tested explicitly.
Consequences for the report card: card.supply is an all-null array for such a
market (no value to show), and the risk gauge (starved AND glut) is structurally
NOT EVALUABLE there, because the glut term is undefined — not "off".

SUPPLY HAS A BASIS, AND THE OVERLAY IS ONLY VALID ON A STOCK BASIS (added
2026-08-02 with Greece)
-----------------------------------------------------------------------------
The glut overlay asks "is there unsold/unoccupied stock hanging over the market".
Every market it was validated on answers that with a STOCK or ABSORPTION measure:
US months-of-inventory plus rental vacancy, Taiwan low-electricity vacancy,
Malaysia NAPIC unsold overhang, Japan 空き家率, Australia the SQM rental vacancy
rate. Greece has no such series at all (vacancy exists only in the 2011 and 2021
censuses) and its supply axis is a pure FLOW: Eurostat dwellings authorised, i.e.
permits issued per quarter.

A flow is not a small-sample version of a stock, it is procyclical with prices.
Greek permits collapsed from an index near 500 in 2005 to 20.3 in 2016Q1 — they
fell WITH prices — so the trailing z read "tight" through the whole 2007-2013
crash and the glut flag stayed OFF for every quarter of it, while it was ON in
2001-2005 and 2017-2024, both followed by strong gains. Under the frozen v3
protocol (Amendment 5, data/compass-backtest-v3.json → gr_holdout) the classifier
starved AND glut then scored OR 0.26, precision 0.000 and recall 0.000 on Greece,
against OR 36.75 / precision 0.824 / recall 0.778 for momentum alone. The glut
term did not add a warning, it destroyed one.

So the rule is general, not a Greece special case: each market DECLARES the basis
of every supply component it carries (SUPPLY_BASIS below), and the glut flag is
emitted ONLY where at least one component present in the data is a stock or
absorption measure. Declaring a component is mandatory — a component with values
but no declared basis raises, so a future market cannot inherit the bug silently.

    warn[i] == true    -> supply glut flagged in that quarter
    warn[i] == false   -> supply measured on a stock basis, no glut that quarter
    warn[i] == null    -> either NOT MEASURABLE (no supply data at all) or
                          MEASURED ON A BASIS THE OVERLAY IS NOT VALID ON

and the two null cases are told apart by market-level flags, each emitted only
in its own case:

    "supply_available": false                       -> not measurable (th)
    "supply_basis": "flow", "glut_valid": false     -> measured, overlay invalid (gr)
    neither key present                             -> stock basis, overlay live
                                                       (us/tw/my/jp/au — bytes
                                                       unchanged by this change)

Renderers therefore face FOUR supply states, not three, and must test the flags
explicitly and in order (supply_available, then glut_valid, then warn), because
bool(null) is false in both Python and JS: an unguarded check renders Greece as
"no glut", which is a false negative for a different reason than Thailand's.
The report-card supply gauge STILL SHOWS A VALUE for a flow market — permits are
a real measurement — but it must be labelled as a flow reading, never as a glut
reading, and the risk gauge there is REFUTED (evaluated and failed), which is a
different and stronger statement than Thailand's NOT EVALUABLE or Australia's
NOT RATED.

Mixed markets: Australia carries a stock component (SQM vacancy) alongside a flow
one (ABS approvals) and both sit inside loose(). The gate is at market level — at
least one stock component present — so Australia keeps its overlay and its exact
previous bytes. Gating each component separately is a live question but would
change a validated market's output and is deliberately not done here.
"""
import json, os, math, sys
import statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MKTS = ['us', 'tw', 'my', 'jp', 'au', 'th', 'gr']

# Declared basis of every supply component a market carries (see module docstring).
#   'stock' = a level or absorption measure: inventory, months-of-inventory,
#             vacancy rate, unsold overhang, empty-homes share.
#   'flow'  = new supply authorised or started per period: permits, approvals.
# The glut overlay is emitted only where at least one PRESENT component is
# 'stock'. A component that has values but no entry here raises in compute().
SUPPLY_BASIS = {
    # months-of-inventory (an absorption measure) + Census rental vacancy rate
    'us': {'months': 'stock', 'vac': 'stock'},
    # 低度使用（用電）住宅比率 vacancy + 使用執照 housing completions
    'tw': {'vac': 'stock', 'months': 'flow'},
    # NAPIC unsold-overhang units + NAPIC/DOSM completions
    'my': {'vac': 'stock', 'months': 'flow'},
    # 空き家率 (Housing and Land Survey) + 建築着工統計 housing starts
    'jp': {'vac': 'stock', 'months': 'flow'},
    # SQM rental vacancy rate + ABS building approvals
    'au': {'vac': 'stock', 'months': 'flow'},
    # no supply series at all: vacancy and months are both 0/141 present
    'th': {},
    # Eurostat sts_cobp_q dwellings authorised. THE ONLY MARKET WHOSE SUPPLY AXIS IS
    # FLOW-ONLY: vacancy is 0/117 (Greece's only tier-1 vacancy data is the 2011 and
    # 2021 censuses), so there is no stock component to anchor the overlay.
    'gr': {'months': 'flow'},
}

def tz(series, win=24, minobs=12):
    out = [None]*len(series); h = []
    for i, v in enumerate(series):
        if v is not None:
            h.append(v)
            if len(h) > win: h.pop(0)
        if v is None or len(h) < minobs: continue
        m = st.median(h); mad = st.median([abs(x-m) for x in h]) or 1e-9
        out[i] = max(-3, min(3, (v-m)/(1.4826*mad)))
    return out

def smooth(a, w=3):
    out = [None]*len(a)
    for i in range(len(a)):
        seg = [a[j] for j in range(max(0, i-w+1), i+1) if a[j] is not None]
        if seg and a[i] is not None: out[i] = sum(seg)/len(seg)
    return out

def yoy(a):
    """YoY growth (%). Guards against annual data forward-filled onto a quarterly axis:
    when the trailing 4-quarter window straddles a hold segment on BOTH ends (a[i]==a[i-4]
    and every point in between is that same flat value), a plain YoY reads a false 0 even
    though the underlying annual series is still growing — this hits the most recent
    quarter(s) right after the last real update. In that case carry forward the last
    genuine (non-degenerate) YoY reading instead of emitting 0."""
    out=[None]*len(a)
    last_good=None
    for i in range(4,len(a)):
        if a[i] is not None and a[i-4] not in (None,0):
            if a[i]==a[i-4] and all(a[j]==a[i] for j in range(i-4,i+1)) and last_good is not None:
                out[i]=last_good
            else:
                out[i]=(a[i]/a[i-4]-1)*100
                last_good=out[i]
    return out

def ez(a, sign=1, minobs=12):
    """EXPANDING (whole-history) robust z — for report-card 'health' gauges: how the current
    level compares to this market's ENTIRE history, not just the recent cycle."""
    out=[None]*len(a); h=[]
    for i,v in enumerate(a):
        if v is not None: h.append(v)
        if v is None or len(h)<minobs: continue
        m=st.median(h); mad=st.median([abs(x-m) for x in h]) or 1e-9
        out[i]=sign*max(-3,min(3,(v-m)/(1.4826*mad)))
    return out

def absz(a, scale=0.7, sign=1):
    return [None if v is None else sign*max(-3,min(3,v/scale)) for v in a]

def build_xc():
    """Cross-country (cross-sectional) report-card layer: where each market sits vs the WORLD now.
    This is the THIRD reference frame — distinct from the compass (trailing, cyclical) and the
    self-history gauges (expanding, vs own past). A market can be neutral vs its own history yet
    expensive vs the world (Taiwan) or expensive vs its own past yet middling vs the world (US).
    Vetted source: data/markets-summary.json (12-market universe). + = attractive / cheap."""
    M = json.load(open(os.path.join(ROOT, 'data', 'markets-summary.json')))['markets']
    ks = list(M.keys())
    def col(f): return {k: M[k].get(f) for k in ks}
    pti, yld, mort = col('priceIncomeRatio'), col('yield'), col('mortgageRate')
    vac, pop = col('vacancy'), col('populationGrowth')
    carry = {k: (round(yld[k]-mort[k], 1) if yld[k] is not None and mort[k] is not None else None) for k in ks}
    def zc(d, higher_better):
        vals = [v for v in d.values() if v is not None]
        m = st.median(vals); mad = st.median([abs(x-m) for x in vals]) or 1e-9
        out = {}
        for k, v in d.items():
            out[k] = None if v is None else round(max(-3, min(3, (v-m)/(1.4826*mad)))*(1 if higher_better else -1), 2)
        return out
    def rk(d, higher_better):
        it = sorted([(k, v) for k, v in d.items() if v is not None], key=lambda x: x[1], reverse=higher_better)
        return {k: i+1 for i, (k, v) in enumerate(it)}, len(it)
    # + = attractive/cheap: low PTI good, high yield good, high carry good, low vacancy good, high pop good
    Z = {'pti': zc(pti, False), 'yield': zc(yld, True), 'carry': zc(carry, True), 'vac': zc(vac, False), 'pop': zc(pop, True)}
    R = {'pti': rk(pti, False), 'yield': rk(yld, True), 'carry': rk(carry, True), 'vac': rk(vac, False), 'pop': rk(pop, True)}
    V = {'pti': pti, 'yield': yld, 'carry': carry, 'vac': vac, 'pop': pop}
    xc = {}
    for k in ks:
        blk = {'n': R['pti'][1]}
        for metric in ['pti', 'yield', 'carry', 'vac', 'pop']:
            blk[metric] = {'v': V[metric][k], 'rank': R[metric][0].get(k), 'z': Z[metric][k]}
        # objective valuation composite = mean cross-sectional z of the 3 valuation angles (+ = cheap/attractive)
        blk['valcomp'] = round(st.mean([Z['pti'][k], Z['yield'][k], Z['carry'][k]]), 2)
        xc[k] = blk
    return xc

# compass quadrant names: (momentum sign, credit sign)
CELLS = {
    'fuelled':  {'en': 'Uptrend · Fuelled',    'zh': '上行·有燃料'},   # mom+ cred+  (strongest)
    'draining': {'en': 'Uptrend · Draining',   'zh': '上行·資金退'},   # mom+ cred-  (fragile rally)
    'reflating':{'en': 'Downtrend · Reflating', 'zh': '下行·資金回流'}, # mom- cred+  (possible bottom)
    'starved':  {'en': 'Downtrend · Starved',  'zh': '下行·斷炊'},     # mom- cred-  (weakest)
}
def cell(mx, cy):
    if mx is None or cy is None: return 'warmup'
    up, fu = mx >= 0, cy >= 0
    return 'fuelled' if (up and fu) else 'draining' if (up and not fu) else 'reflating' if (not up and fu) else 'starved'

def compute(d, valsrc=None, supsrc=None, popyoy=None, xc=None, win=24, basis=None):
    q = d['q']; n = len(q)
    hpi = d['hpi_yoy']; fwd = d['fwd12']
    mom = smooth(tz(hpi, win))                       # X: price momentum
    cred = smooth(d['comps_flow']['credit'])         # Y: real credit impulse (already a trailing z)
    cs = d['comps_struct']
    QUAD = [cell(mom[i], cred[i]) for i in range(n)]

    # supply-glut warning: vacancy or supply-flow z very loose (<= -1)
    def loose(i):
        vv = cs.get('vac', [None]*n)[i]; mm = cs.get('months', [None]*n)[i]
        return (vv is not None and vv <= -1) or (mm is not None and mm <= -1)
    # THIRD AND FOURTH STATES (see module docstring). Third: a market with no supply
    # series at all would score loose()=False everywhere and read as "no glut". Fourth:
    # a market whose only supply component is a FLOW (permits) would score a glut flag
    # that is procyclical and inverts the intended signal. Both emit null, and are told
    # apart by the market-level flags below.
    cbasis = basis or {}
    present = [k for k in ('vac', 'months') if any(v is not None for v in cs.get(k, [None]*n))]
    undeclared = [k for k in present if k not in cbasis]
    if undeclared:
        raise ValueError(f"supply component(s) {undeclared} carry data but have no declared "
                         f"basis in SUPPLY_BASIS; declare 'stock' or 'flow' before building")
    sup_avail = bool(present)
    glut_valid = any(cbasis[k] == 'stock' for k in present)
    warn = [loose(i) for i in range(n)] if glut_valid else [None]*n

    def med(a):
        a = [x for x in a if x is not None]; return round(st.median(a), 1) if a else None
    def stats(name):
        idx = [i for i in range(n) if QUAD[i] == name and fwd[i] is not None]
        v = [fwd[i] for i in idx]
        if not v: return {'n': 0}
        sv = sorted(v)
        return {'n': len(v), 'med': round(st.median(v), 1), 'mn': round(min(v), 1),
                'mx': round(max(v), 1), 'q1': round(sv[len(sv)//4], 1)}
    QSTAT = {k: stats(k) for k in CELLS}

    # era split (frozen design: boundary 2010Q1, pre = q < '2010Q1', post = q >= '2010Q1').
    # Used only for the honesty-upgrade echo line in the Compass UI; does not touch QSTAT itself.
    def era_med_n(name, era):
        idx = [i for i in range(n) if QUAD[i] == name and fwd[i] is not None
               and ((q[i] < '2010Q1') if era == 'pre' else (q[i] >= '2010Q1'))]
        v = [fwd[i] for i in idx]
        return {'med': round(st.median(v), 1) if v else None, 'n': len(v)}
    QSTAT_ERA = {k: {'pre': era_med_n(k, 'pre'), 'post': era_med_n(k, 'post')} for k in CELLS}
    total_pre_scored = sum(QSTAT_ERA[k]['pre']['n'] for k in CELLS)
    ALL_MODERN = total_pre_scored < 8

    def ang(i): return None if (mom[i] is None or cred[i] is None) else math.degrees(math.atan2(cred[i], mom[i]))
    def rad(i): return None if (mom[i] is None or cred[i] is None) else math.hypot(mom[i], cred[i])
    r1 = lambda a: [round(v, 1) if v is not None else None for v in a]
    r2 = lambda a: [round(v, 2) if v is not None else None for v in a]
    r3 = lambda a: [round(v, 3) if v is not None else None for v in a]

    # report-card factors (descriptive, NOT in the compass). Health = position vs the market's
    # WHOLE history (expanding), not the recent cycle — a trailing window hides absolute extremes.
    card = {
        'valuation':  r2(ez(valsrc, -1)) if valsrc else r2(cs.get('val', [None]*n)),   # + = cheap vs full history
        'population': r2(absz(popyoy, 0.7, +1)) if popyoy else r2(cs.get('demo', [None]*n)),  # + = growing (absolute)
        'supply':     r2(ez(supsrc, -1)) if supsrc else r2(cs.get('months', [None]*n)),  # + = tight vs full history
    }
    out = {
        'q': q, 'mom': r3(mom), 'cred': r3(cred), 'quad': QUAD, 'warn': warn,
        'ang': r1([ang(i) for i in range(n)]), 'rad': r3([rad(i) for i in range(n)]),
        'hpi_yoy': r1(hpi), 'fwd12': r1(fwd), 'qstat': QSTAT, 'card': card,
        'xc': xc,   # cross-country report-card layer (vs the world now); None if unavailable
        'qstat_era': QSTAT_ERA, 'all_modern': ALL_MODERN,
    }
    # Each flag is emitted only in its own case, so a stock-basis market with supply data
    # carries neither key and keeps its exact previous bytes.
    if not sup_avail:
        out['supply_available'] = False
    elif not glut_valid:
        out['supply_basis'] = 'flow'
        out['glut_valid'] = False
    return out

def main():
    RAWF = {'tw':'.twdata/tw_raw.json','my':'.mydata/my_raw.json','jp':'.jpdata/jp_raw.json','au':'.audata/au_raw.json',
            'th':'.thdata/th_raw.json','gr':'.grdata/gr_raw.json'}
    XC = build_xc()
    # optional argv filter: `python3 scripts/build_compass.py th` rebuilds only the named
    # market(s). Needed because data/markets-summary.json (the xc source) drifts between
    # runs, so a blanket rebuild silently rewrites every market's cross-sectional block.
    only = [a for a in sys.argv[1:] if a in MKTS]
    for m in (only or MKTS):
        d = json.load(open(os.path.join(ROOT, 'data', f'clock-{m}.json')))
        # report-card source series (absolute levels), standardised over full history in compute()
        if m == 'us':
            r = d['raw']; valsrc = r['val']; supsrc = r['months']; popyoy = r['pop_yoy']
        else:
            rw = json.load(open(os.path.join(ROOT, 'scripts', RAWF[m])))
            if m == 'tw' and rw.get('pti') and any(x is not None for x in rw['pti']):
                valsrc = rw['pti']                                  # real house-price-to-income ratio
            else:
                valsrc = [(rw['price'][i]/rw['income'][i]) if (rw.get('income') and rw['price'][i] and rw['income'][i]) else None
                          for i in range(len(rw['price']))]
            supsrc = rw.get('vacancy')                             # TW low-electricity vacancy / MY overhang / JP 空き家率
            # GREECE (added 2026-08-02): vacancy is 117/117 null (only the 2011 and 2021
            # censuses exist) while `months` — Eurostat quarterly dwellings authorised — is
            # 117/117 present. Fall back to the months level so the report-card supply gauge
            # has a value, matching the glut ring, which already reads comps_struct.months.
            # Sign is the same as vacancy's (ez(..., -1): + = tight vs full history), because
            # high permits = loose supply, exactly as in the clock builders' czlist(months, -1).
            # INERT for every existing market: tw/my/jp/au have real vacancy values, and TH's
            # vacancy and months are BOTH all-null so the fallback yields the same all-null
            # gauge. Verified byte-identical for us/tw/my/jp/au/th.
            if supsrc is None or all(v is None for v in supsrc):
                supsrc = rw.get('months') or supsrc
            popyoy = yoy(rw['pop']) if rw.get('pop') else None
        assert m in SUPPLY_BASIS, f"market {m} must declare its supply basis in SUPPLY_BASIS"
        out = compute(d, valsrc, supsrc, popyoy, xc=XC.get(m), basis=SUPPLY_BASIS[m])
        json.dump(out, open(os.path.join(ROOT, 'data', f'compass-{m}.json'), 'w'), separators=(',', ':'))
        i = len(out['q'])-1
        lab = {'fuelled':'上行·有燃料','draining':'上行·資金退','reflating':'下行·資金回流','starved':'下行·斷炊','warmup':'暖機'}
        w = out['warn'][i]
        ws = w if w is not None else ('n/a (supply is a %s series, glut overlay not valid)' % out['supply_basis']
                                      if out.get('glut_valid') is False else 'n/a (no supply data)')
        print(f"{m.upper()}: {out['q'][i]} → {lab[out['quad'][i]]}  mom={out['mom'][i]} cred={out['cred'][i]} warn={ws}")

if __name__ == '__main__':
    main()
