#!/usr/bin/env python3
"""
Build the Japan property clock (Structure x Flow) from raw quarterly series and inject
it into my/clock.html (Japan market block). Same five-force engine as the US pilot; only
the inputs differ, so the compute half is identical to build_clock_us.py.

INPUT: a JSON file of raw quarterly series (scripts/.jpdata/jp_raw.json), shape:
{
  "q":      ["1975Q1", ...],        # quarter labels, contiguous
  "price":  [ ... ],                # BIS Japan house-price index (level) -> judged + valuation numerator
  "pti":    [ ... ],                # not fetched for JP (no pti field; valuation falls back to price/income) [optional]
  "months": [ ... ],                # e-Stat/FRED housing starts (units, raw count) -> supply (low = tight)  [optional]
  "vacancy":[ ... ],                # 空き家率 (空屋率) — quinquennial Housing & Land Survey, held flat between releases -> supply (low = tight) [optional]
  "gap":    [ ... ],                # not fetched for JP (household formation - completions) [optional]
  "pop":    [ ... ],                # e-Stat/World Bank population (level) -> population (growth = +)   [optional]
  "credit": [ ... ],                # BOJ household housing-loan balance (level) -> money (real growth = +) [optional]
  "rate":   [ ... ],                # BOJ policy / mortgage rate % (nominal) -> money (real, easing = +)  [optional]
  "cpi":    [ ... ],                # e-Stat CPI index (level) -> deflator for credit & rate[optional]
  "gdp":    [ ... ],                # FRED/e-Stat real GDP (level) -> economy (YoY = +)         [optional]
  "unemp":  [ ... ],                # e-Stat unemployment rate % (level) -> economy (falling = +) [optional]
  "income": [ ... ]                 # e-Stat/FRED household income proxy (level, annual-held) -> economy (YoY = +); valuation denominator (no pti for JP)
}
Any series may be absent or contain nulls; a quarter needs >=3 of the components on each
axis to get a reading. Valuation uses `pti` if present, else price/income.

This market shares MY/TW's 6y (24q) trailing standardisation window (not the US's 10y
default), even though JP's own price history is long enough to support a wider one;
override with --win N.

Usage:
    python3 scripts/build_clock_jp.py                 # read .jpdata/jp_raw.json, write + inject
    python3 scripts/build_clock_jp.py --no-inject     # write data/clock-jp.json only
    python3 scripts/build_clock_jp.py --selftest      # run on synthetic data, no files needed
    python3 scripts/build_clock_jp.py --win 40        # use a 10y window (if history allows)
"""
import json, math, os, sys
import statistics as st

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INJSON  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.jpdata', 'jp_raw.json')
OUTJSON = os.path.join(ROOT, 'data', 'clock-jp.json')
PAGE    = os.path.join(ROOT, 'my', 'clock.html')
MARK_A, MARK_B = '/*CLOCK_JP_START*/', '/*CLOCK_JP_END*/'

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

    # valuation: pti if given, else price / real income
    if any(v is not None for v in col('pti')):
        val = col('pti')
    else:
        val = [(price[i]/income[i]) if (price[i] and income[i]) else None for i in range(n)]

    STRUCT = {
        'months': czlist(col('months'), -1, win),                    # supply: low = tight = +
        'vac':    czlist(col('vacancy'), -1, win),                   # supply: low vacancy = +
        'gap':    czlist(col('gap'),     +1, win),                   # demand: under-built = +
        'demo':   absz(yoy(col('pop')), 0.7, +1),                   # population: growth = +
        'val':    czlist(val,            -1, win),                   # valuation: cheap = +
    }
    FLOW = {
        'credit': czlist(yoy(real(col('credit'), cpi)), +1, win),    # money: real credit impulse
        'rate':   czlist([(col('rate')[i]-yoy(cpi)[i]) if (col('rate')[i] is not None and yoy(cpi)[i] is not None) else None
                          for i in range(n)], -1, win),              # money: real rate, easing = +
        'gdp':    czlist(yoy(col('gdp')),   +1, win),                # economy: growth
        'jobs':   czlist(col('unemp'),      -1, win),                # economy: falling unemployment = +
        'income': czlist(yoy(income),       +1, win),               # economy: real income
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

    return {
        'q': q, 'x': r3(X), 'y': r3(Y), 'quad': QUAD,
        'ang': r1([ang(i) for i in range(n)]), 'rad': r3([rad(i) for i in range(n)]),
        'hpi_yoy': r1(hpi_yoy), 'fwd12': r1(FWD),
        'comps_struct': {k: r2(v) for k, v in STRUCT.items()},
        'comps_flow':   {k: r2(v) for k, v in FLOW.items()},
        'raw': {'val': r2(val)},
        'qstat': QSTAT,
        'win': win,
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
    print('selftest OK')

def main():
    if '--selftest' in sys.argv:
        selftest(); return
    win = 24
    if '--win' in sys.argv: win = int(sys.argv[sys.argv.index('--win')+1])
    if not os.path.exists(INJSON):
        print(f'no input at {INJSON} — run --selftest, or place raw TW series there first'); sys.exit(1)
    raw = json.load(open(INJSON))
    out = compute(raw, win)
    compact = json.dumps(out, separators=(',', ':'))
    os.makedirs(os.path.dirname(OUTJSON), exist_ok=True)
    open(OUTJSON, 'w').write(compact)
    labels = {'expansion':'Primed·Expansion','base':'Base·Coiling','meltup':'Late·Melt-up','downturn':'Correction·Downturn'}
    print(f'quarters {out["q"][0]}..{out["q"][-1]}  current -> {labels.get(out["quad"][-1], out["quad"][-1])}  (win={win})')
    for k in ['expansion','base','meltup','downturn']:
        s = out['qstat'][k]; print(f'  {labels[k]:20} n={s["n"]:<3} med={s.get("med")} q1={s.get("q1")}')
    print(f'wrote {OUTJSON} ({len(compact)} bytes)')
    if '--no-inject' not in sys.argv:
        h = open(PAGE, encoding='utf-8').read()
        if MARK_A in h and MARK_B in h:
            import re
            h = re.sub(re.escape(MARK_A)+'.*?'+re.escape(MARK_B),
                       MARK_A+'var D_JP = '+compact+';'+MARK_B, h, count=1, flags=re.S)
            open(PAGE, 'w', encoding='utf-8').write(h)
            print(f'injected into {PAGE}')
        else:
            print('TW markers not yet in page; wrote JSON only (add toggle first)')

if __name__ == '__main__':
    main()
