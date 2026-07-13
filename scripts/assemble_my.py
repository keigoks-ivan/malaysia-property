#!/usr/bin/env python3
"""Assemble my_raw.json from the BIS price seed + the workflow's fetched MY series,
ready for build_clock_my.py. Axis is the workflow axis (2000Q1–2026Q1); BIS price
(1988–2026) is aligned onto it."""
import json, os

SCRATCH = '/private/tmp/claude-501/-Users-ivanchang-malaysia-property/52542b53-2f2a-49e2-9a78-6dd7a75141c7/scratchpad'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, 'scripts', '.mydata', 'my_seed.json')
WF   = os.path.join(SCRATCH, 'my_workflow_out.json')
OUT  = os.path.join(ROOT, 'scripts', '.mydata', 'my_raw.json')

MAP = {  # workflow key -> my_raw field
    'gdp_real': 'gdp', 'unemp': 'unemp', 'cpi': 'cpi', 'pop': 'pop', 'income': 'income',
    'credit': 'credit', 'rate': 'rate', 'overhang': 'vacancy', 'completions': 'months',
}

def main():
    seed = json.load(open(SEED))
    seed_price = dict(zip(seed['q'], seed['price']))

    if os.path.exists(WF):
        wf = json.load(open(WF)); qaxis = wf['axis']; by = {r['key']: r for r in wf.get('results', []) if r}
    else:
        qaxis = [f'{y}Q{q}' for y in range(2000, 2027) for q in range(1, 5)]
        qaxis = qaxis[:qaxis.index('2026Q1') + 1]
        by = {}
        for k in MAP:
            p = os.path.join(SCRATCH, 'my', k + '.json')
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
        if sum(1 for x in aligned if x is not None) < 8:
            missing.append(wkey + '(sparse)'); continue
        if field in ('vacancy', 'months', 'income', 'pop', 'credit'):   # low-freq / lagged -> carry forward <=4q
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
