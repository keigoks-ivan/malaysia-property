#!/usr/bin/env python3
"""
Test 8 backtest: does the Compass (momentum x credit, four cells) rank forward
3-year house-price returns in the declared order?

Declared ahead of looking at outcomes (theory, not a fit):
    Fuelled >= Draining >= Reflating >= Starved

Reads the compass engine's own already-computed output (data/compass-<m>.json,
built by scripts/build_compass.py) — no raw series are re-fetched or recomputed
here. Two measurements per market:

  1. Cell medians + n, taken directly from qstat (realized 3y-forward return
     distribution per cell, full history). Compared pairwise against the
     6 declared inequalities (C(4,2)) to get a concordance score.
  2. Spearman rank correlation between each quarter's declared-cell-rank
     (fuelled=4 best .. starved=1 worst) and that quarter's realized fwd12,
     over every quarter with non-null fwd12 (warmup quarters excluded).

Also freezes each market's current (last non-null) cell for the 2026 forward
check, per the page's existing v2-freeze convention.

No external fetch. Standard library only (manual Spearman, no scipy dependency).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MKTS = ['us', 'tw', 'my', 'jp', 'au']
CELLS = ['fuelled', 'draining', 'reflating', 'starved']
DECLARED_RANK = {'fuelled': 4, 'draining': 3, 'reflating': 2, 'starved': 1}
PAIRS = [('fuelled', 'draining'), ('fuelled', 'reflating'), ('fuelled', 'starved'),
         ('draining', 'reflating'), ('draining', 'starved'), ('reflating', 'starved')]


def spearman(x, y):
    """Manual Spearman rank correlation with average ranks for ties. Returns (rho, n)."""
    n = len(x)
    if n < 3:
        return None, n

    def ranks(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and a[order[j + 1]] == a[order[i]]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg_rank
            i = j + 1
        return r

    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    vx = sum((v - mx) ** 2 for v in rx)
    vy = sum((v - my) ** 2 for v in ry)
    if vx == 0 or vy == 0:
        return None, n
    rho = cov / (vx ** 0.5 * vy ** 0.5)
    return round(rho, 3), n


def add_quarters(qstr, nq):
    """qstr like '2026Q1' + nq quarters -> 'YYYYQx'."""
    y, q = int(qstr[:4]), int(qstr[5])
    total = (y * 4 + (q - 1)) + nq
    ny, nq2 = divmod(total, 4)
    return f"{ny}Q{nq2 + 1}"


def analyze(mkt):
    d = json.load(open(os.path.join(ROOT, 'data', f'compass-{mkt}.json')))
    qstat = d['qstat']
    medians = {c: qstat[c]['med'] for c in CELLS}
    ns = {c: qstat[c]['n'] for c in CELLS}

    # pairwise concordance vs declared ordering
    concordant = 0
    pair_detail = []
    for a, b in PAIRS:
        ok = medians[a] > medians[b]
        concordant += 1 if ok else 0
        pair_detail.append((a, b, ok, medians[a], medians[b]))

    starved_is_min = medians['starved'] == min(medians.values())
    fuelled_is_max = medians['fuelled'] == max(medians.values())

    # quarter-level Spearman: declared rank vs realized fwd12
    xs, ys = [], []
    for i in range(len(d['q'])):
        cq = d['quad'][i]
        fv = d['fwd12'][i]
        if cq in DECLARED_RANK and fv is not None:
            xs.append(DECLARED_RANK[cq])
            ys.append(fv)
    rho, n_scored = spearman(xs, ys)

    # Primary verdict criterion is the quarter-level rho (the agreement measure),
    # not the cell-median concordance (which is coarser and more ties-prone).
    # Thresholds fixed before reading market-by-market results: rho>=0.3 holds,
    # 0.1-0.3 weak, <0.1 breaks.
    if rho is not None and rho >= 0.3:
        verdict = 'HOLDS'
    elif rho is not None and rho >= 0.1:
        verdict = 'WEAK'
    else:
        verdict = 'BREAKS'

    # 2026 freeze: last quarter with a defined (non-warmup) cell
    last_i = len(d['q']) - 1
    frozen = {
        'quarter': d['q'][last_i], 'cell': d['quad'][last_i],
        'mom': d['mom'][last_i], 'cred': d['cred'][last_i],
        'checkable': add_quarters(d['q'][last_i], 12),
    }

    return {
        'mkt': mkt, 'medians': medians, 'ns': ns, 'pair_detail': pair_detail,
        'concordant': concordant, 'starved_is_min': starved_is_min,
        'fuelled_is_max': fuelled_is_max, 'rho': rho, 'n_scored': n_scored,
        'verdict': verdict, 'frozen': frozen,
    }


def main():
    results = {}
    print("Test 8 — Compass backtest: declared ordering Fuelled >= Draining >= Reflating >= Starved\n")
    for m in MKTS:
        r = analyze(m)
        results[m] = r
        print(f"=== {m.upper()} ===")
        for c in CELLS:
            print(f"  {c:10s} med={r['medians'][c]:>6}%  n={r['ns'][c]}")
        print(f"  pairwise concordance: {r['concordant']}/6")
        for a, b, ok, va, vb in r['pair_detail']:
            mark = 'OK' if ok else 'X '
            print(f"    [{mark}] {a}({va}) > {b}({vb})")
        print(f"  starved = min cell: {r['starved_is_min']}   fuelled = max cell: {r['fuelled_is_max']}")
        print(f"  quarter-level Spearman rho (declared rank vs realized fwd12): {r['rho']}  (n={r['n_scored']})")
        print(f"  VERDICT: {r['verdict']}")
        f = r['frozen']
        print(f"  2026 freeze: {f['quarter']} = {f['cell']}  (mom={f['mom']}, cred={f['cred']})  checkable {f['checkable']}")
        print()

    print("=== Summary ===")
    for m in MKTS:
        r = results[m]
        print(f"  {m.upper():3s}  concordance {r['concordant']}/6  rho={r['rho']:>6}  verdict={r['verdict']:8s}  frozen={r['frozen']['cell']} as of {r['frozen']['quarter']}")


if __name__ == '__main__':
    main()
