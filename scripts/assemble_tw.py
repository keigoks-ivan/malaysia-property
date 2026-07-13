#!/usr/bin/env python3
"""Assemble tw_raw.json from the Sinyi price seed + the workflow's fetched gov series,
then it's ready for build_clock_tw.py. Reads the workflow return dumped to
scratchpad/tw_workflow_out.json (shape {axis:[...], results:[{key,available,q,v},...]})."""
import json, os

SCRATCH = '/private/tmp/claude-501/-Users-ivanchang-malaysia-property/52542b53-2f2a-49e2-9a78-6dd7a75141c7/scratchpad'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, 'scripts', '.twdata', 'tw_seed.json')
WF   = os.path.join(SCRATCH, 'tw_workflow_out.json')
OUT  = os.path.join(ROOT, 'scripts', '.twdata', 'tw_raw.json')

# workflow key -> tw_raw field
MAP = {
    'gdp_real': 'gdp', 'unemp': 'unemp', 'cpi': 'cpi', 'pop2554': 'pop', 'pti': 'pti',
    'credit_bal': 'credit', 'mortgage_rate': 'rate', 'lowuse': 'vacancy', 'completions': 'months',
}

def main():
    seed = json.load(open(SEED))
    qaxis = seed['q']
    raw = {'q': qaxis, 'price': seed['price']}
    got, missing = [], []

    if os.path.exists(WF):
        wf = json.load(open(WF))
        by = {r['key']: r for r in wf.get('results', []) if r}
    else:
        # fall back to per-key files agents may have written
        by = {}
        for k in MAP:
            p = os.path.join(SCRATCH, 'tw', k + '.json')
            if os.path.exists(p):
                try: by[k] = json.load(open(p))
                except Exception: pass

    for wkey, field in MAP.items():
        r = by.get(wkey)
        if not r or not r.get('available') or not r.get('v'):
            missing.append(wkey); continue
        q, v = r.get('q', []), r.get('v', [])
        idx = {qq: i for i, qq in enumerate(q)}
        aligned = [(v[idx[qq]] if qq in idx and idx[qq] < len(v) else None) for qq in qaxis]
        if sum(1 for x in aligned if x is not None) < 8:
            missing.append(wkey + '(too sparse)'); continue
        # low-frequency / lagged structural series (annual vacancy, quarterly-but-lagged PTI,
        # completions) get carried forward at most 4 quarters so the CURRENT quarter has a reading;
        # these move slowly within a year, so last-observation-carried-forward is defensible.
        if field in ('pti', 'vacancy', 'months'):
            lv = max((i for i, x in enumerate(aligned) if x is not None), default=-1)
            if lv >= 0:
                for j in range(lv + 1, min(len(aligned), lv + 1 + 4)):
                    aligned[j] = aligned[lv]
        raw[field] = aligned
        got.append(f'{field}<-{wkey}')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(raw, open(OUT, 'w'), ensure_ascii=False)
    print('assembled', OUT)
    print('  price 2001Q1..2026Q1  n=', len(qaxis))
    print('  got   :', ', '.join(got) if got else '(none)')
    print('  missing:', ', '.join(missing) if missing else '(none)')
    # quick coverage per field
    for f in ['gdp','unemp','cpi','pop','pti','credit','rate','vacancy','months']:
        if f in raw:
            nn = sum(1 for x in raw[f] if x is not None)
            first = next((qaxis[i] for i,x in enumerate(raw[f]) if x is not None), '-')
            print(f'    {f:8} n={nn:<3} from {first}')

if __name__ == '__main__':
    main()
