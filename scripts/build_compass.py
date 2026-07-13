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
"""
import json, os, math
import statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MKTS = ['us', 'tw', 'my', 'jp']

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
    out=[None]*len(a)
    for i in range(4,len(a)):
        if a[i] is not None and a[i-4] not in (None,0): out[i]=(a[i]/a[i-4]-1)*100
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

def compute(d, valsrc=None, supsrc=None, popyoy=None, xc=None, win=24):
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
    warn = [loose(i) for i in range(n)]

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
    return {
        'q': q, 'mom': r3(mom), 'cred': r3(cred), 'quad': QUAD, 'warn': warn,
        'ang': r1([ang(i) for i in range(n)]), 'rad': r3([rad(i) for i in range(n)]),
        'hpi_yoy': r1(hpi), 'fwd12': r1(fwd), 'qstat': QSTAT, 'card': card,
        'xc': xc,   # cross-country report-card layer (vs the world now); None if unavailable
    }

def main():
    RAWF = {'tw':'.twdata/tw_raw.json','my':'.mydata/my_raw.json','jp':'.jpdata/jp_raw.json'}
    XC = build_xc()
    for m in MKTS:
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
            popyoy = yoy(rw['pop']) if rw.get('pop') else None
        out = compute(d, valsrc, supsrc, popyoy, xc=XC.get(m))
        json.dump(out, open(os.path.join(ROOT, 'data', f'compass-{m}.json'), 'w'), separators=(',', ':'))
        i = len(out['q'])-1
        lab = {'fuelled':'上行·有燃料','draining':'上行·資金退','reflating':'下行·資金回流','starved':'下行·斷炊','warmup':'暖機'}
        print(f"{m.upper()}: {out['q'][i]} → {lab[out['quad'][i]]}  mom={out['mom'][i]} cred={out['cred'][i]} warn={out['warn'][i]}")

if __name__ == '__main__':
    main()
