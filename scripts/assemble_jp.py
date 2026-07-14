#!/usr/bin/env python3
"""Assemble jp_raw.json from the BIS price seed + the workflow's fetched JP series.
Axis 1975Q1-2025Q4. `interp()` linearly interpolates internal None gaps for the
low-frequency fields (vacancy, income) IF the fetched series has any such gaps.
In practice, on the data this pipeline actually receives, the fetch workflow already
returns every quarter pre-filled (e.g. vacancy arrives as a step, holding each
5-yearly survey reading flat across the quarters until the next release), so
interp() is a no-op here — it does not turn the step into a ramp. Separately, several
lagged fields (vacancy/months/income/pop/credit/cpi) get a <=4-quarter carry-forward
at the tail, past their last real observation."""
import json, os

SCRATCH = '/private/tmp/claude-501/-Users-ivanchang-malaysia-property/52542b53-2f2a-49e2-9a78-6dd7a75141c7/scratchpad'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, 'scripts', '.jpdata', 'jp_seed.json')
WF   = os.path.join(SCRATCH, 'jp_workflow_out.json')
OUT  = os.path.join(ROOT, 'scripts', '.jpdata', 'jp_raw.json')

MAP = {  # workflow key -> jp_raw field
    'gdp_real': 'gdp', 'unemp': 'unemp', 'cpi': 'cpi', 'pop': 'pop', 'income': 'income',
    'credit': 'credit', 'rate': 'rate', 'starts': 'months', 'vacancy': 'vacancy',
}

def interp(a):
    """linear-interpolate internal None gaps between known points (leaves leading/trailing None)."""
    idx = [i for i, x in enumerate(a) if x is not None]
    if len(idx) < 2: return a[:]
    out = a[:]
    for k in range(len(idx) - 1):
        i0, i1 = idx[k], idx[k + 1]
        if i1 == i0 + 1: continue
        for j in range(i0 + 1, i1):
            out[j] = a[i0] + (a[i1] - a[i0]) * (j - i0) / (i1 - i0)
    return out

def main():
    seed = json.load(open(SEED)); seed_price = dict(zip(seed['q'], seed['price']))
    if os.path.exists(WF):
        wf = json.load(open(WF)); qaxis = wf['axis']; by = {r['key']: r for r in wf.get('results', []) if r}
    else:
        qaxis = [f'{y}Q{q}' for y in range(1975, 2026) for q in range(1, 5)]
        by = {}
        for k in MAP:
            p = os.path.join(SCRATCH, 'jp', k + '.json')
            if os.path.exists(p):
                try: by[k] = json.load(open(p))
                except Exception: pass

    raw = {'q': qaxis, 'price': [seed_price.get(qq) for qq in qaxis]}
    got, missing = [], []
    for wkey, field in MAP.items():
        r = by.get(wkey)
        if not r or not r.get('available') or not r.get('v'):
            missing.append(wkey); continue
        idx = {qq: i for i, qq in enumerate(r.get('q', []))}
        v = r.get('v', [])
        aligned = [(v[idx[qq]] if qq in idx and idx[qq] < len(v) else None) for qq in qaxis]
        if field in ('vacancy', 'income'):      # low-frequency -> interpolate internal gaps
            aligned = interp(aligned)
        if sum(1 for x in aligned if x is not None) < 8:
            missing.append(wkey + '(sparse)'); continue
        if field in ('vacancy', 'months', 'income', 'pop', 'credit', 'cpi'):  # lagged -> carry forward <=4q
            lv = max((i for i, x in enumerate(aligned) if x is not None), default=-1)
            if lv >= 0:
                for j in range(lv + 1, min(len(aligned), lv + 1 + 4)): aligned[j] = aligned[lv]
        raw[field] = aligned; got.append(f'{field}<-{wkey}')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(raw, open(OUT, 'w'), ensure_ascii=False)
    print('assembled', OUT, '| axis', qaxis[0], '..', qaxis[-1], 'n=', len(qaxis))
    print('  price non-null:', sum(1 for x in raw['price'] if x is not None))
    print('  got   :', ', '.join(got) if got else '(none)')
    print('  missing:', ', '.join(missing) if missing else '(none)')
    for f in ['gdp','unemp','cpi','pop','income','credit','rate','vacancy','months']:
        if f in raw:
            nn = sum(1 for x in raw[f] if x is not None)
            first = next((qaxis[i] for i,x in enumerate(raw[f]) if x is not None), '-')
            print(f'    {f:8} n={nn:<3} from {first}')

if __name__ == '__main__':
    main()
