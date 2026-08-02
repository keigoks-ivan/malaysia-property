#!/usr/bin/env python3
"""
Build the Greece property clock (Structure x Flow) from raw quarterly series.
Same five-force engine as the US pilot and the JP/TW/MY/AU/TH builders; only the
inputs differ, so the compute half is the same logic as build_clock_au.py. Like
Australia and Thailand, Greece has NO legacy market page to inject into, so this
script only ever writes data/clock-gr.json — it never opens, reads or creates any
HTML file at all.

INPUT: scripts/.grdata/gr_raw.json (provenance in scripts/.grdata/NOTES.md), shape:
{
  "q":      ["1997Q1", ...],        # 117 contiguous quarters, 1997Q1-2026Q1
  "price":  [ ... ],                # BIS Residential Property Prices, Greece (nominal; FRED QGRN628BIS) -> judged + valuation numerator
  "pti":    [ ... ],                # ALL NULL — no official Greek price-to-income ratio exists -> valuation falls back to price/income
  "months": [ ... ],                # Eurostat sts_cobp_q dwellings AUTHORISED, quarterly index 2021=100, NSA -> supply (low = tight)
  "vacancy":[ ... ],                # ALL NULL — Greece's only tier-1 vacancy data is the 2011 and 2021 censuses (two points, ten years apart)
  "gap":    [ ... ],                # not sourced (no household formation - completions series)
  "pop":    [ ... ],                # Eurostat namq_10_pe POP_NC, thousands of persons, genuinely quarterly -> population (YoY = +)
  "credit": [ ... ],                # BIS credit to households, EUR bn, ALL LENDERS (FRED CRDQGRAHABIS) -> money (real growth = +)
  "rate":   [ ... ],                # drachma overnight call rate pre-2001Q1, ECB DEPOSIT FACILITY rate after (spliced) -> money (real, easing = +)
  "cpi":    [ ... ],                # Eurostat HICP index 2025=100, NSA -> deflator for credit & rate
  "gdp":    [ ... ],                # Eurostat nominal GDP, EUR m -> economy (YoY = +)
  "unemp":  [ ... ],                # OECD/Eurostat harmonised unemployment rate % -> economy (falling = +)
  "income": [ ... ]                 # Eurostat household gross disposable income (B6G, S14_S15, EUR m) -> economy (YoY = +); valuation denominator
}
Any series may be absent or contain nulls; a quarter needs >=3 of the components on each
axis to get a reading. Valuation uses `pti` if present, else price/income.

WHAT IS DIFFERENT ABOUT GREECE — read before using any output of this file
--------------------------------------------------------------------------
1. THE SUPPLY AXIS IS POPULATED, AND IT RESTS ON ONE COMPONENT. `months` is
   117/117 present (Eurostat quarterly dwellings authorised, index 2021=100),
   the same slot, sign and convention as Australia's ABS building approvals:
   high = more permits = looser future supply, sign -1. `vacancy` is 117/117 null
   and cannot be rescued (2011 and 2021 censuses only). So downstream
   build_compass.py does NOT emit "supply_available": false for Greece — the
   supply-glut ring and the report-card supply gauge both work from 1997Q1 — but
   they are a PURE PERMITS-FLOW reading with no vacancy cross-check. Describe them
   that way; a permits collapse and an empty-homes stock are not the same fact.
2. TWO REGULATORY ARTEFACTS IN `months` THAT MUST NOT SILENTLY DRIVE A GLUT FLAG.
   (a) 2005Q4 = 1505.0 is a VAT pull-forward: 19% VAT applied to buildings
   permitted from 1 January 2006, so the whole country filed in Q4 2005. (b) 2025
   is depressed by the suspension of the New Building Regulation (NOK) bonuses
   (December 2024 to May 2025), which froze filings — so 2026Q1's +70.2% y/y sits
   on an artificially weak base and is not a clean demand signal. Both are real
   published values and are NOT smoothed here; the caveat travels in `meta`.
3. `rate` IS NOT A GREEK MONETARY CONDITION AFTER 2001. From 2001Q1 the field is
   the ECB deposit facility rate — Greece has had no national policy rate since
   euro entry — and during 2010-2018 Greek financial conditions were violently
   disconnected from it: the Greek 10-year yield peaked at 29.24% (February 2012)
   while the ECB policy rate sat at 1.00%. Any reading of the money axis as "Greek
   monetary conditions" is unreliable across that decade. The splice at
   2000Q4/2001Q1 is a -3.427pp step (7.177% -> 3.750%), of which about -2.333pp is
   genuine convergence and -1.093pp is the change of concept, so YoY through 2001
   is not clean either.
4. `credit` IS ALL-LENDER, NOT BANKS — deliberately. BIS credit to households fell
   -32.3% from its 2010Q3 peak (EUR 139.3bn -> 94.3bn at 2025Q4); the ECB bank
   housing-loan stock fell -68.6% over the same window. The difference is the
   Hercules/HAPS securitisations moving loans off bank books to servicers and SPVs
   — the households still owe them. The credit-impulse axis here therefore measures
   LENDER-UNIVERSE credit, which is the right choice, and any page describing Greek
   deleveraging off the bank series alone is wrong.
5. CREDIT ENDS ONE QUARTER EARLY. BIS household credit runs to 2025Q4 while BIS
   prices run to 2026Q1 (the normal state of the file at any refresh). The last
   credit value is NOT carried forward: the flow axis and the Compass credit
   reading are null at 2026Q1, so the current *complete* reading is 2025Q4 and
   2026Q1 carries momentum only.
6. VALUATION EXISTS ONLY FROM 1999Q1 AND IS TRUSTWORTHY ONLY FROM ~2005. `pti` is
   null (no official Greek PTI, and Greece is absent from Eurostat's HPI collection
   altogether, so there is also NO independent tier-1 cross-check on the BIS price
   series). Valuation = price / income, and `income` starts 1999Q1, so with the
   shared 24q window and minobs=12 the first valuation z appears ~2002 and the
   window is not fully populated until ~2005.
7. `cpi` IS HICP, NOT BIS's OWN DEFLATOR, AND cpi/months ARE NSA. The national CPI
   (GRCCPIALLMINMEI) is exactly BIS's deflator and reproduces QGRR628BIS to 0.045%,
   but it is discontinued at 2025-04, so Eurostat HICP is used throughout instead
   (max level divergence 2.15% over 29 years). Anything that claims to show "the
   BIS real house price index" must use QGRR628BIS directly rather than recomputing
   it from price/cpi here. Both `cpi` and `months` are NSA (permits seasonal
   factors: Q1 0.881, Q2 1.018, Q3 0.993, Q4 1.114) — read YoY only, never QoQ.
8. THE PRICE TAIL IS PROVISIONAL. The Bank of Greece flags 2025Q2-2026Q1 as
   Provisional on its parallel index and revises it; the last four `price` quarters
   (and the most recent `gdp`, `income`, `months`) should be treated as provisional.
9. EARLY-QUARTER COVERAGE. `unemp` starts 1998Q2 and `income` 1999Q1, so the
   economy axis rests on `gdp` alone until 1998Q2 and valuation does not exist
   until 1999Q1. None of this is backfilled.

Axis 1997Q1-2026Q1 (117q). Honest nulls: pti and vacancy throughout, credit 2026Q1,
unemp pre-1998Q2, income pre-1999Q1. Nothing is interpolated or forward-filled.

This market shares MY/TW/JP/AU/TH's 6y (24q) trailing standardisation window (not
the US's 10y default); override with --win N.

Usage:
    python3 scripts/build_clock_gr.py            # read .grdata/gr_raw.json, write data/clock-gr.json
    python3 scripts/build_clock_gr.py --selftest # run on synthetic data, no files needed
    python3 scripts/build_clock_gr.py --win 40   # use a 10y window (if history allows)
"""
import json, math, os, sys
import statistics as st

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INJSON  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.grdata', 'gr_raw.json')
OUTJSON = os.path.join(ROOT, 'data', 'clock-gr.json')

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

    # valuation: pti if given, else price / income (GR has no pti — see docstring note 6)
    if any(v is not None for v in col('pti')):
        val = col('pti')
    else:
        val = [(price[i]/income[i]) if (price[i] and income[i]) else None for i in range(n)]

    STRUCT = {
        'months': czlist(col('months'), -1, win),                    # supply: low permits = tight = +
        'vac':    czlist(col('vacancy'), -1, win),                   # all null for GR (no quarterly vacancy series)
        'gap':    czlist(col('gap'),     +1, win),                   # not sourced for GR
        'demo':   absz(yoy(col('pop')), 0.7, +1),                    # population: growth = +
        'val':    czlist(val,            -1, win),                   # valuation: cheap = +
    }
    FLOW = {
        'credit': czlist(yoy(real(col('credit'), cpi)), +1, win),    # money: real credit impulse (ALL-LENDER, see note 4)
        'rate':   czlist([(col('rate')[i]-yoy(cpi)[i]) if (col('rate')[i] is not None and yoy(cpi)[i] is not None) else None
                          for i in range(n)], -1, win),              # money: real rate, easing = + (ECB rate from 2001, see note 3)
        'gdp':    czlist(yoy(col('gdp')),   +1, win),                # economy: growth
        'jobs':   czlist(col('unemp'),      -1, win),                # economy: falling unemployment = +
        'income': czlist(yoy(income),       +1, win),                # economy: income growth
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
    supply_components = [k for k in ('months', 'vac') if any(v is not None for v in STRUCT[k])]
    meta = {
        'market': 'gr',
        'supply_available': len(supply_components) > 0,
        'supply_components': supply_components,          # ['months'] — permits flow only, NO vacancy cross-check
        'supply_basis': 'Eurostat sts_cobp_q dwellings authorised, quarterly index 2021=100, NSA, 117/117 present. '
                        'The supply axis and the glut warning rest on this SINGLE component: vacancy is null for '
                        'every quarter (Greece publishes tier-1 vacancy only in the 2011 and 2021 censuses). Read it '
                        'as a permits-flow reading, not as an inventory or empty-homes reading.',
        'supply_artefacts': '2005Q4 = 1505.0 is a VAT pull-forward (19% VAT on buildings permitted from 2006-01-01); '
                            '2025 is depressed by the suspension of the NOK floor-area/height bonuses (Dec 2024 - May '
                            '2025), so 2026Q1 +70.2% y/y sits on an artificial base. Neither may drive a glut flag '
                            'without comment. NSA: read YoY only.',
        'structure_axis_available': any(v is not None for v in X),
        'valuation_basis': 'price / income, where income = Eurostat household gross disposable income (B6G, S14_S15, '
                           'EUR m). No pti exists for Greece, and Greece is absent from Eurostat prc_hpi_q, so there '
                           'is no independent tier-1 cross-check on the BIS price series either.',
        'valuation_first_obs': first_q(val),
        'valuation_first_z': first_q(STRUCT['val']),
        'credit_last_obs': last_q(col('credit')),
        'price_last_obs': last_q(price),
        'current_complete_quarter': last_q(FLOW['credit']),  # last quarter with a credit reading; 2026Q1 is price-only
        'credit_note': 'BIS household credit lags BIS prices by one quarter and is NOT carried forward, so the flow / '
                       'credit reading is null at the final quarter by design. The series is ALL-LENDER (-32.3% from '
                       'the 2010Q3 peak) not banks-only (-68.6%): the gap is Hercules/HAPS securitisation, not repayment.',
        'rate_note': 'ECB deposit facility rate from 2001Q1 (drachma overnight call rate before, spliced at '
                     '2000Q4/2001Q1 with a -3.427pp step). Greece has no national policy rate; in 2010-2018 Greek '
                     'financial conditions were violently disconnected from it (10y yield peak 29.24% in Feb 2012 vs '
                     'a 1.00% policy rate), so the rate component of the money axis is unreliable across that decade '
                     'and must not be averaged over silently.',
        'cpi_note': 'Eurostat HICP (2025=100), NSA — not BIS\'s own deflator. The national CPI that IS BIS\'s deflator '
                    'is discontinued at 2025-04. Max level divergence 2.15% over 29 years. For "the BIS real house '
                    'price index" use FRED QGRR628BIS directly, never price/cpi from this file.',
        'pop_note': 'Eurostat quarterly national-accounts population — genuinely quarterly, but its within-year shape '
                    'is the compiler\'s interpolation of annual demography, so only YoY carries information. Diverges '
                    'from World Bank by 70-126k after 2021; do not mix the two in one chart.',
        'provisional_tail': 'The last four price quarters (2025Q2-2026Q1) are provisional (BoG flags its parallel '
                            'index as such and revises it); the most recent gdp, income and months are subject to '
                            'normal revision.',
        'drawdown_note': 'Real house prices (BIS QGRR628BIS): peak 2007Q3 = 119.53, trough 2017Q2 = 62.13, -48.0%; '
                         '2026Q1 = 96.98, still -18.9% below the 2007 peak. Nominal prices are +9.5% above their '
                         '2008Q3 peak — the nominal series used here does NOT show the crash the real series does.',
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
    # synthetic 1997Q1.. with a slow cycle in structure and a fast cycle in flow
    q = [f'{y}Q{qq}' for y in range(1997, 2027) for qq in range(1, 5)][:117]
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
        'unemp':  [10+4*math.sin(i/6.0+1) for i in range(n)],
        'rate':   [4+2*math.cos(i/8.0) for i in range(n)],
        'credit': [100*(1.05**(i/4))*(1+0.03*math.sin(i/7.0)) for i in range(n)],
        'pop':    [100*(1.002**(i/4)) for i in range(n)],
        'months': [200+80*math.sin(i/10.0) for i in range(n)],
        'vacancy':[None]*n,          # Greece's actual shape: supply from permits ONLY
        'pti':    [None]*n,
    }
    out = compute(raw, win=24)
    labels = {'expansion':'Primed·Expansion','base':'Base·Coiling','meltup':'Late·Melt-up','downturn':'Correction·Downturn'}
    fv = next((q[i] for i in range(n) if out['x'][i] is not None), None)
    print(f'selftest: {n} quarters {q[0]}..{q[-1]}; first reading {fv}; current {q[-1]} -> {labels.get(out["quad"][-1], out["quad"][-1])}')
    for k in ['expansion','base','meltup','downturn']:
        s = out['qstat'][k]; print(f'  {labels[k]:20} n={s["n"]:<3} med={s.get("med")} q1={s.get("q1")}')
    m = out['meta']
    print(f'  supply_available={m["supply_available"]} components={m["supply_components"]} '
          f'structure_axis_available={m["structure_axis_available"]}')
    assert any(v is not None for v in out['x']), 'no readings produced'
    assert set(out['quad']) - {'warmup'}, 'no corners assigned'
    # Greece-specific: supply must be live off `months` alone, with vacancy absent
    assert m['supply_available'] is True and m['supply_components'] == ['months'], \
        'supply axis must be live from months alone (vacancy is null for GR)'
    assert all(v is None for v in out['comps_struct']['vac']), 'vac must stay empty'
    assert any(v is not None for v in out['comps_struct']['months']), 'months z must be populated'
    print('selftest OK (incl. single-component supply path)')

def main():
    if '--selftest' in sys.argv:
        selftest(); return
    win = 24
    if '--win' in sys.argv: win = int(sys.argv[sys.argv.index('--win')+1])
    if not os.path.exists(INJSON):
        print(f'no input at {INJSON} — run --selftest, or place raw GR series there first'); sys.exit(1)
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
    print(f'  supply_available={m["supply_available"]} components={m["supply_components"]}  '
          f'structure_axis_available={m["structure_axis_available"]}')
    print(f'  valuation first obs {m["valuation_first_obs"]} / first z {m["valuation_first_z"]}; '
          f'credit last {m["credit_last_obs"]} vs price last {m["price_last_obs"]}')
    print(f'wrote {OUTJSON} ({len(compact)} bytes)')
    # Greece has NO market page (like AU and TH, unlike JP/TW/MY). This script never opens,
    # reads or writes any HTML — there is deliberately no injection path here at all.

if __name__ == '__main__':
    main()
