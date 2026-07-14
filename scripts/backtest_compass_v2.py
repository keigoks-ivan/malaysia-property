#!/usr/bin/env python3
"""
Compass v2 predictive-upgrade evaluation harness.

Implements scripts/compass_v2_protocol.md LITERALLY (frozen 2026-07-14, before
any evaluation run). Zero design discretion here: formulas, constants, metrics
and thresholds all come from the protocol file. Where anything below and the
protocol disagree, the protocol wins — this file should be read alongside it.

Candidates (all trailing-only, data <= t):
  baseline : DECLARED_RANK[quad]                          (fuelled=4..starved=1)
  C1       : S1 = mom + 0.5*cred
  C2       : S2 = S1 + 0.5*(cred[t] - cred[t-2])           (null if t-2 missing)
  C4       : S4 = S1 - 0.5*(1 if warn[t] else 0)
  C3       : S3 = vol_z + 0.5*cred   (TW always attempted; MY only if a volume
             file exists) -- vol_z = smooth(tz(vol_yoy, win=24), 3), tz/smooth
             copied EXACTLY from scripts/build_compass.py.

No external fetch. Standard library only (manual Spearman, reusing the exact
convention from scripts/backtest_compass.py -- average ranks for ties).

Does NOT edit any page, any compass pipeline file, or data/compass-*.json.
Writes only data/compass-backtest-v2.json.
"""
import json, os, statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MKTS = ['us', 'tw', 'my', 'jp']
DECLARED_RANK = {'fuelled': 4, 'draining': 3, 'reflating': 2, 'starved': 1}
TIE_ORDER = ['baseline', 'C1', 'C4', 'C2', 'C3']  # simpler candidate wins ties

TEST8_BASELINE = {'us': 0.58, 'tw': 0.081, 'my': 0.71, 'jp': 0.40}

VOLUME_FILES = {
    'tw': os.path.join(ROOT, 'scripts', '.twdata', 'tw_volume.json'),
    'my': os.path.join(ROOT, 'scripts', '.mydata', 'my_volume.json'),
}

OVERLAP_CAVEAT = (
    "Overlap robustness: forward windows overlap (serial correlation inflates n). "
    "Report ρ on non-overlapping subsamples: every 12th quarter at offsets "
    "{0,4,8}, median of the offsets, with per-offset n. Small-n caveat printed."
)
CONTAMINATION_NOTE = (
    "Test 8's full-sample cell medians for all four markets are already published; "
    "no design after 2026-07-13 is blind to them. Mitigation: the candidate set is "
    "closed at these four, every formula and constant is fixed above, and the "
    "walk-forward selection uses only matured (information-lagged) data at each date."
)
AMENDMENT1_TIMING_DISCLOSURE = (
    "Timing disclosure: this amendment was written after seeing the first run FAIL "
    "under the original metric (US delta −0.13). The reader can judge both numbers."
)


# ---------------------------------------------------------------------------
# Manual Spearman -- identical convention to scripts/backtest_compass.py
# ---------------------------------------------------------------------------
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


def paired(xs, ys):
    """Filter to indices where both series are non-null."""
    x2, y2 = [], []
    for a, b in zip(xs, ys):
        if a is not None and b is not None:
            x2.append(a)
            y2.append(b)
    return x2, y2


# ---------------------------------------------------------------------------
# tz() / smooth() / yoy() -- copied EXACTLY from scripts/build_compass.py
# ---------------------------------------------------------------------------
def tz(series, win=24, minobs=12):
    out = [None] * len(series); h = []
    for i, v in enumerate(series):
        if v is not None:
            h.append(v)
            if len(h) > win: h.pop(0)
        if v is None or len(h) < minobs: continue
        m = st.median(h); mad = st.median([abs(x - m) for x in h]) or 1e-9
        out[i] = max(-3, min(3, (v - m) / (1.4826 * mad)))
    return out


def smooth(a, w=3):
    out = [None] * len(a)
    for i in range(len(a)):
        seg = [a[j] for j in range(max(0, i - w + 1), i + 1) if a[j] is not None]
        if seg and a[i] is not None: out[i] = sum(seg) / len(seg)
    return out


def yoy(a):
    out = [None] * len(a)
    for i in range(4, len(a)):
        if a[i] is not None and a[i - 4] not in (None, 0): out[i] = (a[i] / a[i - 4] - 1) * 100
    return out


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_market(mkt):
    d = json.load(open(os.path.join(ROOT, 'data', f'compass-{mkt}.json')))
    return {
        'q': d['q'], 'mom': d['mom'], 'cred': d['cred'], 'warn': d['warn'],
        'quad': d['quad'], 'fwd12': d['fwd12'], 'n': len(d['q']),
    }


def load_volume(mkt):
    """C3 sticky-market volume input. Returns quarter->vol_z dict, or None if unavailable."""
    path = VOLUME_FILES.get(mkt)
    if not path or not os.path.exists(path):
        return None
    v = json.load(open(path))
    if 'q' not in v or 'vol' not in v:
        return None
    vol_yoy = yoy(v['vol'])
    vol_z = smooth(tz(vol_yoy, win=24), 3)
    return dict(zip(v['q'], vol_z))


# ---------------------------------------------------------------------------
# Candidate scores
# ---------------------------------------------------------------------------
def compute_candidates(d, vol_z_by_q=None):
    n = d['n']
    mom, cred, warn, quad = d['mom'], d['cred'], d['warn'], d['quad']

    S0 = [DECLARED_RANK.get(quad[i]) for i in range(n)]

    S1 = [None] * n
    for i in range(n):
        if mom[i] is not None and cred[i] is not None:
            S1[i] = mom[i] + 0.5 * cred[i]

    S2 = [None] * n
    for i in range(n):
        if S1[i] is None or i - 2 < 0: continue
        c_t, c_t2 = cred[i], cred[i - 2]
        if c_t is None or c_t2 is None: continue
        S2[i] = S1[i] + 0.5 * (c_t - c_t2)

    S4 = [None] * n
    for i in range(n):
        if S1[i] is None: continue
        S4[i] = S1[i] - 0.5 * (1 if warn[i] else 0)

    cand = {'baseline': S0, 'C1': S1, 'C2': S2, 'C4': S4}

    if vol_z_by_q is not None:
        S3 = [None] * n
        for i in range(n):
            vz = vol_z_by_q.get(d['q'][i])  # aligned by quarter LABEL, not index
            c = cred[i]
            if vz is None or c is None: continue
            S3[i] = vz + 0.5 * c
        cand['C3'] = S3

    return cand


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def full_period(scores, fwd12):
    x, y = paired(scores, fwd12)
    rho, n = spearman(x, y)
    return {'rho': rho, 'n': n}


def overlap_robustness(scores, fwd12, n):
    per_offset = {}
    for offset in (0, 4, 8):
        idx = list(range(offset, n, 12))
        xs, ys = paired([scores[i] for i in idx], [fwd12[i] for i in idx])
        rho, cnt = spearman(xs, ys)
        per_offset[offset] = {'rho': rho, 'n': cnt, 'small_n_caveat': cnt < 10}
    rhos = [v['rho'] for v in per_offset.values() if v['rho'] is not None]
    median_rho = round(st.median(rhos), 3) if rhos else None
    return {'per_offset': per_offset, 'median_rho': median_rho}


def decade_of(qlabel):
    y = int(qlabel[:4])
    return f"{(y // 10) * 10}s"


def decade_consistency(qs, scores, fwd12):
    buckets = {}
    for i, ql in enumerate(qs):
        if scores[i] is None or fwd12[i] is None: continue
        dec = decade_of(ql)
        buckets.setdefault(dec, {'x': [], 'y': []})
        buckets[dec]['x'].append(scores[i])
        buckets[dec]['y'].append(fwd12[i])
    out = {}
    for dec in sorted(buckets):
        xy = buckets[dec]
        if len(xy['x']) >= 8:
            rho, n = spearman(xy['x'], xy['y'])
            out[dec] = {'rho': rho, 'n': n}
    pos = sum(1 for v in out.values() if v['rho'] is not None and v['rho'] > 0)
    total = sum(1 for v in out.values() if v['rho'] is not None)
    return {'by_decade': out, 'positive_decades': pos, 'total_decades': total}


def midrank_percentile(v, pool_vals):
    """Percentile of v within pool_vals, midrank convention (protocol Amendment 1, metric
    v2.1): (count_less + 0.5*count_equal) / len(pool_vals). pool_vals are matured
    common-set values at the selection date -> no look-ahead."""
    if v is None or not pool_vals:
        return None
    less = sum(1 for u in pool_vals if u < v)
    equal = sum(1 for u in pool_vals if u == v)
    return (less + 0.5 * equal) / len(pool_vals)


def walk_forward(d, cand, pool_names):
    """Protocol Evaluation.4 -- expanding window, matured-quarter selection every 4 quarters.

    Two composite metrics (protocol Amendment 1):
      raw_pooled      -- original spec: composite[t] = cand[best][t] raw. Candidates live
                         on incommensurable scales (baseline = rank 1-4; C1/C2/C4
                         continuous), so scale switches pollute the pooled Spearman.
      percentile_v2_1 -- corrected: applied scores replaced by their percentile within
                         the chosen candidate's matured common-set values at T (midrank);
                         the baseline comparison series transformed identically."""
    n = d['n']
    fwd12 = d['fwd12']

    def matured_count(T):
        # matured t in [0, T-12] => count = T-11 (T indices 0-based)
        return max(0, T - 11)

    start_T = None
    for t in range(n):
        if matured_count(t) >= 40:
            start_T = t
            break
    if start_T is None:
        return {'insufficient_data': True}

    selection_dates = list(range(start_T, n, 4))
    history = []
    composite = [None] * n        # raw_pooled (original metric)
    composite_pct = [None] * n    # percentile_v2_1 (corrected metric)
    baseline_pct = [None] * n     # baseline transformed identically (symmetry)
    applied = []

    ordered_pool = [nm for nm in TIE_ORDER if nm in pool_names]

    for T in selection_dates:
        matured_idx = list(range(0, max(0, T - 11)))
        common = []
        for t in matured_idx:
            if fwd12[t] is None: continue
            if all(cand[nm][t] is not None for nm in pool_names):
                common.append(t)

        cand_rho = {}
        for nm in ordered_pool:
            xs = [cand[nm][t] for t in common]
            ys = [fwd12[t] for t in common]
            rho, cnt = spearman(xs, ys)
            cand_rho[nm] = {'rho': rho, 'n': cnt}

        best, best_rho = None, -999.0
        for nm in ordered_pool:
            r = cand_rho[nm]['rho']
            if r is None: continue
            if r > best_rho + 1e-12:
                best_rho, best = r, nm
        if best is None:
            best = 'baseline'  # degenerate fallback: no candidate scorable yet

        end = min(T + 3, n - 1)
        pool_best_vals = [cand[best][u] for u in common]        # matured-only at T
        pool_base_vals = [cand['baseline'][u] for u in common]  # matured-only at T
        for t in range(T, end + 1):
            composite[t] = cand[best][t]
            composite_pct[t] = midrank_percentile(cand[best][t], pool_best_vals)
            baseline_pct[t] = midrank_percentile(cand['baseline'][t], pool_base_vals)
            applied.append(t)

        history.append({
            'T': T, 'T_q': d['q'][T], 'n_matured_raw': len(matured_idx),
            'n_common': len(common), 'candidate_rho': cand_rho, 'chosen': best,
            'applied_range': [d['q'][T], d['q'][end]],
        })

    applied = sorted(set(applied))

    # -- raw_pooled (original metric, kept unchanged) --
    xs, ys = paired([composite[t] for t in applied], [fwd12[t] for t in applied])
    comp_rho, comp_n = spearman(xs, ys)
    xsb, ysb = paired([cand['baseline'][t] for t in applied], [fwd12[t] for t in applied])
    base_rho, base_n = spearman(xsb, ysb)

    # -- percentile_v2_1 (corrected metric, Amendment 1): both rhos over the SAME
    #    applied window, paired non-null (composite_pct, baseline_pct, fwd12 all non-null)
    pct_idx = [t for t in applied
               if composite_pct[t] is not None and baseline_pct[t] is not None
               and fwd12[t] is not None]
    cpct_rho, cpct_n = spearman([composite_pct[t] for t in pct_idx],
                                [fwd12[t] for t in pct_idx])
    bpct_rho, bpct_n = spearman([baseline_pct[t] for t in pct_idx],
                                [fwd12[t] for t in pct_idx])

    return {
        'insufficient_data': False,
        'start_T': start_T, 'start_T_q': d['q'][start_T],
        'n_selection_dates': len(selection_dates),
        'applied_quarters': [d['q'][t] for t in applied],
        # raw_pooled = original metric (protocol pre-amendment), kept for the reader
        'composite_rho': comp_rho, 'composite_n': comp_n,
        'baseline_rho_same_window': base_rho, 'baseline_n_same_window': base_n,
        'delta_vs_baseline': (round(comp_rho - base_rho, 3)
                               if comp_rho is not None and base_rho is not None else None),
        # percentile_v2_1 = corrected metric (Amendment 1) -- operative for thresholds
        'percentile_v2_1': {
            'composite_pct_rho': cpct_rho,
            'baseline_pct_rho': bpct_rho,
            'n': cpct_n,
            'delta_pct': (round(cpct_rho - bpct_rho, 3)
                           if cpct_rho is not None and bpct_rho is not None else None),
        },
        'history': history,
        '_composite_pct_series': composite_pct,  # used by the truncation smoke test
    }


# ---------------------------------------------------------------------------
# Look-ahead smoke test (truncation test for C1 / C2)
# ---------------------------------------------------------------------------
def truncation_test(d, mkt, k=None):
    n = d['n']
    if k is None:
        k = n - 10  # leave a real tail to truncate away
    full = compute_candidates(d)
    d_trunc = {'q': d['q'][:k], 'mom': d['mom'][:k], 'cred': d['cred'][:k],
               'warn': d['warn'][:k], 'quad': d['quad'][:k], 'fwd12': d['fwd12'][:k], 'n': k}
    trunc = compute_candidates(d_trunc)
    ok = True
    mismatches = []
    for name in ('C1', 'C2'):
        for i in range(k):
            fv, tv = full[name][i], trunc[name][i]
            if fv != tv:
                ok = False
                mismatches.append((name, i, fv, tv))

    # composite_pct (metric v2.1) truncation check: the walk-forward percentile series
    # for quarters < k must be identical whether or not the tail exists. Note: truncating
    # fwd12 removes NOTHING material — fwd12 at matured quarters (t <= T-12 < k-12) is
    # unchanged by the cut, so any mismatch would indicate look-ahead.
    pool = ['baseline', 'C1', 'C2', 'C4']
    wf_full = walk_forward(d, full, pool)
    wf_trunc = walk_forward(d_trunc, trunc, pool)
    pct_checked = 0
    if not wf_full.get('insufficient_data') and not wf_trunc.get('insufficient_data'):
        sf = wf_full['_composite_pct_series']
        stq = wf_trunc['_composite_pct_series']
        for i in range(k):
            if stq[i] is None and sf[i] is None:
                continue
            pct_checked += 1
            if sf[i] != stq[i]:
                ok = False
                mismatches.append(('composite_pct', i, sf[i], stq[i]))
    return {'market': mkt, 'k': k, 'n_full': n, 'pass': ok,
            'composite_pct_quarters_checked': pct_checked, 'mismatches': mismatches[:5]}


# ---------------------------------------------------------------------------
# Self-check: baseline must reproduce Test 8
# ---------------------------------------------------------------------------
def baseline_selfcheck(mkt, rho):
    expected = TEST8_BASELINE[mkt]
    ok = rho is not None and abs(rho - expected) <= 0.01
    return {'market': mkt, 'expected': expected, 'got': rho, 'pass': ok}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def analyze_market(mkt):
    d = load_market(mkt)
    vol_z_by_q = load_volume(mkt) if mkt in VOLUME_FILES else None
    c3_available = vol_z_by_q is not None
    if mkt in VOLUME_FILES and not c3_available:
        print(f"C3: volume data not available, skipped ({mkt.upper()})")

    cand = compute_candidates(d, vol_z_by_q if c3_available else None)
    pool_names = ['baseline', 'C1', 'C2', 'C4'] + (['C3'] if c3_available else [])

    result = {'market': mkt, 'n_quarters': d['n'], 'c3_available': c3_available,
               'candidates': {}}

    for name in pool_names:
        s = cand[name]
        result['candidates'][name] = {
            'full_period': full_period(s, d['fwd12']),
            'overlap_robustness': overlap_robustness(s, d['fwd12'], d['n']),
            'decade_consistency': decade_consistency(d['q'], s, d['fwd12']),
        }

    wf = walk_forward(d, cand, pool_names)
    wf.pop('_composite_pct_series', None)  # internal (truncation test only), keep JSON clean
    result['walk_forward'] = wf
    return d, cand, result


def print_market_report(mkt, result):
    print(f"\n=== {mkt.upper()} ===  (n={result['n_quarters']} quarters, C3 available: {result['c3_available']})")
    for name, m in result['candidates'].items():
        fp = m['full_period']
        ov = m['overlap_robustness']
        dc = m['decade_consistency']
        print(f"  [{name}]")
        print(f"    full-period rho = {fp['rho']}  (n={fp['n']})")
        for off, v in ov['per_offset'].items():
            cav = "  <-- small-n caveat" if v['small_n_caveat'] else ""
            print(f"    overlap offset={off}: rho={v['rho']}  n={v['n']}{cav}")
        print(f"    overlap median rho = {ov['median_rho']}")
        dec_str = ", ".join(f"{k}:{v['rho']}(n={v['n']})" for k, v in dc['by_decade'].items())
        print(f"    decade rho: {dec_str if dec_str else '(no decade with n>=8)'}")
        print(f"    decades positive: {dc['positive_decades']}/{dc['total_decades']}")

    wf = result['walk_forward']
    if wf.get('insufficient_data'):
        print("  [walk-forward] insufficient matured history (<40 matured quarters) -- skipped")
    else:
        print(f"  [walk-forward] start={wf['start_T_q']}  selection_dates={wf['n_selection_dates']}"
              f"  applied_quarters={len(wf['applied_quarters'])}")
        print(f"    raw_pooled (original metric): composite rho = {wf['composite_rho']} (n={wf['composite_n']})"
              f"   vs baseline rho (same window) = {wf['baseline_rho_same_window']} (n={wf['baseline_n_same_window']})"
              f"   delta = {wf['delta_vs_baseline']}")
        p = wf['percentile_v2_1']
        print(f"    percentile_v2_1 (corrected, operative): composite_pct rho = {p['composite_pct_rho']}"
              f"   vs baseline_pct rho = {p['baseline_pct_rho']}   delta_pct = {p['delta_pct']}   (n={p['n']})")
        chosen_counts = {}
        for h in wf['history']:
            chosen_counts[h['chosen']] = chosen_counts.get(h['chosen'], 0) + 1
        print(f"    selection history (chosen candidate counts): {chosen_counts}")


def _overall_verdict(deltas):
    beat_010 = [m for m in ('us', 'jp', 'my') if deltas.get(m) is not None and deltas[m] >= 0.10]
    worse_than_005 = [m for m in MKTS if deltas.get(m) is not None and deltas[m] < -0.05]
    ok = len(beat_010) >= 2 and len(worse_than_005) == 0
    return {
        'deltas_vs_baseline': deltas,
        'markets_beating_baseline_by_0.10_among_us_jp_my': beat_010,
        'markets_degrading_more_than_0.05': worse_than_005,
        'overall_pass': ok,
        'overall_status': 'PASS' if ok else 'FAIL',
    }


def evaluate_thresholds(results):
    """Frozen thresholds from protocol §Success thresholds, evaluated under BOTH metrics.
    Per Amendment 1 the percentile_v2_1 metric is the operative verdict; the raw_pooled
    (original) verdict is shown alongside."""
    deltas_raw, deltas_pct = {}, {}
    for mkt in MKTS:
        wf = results[mkt]['walk_forward']
        if not wf.get('insufficient_data'):
            deltas_raw[mkt] = wf['delta_vs_baseline']
            deltas_pct[mkt] = wf['percentile_v2_1']['delta_pct']

    raw_verdict = _overall_verdict(deltas_raw)
    pct_verdict = _overall_verdict(deltas_pct)

    tw_c3 = results['tw']['candidates'].get('C3')
    if tw_c3 is not None:
        tw_c3_rho = tw_c3['full_period']['rho']
        tw_c3_pass = tw_c3_rho is not None and tw_c3_rho >= 0.30
        tw_c3_status = 'PASS' if tw_c3_pass else 'FAIL'
    else:
        tw_c3_rho = None
        tw_c3_pass = None
        tw_c3_status = 'NOT EVALUATED (no TW volume data)'

    return {
        'operative_metric': 'percentile_v2_1 (protocol Amendment 1)',
        'percentile_v2_1': pct_verdict,   # operative verdict
        'raw_pooled': raw_verdict,        # original metric, shown alongside
        'amendment1_timing_disclosure': AMENDMENT1_TIMING_DISCLOSURE,
        'tw_c3_full_period_rho': tw_c3_rho,
        'tw_c3_pass': tw_c3_pass,
        'tw_c3_status': tw_c3_status,
    }


def main():
    print("Compass v2 predictive-upgrade evaluation")
    print("Protocol: scripts/compass_v2_protocol.md (frozen 2026-07-14)\n")

    # --- fwd12 alignment spot-check (raw json values, eyeball vs protocol) ---
    print("--- fwd12 alignment spot-check (raw compass-<m>.json values) ---")
    spot = {}
    for mkt in MKTS:
        d = json.load(open(os.path.join(ROOT, 'data', f'compass-{mkt}.json')))
        i = min(20, len(d['q']) - 1)
        spot[mkt] = {'q': d['q'][i], 'fwd12': d['fwd12'][i], 'quad': d['quad'][i]}
        print(f"  {mkt.upper()}: {d['q'][i]}  fwd12={d['fwd12'][i]}  quad={d['quad'][i]}")
    print()

    all_d, all_cand, all_results = {}, {}, {}
    for mkt in MKTS:
        d, cand, result = analyze_market(mkt)
        all_d[mkt], all_cand[mkt], all_results[mkt] = d, cand, result

    # --- self-check: baseline reproduces Test 8 ---
    print("--- Self-check: baseline full-period rho vs published Test 8 ---")
    selfchecks = []
    for mkt in MKTS:
        rho = all_results[mkt]['candidates']['baseline']['full_period']['rho']
        chk = baseline_selfcheck(mkt, rho)
        selfchecks.append(chk)
        status = 'PASS' if chk['pass'] else 'FAIL'
        print(f"  {mkt.upper()}: expected={chk['expected']}  got={chk['got']}  [{status}]")
    baseline_selfcheck_pass = all(c['pass'] for c in selfchecks)
    print(f"  Baseline reproduction: {'PASS' if baseline_selfcheck_pass else 'FAIL'}")
    print()

    # --- look-ahead smoke test ---
    print("--- Look-ahead smoke test (truncation test, C1/C2 + composite_pct, TW) ---")
    trunc_result = truncation_test(all_d['tw'], 'tw')
    print(f"  market=TW  truncated at k={trunc_result['k']} of n={trunc_result['n_full']}"
          f"  composite_pct quarters checked={trunc_result['composite_pct_quarters_checked']}"
          f"  result={'PASS (no values changed)' if trunc_result['pass'] else 'FAIL'}")
    if not trunc_result['pass']:
        print(f"    mismatches (first 5): {trunc_result['mismatches']}")
    print()

    # --- per-market report ---
    for mkt in MKTS:
        print_market_report(mkt, all_results[mkt])

    # --- summary table ---
    print("\n=== Summary: full-period rho by candidate ===")
    header_cands = ['baseline', 'C1', 'C2', 'C4', 'C3']
    print("  " + f"{'MKT':5s}" + "".join(f"{c:>10s}" for c in header_cands))
    for mkt in MKTS:
        row = f"  {mkt.upper():5s}"
        for c in header_cands:
            v = all_results[mkt]['candidates'].get(c)
            cell = v['full_period']['rho'] if v else '--'
            row += f"{cell:>10}"
        print(row)

    print("\n=== Summary: walk-forward composite vs baseline (raw_pooled = original metric) ===")
    for mkt in MKTS:
        wf = all_results[mkt]['walk_forward']
        if wf.get('insufficient_data'):
            print(f"  {mkt.upper():5s}  insufficient data")
        else:
            print(f"  {mkt.upper():5s}  composite={wf['composite_rho']:>7}  baseline={wf['baseline_rho_same_window']:>7}"
                  f"  delta={wf['delta_vs_baseline']:>7}  n={wf['composite_n']}")

    print("\n=== Summary: walk-forward percentile_v2_1 (corrected metric, Amendment 1 — operative) ===")
    for mkt in MKTS:
        wf = all_results[mkt]['walk_forward']
        if wf.get('insufficient_data'):
            print(f"  {mkt.upper():5s}  insufficient data")
        else:
            p = wf['percentile_v2_1']
            print(f"  {mkt.upper():5s}  composite_pct={p['composite_pct_rho']:>7}  baseline_pct={p['baseline_pct_rho']:>7}"
                  f"  delta_pct={p['delta_pct']:>7}  n={p['n']}")

    thresholds = evaluate_thresholds(all_results)

    # --- HONESTY block ---
    print("\n=== HONESTY ===")
    print("Overlap caveat:")
    print(f"  {OVERLAP_CAVEAT}")
    print("Contamination disclosure:")
    print(f"  {CONTAMINATION_NOTE}")
    print("Amendment 1 (metric v2.1) timing disclosure:")
    print(f"  {AMENDMENT1_TIMING_DISCLOSURE}")
    print("Frozen thresholds (protocol §Success thresholds):")
    print("  Overall: walk-forward composite rho >= baseline+0.10 in >=2 of {US, JP, MY},")
    print("           with no market degrading by more than 0.05.")
    pv = thresholds['percentile_v2_1']
    rv = thresholds['raw_pooled']
    print("  Under percentile_v2_1 (corrected metric — OPERATIVE verdict):")
    print(f"    -> markets beating baseline by >=0.10 (of US/JP/MY): {pv['markets_beating_baseline_by_0.10_among_us_jp_my']}")
    print(f"    -> markets degrading more than 0.05 (any market): {pv['markets_degrading_more_than_0.05']}")
    print(f"    -> deltas vs baseline (pct): {pv['deltas_vs_baseline']}")
    print(f"    -> OVERALL (operative): {pv['overall_status']}")
    print("  Under raw_pooled (original metric — shown alongside per Amendment 1):")
    print(f"    -> markets beating baseline by >=0.10 (of US/JP/MY): {rv['markets_beating_baseline_by_0.10_among_us_jp_my']}")
    print(f"    -> markets degrading more than 0.05 (any market): {rv['markets_degrading_more_than_0.05']}")
    print(f"    -> deltas vs baseline (raw): {rv['deltas_vs_baseline']}")
    print(f"    -> OVERALL (raw, non-operative): {rv['overall_status']}")
    print("  Taiwan (C3 pilot): full-period rho(S3) >= 0.30 (baseline 0.081).")
    print(f"    -> TW C3 full-period rho: {thresholds['tw_c3_full_period_rho']}")
    print(f"    -> TW C3: {thresholds['tw_c3_status']}")
    print("  Anything short of these = negative/partial result, published as-is on /my/framework;")
    print("  the live clock page changes only if thresholds are met.")

    # --- write output file ---
    out = {
        'protocol': 'scripts/compass_v2_protocol.md frozen 2026-07-14',
        'fwd12_spotcheck': spot,
        'baseline_selfcheck': selfchecks,
        'baseline_selfcheck_pass': baseline_selfcheck_pass,
        'lookahead_truncation_test': trunc_result,
        'markets': all_results,
        'threshold_evaluation': thresholds,
        'honesty': {
            'overlap_caveat': OVERLAP_CAVEAT,
            'contamination_note': CONTAMINATION_NOTE,
            'amendment1_timing_disclosure': AMENDMENT1_TIMING_DISCLOSURE,
        },
    }
    out_path = os.path.join(ROOT, 'data', 'compass-backtest-v2.json')
    json.dump(out, open(out_path, 'w'), indent=2)
    print(f"\nWrote {out_path}")


if __name__ == '__main__':
    main()
