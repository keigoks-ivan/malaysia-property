#!/usr/bin/env python3
"""
Build the US property clock (Structure x Flow, five forces) and inject it into my/clock.html.

Five forces -> two axes, all real FRED series, quarterly 1975Q1-latest:
  X = Structure (slow):  supply (months-supply, vacancy) + demand (formation - completions)
                         + population (prime-age 25-54 growth) + valuation (price / real income)
  Y = Flow (fast):       money (real mortgage-credit impulse, real 30y rate)
                         + economy (real GDP, unemployment, real disposable income)

Each input -> causal robust z over a TRAILING 10y window (de-trends secular drift, no look-ahead).
Axes = mean of components, lightly 3q-smoothed. Corner = sign(X) x sign(Y).

Usage:
    python3 scripts/build_clock_us.py            # fetch fresh FRED, write data + inject page
    python3 scripts/build_clock_us.py --no-inject  # only write data/clock-us.json
    python3 scripts/build_clock_us.py --offline    # reuse cached CSVs in scripts/.fredcache

Quarterly refresh: just run it. It rewrites data/clock-us.json and the embedded block in
my/clock.html (between the CLOCK_DATA_START / CLOCK_DATA_END markers).
"""
import csv, json, math, os, re, sys, io
import statistics as st
import urllib.request
from collections import OrderedDict

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.fredcache')
PAGE   = os.path.join(ROOT, 'my', 'clock.html')
OUTJSON= os.path.join(ROOT, 'data', 'clock-us.json')

SERIES = ['UNRATE','GDPC1','DPIC96','LNU00000060','MSACSR','RHVRUSQ156N','HHMSDODNS',
          'MORTGAGE30US','CPIAUCSL','USSTHPI','COMPUTSA','TTLHH','HSN1F']

def fetch(series_id, offline=False):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, series_id + '.csv')
    if offline and os.path.exists(path):
        return open(path, encoding='utf-8').read()
    if not offline:
        url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=' + series_id
        req = urllib.request.Request(url, headers={'User-Agent':'clock-builder/1.0'})
        data = urllib.request.urlopen(req, timeout=60).read().decode('utf-8')
        open(path, 'w', encoding='utf-8').write(data)
        return data
    return open(path, encoding='utf-8').read()

def parse(text):
    out = OrderedDict()
    r = csv.reader(io.StringIO(text)); next(r, None)
    for row in r:
        if len(row) < 2 or row[1] in ('.', '', 'NA'):
            continue
        try: out[row[0]] = float(row[1])
        except ValueError: pass
    return out

def to_q(monthly, how='mean'):
    buck = {}
    for d, v in monthly.items():
        y, m, _ = d.split('-'); q = (int(m)-1)//3+1
        buck.setdefault(f'{y}Q{q}', []).append((int(m), v))
    out = {}
    for k, lst in buck.items():
        lst.sort()
        out[k] = (sum(v for _, v in lst)/len(lst)) if how == 'mean' else lst[-1][1]
    return out

def q_from_qtr(qd):
    out = {}
    for d, v in qd.items():
        y, m, _ = d.split('-'); q = (int(m)-1)//3+1; out[f'{y}Q{q}'] = v
    return out

def main():
    offline  = '--offline' in sys.argv
    inject   = '--no-inject' not in sys.argv

    raw = {sid: parse(fetch(sid, offline)) for sid in SERIES}

    # quarter axis 1975Q1 .. last quarter present in USSTHPI
    last = q_from_qtr(raw['USSTHPI'])
    def qkey(k): y, q = k.split('Q'); return (int(y), int(q))
    end_y, end_q = qkey(sorted(last, key=qkey)[-1])
    QS = []
    for y in range(1975, end_y+1):
        for q in range(1, 5):
            QS.append(f'{y}Q{q}')
            if y == end_y and q == end_q: break
        if y == end_y: break
    def series(d): return [d.get(q) for q in QS]

    unrate = to_q(raw['UNRATE'], 'mean');  gdp = q_from_qtr(raw['GDPC1'])
    rdpi   = q_from_qtr(raw['DPIC96']);    pop = to_q(raw['LNU00000060'], 'mean')
    months = to_q(raw['MSACSR'], 'mean');  vac = q_from_qtr(raw['RHVRUSQ156N'])
    mort   = q_from_qtr(raw['HHMSDODNS']); rate30 = to_q(raw['MORTGAGE30US'], 'mean')
    cpi    = to_q(raw['CPIAUCSL'], 'mean');hpi = q_from_qtr(raw['USSTHPI'])
    compl  = to_q(raw['COMPUTSA'], 'mean');sales = to_q(raw['HSN1F'], 'mean')
    hh_annual = {int(d[:4]): v for d, v in raw['TTLHH'].items()}

    def hh_q(q):
        y = int(q[:4]); frac = (int(q[-1])-1)/4.0
        a = hh_annual.get(y); b = hh_annual.get(y+1)
        if a is None: return None
        if b is None: b = a
        return a + (b-a)*frac
    households = [hh_q(q) for q in QS]

    def yoy(lst):
        out = [None]*len(lst)
        for i in range(4, len(lst)):
            a, b = lst[i-4], lst[i]
            if a not in (None, 0) and b is not None: out[i] = (b/a-1)*100
        return out

    S = {}
    S['hpi'] = series(hpi);     S['hpi_yoy'] = yoy(S['hpi'])
    S['cpi'] = series(cpi);     S['cpi_yoy'] = yoy(S['cpi'])
    S['unrate'] = series(unrate)
    S['gdp'] = series(gdp);     S['gdp_yoy'] = yoy(S['gdp'])
    S['rdpi'] = series(rdpi);   S['rdpi_yoy'] = yoy(S['rdpi'])
    S['pop'] = series(pop);     S['pop_yoy'] = yoy(S['pop'])
    S['months'] = series(months); S['vac'] = series(vac)
    S['rate30'] = series(rate30); S['compl'] = series(compl)
    S['sales'] = series(sales); S['sales_yoy'] = yoy(S['sales'])
    S['hh'] = households

    real_mort = [(m/c if (m and c) else None) for m, c in zip(series(mort), S['cpi'])]
    S['credit_real_yoy'] = yoy(real_mort)
    S['real_rate'] = [(S['rate30'][i]-S['cpi_yoy'][i]) if (S['rate30'][i] is not None and S['cpi_yoy'][i] is not None) else None
                      for i in range(len(QS))]
    form = [None]*len(QS)
    for i in range(4, len(QS)):
        if households[i] is not None and households[i-4] is not None:
            form[i] = households[i]-households[i-4]
    S['formation'] = form
    S['gap'] = [(form[i]-S['compl'][i]) if (form[i] is not None and S['compl'][i] is not None) else None
                for i in range(len(QS))]
    S['val'] = [(S['hpi'][i]/S['rdpi'][i]*1000) if (S['hpi'][i] and S['rdpi'][i]) else None
                for i in range(len(QS))]

    # causal robust z over trailing window (win=40q, min 16 obs)
    def czlist(vals, sign=1, win=40, minobs=16):
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

    FLOW = OrderedDict([
        ('credit', czlist(S['credit_real_yoy'], +1)),
        ('rate',   czlist(S['real_rate'],       -1)),
        ('gdp',    czlist(S['gdp_yoy'],          +1)),
        ('jobs',   czlist(S['unrate'],           -1)),
        ('income', czlist(S['rdpi_yoy'],         +1)),
    ])
    STRUCT = OrderedDict([
        ('months', czlist(S['months'], -1)),
        ('vac',    czlist(S['vac'],    -1)),
        ('gap',    czlist(S['gap'],    +1)),
        ('demo',   czlist(S['pop_yoy'],+1)),
        ('val',    czlist(S['val'],    -1)),
    ])

    def blend(comps):
        out = [None]*len(QS)
        for i in range(len(QS)):
            vals = [c[i] for c in comps.values() if c[i] is not None]
            if len(vals) >= 3: out[i] = sum(vals)/len(vals)
        return out

    Xr, Yr = blend(STRUCT), blend(FLOW)
    def smooth(a, w=3):
        out = [None]*len(a)
        for i in range(len(a)):
            seg = [a[j] for j in range(max(0, i-w+1), i+1) if a[j] is not None]
            if seg and a[i] is not None: out[i] = sum(seg)/len(seg)
        return out
    X, Y = smooth(Xr), smooth(Yr)

    def quad(i):
        if X[i] is None or Y[i] is None: return 'warmup'
        hi, up = X[i] >= 0, Y[i] >= 0
        return 'expansion' if (hi and up) else 'base' if (hi and not up) else 'meltup' if up else 'downturn'
    QUAD = [quad(i) for i in range(len(QS))]

    def fwd12(i):
        if i+12 >= len(QS): return None
        a, b = S['hpi'][i], S['hpi'][i+12]
        return (b/a-1)*100 if (a and b) else None
    FWD = [fwd12(i) for i in range(len(QS))]

    def stats(name):
        v = [FWD[i] for i in range(len(QS)) if QUAD[i] == name and FWD[i] is not None]
        if not v: return {'n': 0}
        sv = sorted(v)
        return {'n': len(v), 'med': round(st.median(v), 1), 'mn': round(min(v), 1),
                'mx': round(max(v), 1), 'q1': round(sv[len(sv)//4], 1)}
    QSTAT = {k: stats(k) for k in ['expansion', 'base', 'meltup', 'downturn']}

    def ang(i):
        return None if (X[i] is None or Y[i] is None) else math.degrees(math.atan2(Y[i], X[i]))
    def rad(i):
        return None if (X[i] is None or Y[i] is None) else math.hypot(X[i], Y[i])
    def r3(a): return [round(v, 3) if v is not None else None for v in a]
    def r1(a): return [round(v, 1) if v is not None else None for v in a]
    def r2(a): return [round(v, 2) if v is not None else None for v in a]

    out = {
        'q': QS, 'x': r3(X), 'y': r3(Y), 'quad': QUAD,
        'ang': r1([ang(i) for i in range(len(QS))]), 'rad': r3([rad(i) for i in range(len(QS))]),
        'hpi_yoy': r1(S['hpi_yoy']), 'fwd12': r1(FWD),
        'comps_struct': {k: r2(c) for k, c in STRUCT.items()},
        'comps_flow':   {k: r2(c) for k, c in FLOW.items()},
        'raw': {k: r2(S[k]) for k in ['months','vac','gap','pop_yoy','val','credit_real_yoy',
                                      'real_rate','gdp_yoy','unrate','rdpi_yoy','sales_yoy']},
        'qstat': QSTAT,
    }
    compact = json.dumps(out, separators=(',', ':'))
    os.makedirs(os.path.dirname(OUTJSON), exist_ok=True)
    open(OUTJSON, 'w').write(compact)

    labels = {'expansion':'Primed·Expansion','base':'Base·Coiling',
              'meltup':'Late·Melt-up','downturn':'Correction·Downturn'}
    print(f'quarters: {QS[0]}..{QS[-1]}  (n={len(QS)})')
    print(f'current {QS[-1]}: {labels[QUAD[-1]]}  X={X[-1]:+.2f}  Y={Y[-1]:+.2f}')
    for k in ['expansion','base','meltup','downturn']:
        s = QSTAT[k]
        print(f'  {labels[k]:20} n={s["n"]:<3} med={s.get("med")}  q1={s.get("q1")}  '
              f'range={s.get("mn")}..{s.get("mx")}')
    print(f'wrote {OUTJSON} ({len(compact)} bytes)')

    if inject:
        h = open(PAGE, encoding='utf-8').read()
        if 'CLOCK_DATA_START' not in h:
            print('WARNING: markers not found in page; skipping injection'); return
        h = re.sub(r'/\*CLOCK_DATA_START\*/.*?/\*CLOCK_DATA_END\*/',
                   '/*CLOCK_DATA_START*/var D_US = ' + compact + ';/*CLOCK_DATA_END*/', h, count=1, flags=re.S)
        open(PAGE, 'w', encoding='utf-8').write(h)
        print(f'injected into {PAGE}')

if __name__ == '__main__':
    main()
