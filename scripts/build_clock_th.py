#!/usr/bin/env python3
"""
Build the Thailand (Bangkok) property clock (Structure x Flow) from raw quarterly
series. Same five-force engine as the US pilot and the JP/TW/MY/AU builders; only
the inputs differ, so the compute half is byte-for-byte the same logic as
build_clock_au.py. Like Australia, Thailand has NO legacy market page to inject
into, so this script only ever writes data/clock-th.json — it never opens, reads
or creates any HTML file at all.

INPUT: scripts/.thdata/th_raw.json (provenance in scripts/.thdata/NOTES.md), shape:
{
  "q":      ["1991Q1", ...],        # 141 contiguous quarters, 1991Q1-2026Q1
  "price":  [ ... ],                # BIS Residential Property Prices for BANGKOK (nominal, 2010=100; FRED QTHN628BIS) -> judged + valuation numerator
  "pti":    [ ... ],                # ALL NULL — no official Thai price-to-income ratio exists -> valuation falls back to price/income
  "months": [ ... ],                # ALL NULL — Thailand publishes no housing inventory / absorption series
  "vacancy":[ ... ],                # ALL NULL — Thailand publishes no rental-vacancy series
  "gap":    [ ... ],                # not sourced (no household formation - completions series)
  "pop":    [ ... ],                # World Bank WDI total population, ANNUAL stepped onto the quarterly axis -> population (YoY = +)
  "credit": [ ... ],                # BIS household credit, THB bn, break-adjusted (FRED CRDQTHAHABIS) -> money (real growth = +)
  "rate":   [ ... ],                # money-market rate pre-2000Q3, BOT policy rate after (spliced) -> money (real, easing = +)
  "cpi":    [ ... ],                # IMF CPI index 2010=100 -> deflator for credit & rate
  "gdp":    [ ... ],                # IMF QNEA nominal GDP, THB bn -> economy (YoY = +)
  "unemp":  [ ... ],                # IMF LS unemployment rate % -> economy (falling = +)
  "income": [ ... ]                 # ILOSTAT AVERAGE MONTHLY EARNINGS PER EMPLOYEE (baht) -> economy (YoY = +); valuation denominator
}
Any series may be absent or contain nulls; a quarter needs >=3 of the components on each
axis to get a reading. Valuation uses `pti` if present, else price/income.

WHAT IS DIFFERENT ABOUT THAILAND — read before using any output of this file
---------------------------------------------------------------------------
1. NO SUPPLY DATA AT ALL. `months` and `vacancy` are 141/141 null. This is a real
   provenance gap, not a fetch failure: Thailand publishes no official quarterly
   inventory, absorption or vacancy series, REIC's statistics pages are an
   unextractable SPA, and the private surveys (AREA / SCB EIC / Knight Frank) are
   annual, start ~2021 and disagree by >60% on the same "Greater Bangkok unsold
   units" concept. The correct state is UNAVAILABLE — NOT "no glut". Bangkok is in
   fact the most oversupplied market covered on this site (this site's own
   /th/report documents 210,112 unsold units and 49.5 months of stock), so any
   rendering that reads "no supply-glut warning" for Thailand would be a false
   negative and flatly contradict our own market report. Downstream:
   build_compass.py emits `warn = null` (not false) for every Thai quarter plus a
   market-level `"supply_available": false`; the report-card supply gauge is an
   all-null array. See that script's docstring for the exact contract.
2. STRUCTURE AXIS (X) IS NOT COMPUTABLE. With months / vacancy / gap all null,
   at most two structure components can ever exist (population and valuation), and
   the engine requires >=3 — so `x`, `quad`, `ang`, `rad` and `qstat` are null /
   'warmup' for the entire 141 quarters BY DESIGN. That is the honest result, not a
   bug: this clock's Structure axis cannot be built for Thailand. The Compass
   (momentum x credit) does NOT use X and is fully computable — Thailand's usable
   instrument is the Compass, not this Structure x Flow clock.
3. VALUATION IS THIN AND NOT CROSS-MARKET COMPARABLE. `pti` is null, so valuation
   = price / income, and `income` only begins 2014Q1 (with 2015Q1 deliberately
   null — an evident ILOSTAT unit error, removed rather than interpolated). With
   the shared 24q window and the shared minobs=12 convention the first valuation z
   appears only once 12 real observations exist (~2017); the window is not fully
   populated until ~2020. Nothing before 2014Q1 is emitted at all — no
   backfilling. AND: `income` here is ILOSTAT average monthly earnings PER EMPLOYEE
   (baht/worker/month), NOT household disposable income as used for AU — the two
   are not unit-comparable, so Thailand's valuation gauge must never be placed on a
   like-for-like scale against another market's.
4. CREDIT ENDS ONE QUARTER EARLY. BIS household credit runs to 2025Q4 while BIS
   prices run to 2026Q1. The last credit value is NOT carried forward: the flow
   axis and the Compass credit reading are null at 2026Q1, so the current
   *complete* reading is 2025Q4 and 2026Q1 carries momentum only. Show it with an
   explanation; never impute it.
5. POP IS AN ANNUAL STEP. The World Bank annual value is repeated across its four
   quarters, so within-year QoQ change is identically zero; only the Q4->Q1 step
   carries information. YoY (lag 4) always compares two different annual values, so
   YoY is well defined at every quarter. 2026Q1 is null (2026 WDI unreleased).
   Thailand's population peaked in 2022 and has fallen every year since — the
   negative population reading is real.
6. UNEMP has seven missing COVID-era quarters (2020Q2, 2021Q1-2022Q3) and sits
   structurally near 1% because of the large informal/agricultural workforce, so
   its z is driven by very small absolute moves.

Axis 1991Q1-2026Q1 (141q). Honest nulls: credit 1991Q1-1991Q3 and 2026Q1, gdp
1991Q1-1992Q4, pop 2026Q1, unemp pre-2001Q1 + the COVID holes, income pre-2014Q1
+ 2015Q1, and pti/months/vacancy throughout. None of these are backfilled.

This market shares MY/TW/JP/AU's 6y (24q) trailing standardisation window (not the
US's 10y default); override with --win N.

Usage:
    python3 scripts/build_clock_th.py            # read .thdata/th_raw.json, write data/clock-th.json
    python3 scripts/build_clock_th.py --selftest # run on synthetic data, no files needed
    python3 scripts/build_clock_th.py --win 40   # use a 10y window (if history allows)
"""
import json, math, os, sys
import statistics as st

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INJSON  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.thdata', 'th_raw.json')
OUTJSON = os.path.join(ROOT, 'data', 'clock-th.json')

def yoy(lst):
    out = [None]*len(lst)
    for i in range(4, len(lst)):
        a, b = lst[i-4], lst[i]
        if a not in (None, 0) and b is not None: out[i] = (b/a-1)*100
    return out

def real(level, cpi):
    return [(level[i]/cpi[i]) if (level and cpi and level[i] is not None and cpi[i] is not None) else None
            for i in range(len(level))]

def czlist(vals, sign=1, win=24, minobs=12):
    """causal robust z over a trailing window (de-trend; no look-ahead)."""
    out = [None]*len(vals); hist = []
    for i, v in enumerate(vals):
        if v is not None:
            hist.append(v)
            if len(hist) > win: hist.pop(0)
        if v is None or len(hist) < minobs: continue
        med = st.median(hist)
        mad = st.median([abs(h-med) for h in hist]) or 1e-9
        out[i] = sign*max(-3, min(3, (v-med)/(1.4826*mad)))
    return out

def absz(vals, scale, sign=1):
    # absolute-direction score (NOT de-meaned) — for monotonic structural trends like population
    return [None if v is None else sign*max(-3, min(3, v/scale)) for v in vals]

def smooth(a, w=3):
    out = [None]*len(a)
    for i in range(len(a)):
        seg = [a[j] for j in range(max(0, i-w+1), i+1) if a[j] is not None]
        if seg and a[i] is not None: out[i] = sum(seg)/len(seg)
    return out

def compute(raw, win=24):
    q = raw['q']; n = len(q)
    def col(k): return raw.get(k, [None]*n)
    price = col('price'); cpi = col('cpi'); income = col('income')

    # valuation: pti if given, else price / income. For TH pti is all-null and income
    # starts 2014Q1, so val is null before 2014Q1 — never backfilled.
    if any(v is not None for v in col('pti')):
        val = col('pti')
    else:
        val = [(price[i]/income[i]) if (price[i] and income[i]) else None for i in range(n)]

    STRUCT = {
        'months': czlist(col('months'), -1, win),                    # supply: low = tight = + (TH: all null, no data)
        'vac':    czlist(col('vacancy'), -1, win),                   # supply: low vacancy = + (TH: all null, no data)
        'gap':    czlist(col('gap'),     +1, win),                   # demand: under-built = + (TH: not sourced)
        'demo':   absz(yoy(col('pop')), 0.7, +1),                    # population: growth = +
        'val':    czlist(val,            -1, win),                   # valuation: cheap = +
    }
    FLOW = {
        'credit': czlist(yoy(real(col('credit'), cpi)), +1, win),    # money: real credit impulse
        'rate':   czlist([(col('rate')[i]-yoy(cpi)[i]) if (col('rate')[i] is not None and yoy(cpi)[i] is not None) else None
                          for i in range(n)], -1, win),              # money: real rate, easing = +
        'gdp':    czlist(yoy(col('gdp')),   +1, win),                # economy: growth
        'jobs':   czlist(col('unemp'),      -1, win),                # economy: falling unemployment = +
        'income': czlist(yoy(income),       +1, win),                # economy: real income
    }

    def blend(comps):
        out = [None]*n
        for i in range(n):
            vals = [c[i] for c in comps.values() if c[i] is not None]
            if len(vals) >= 3: out[i] = sum(vals)/len(vals)
        return out
    X, Y = smooth(blend(STRUCT)), smooth(blend(FLOW))

    def quad(i):
        if X[i] is None or Y[i] is None: return 'warmup'
        hi, up = X[i] >= 0, Y[i] >= 0
        return 'expansion' if (hi and up) else 'base' if (hi and not up) else 'meltup' if up else 'downturn'
    QUAD = [quad(i) for i in range(n)]

    hpi_yoy = yoy(price)
    def fwd12(i):
        if i+12 >= n: return None
        a, b = price[i], price[i+12]
        return (b/a-1)*100 if (a and b) else None
    FWD = [fwd12(i) for i in range(n)]

    def stats(name):
        v = [FWD[i] for i in range(n) if QUAD[i] == name and FWD[i] is not None]
        if not v: return {'n': 0}
        sv = sorted(v)
        return {'n': len(v), 'med': round(st.median(v), 1), 'mn': round(min(v), 1),
                'mx': round(max(v), 1), 'q1': round(sv[len(sv)//4], 1)}
    QSTAT = {k: stats(k) for k in ['expansion', 'base', 'meltup', 'downturn']}

    def ang(i): return None if (X[i] is None or Y[i] is None) else math.degrees(math.atan2(Y[i], X[i]))
    def rad(i): return None if (X[i] is None or Y[i] is None) else math.hypot(X[i], Y[i])
    r1 = lambda a: [round(v, 1) if v is not None else None for v in a]
    r2 = lambda a: [round(v, 2) if v is not None else None for v in a]
    r3 = lambda a: [round(v, 3) if v is not None else None for v in a]

    # availability metadata — machine-readable version of the caveats in this
    # docstring, so a renderer never has to guess whether a null means "no data"
    # or "warming up".
    def first_q(series):
        for i in range(n):
            if series[i] is not None: return q[i]
        return None
    def last_q(series):
        for i in range(n-1, -1, -1):
            if series[i] is not None: return q[i]
        return None
    meta = {
        'market': 'th',
        'supply_available': False,          # months + vacancy are 141/141 null: state is UNAVAILABLE, not "no glut"
        'supply_reason': 'Thailand publishes no official quarterly housing inventory / absorption / vacancy series; '
                         'REIC is an unextractable SPA and the private surveys are annual, start ~2021 and disagree '
                         'by >60% on the same concept. Never render this as "no supply-glut warning".',
        'structure_axis_available': False,  # <3 structure components can ever exist -> x/quad are null for all quarters
        'structure_reason': 'Only population and valuation can ever be present on the Structure axis (months, vacancy '
                            'and gap are null), and the engine requires >=3 components, so x/quad/ang/rad/qstat are '
                            'empty for the whole series by design. Use the Compass (momentum x credit) for Thailand.',
        'valuation_basis': 'price / income, where income = ILOSTAT average monthly earnings PER EMPLOYEE (baht), '
                           'NOT household disposable income — not unit-comparable with other markets on this site.',
        'valuation_first_obs': first_q(val),
        'valuation_first_z': first_q(STRUCT['val']),
        'credit_last_obs': last_q(col('credit')),
        'price_last_obs': last_q(price),
        'current_complete_quarter': last_q(FLOW['credit']),  # last quarter with a credit reading; 2026Q1 is price-only
        'credit_note': 'BIS household credit lags BIS prices by one quarter. The last credit value is NOT carried '
                       'forward; the flow/credit reading is null at the final quarter by design.',
        'pop_note': 'Annual World Bank value stepped onto the quarterly axis: within-year QoQ change is zero by '
                    'construction; YoY (lag 4) is well defined. Thailand\'s population peaked in 2022 and has '
                    'declined every year since — the negative reading is real.',
    }

    return {
        'q': q, 'x': r3(X), 'y': r3(Y), 'quad': QUAD,
        'ang': r1([ang(i) for i in range(n)]), 'rad': r3([rad(i) for i in range(n)]),
        'hpi_yoy': r1(hpi_yoy), 'fwd12': r1(FWD),
        'comps_struct': {k: r2(v) for k, v in STRUCT.items()},
        'comps_flow':   {k: r2(v) for k, v in FLOW.items()},
        'raw': {'val': r2(val)},
        'qstat': QSTAT,
        'win': win,
        'meta': meta,
    }

def selftest():
    # synthetic 1991Q1.. with a slow cycle in structure and a fast cycle in flow
    q = [f'{y}Q{qq}' for y in range(1991, 2027) for qq in range(1, 5)][:141]
    n = len(q)
    price, base = [], 100.0
    for i in range(n):
        base *= 1 + (0.02 + 0.03*math.sin(i/9.0)) / 4
        price.append(round(base, 2))
    raw = {
        'q': q, 'price': price,
        'cpi':    [100*(1.01**(i/4)) for i in range(n)],
        'income': [100*(1.02**(i/4)) for i in range(n)],
        'gdp':    [100*(1.03**(i/4))*(1+0.02*math.sin(i/6.0)) for i in range(n)],
        'unemp':  [4+1.5*math.sin(i/6.0+1) for i in range(n)],
        'rate':   [4+2*math.cos(i/8.0) for i in range(n)],
        'credit': [100*(1.05**(i/4))*(1+0.03*math.sin(i/7.0)) for i in range(n)],
        'pop':    [100*(1.005**(i/4)) for i in range(n)],
        'months': [6+2*math.sin(i/10.0) for i in range(n)],
        'vacancy':[10+2*math.cos(i/11.0) for i in range(n)],
        'gap':    [20*math.sin(i/9.0) for i in range(n)],
    }
    out = compute(raw, win=24)
    labels = {'expansion':'Primed·Expansion','base':'Base·Coiling','meltup':'Late·Melt-up','downturn':'Correction·Downturn'}
    fv = next((q[i] for i in range(n) if out['x'][i] is not None), None)
    print(f'selftest: {n} quarters {q[0]}..{q[-1]}; first reading {fv}; current {q[-1]} -> {labels.get(out["quad"][-1], out["quad"][-1])}')
    for k in ['expansion','base','meltup','downturn']:
        s = out['qstat'][k]; print(f'  {labels[k]:20} n={s["n"]:<3} med={s.get("med")} q1={s.get("q1")}')
    assert any(v is not None for v in out['x']), 'no readings produced'
    assert set(out['quad']) - {'warmup'}, 'no corners assigned'
    # the supply-unavailable path: strip months/vacancy and confirm the metadata says so
    # (mirrors the real Thai input: months, vacancy AND gap all absent)
    raw2 = dict(raw); raw2['months'] = [None]*n; raw2['vacancy'] = [None]*n; raw2['gap'] = [None]*n
    out2 = compute(raw2, win=24)
    assert out2['meta']['supply_available'] is False, 'supply_available must be False with no supply series'
    assert out2['meta']['structure_axis_available'] is False, 'structure axis must be flagged unavailable'
    assert all(v is None for v in out2['x']), 'structure axis must be empty with <3 components'
    print('selftest OK (incl. supply-unavailable path)')

def main():
    if '--selftest' in sys.argv:
        selftest(); return
    win = 24
    if '--win' in sys.argv: win = int(sys.argv[sys.argv.index('--win')+1])
    if not os.path.exists(INJSON):
        print(f'no input at {INJSON} — run --selftest, or place raw TH series there first'); sys.exit(1)
    raw = json.load(open(INJSON))
    out = compute(raw, win)
    compact = json.dumps(out, separators=(',', ':'), ensure_ascii=False)
    os.makedirs(os.path.dirname(OUTJSON), exist_ok=True)
    open(OUTJSON, 'w', encoding='utf-8').write(compact)
    labels = {'expansion':'Primed·Expansion','base':'Base·Coiling','meltup':'Late·Melt-up','downturn':'Correction·Downturn'}
    print(f'quarters {out["q"][0]}..{out["q"][-1]}  current -> {labels.get(out["quad"][-1], out["quad"][-1])}  (win={win})')
    for k in ['expansion','base','meltup','downturn']:
        s = out['qstat'][k]; print(f'  {labels[k]:20} n={s["n"]:<3} med={s.get("med")} q1={s.get("q1")}')
    m = out['meta']
    print(f'  supply_available={m["supply_available"]}  structure_axis_available={m["structure_axis_available"]}')
    print(f'  valuation first obs {m["valuation_first_obs"]} / first z {m["valuation_first_z"]}; '
          f'credit last {m["credit_last_obs"]} vs price last {m["price_last_obs"]}')
    print(f'wrote {OUTJSON} ({len(compact)} bytes)')
    # Thailand has NO market page (like AU, unlike JP/TW/MY). This script never opens,
    # reads or writes any HTML — there is deliberately no injection path here at all.

if __name__ == '__main__':
    main()
