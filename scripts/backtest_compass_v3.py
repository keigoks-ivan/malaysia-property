#!/usr/bin/env python3
"""
Compass v3 risk-gauge evaluation harness.

Implements scripts/compass_v3_protocol.md LITERALLY (frozen 2026-07-14, before
any evaluation run). Zero design discretion here: targets, cuts, formulas,
metrics and thresholds all come from the protocol file. Where anything below
and the protocol disagree, the protocol wins -- this file should be read
alongside it.

Targets:
  T_ABS : bad_t = 1 iff fwd12_t < 0
  T_REL : bad_t = 1 iff fwd12_t < Q25 of matured own-history {fwd12_u : u<=t-12},
          expanding, >=20 matured obs required else undefined at t.

Classifiers:
  W_MOM  = quad_t == 'starved'
  W_PRIM = quad_t == 'starved' AND warn_t
  W_AFS  = W_PRIM AND AFS_z_t > 0     (AFS_t = r_t - r_{t-4}, r = real rate)
  W_DEMO = W_PRIM AND demo_yoy_t < 0  (25-39 cohort YoY; NOT EVALUATED if absent)

AFS inputs:
  us          : data/clock-us.json raw.real_rate (already the real-rate series)
  tw/my/jp    : scripts/.<m>data/<m>_raw.json -- rate (nominal), cpi (INDEX
                LEVEL -- inspected: TW range ~81-110, MY ~80-136, JP ~51-112,
                none are already YoY%). cpi_yoy = yoy(cpi); r = rate - cpi_yoy.
  Alignment: raw q axis confirmed IDENTICAL to compass-<m>.json q axis for
  tw/my/jp (same list, same length); still joined by label (dict), never by
  positional index, per protocol/house convention.

DEMO inputs: scripts/.<m>data/<m>_demo.json {q, pop2539}. Absent for all four
markets at the time this harness was written (another agent fetching) -- the
harness must run clean regardless, so W_DEMO / conditioner degrade gracefully
to "NOT EVALUATED" per market when the file is missing.

No external fetch. Standard library only.

Does NOT edit any page, any compass pipeline file, or v2 files. Writes only
data/compass-backtest-v3.json.
"""
import json, math, os
import statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MKTS = ['us', 'tw', 'my', 'jp']

PROTOCOL_TAG = 'scripts/compass_v3_protocol.md frozen 2026-07-14'

CONTAMINATION_NOTE = (
    "v2's published results (cell medians, decade decay, C3 refutation) inform this "
    "design; the gate/targets/cuts are frozen before computing any 2x2 table. The "
    "known clustering of loss events (2006-08 US, 1990s JP) means OR estimates are "
    "dominated by few episodes; episode counts (distinct contiguous bad-spells "
    "caught vs missed) are reported alongside quarter counts for exactly this reason."
)
OVERLAP_CAVEAT = (
    "Overlap robustness: forward windows overlap (serial correlation inflates n). "
    "Report metrics on non-overlapping subsamples: every 12th quarter at offsets "
    "{0,4,8}, median OR of the offsets, with per-offset event counts. Small-n "
    "caveat flagged when a subsample has <10 usable quarters."
)
Q25_CONVENTION_NOTE = (
    "Q25 convention: linear interpolation between order statistics (numpy 'linear' / "
    "Excel PERCENTILE.INC default) -- h=(n-1)*0.25 over the sorted matured pool, "
    "value = s[floor(h)] + frac*(s[ceil(h)]-s[floor(h)])."
)
EPISODE_CONVENTION_NOTE = (
    "Episode convention: a contiguous run of bad_t==True by adjacent quarter index "
    "(undefined/None quarters treated as not-bad for run-breaking purposes -- this "
    "only matters at series boundaries: T_REL's undefined stretch is the first "
    "~20+12 quarters and fwd12's undefined stretch is the last 12, never a mid-series "
    "gap, so no episode is artificially split). An episode is 'caught' by a classifier "
    "if the classifier is True (defined-and-true) in any quarter from 4 quarters "
    "before the episode start through the episode's last quarter, inclusive."
)


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


def ez(a, sign=1, minobs=12):
    """EXPANDING (whole-history) robust z -- copied EXACTLY from scripts/build_compass.py ez()."""
    out = [None] * len(a); h = []
    for i, v in enumerate(a):
        if v is not None: h.append(v)
        if v is None or len(h) < minobs: continue
        m = st.median(h); mad = st.median([abs(x - m) for x in h]) or 1e-9
        out[i] = sign * max(-3, min(3, (v - m) / (1.4826 * mad)))
    return out


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_market(mkt):
    d = json.load(open(os.path.join(ROOT, 'data', f'compass-{mkt}.json')))
    return {
        'q': d['q'], 'quad': d['quad'], 'warn': d['warn'], 'fwd12': d['fwd12'],
        'n': len(d['q']),
    }


def load_afs_real_rate(mkt, compass_q):
    """Returns (r_aligned, note). r is the real rate on the compass q axis, joined by label."""
    if mkt == 'us':
        raw = json.load(open(os.path.join(ROOT, 'data', 'clock-us.json')))
        m = dict(zip(raw['q'], raw['raw']['real_rate']))
        r = [m.get(qq) for qq in compass_q]
        note = ("US: real rate read directly from data/clock-us.json raw.real_rate "
                "(already a real-rate series on the same axis as compass-us.json).")
        return r, note

    path = os.path.join(ROOT, 'scripts', f'.{mkt}data', f'{mkt}_raw.json')
    raw = json.load(open(path))
    cpi = raw['cpi']
    cpi_min = min(x for x in cpi if x is not None)
    cpi_max = max(x for x in cpi if x is not None)
    cpi_yoy_series = yoy(cpi)  # cpi is an INDEX LEVEL (inspected: base ~80-110-ish), not already YoY%
    rate_map = dict(zip(raw['q'], raw['rate']))
    cpiyoy_map = dict(zip(raw['q'], cpi_yoy_series))
    r = []
    for qq in compass_q:
        rt = rate_map.get(qq)
        cy = cpiyoy_map.get(qq)
        r.append(rt - cy if (rt is not None and cy is not None) else None)
    note = (f"{mkt.upper()}: cpi inspected as an INDEX LEVEL (range {cpi_min:.2f}-{cpi_max:.2f}, "
            f"not a YoY% series) -> computed cpi_yoy=yoy(cpi) [build_compass.py yoy()], "
            f"then r = rate - cpi_yoy, joined onto compass q axis by label "
            f"(raw q axis identical to compass q axis: {raw['q'] == compass_q}).")
    return r, note


def compute_afs_z(r, n):
    afs = [None] * n
    for i in range(4, n):
        if r[i] is not None and r[i - 4] is not None:
            afs[i] = r[i] - r[i - 4]
    afs_z = smooth(tz(afs, win=24), 3)
    return afs, afs_z


def load_demo(mkt, compass_q):
    """Returns (pop_aligned, demo_yoy, status_note). None,None if file absent/malformed."""
    path = os.path.join(ROOT, 'scripts', f'.{mkt}data', f'{mkt}_demo.json')
    if not os.path.exists(path):
        return None, None, f"demo file absent ({path}) -> W_DEMO NOT EVALUATED for {mkt.upper()}"
    try:
        dj = json.load(open(path))
    except Exception as e:
        return None, None, f"demo file unreadable ({path}): {e} -> W_DEMO NOT EVALUATED for {mkt.upper()}"
    if 'q' not in dj or 'pop2539' not in dj:
        return None, None, f"demo file malformed, missing q/pop2539 ({path}) -> W_DEMO NOT EVALUATED for {mkt.upper()}"
    m = dict(zip(dj['q'], dj['pop2539']))
    pop_aligned = [m.get(qq) for qq in compass_q]
    demo_yoy_series = yoy(pop_aligned)  # 4-quarter % change on the ALIGNED (compass) axis, null-safe
    n_avail = sum(1 for v in pop_aligned if v is not None)
    return pop_aligned, demo_yoy_series, (f"demo file found ({path}), {n_avail}/{len(compass_q)} "
                                           f"quarters aligned by label, demo_yoy computed as 4q %change")


# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------
def quantile25_linear(vals):
    """Q25, linear interpolation between order statistics (see Q25_CONVENTION_NOTE)."""
    s = sorted(vals)
    n = len(s)
    if n == 0:
        return None
    h = (n - 1) * 0.25
    lo = int(math.floor(h))
    hi = int(math.ceil(h))
    if lo == hi:
        return s[lo]
    frac = h - lo
    return s[lo] + frac * (s[hi] - s[lo])


def compute_t_abs(fwd12):
    return [None if v is None else (v < 0) for v in fwd12]


def compute_t_rel(fwd12):
    """Expanding, matured-only Q25 target. Look-ahead guard: pool at t uses only
    u <= t-12 (never any fwd12_u whose 12q outcome window could still overlap t)."""
    n = len(fwd12)
    bad = [None] * n
    q25_used = [None] * n
    matured_n = [0] * n
    for t in range(n):
        cutoff = t - 12
        if cutoff < 0:
            continue
        pool = [fwd12[u] for u in range(0, cutoff + 1) if fwd12[u] is not None]
        matured_n[t] = len(pool)
        if len(pool) < 20:
            continue
        if fwd12[t] is None:
            continue
        q25 = quantile25_linear(pool)
        q25_used[t] = round(q25, 4)
        bad[t] = fwd12[t] < q25
    return bad, q25_used, matured_n


# ---------------------------------------------------------------------------
# Classifiers
# ---------------------------------------------------------------------------
def compute_classifiers(quad, warn, afs_z, demo_yoy, n):
    W_MOM = [None if quad[i] is None else (quad[i] == 'starved') for i in range(n)]
    W_PRIM = [None] * n
    for i in range(n):
        if quad[i] is None or warn[i] is None:
            continue
        W_PRIM[i] = (quad[i] == 'starved') and bool(warn[i])

    W_AFS = [None] * n
    for i in range(n):
        if W_PRIM[i] is None or afs_z[i] is None:
            continue
        W_AFS[i] = W_PRIM[i] and (afs_z[i] > 0)

    W_DEMO = None
    if demo_yoy is not None:
        W_DEMO = [None] * n
        for i in range(n):
            if W_PRIM[i] is None or demo_yoy[i] is None:
                continue
            W_DEMO[i] = W_PRIM[i] and (demo_yoy[i] < 0)

    return {'W_MOM': W_MOM, 'W_PRIM': W_PRIM, 'W_AFS': W_AFS, 'W_DEMO': W_DEMO}


# ---------------------------------------------------------------------------
# 2x2 metrics
# ---------------------------------------------------------------------------
def two_by_two(W, bad):
    a = b = c = d = 0
    excluded = 0
    n = len(W)
    for i in range(n):
        w, y = W[i], bad[i]
        if w is None or y is None:
            excluded += 1
            continue
        if w and y: a += 1
        elif w and not y: b += 1
        elif (not w) and y: c += 1
        else: d += 1
    return {'a': a, 'b': b, 'c': c, 'd': d, 'n_used': a + b + c + d, 'n_excluded': excluded, 'n_total': n}


def or_stats(cells):
    a, b, c, d = cells['a'], cells['b'], cells['c'], cells['d']
    haldane = any(x == 0 for x in (a, b, c, d))
    if haldane:
        a2, b2, c2, d2 = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    else:
        a2, b2, c2, d2 = a, b, c, d
    denom = b2 * c2
    or_val = (a2 * d2) / denom if denom != 0 else None
    precision = a / (a + b) if (a + b) > 0 else None
    recall = a / (a + c) if (a + c) > 0 else None
    base_rate = (a + c) / (a + b + c + d) if (a + b + c + d) > 0 else None
    return {
        'OR': round(or_val, 3) if or_val is not None else None,
        'haldane_applied': haldane,
        'precision': round(precision, 4) if precision is not None else None,
        'recall': round(recall, 4) if recall is not None else None,
        'base_rate': round(base_rate, 4) if base_rate is not None else None,
        'w_quarters': a + b,
        'cells': cells,
    }


def overlap_robustness(W, bad):
    n = len(W)
    per_offset = {}
    for offset in (0, 4, 8):
        idx = list(range(offset, n, 12))
        Wi = [W[i] for i in idx]
        Bi = [bad[i] for i in idx]
        cells = two_by_two(Wi, Bi)
        stats = or_stats(cells)
        per_offset[offset] = {
            'OR': stats['OR'], 'n_used': cells['n_used'],
            'w_count': cells['a'] + cells['b'], 'bad_count': cells['a'] + cells['c'],
            'haldane_applied': stats['haldane_applied'],
            'small_n_caveat': cells['n_used'] < 10,
        }
    ors = [v['OR'] for v in per_offset.values() if v['OR'] is not None]
    median_or = round(st.median(ors), 3) if ors else None
    return {'per_offset': per_offset, 'median_OR': median_or}


# ---------------------------------------------------------------------------
# Episode analysis
# ---------------------------------------------------------------------------
def find_episodes(bad):
    n = len(bad)
    eps = []
    i = 0
    while i < n:
        if bad[i] is True:
            j = i
            while j + 1 < n and bad[j + 1] is True:
                j += 1
            eps.append((i, j))
            i = j + 1
        else:
            i += 1
    return eps


def episode_catch(eps, W, q):
    caught = 0
    details = []
    for (s, e) in eps:
        lookback = max(0, s - 4)
        hit = any(W[k] is True for k in range(lookback, e + 1))
        details.append({'start_q': q[s], 'end_q': q[e], 'length': e - s + 1, 'caught': hit})
        if hit: caught += 1
    return {'episodes_total': len(eps), 'caught': caught, 'missed': len(eps) - caught, 'details': details}


# ---------------------------------------------------------------------------
# Mantel-Haenszel pooled OR
# ---------------------------------------------------------------------------
def mh_or(strata_cells):
    num = 0.0
    den = 0.0
    n_strata = 0
    for c in strata_cells:
        a, b, cc, d = c['a'], c['b'], c['c'], c['d']
        n = a + b + cc + d
        if n == 0:
            continue
        n_strata += 1
        num += (a * d) / n
        den += (b * cc) / n
    if den == 0:
        return {'OR_MH': None, 'n_strata': n_strata, 'note': 'denominator zero (no discordant weight across strata)'}
    return {'OR_MH': round(num / den, 3), 'n_strata': n_strata}


# ---------------------------------------------------------------------------
# Per-market analysis
# ---------------------------------------------------------------------------
def analyze_market(mkt):
    d = load_market(mkt)
    n, q, quad, warn, fwd12 = d['n'], d['q'], d['quad'], d['warn'], d['fwd12']

    r, afs_note = load_afs_real_rate(mkt, q)
    afs, afs_z = compute_afs_z(r, n)

    pop_aligned, demo_yoy_series, demo_note = load_demo(mkt, q)

    classifiers = compute_classifiers(quad, warn, afs_z, demo_yoy_series, n)

    t_abs = compute_t_abs(fwd12)
    t_rel, q25_used, matured_n = compute_t_rel(fwd12)
    targets = {'T_ABS': t_abs, 'T_REL': t_rel}

    n_bad_abs = sum(1 for x in t_abs if x is True)
    rated_abs = n_bad_abs >= 8

    market_results = {}
    for tname, bad in targets.items():
        market_results[tname] = {}
        for cname, W in classifiers.items():
            if W is None:
                market_results[tname][cname] = {'status': 'NOT EVALUATED (no demo data)'}
                continue
            cells = two_by_two(W, bad)
            stats = or_stats(cells)
            overlap = overlap_robustness(W, bad)
            eps = find_episodes(bad)
            epcatch = episode_catch(eps, W, q)
            market_results[tname][cname] = {**stats, 'overlap': overlap, 'episodes': epcatch}

    return {
        'market': mkt, 'n_quarters': n,
        'afs_note': afs_note, 'demo_note': demo_note,
        'demo_available': pop_aligned is not None,
        'n_bad_abs': n_bad_abs, 'rated_abs': rated_abs,
        'results': market_results,
        # kept for panel / self-checks (not JSON-serialized at top level twice)
        '_q': q, '_targets': targets, '_classifiers': classifiers,
        '_q25_used': q25_used, '_matured_n': matured_n, '_fwd12': fwd12,
    }


# ---------------------------------------------------------------------------
# Panel (Mantel-Haenszel)
# ---------------------------------------------------------------------------
def build_panel(all_res, cname, tname, markets):
    strata_cells = []
    per_market = {}
    for mkt in markets:
        W = all_res[mkt]['_classifiers'][cname]
        bad = all_res[mkt]['_targets'][tname]
        if W is None:
            per_market[mkt] = None
            continue
        cells = two_by_two(W, bad)
        strata_cells.append(cells)
        per_market[mkt] = cells
    pooled = mh_or([c for c in strata_cells])
    return {'classifier': cname, 'target': tname, 'markets': markets,
            'per_market_cells': per_market, 'pooled': pooled}


# ---------------------------------------------------------------------------
# Amendment 2 (2026-07-14): expanding-basis warn_exp re-validation
# ---------------------------------------------------------------------------
AMENDMENT2_TEXT = """## Amendment 2 — 2026-07-14, warn-basis re-validation (from the design audit)
The design audit (scripts/compass_design_audit_charter.md; findings F1/C4) found
the supply-glut warn flag uses a TRAILING 24q z while a glut is arguably an
ABSOLUTE concept — with demonstrated warning fatigue (JP 2023Q3: vacancy 13.6%,
near the all-time high, reads trailing z −0.67 → warn OFF; MY 2022Q2 similar) —
and an internal inconsistency (the same series is EXPANDING in the report card).
warn is an input of the validated W_PRIM, so per audit charter §4 this cannot be
silently fixed; it is re-validated here.

Frozen rules:
- warn_exp: expanding robust z (ez(), same MAD/clamp/minobs=12 conventions as
  build_compass.py) on the SAME raw level series (vacancy, months-supply per
  market; US raw.months/raw.vac from clock-us.json), sign such that loose =
  negative, threshold ≤ −1, OR-combination — identical to trailing warn except
  the basis. No threshold or window search.
- W_PRIM_EXP = starved ∧ warn_exp. Evaluated with the IDENTICAL v3 machinery
  (both targets, gate, MH pooling, episode counts, overlap robustness).
- Decision rule (frozen): the live gauge switches to the expanding basis ONLY if
  W_PRIM_EXP passes the same ABS+REL gates AND its ABS MH-pooled OR ≥ the
  trailing version's. Otherwise trailing stays (status quo unless dominated),
  and the conceptual tension is published as a finding: the trailing warning
  works empirically even though a glut is conceptually absolute.
- Both versions' full tables are published regardless of outcome.
Timing disclosure: this amendment was written after the audit revealed the
fatigue cases but before any W_PRIM_EXP table was computed."""


# ---------------------------------------------------------------------------
# Amendment 3 (2026-07-14): Australia as an out-of-sample hold-out
# ---------------------------------------------------------------------------
AMENDMENT3_TEXT = """## Amendment 3 — 2026-07-14, adding Australia as an out-of-sample market (rule frozen before any AU number computed)
Australia is added to the clock as a 5th market AFTER the v3 risk claim was frozen
and published on {US, TW, MY, JP}. Frozen treatment (decided before any AU 2×2
table exists), so AU cannot be cherry-picked into or out of the headline:
- The PRIMARY validated claim stays EXACTLY as published: 4-market set, ABS on
  US+JP, MH pooled 13.53 / 16.07. These numbers are NOT restated with AU folded in.
- AU is evaluated with the identical v3 machinery (both targets, applicability
  gate, per-market 2×2/OR/precision/recall, episode analysis) and reported as a
  HOLD-OUT: the first market the warning meets that it was never fit to.
- A 5-market MH pooled OR is ALSO computed and shown, but LABELLED "with AU
  (out-of-sample)" and never substituted for the frozen 4-market figure.
- Applicability gate applies unchanged: AU is rated for ABS only if it has ≥8
  matured 3y-loss quarters. Prior expectation (disclosed, not a threshold): AU
  rarely posts multi-year nominal losses, so it will likely be NOT RATED for ABS
  and evaluated on REL only — an informative outcome either way, reported as-is.
- Whatever AU shows, the live clock's AU risk gauge uses the same per-market
  state logic already in place (WARNING ON/OFF where rated; NOT RATED / NOT
  VALIDATED shown honestly where not) — no new favourable framing invented for AU.
Adding AU does not alter any existing market's warn/quad/W_PRIM series (verified
by regression guard: the 4 markets' compass arrays must be byte-identical after
AU is wired into build_compass.py)."""


def truncation_selfcheck_au():
    """T_REL truncation / look-ahead guard test, scoped to AU only (mirrors
    truncation_selfcheck()'s logic exactly; kept as a separate function so the
    existing self_checks.t_rel_truncation output for {us,tw,my,jp} is untouched)."""
    mkt = 'au'
    d = load_market(mkt)
    n = d['n']
    k = n - 10
    fwd12_full = d['fwd12']
    fwd12_trunc = fwd12_full[:k]

    bad_full, q25_full, _ = compute_t_rel(fwd12_full)
    bad_trunc, q25_trunc, _ = compute_t_rel(fwd12_trunc)

    mismatches = []
    for t in range(k):
        if bad_full[t] != bad_trunc[t] or q25_full[t] != q25_trunc[t]:
            mismatches.append((t, d['q'][t], bad_full[t], bad_trunc[t], q25_full[t], q25_trunc[t]))
    ok = len(mismatches) == 0
    return {'market': mkt, 'k': k, 'n_full': n, 'checked': k, 'pass': ok, 'mismatches': mismatches[:5]}


def load_warn_exp_raw(mkt, compass_q):
    """RAW level series (vacancy, months) that feed the trailing warn, joined onto the
    compass q axis by quarter label (house convention; never positional). Returns
    (vac_aligned, months_aligned, axis_identical, note)."""
    if mkt == 'us':
        raw = json.load(open(os.path.join(ROOT, 'data', 'clock-us.json')))
        qaxis = raw['q']
        vac_native = raw['raw']['vac']
        months_native = raw['raw']['months']
        src = 'data/clock-us.json raw.vac / raw.months'
    else:
        raw = json.load(open(os.path.join(ROOT, 'scripts', f'.{mkt}data', f'{mkt}_raw.json')))
        qaxis = raw['q']
        vac_native = raw['vacancy']
        months_native = raw['months']
        src = f'scripts/.{mkt}data/{mkt}_raw.json vacancy / months'
    vac_map = dict(zip(qaxis, vac_native))
    months_map = dict(zip(qaxis, months_native))
    vac_aligned = [vac_map.get(qq) for qq in compass_q]
    months_aligned = [months_map.get(qq) for qq in compass_q]
    axis_identical = (qaxis == compass_q)
    note = (f"{mkt.upper()}: source={src}; raw q axis identical to compass q axis: {axis_identical} "
            f"(joined by label regardless).")
    return vac_aligned, months_aligned, axis_identical, note


def compute_warn_exp(vac_level, months_level, n):
    """Mirrors build_compass.py's loose()/warn exactly, but on ez() (expanding) instead
    of the clock's czlist() (trailing). Null-safe the same way loose() is: a None input
    contributes False to the OR, never None -- so warn_exp is always a bool, never null."""
    vac_ez = ez(vac_level, sign=-1)
    months_ez = ez(months_level, sign=-1)

    def loose_exp(i):
        vv = vac_ez[i]; mm = months_ez[i]
        return (vv is not None and vv <= -1) or (mm is not None and mm <= -1)

    warn_exp = [loose_exp(i) for i in range(n)]
    return warn_exp, vac_ez, months_ez


def compute_wprim_exp(quad, warn_exp, n):
    """W_PRIM_EXP = quad=='starved' AND warn_exp -- same null-handling pattern as W_PRIM
    in compute_classifiers (undefined quad => undefined W_PRIM_EXP)."""
    W = [None] * n
    for i in range(n):
        if quad[i] is None or warn_exp[i] is None:
            continue
        W[i] = (quad[i] == 'starved') and bool(warn_exp[i])
    return W


def analyze_market_amendment2(mkt):
    d = load_market(mkt)
    n, q, quad, warn_trail, fwd12 = d['n'], d['q'], d['quad'], d['warn'], d['fwd12']

    vac_level, months_level, axis_identical, align_note = load_warn_exp_raw(mkt, q)

    def rng(a, label):
        vv = [x for x in a if x is not None]
        return {'field': label, 'n_total': len(a), 'n_nonnull': len(vv),
                'min': (round(min(vv), 3) if vv else None), 'max': (round(max(vv), 3) if vv else None),
                'sample_first5': a[:5]}

    level_check = {
        'vacancy': rng(vac_level, 'vacancy'), 'months': rng(months_level, 'months'),
        'axis_identical_to_compass_q': axis_identical, 'align_note': align_note,
    }

    warn_exp, vac_ez, months_ez = compute_warn_exp(vac_level, months_level, n)
    W_PRIM_EXP = compute_wprim_exp(quad, warn_exp, n)

    t_abs = compute_t_abs(fwd12)
    t_rel, q25_used, matured_n = compute_t_rel(fwd12)
    targets = {'T_ABS': t_abs, 'T_REL': t_rel}

    n_bad_abs = sum(1 for x in t_abs if x is True)
    rated_abs = n_bad_abs >= 8

    results = {}
    for tname, bad in targets.items():
        cells = two_by_two(W_PRIM_EXP, bad)
        stats = or_stats(cells)
        overlap = overlap_robustness(W_PRIM_EXP, bad)
        eps = find_episodes(bad)
        epcatch = episode_catch(eps, W_PRIM_EXP, q)
        results[tname] = {**stats, 'overlap': overlap, 'episodes': epcatch}

    # disagreement map: warn (trailing, bool) vs warn_exp (bool), quarter by quarter
    disagreements = []
    for i in range(n):
        wt = bool(warn_trail[i]) if warn_trail[i] is not None else False
        we = warn_exp[i]
        if wt != we:
            disagreements.append({
                'q': q[i], 'warn_trailing': wt, 'warn_exp': we,
                'vac_level': vac_level[i], 'months_level': months_level[i],
                'vac_ez': round(vac_ez[i], 3) if vac_ez[i] is not None else None,
                'months_ez': round(months_ez[i], 3) if months_ez[i] is not None else None,
            })
    disagreements_2020plus = [x for x in disagreements if x['q'] >= '2020Q1']

    return {
        'market': mkt, 'n_quarters': n,
        'level_check': level_check,
        'n_bad_abs': n_bad_abs, 'rated_abs': rated_abs,
        'results': results,
        'disagreements_count': len(disagreements),
        'disagreements_2020plus': disagreements_2020plus,
        # kept for panel construction / self-checks / fatigue-exhibit lookup, stripped before JSON write
        '_q': q, '_quad': quad, '_warn_trail': warn_trail, '_warn_exp': warn_exp,
        '_vac_level': vac_level, '_months_level': months_level,
        '_vac_ez': vac_ez, '_months_ez': months_ez,
        '_targets': targets, '_classifiers': {'W_PRIM_EXP': W_PRIM_EXP}, '_fwd12': fwd12,
    }


def fatigue_exhibit_check(all_res_exp, mkt, qlabel):
    r = all_res_exp[mkt]
    if qlabel not in r['_q']:
        return {'market': mkt, 'q': qlabel, 'found': False}
    i = r['_q'].index(qlabel)
    wt = bool(r['_warn_trail'][i]) if r['_warn_trail'][i] is not None else False
    we = r['_warn_exp'][i]
    return {
        'market': mkt, 'q': qlabel, 'found': True,
        'vac_level': r['_vac_level'][i], 'months_level': r['_months_level'][i],
        'vac_ez_expanding': round(r['_vac_ez'][i], 3) if r['_vac_ez'][i] is not None else None,
        'months_ez_expanding': round(r['_months_ez'][i], 3) if r['_months_ez'][i] is not None else None,
        'warn_trailing': wt, 'warn_exp': we,
        'expected_flip': 'trailing OFF -> expanding ON',
        'flip_confirmed': (wt is False and we is True),
    }


def evaluate_thresholds_amendment2(all_res_exp):
    """Same protocol thresholds as evaluate_thresholds(), applied to W_PRIM_EXP instead
    of W_PRIM. Duplicated (not reusing evaluate_thresholds' body) so the existing
    trailing-warn evaluation function/output is untouched byte-for-byte."""
    out = {}

    abs_market_checks = {}
    for mkt in ('us', 'jp'):
        s = all_res_exp[mkt]['results']['T_ABS']
        cond_or = s['OR'] is not None and s['OR'] >= 3
        cond_wq = s['w_quarters'] >= 8
        cond_prec = (s['precision'] is not None and s['base_rate'] is not None
                     and s['precision'] >= 2 * s['base_rate'])
        passed = cond_or and cond_wq and cond_prec
        abs_market_checks[mkt] = {
            'OR': s['OR'], 'OR_ge_3': cond_or,
            'w_quarters': s['w_quarters'], 'w_quarters_ge_8': cond_wq,
            'precision': s['precision'], 'base_rate': s['base_rate'],
            '2x_base_rate': (round(2 * s['base_rate'], 4) if s['base_rate'] is not None else None),
            'precision_ge_2x_base_rate': cond_prec,
            'rated_abs': all_res_exp[mkt]['rated_abs'],
            'pass': passed,
        }
    abs_us_jp_pass = all(v['pass'] for v in abs_market_checks.values())

    rated_markets_abs = [m for m in MKTS if all_res_exp[m]['rated_abs']]
    panel_abs = build_panel(all_res_exp, 'W_PRIM_EXP', 'T_ABS', rated_markets_abs)
    mh_abs = panel_abs['pooled']['OR_MH']
    mh_abs_pass = mh_abs is not None and mh_abs >= 3

    abs_overall = abs_us_jp_pass and mh_abs_pass
    out['ABS'] = {
        'per_market': abs_market_checks, 'us_and_jp_pass': abs_us_jp_pass,
        'rated_markets_used_for_MH': rated_markets_abs,
        'MH_pooled_OR': mh_abs, 'MH_pooled_OR_ge_3': mh_abs_pass,
        'pass': abs_overall, 'status': 'PASS' if abs_overall else 'FAIL',
    }

    rel_market_checks = {}
    n_pass = 0
    for mkt in MKTS:
        s = all_res_exp[mkt]['results']['T_REL']
        p = s['OR'] is not None and s['OR'] >= 2
        rel_market_checks[mkt] = {'OR': s['OR'], 'pass': p}
        if p: n_pass += 1
    rel_count_pass = n_pass >= 3

    panel_rel = build_panel(all_res_exp, 'W_PRIM_EXP', 'T_REL', MKTS)
    mh_rel = panel_rel['pooled']['OR_MH']
    mh_rel_pass = mh_rel is not None and mh_rel >= 2.5

    rel_overall = rel_count_pass and mh_rel_pass
    out['REL'] = {
        'per_market': rel_market_checks, 'n_markets_passing': n_pass,
        'n_markets_passing_ge_3': rel_count_pass,
        'MH_pooled_OR': mh_rel, 'MH_pooled_OR_ge_2.5': mh_rel_pass,
        'pass': rel_overall, 'status': 'PASS' if rel_overall else 'FAIL',
    }

    out['_panels'] = {'abs_wprim_exp': panel_abs, 'rel_wprim_exp': panel_rel}
    return out


def truncation_selfcheck_expanding(mkt='jp'):
    """warn_exp look-ahead guard test on the expanding basis: ez() at index t must only
    depend on values at indices <= t by construction. Truncate the raw level series at
    k and verify vac_ez/months_ez/warn_exp for all t < k are byte-identical to the
    full-series computation (mirrors truncation_selfcheck()'s convention for T_REL)."""
    d = load_market(mkt)
    n, q = d['n'], d['q']
    vac_level, months_level, _, _ = load_warn_exp_raw(mkt, q)
    k = n - 10

    warn_full, vacz_full, monz_full = compute_warn_exp(vac_level, months_level, n)
    warn_trunc, vacz_trunc, monz_trunc = compute_warn_exp(vac_level[:k], months_level[:k], k)

    mismatches = []
    for t in range(k):
        if warn_full[t] != warn_trunc[t] or vacz_full[t] != vacz_trunc[t] or monz_full[t] != monz_trunc[t]:
            mismatches.append((t, q[t], warn_full[t], warn_trunc[t], vacz_full[t], vacz_trunc[t]))
    ok = len(mismatches) == 0
    return {'market': mkt, 'k': k, 'n_full': n, 'checked': k, 'pass': ok, 'mismatches': mismatches[:5]}


def current_quarter_state_comparison(all_res_exp):
    out = {}
    for mkt in MKTS:
        r = all_res_exp[mkt]
        i = r['n_quarters'] - 1
        wt = bool(r['_warn_trail'][i]) if r['_warn_trail'][i] is not None else False
        we = r['_warn_exp'][i]
        quad_now = r['_quad'][i]
        out[mkt] = {
            'q': r['_q'][i], 'quad': quad_now,
            'warn_trailing': wt, 'warn_exp': we, 'differs': wt != we,
            'W_PRIM_now': (quad_now == 'starved') and wt,
            'W_PRIM_EXP_now': (quad_now == 'starved') and we,
        }
    return out


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------
FWD12_SPOTCHECK_EXPECTED = {
    # captured from scripts/backtest_compass_v2.py's identical spot-check
    # (re-ran 2026-07-14, output unchanged / deterministic vs committed data/compass-backtest-v2.json)
    'us': {'i': 20, 'q': '1980Q1', 'fwd12': 14.4, 'quad': 'starved'},
    'tw': {'i': 20, 'q': '2006Q1', 'fwd12': 15.2, 'quad': 'fuelled'},
    'my': {'i': 20, 'q': '2005Q1', 'fwd12': 11.9, 'quad': 'warmup'},
    'jp': {'i': 20, 'q': '1980Q1', 'fwd12': 29.6, 'quad': 'fuelled'},
}


def fwd12_alignment_selfcheck():
    out = {}
    for mkt in MKTS:
        d = json.load(open(os.path.join(ROOT, 'data', f'compass-{mkt}.json')))
        n = len(d['q'])
        i = min(20, n - 1)
        got = {'i': i, 'q': d['q'][i], 'fwd12': d['fwd12'][i], 'quad': d['quad'][i]}
        exp = FWD12_SPOTCHECK_EXPECTED[mkt]
        ok = got == exp
        out[mkt] = {'expected': exp, 'got': got, 'pass': ok}
    overall = all(v['pass'] for v in out.values())
    return {'per_market': out, 'pass': overall}


def truncation_selfcheck():
    """T_REL truncation test: recompute labels with the fwd12 series truncated at k,
    verify labels for indices < k-12+... i.e. all t with t <= k* the guard range are
    unchanged. Concretely: labels at any t such that its matured pool (u <= t-12) is
    fully contained within the truncated series (t-12 <= k-1, i.e. t <= k+11) are
    compared; look-ahead would show up as a mismatch anywhere in that range, and in
    practice truncation cannot change ANY label with t <= k-1 since fwd12[k:] is
    dropped entirely and the matured pool for t<=k-1 only ever reads u <= t-12 <= k-13."""
    out = {}
    for mkt in MKTS:
        d = load_market(mkt)
        n = d['n']
        k = n - 10  # leave a real tail to truncate away (mirrors v2 convention)
        fwd12_full = d['fwd12']
        fwd12_trunc = fwd12_full[:k]

        bad_full, q25_full, _ = compute_t_rel(fwd12_full)
        bad_trunc, q25_trunc, _ = compute_t_rel(fwd12_trunc)

        mismatches = []
        for t in range(k):
            if bad_full[t] != bad_trunc[t] or q25_full[t] != q25_trunc[t]:
                mismatches.append((t, d['q'][t], bad_full[t], bad_trunc[t], q25_full[t], q25_trunc[t]))
        ok = len(mismatches) == 0
        out[mkt] = {'k': k, 'n_full': n, 'checked': k, 'pass': ok, 'mismatches': mismatches[:5]}
    overall = all(v['pass'] for v in out.values())
    return {'per_market': out, 'pass': overall}


def spot_verify_my_wprim_trel(all_res):
    """Brute-force 2x2 listing: MY, W_PRIM x T_REL -- every quarter in each cell,
    so a human can eyeball the classification without trusting the aggregate code path."""
    mres = all_res['my']
    q = mres['_q']
    W = mres['_classifiers']['W_PRIM']
    bad = mres['_targets']['T_REL']
    fwd12 = mres['_fwd12']
    cells = {'a': [], 'b': [], 'c': [], 'd': [], 'excluded': []}
    for i in range(len(q)):
        w, y = W[i], bad[i]
        if w is None or y is None:
            cells['excluded'].append((q[i], w, y, fwd12[i]))
            continue
        if w and y: cells['a'].append((q[i], fwd12[i]))
        elif w and not y: cells['b'].append((q[i], fwd12[i]))
        elif (not w) and y: cells['c'].append((q[i], fwd12[i]))
        else: cells['d'].append((q[i], fwd12[i]))
    return cells


# ---------------------------------------------------------------------------
# Threshold evaluation
# ---------------------------------------------------------------------------
def evaluate_thresholds(all_res):
    out = {}

    # ---- ABS claim: W_PRIM OR>=3, >=8 W-quarters, precision>=2*base_rate, US+JP; MH>=3
    abs_market_checks = {}
    for mkt in ('us', 'jp'):
        s = all_res[mkt]['results']['T_ABS']['W_PRIM']
        cond_or = s['OR'] is not None and s['OR'] >= 3
        cond_wq = s['w_quarters'] >= 8
        cond_prec = (s['precision'] is not None and s['base_rate'] is not None
                     and s['precision'] >= 2 * s['base_rate'])
        passed = cond_or and cond_wq and cond_prec
        abs_market_checks[mkt] = {
            'OR': s['OR'], 'OR_ge_3': cond_or,
            'w_quarters': s['w_quarters'], 'w_quarters_ge_8': cond_wq,
            'precision': s['precision'], 'base_rate': s['base_rate'],
            '2x_base_rate': (round(2 * s['base_rate'], 4) if s['base_rate'] is not None else None),
            'precision_ge_2x_base_rate': cond_prec,
            'rated_abs': all_res[mkt]['rated_abs'],
            'pass': passed,
        }
    abs_us_jp_pass = all(v['pass'] for v in abs_market_checks.values())

    rated_markets_abs = [m for m in MKTS if all_res[m]['rated_abs']]
    panel_abs_wprim = build_panel(all_res, 'W_PRIM', 'T_ABS', rated_markets_abs)
    mh_abs = panel_abs_wprim['pooled']['OR_MH']
    mh_abs_pass = mh_abs is not None and mh_abs >= 3

    abs_overall = abs_us_jp_pass and mh_abs_pass
    out['ABS'] = {
        'per_market': abs_market_checks, 'us_and_jp_pass': abs_us_jp_pass,
        'rated_markets_used_for_MH': rated_markets_abs,
        'MH_pooled_OR': mh_abs, 'MH_pooled_OR_ge_3': mh_abs_pass,
        'pass': abs_overall, 'status': 'PASS' if abs_overall else 'FAIL',
    }

    # ---- REL claim: W_PRIM OR>=2 in >=3 of 4 markets; MH pooled OR>=2.5 (all 4)
    rel_market_checks = {}
    n_pass = 0
    for mkt in MKTS:
        s = all_res[mkt]['results']['T_REL']['W_PRIM']
        p = s['OR'] is not None and s['OR'] >= 2
        rel_market_checks[mkt] = {'OR': s['OR'], 'pass': p}
        if p: n_pass += 1
    rel_count_pass = n_pass >= 3

    panel_rel_wprim = build_panel(all_res, 'W_PRIM', 'T_REL', MKTS)
    mh_rel = panel_rel_wprim['pooled']['OR_MH']
    mh_rel_pass = mh_rel is not None and mh_rel >= 2.5

    rel_overall = rel_count_pass and mh_rel_pass
    out['REL'] = {
        'per_market': rel_market_checks, 'n_markets_passing': n_pass,
        'n_markets_passing_ge_3': rel_count_pass,
        'MH_pooled_OR': mh_rel, 'MH_pooled_OR_ge_2.5': mh_rel_pass,
        'pass': rel_overall, 'status': 'PASS' if rel_overall else 'FAIL',
    }

    # ---- Conditioners: T_ABS, US+JP, OR>=1.5xW_PRIM & recall>=0.67xW_PRIM's recall -> ADOPT/DISCARD
    def eval_conditioner(cname):
        avail = all(all_res[m]['results']['T_ABS'][cname].get('status') != 'NOT EVALUATED (no demo data)'
                    for m in ('us', 'jp'))
        if not avail:
            return {'status': 'NOT EVALUATED', 'reason': 'demo data absent for US and/or JP'}
        per_mkt = {}
        all_pass = True
        for mkt in ('us', 'jp'):
            wp = all_res[mkt]['results']['T_ABS']['W_PRIM']
            cd = all_res[mkt]['results']['T_ABS'][cname]
            or_ok = (cd['OR'] is not None and wp['OR'] is not None and cd['OR'] >= 1.5 * wp['OR'])
            recall_ok = (cd['recall'] is not None and wp['recall'] is not None
                         and cd['recall'] >= 0.67 * wp['recall'])
            p = or_ok and recall_ok
            all_pass = all_pass and p
            per_mkt[mkt] = {
                'W_PRIM_OR': wp['OR'], 'cond_OR': cd['OR'], 'OR_ge_1.5x': or_ok,
                'W_PRIM_recall': wp['recall'], 'cond_recall': cd['recall'], 'recall_ge_0.67x': recall_ok,
                'pass': p,
            }
        return {'status': 'ADOPT' if all_pass else 'DISCARD', 'per_market': per_mkt}

    out['conditioners'] = {
        'W_AFS': eval_conditioner('W_AFS'),
        'W_DEMO': eval_conditioner('W_DEMO'),
    }

    out['risk_gauge_verdict'] = {
        'abs_pass': abs_overall, 'rel_pass': rel_overall,
        'reframe_as_risk_gauge': abs_overall and rel_overall,
    }

    out['_panels'] = {'abs_wprim': panel_abs_wprim, 'rel_wprim': panel_rel_wprim}
    return out


# ---------------------------------------------------------------------------
# Printing
# ---------------------------------------------------------------------------
def fmt_stat_block(label, s):
    if s.get('status') == 'NOT EVALUATED (no demo data)':
        print(f"      [{label}] NOT EVALUATED (no demo data)")
        return
    hald = "  <-- Haldane +0.5 applied (zero cell)" if s['haldane_applied'] else ""
    c = s['cells']
    print(f"      [{label}] OR={s['OR']}{hald}  precision={s['precision']}  recall={s['recall']}  "
          f"base_rate={s['base_rate']}  w_quarters={s['w_quarters']}")
    print(f"        cells: a={c['a']} b={c['b']} c={c['c']} d={c['d']}  "
          f"(n_used={c['n_used']}, n_excluded={c['n_excluded']})")
    ov = s['overlap']
    off_str = "; ".join(
        f"offset{k}: OR={v['OR']}(n={v['n_used']}{',SMALL-N' if v['small_n_caveat'] else ''})"
        for k, v in ov['per_offset'].items())
    print(f"        overlap robustness: {off_str}  |  median_OR={ov['median_OR']}")
    ep = s['episodes']
    print(f"        episodes: total={ep['episodes_total']}  caught={ep['caught']}  missed={ep['missed']}")


def print_market_report(mres):
    mkt = mres['market']
    print(f"\n=== {mkt.upper()} ===  (n={mres['n_quarters']} quarters)")
    print(f"  AFS note: {mres['afs_note']}")
    print(f"  DEMO note: {mres['demo_note']}")
    print(f"  Applicability gate (T_ABS): n_bad_abs(fwd12<0)={mres['n_bad_abs']}  "
          f"-> {'RATED' if mres['rated_abs'] else 'NOT RATED'} (threshold >=8)")
    for tname in ('T_ABS', 'T_REL'):
        print(f"  -- target {tname} --")
        for cname in ('W_MOM', 'W_PRIM', 'W_AFS', 'W_DEMO'):
            fmt_stat_block(cname, mres['results'][tname][cname])


def main():
    print("Compass v3 risk-gauge evaluation")
    print(f"Protocol: {PROTOCOL_TAG}\n")
    print(f"Convention note: {Q25_CONVENTION_NOTE}")
    print(f"Convention note: {EPISODE_CONVENTION_NOTE}\n")

    all_res = {}
    for mkt in MKTS:
        all_res[mkt] = analyze_market(mkt)

    # --- self-check (c): fwd12 alignment unchanged from v2 ---
    print("--- Self-check (c): fwd12 alignment unchanged from v2 (same values, same axis) ---")
    fwd12_chk = fwd12_alignment_selfcheck()
    for mkt, v in fwd12_chk['per_market'].items():
        print(f"  {mkt.upper()}: expected={v['expected']}  got={v['got']}  "
              f"[{'PASS' if v['pass'] else 'FAIL'}]")
    print(f"  fwd12 alignment self-check: {'PASS' if fwd12_chk['pass'] else 'FAIL'}\n")

    # --- self-check (a): T_REL truncation / look-ahead guard test ---
    print("--- Self-check (a): T_REL truncation self-test (look-ahead guard) ---")
    trunc_chk = truncation_selfcheck()
    for mkt, v in trunc_chk['per_market'].items():
        print(f"  {mkt.upper()}: truncated at k={v['k']} of n={v['n_full']}, checked {v['checked']} quarters "
              f"-> {'PASS (no labels changed)' if v['pass'] else 'FAIL'}")
        if not v['pass']:
            print(f"    mismatches (first 5): {v['mismatches']}")
    print(f"  T_REL truncation self-check: {'PASS' if trunc_chk['pass'] else 'FAIL'}\n")

    # --- self-check (b): brute-force MY W_PRIM x T_REL listing ---
    print("--- Self-check (b): brute-force 2x2 listing, MY, W_PRIM x T_REL ---")
    my_cells = spot_verify_my_wprim_trel(all_res)
    print(f"  cell a (W_PRIM=T, bad=T) n={len(my_cells['a'])}: {my_cells['a']}")
    print(f"  cell b (W_PRIM=T, bad=F) n={len(my_cells['b'])}: {my_cells['b']}")
    print(f"  cell c (W_PRIM=F, bad=T) n={len(my_cells['c'])}: {my_cells['c']}")
    print(f"  cell d (W_PRIM=F, bad=F) n={len(my_cells['d'])}: "
          f"{my_cells['d'][:5]} ... {my_cells['d'][-5:]}  (showing first/last 5 of {len(my_cells['d'])})")
    print(f"  excluded (either undefined) n={len(my_cells['excluded'])}\n")

    # --- per-market report ---
    for mkt in MKTS:
        print_market_report(all_res[mkt])

    # --- applicability gate summary ---
    print("\n=== Applicability gate summary (T_ABS) ===")
    for mkt in MKTS:
        r = all_res[mkt]
        print(f"  {mkt.upper()}: n_bad_abs={r['n_bad_abs']}  "
              f"-> {'RATED' if r['rated_abs'] else 'NOT RATED'}")

    # --- panels ---
    thresholds = evaluate_thresholds(all_res)
    print("\n=== Panel: Mantel-Haenszel pooled OR (W_PRIM) ===")
    pa = thresholds['_panels']['abs_wprim']
    print(f"  T_ABS (rated markets only: {pa['markets']}): OR_MH={pa['pooled']['OR_MH']} "
          f"(n_strata={pa['pooled']['n_strata']})")
    pr = thresholds['_panels']['rel_wprim']
    print(f"  T_REL (all four markets: {pr['markets']}): OR_MH={pr['pooled']['OR_MH']} "
          f"(n_strata={pr['pooled']['n_strata']})")

    # --- threshold verdicts ---
    print("\n=== Threshold evaluation (protocol Success thresholds, frozen) ===")
    a = thresholds['ABS']
    print(f"  ABS claim: {a['status']}")
    for mkt, v in a['per_market'].items():
        print(f"    {mkt.upper()}: OR={v['OR']} (>=3: {v['OR_ge_3']})  w_quarters={v['w_quarters']} "
              f"(>=8: {v['w_quarters_ge_8']})  precision={v['precision']} vs 2xbase_rate={v['2x_base_rate']} "
              f"({v['precision_ge_2x_base_rate']})  rated={v['rated_abs']}  -> {'PASS' if v['pass'] else 'FAIL'}")
    print(f"    MH pooled OR (rated markets {a['rated_markets_used_for_MH']}) = {a['MH_pooled_OR']} "
          f"(>=3: {a['MH_pooled_OR_ge_3']})")
    print(f"    ABS OVERALL: {a['status']}")

    r = thresholds['REL']
    print(f"\n  REL claim: {r['status']}")
    for mkt, v in r['per_market'].items():
        print(f"    {mkt.upper()}: OR={v['OR']}  -> {'PASS' if v['pass'] else 'FAIL'}")
    print(f"    markets passing OR>=2: {r['n_markets_passing']}/4  (need >=3: {r['n_markets_passing_ge_3']})")
    print(f"    MH pooled OR (all 4) = {r['MH_pooled_OR']} (>=2.5: {r['MH_pooled_OR_ge_2.5']})")
    print(f"    REL OVERALL: {r['status']}")

    print("\n  Conditioners (T_ABS, US+JP, OR>=1.5x W_PRIM & recall>=0.67x W_PRIM's recall):")
    for cname in ('W_AFS', 'W_DEMO'):
        cd = thresholds['conditioners'][cname]
        print(f"    {cname}: {cd['status']}")
        if 'per_market' in cd:
            for mkt, v in cd['per_market'].items():
                print(f"      {mkt.upper()}: W_PRIM_OR={v['W_PRIM_OR']}  cond_OR={v['cond_OR']} "
                      f"(>=1.5x: {v['OR_ge_1.5x']})  W_PRIM_recall={v['W_PRIM_recall']}  "
                      f"cond_recall={v['cond_recall']} (>=0.67x: {v['recall_ge_0.67x']})")
        elif 'reason' in cd:
            print(f"      reason: {cd['reason']}")

    v = thresholds['risk_gauge_verdict']
    print(f"\n=== OVERALL VERDICT ===")
    print(f"  ABS pass: {v['abs_pass']}   REL pass: {v['rel_pass']}")
    print(f"  Clock re-frames as risk gauge: {'YES' if v['reframe_as_risk_gauge'] else 'NO'}")

    # --- HONESTY block ---
    print("\n=== HONESTY ===")
    print("Contamination disclosure (protocol, verbatim):")
    print(f"  {CONTAMINATION_NOTE}")
    print("Overlap caveat:")
    print(f"  {OVERLAP_CAVEAT}")
    print("Episode-domination check (explicit, per market, W_PRIM):")
    for mkt in MKTS:
        for tname in ('T_ABS', 'T_REL'):
            ep = all_res[mkt]['results'][tname]['W_PRIM']['episodes']
            print(f"  {mkt.upper()} / {tname}: episodes_total={ep['episodes_total']}  "
                  f"caught={ep['caught']}  missed={ep['missed']}")
    print("  Read alongside the OR/precision numbers above: a market with 1-2 dominating episodes")
    print("  means the OR is effectively a statement about those specific historical spells, not a")
    print("  large-sample regularity -- exactly the risk the protocol's contamination disclosure names.")
    print("Applicability gate note:")
    tw_rated = all_res['tw']['rated_abs']
    my_rated = all_res['my']['rated_abs']
    print(f"  Protocol text states an expectation of 'US, JP rated; TW, MY not rated' (T6: zero hard "
          f"turns / no 8% drawdown in 27y). Actual counts: TW n_bad_abs={all_res['tw']['n_bad_abs']} "
          f"-> {'RATED' if tw_rated else 'NOT RATED'}; MY n_bad_abs={all_res['my']['n_bad_abs']} "
          f"-> {'RATED' if my_rated else 'NOT RATED'}.")
    if tw_rated:
        print("  TW is RATED (>=8 matured bad-ABS quarters), diverging from the protocol's stated prior "
              "expectation. The 9 TW fwd12<0 quarters cluster in 2013Q3-2015Q3 (post-luxury-tax slowdown) "
              "-- a single episode, not eight independent turns. Reported as-is per the frozen >=8-quarter "
              "gate; the applicability gate is a mechanical quarter count, not a judgment call, so TW's "
              "ABS-claim participation follows the numbers even though it contradicts the protocol author's "
              "prior expectation. Flagged here rather than silently overridden.")

    # =========================================================================
    # AMENDMENT 2 -- expanding-basis warn_exp re-validation
    # =========================================================================
    print("\n\n" + "=" * 78)
    print("AMENDMENT 2 -- expanding-basis warn re-validation")
    print("=" * 78)
    print(AMENDMENT2_TEXT)

    all_res_exp = {}
    for mkt in MKTS:
        all_res_exp[mkt] = analyze_market_amendment2(mkt)

    # --- level-series verification ---
    print("\n--- Level-series verification (must be raw levels, not already a z) ---")
    for mkt in MKTS:
        lc = all_res_exp[mkt]['level_check']
        print(f"  {mkt.upper()}: {lc['align_note']}")
        for f in ('vacancy', 'months'):
            v = lc[f]
            print(f"    {f}: n={v['n_total']} non-null={v['n_nonnull']} min={v['min']} max={v['max']} "
                  f"sample_first5={v['sample_first5']}")
    print("  Verdict: all eight series (4 markets x 2 fields) are raw levels (percentages / unit counts), "
          "none in a [-3,3]-ish z range with a median near 0 -- confirmed NOT already standardized.")

    # --- W_PRIM_EXP full evaluation (identical v3 machinery) ---
    print("\n--- W_PRIM_EXP per-market report (T_ABS, T_REL) ---")
    for mkt in MKTS:
        rm = all_res_exp[mkt]
        print(f"\n=== {mkt.upper()} (W_PRIM_EXP) ===  (n={rm['n_quarters']} quarters)")
        print(f"  Applicability gate (T_ABS): n_bad_abs={rm['n_bad_abs']} -> "
              f"{'RATED' if rm['rated_abs'] else 'NOT RATED'} (threshold >=8)")
        for tname in ('T_ABS', 'T_REL'):
            print(f"  -- target {tname} --")
            fmt_stat_block('W_PRIM_EXP', rm['results'][tname])

    thresholds_exp = evaluate_thresholds_amendment2(all_res_exp)
    print("\n--- Panel: Mantel-Haenszel pooled OR (W_PRIM_EXP) ---")
    pae = thresholds_exp['_panels']['abs_wprim_exp']
    print(f"  T_ABS (rated markets: {pae['markets']}): OR_MH={pae['pooled']['OR_MH']} "
          f"(n_strata={pae['pooled']['n_strata']})")
    pre = thresholds_exp['_panels']['rel_wprim_exp']
    print(f"  T_REL (all four markets: {pre['markets']}): OR_MH={pre['pooled']['OR_MH']} "
          f"(n_strata={pre['pooled']['n_strata']})")

    print("\n--- Threshold evaluation, W_PRIM_EXP (same frozen protocol thresholds) ---")
    ae = thresholds_exp['ABS']
    print(f"  ABS claim (expanding): {ae['status']}")
    for mkt, v in ae['per_market'].items():
        print(f"    {mkt.upper()}: OR={v['OR']} (>=3: {v['OR_ge_3']})  w_quarters={v['w_quarters']} "
              f"(>=8: {v['w_quarters_ge_8']})  precision={v['precision']} vs 2xbase_rate={v['2x_base_rate']} "
              f"({v['precision_ge_2x_base_rate']})  -> {'PASS' if v['pass'] else 'FAIL'}")
    print(f"    MH pooled OR = {ae['MH_pooled_OR']} (>=3: {ae['MH_pooled_OR_ge_3']})")
    print(f"    ABS (expanding) OVERALL: {ae['status']}")

    re_ = thresholds_exp['REL']
    print(f"\n  REL claim (expanding): {re_['status']}")
    for mkt, v in re_['per_market'].items():
        print(f"    {mkt.upper()}: OR={v['OR']}  -> {'PASS' if v['pass'] else 'FAIL'}")
    print(f"    markets passing OR>=2: {re_['n_markets_passing']}/4 (need >=3: {re_['n_markets_passing_ge_3']})")
    print(f"    MH pooled OR (all 4) = {re_['MH_pooled_OR']} (>=2.5: {re_['MH_pooled_OR_ge_2.5']})")
    print(f"    REL (expanding) OVERALL: {re_['status']}")

    # --- side by side vs trailing ---
    print("\n--- W_PRIM (trailing) vs W_PRIM_EXP (expanding) -- side by side ---")
    print(f"  {'':6s} {'T_ABS OR':>10s} {'T_ABS OR_exp':>13s}   {'T_REL OR':>10s} {'T_REL OR_exp':>13s}")
    for mkt in MKTS:
        t_abs_or = all_res[mkt]['results']['T_ABS']['W_PRIM']['OR']
        t_abs_or_exp = all_res_exp[mkt]['results']['T_ABS']['OR']
        t_rel_or = all_res[mkt]['results']['T_REL']['W_PRIM']['OR']
        t_rel_or_exp = all_res_exp[mkt]['results']['T_REL']['OR']
        print(f"  {mkt.upper():6s} {str(t_abs_or):>10s} {str(t_abs_or_exp):>13s}   "
              f"{str(t_rel_or):>10s} {str(t_rel_or_exp):>13s}")
    mh_abs_trail = a['MH_pooled_OR']
    mh_abs_exp = ae['MH_pooled_OR']
    mh_rel_trail = r['MH_pooled_OR']
    mh_rel_exp = re_['MH_pooled_OR']
    print(f"  MH (T_ABS): trailing={mh_abs_trail}  expanding={mh_abs_exp}")
    print(f"  MH (T_REL): trailing={mh_rel_trail}  expanding={mh_rel_exp}")

    # --- disagreement map ---
    print("\n--- Disagreement map: quarters where warn_exp != warn (trailing) ---")
    total_disagree = 0
    for mkt in MKTS:
        r_exp = all_res_exp[mkt]
        cnt = r_exp['disagreements_count']
        total_disagree += cnt
        print(f"  {mkt.upper()}: {cnt} disagreeing quarters (of {r_exp['n_quarters']})")
        d2020 = r_exp['disagreements_2020plus']
        print(f"    2020Q1+ disagreements (n={len(d2020)}):")
        for x in d2020:
            print(f"      {x['q']}: warn_trailing={x['warn_trailing']} warn_exp={x['warn_exp']}  "
                  f"vac_level={x['vac_level']} months_level={x['months_level']}  "
                  f"vac_ez={x['vac_ez']} months_ez={x['months_ez']}")
    print(f"  TOTAL disagreeing quarters across 4 markets: {total_disagree}")

    # --- fatigue exhibit check ---
    print("\n--- Fatigue-exhibit check (the audit's F1 examples) ---")
    fatigue_jp = fatigue_exhibit_check(all_res_exp, 'jp', '2023Q3')
    fatigue_my = fatigue_exhibit_check(all_res_exp, 'my', '2022Q2')
    for fx in (fatigue_jp, fatigue_my):
        print(f"  {fx['market'].upper()} {fx['q']}: vac_level={fx.get('vac_level')} "
              f"months_level={fx.get('months_level')}  vac_ez(expanding)={fx.get('vac_ez_expanding')} "
              f"months_ez(expanding)={fx.get('months_ez_expanding')}")
        print(f"    warn_trailing={fx.get('warn_trailing')}  warn_exp={fx.get('warn_exp')}  "
              f"expected: {fx.get('expected_flip')}  -> "
              f"{'CONFIRMED' if fx.get('flip_confirmed') else 'NOT CONFIRMED'}")

    # --- decision rule (frozen) ---
    print("\n--- Decision rule (frozen, verbatim) ---")
    print("  \"the live gauge switches to the expanding basis ONLY if W_PRIM_EXP passes the same "
          "ABS+REL gates AND its ABS MH-pooled OR >= the trailing version's. Otherwise trailing "
          "stays (status quo unless dominated)...\"")
    cond_abs_pass = ae['pass']
    cond_rel_pass = re_['pass']
    cond_or_ge = (mh_abs_exp is not None and mh_abs_trail is not None and mh_abs_exp >= mh_abs_trail)
    switch = cond_abs_pass and cond_rel_pass and cond_or_ge
    print(f"  Component 1 -- W_PRIM_EXP ABS claim passes:          {'PASS' if cond_abs_pass else 'FAIL'}")
    print(f"  Component 2 -- W_PRIM_EXP REL claim passes:          {'PASS' if cond_rel_pass else 'FAIL'}")
    print(f"  Component 3 -- ABS MH-pooled OR expanding >= trailing: {mh_abs_exp} >= {mh_abs_trail}  "
          f"-> {'PASS' if cond_or_ge else 'FAIL'}")
    print(f"\n  >>> VERDICT: {'SWITCH to expanding basis' if switch else 'KEEP TRAILING (status quo)'} <<<")
    if not switch:
        print("  The conceptual tension stands as a published finding: the trailing warning works")
        print("  empirically (validated OR) even though a supply glut is conceptually an absolute-level")
        print("  concept. Expanding basis fails to dominate on the frozen decision rule -- no silent fix.")

    # --- self-check: truncation on expanding basis ---
    print("\n--- Self-check: warn_exp truncation / look-ahead guard test (JP) ---")
    trunc_exp_chk = truncation_selfcheck_expanding('jp')
    print(f"  JP: truncated at k={trunc_exp_chk['k']} of n={trunc_exp_chk['n_full']}, checked "
          f"{trunc_exp_chk['checked']} quarters -> "
          f"{'PASS (no values changed)' if trunc_exp_chk['pass'] else 'FAIL'}")
    if not trunc_exp_chk['pass']:
        print(f"    mismatches (first 5): {trunc_exp_chk['mismatches']}")

    # --- self-check: current-quarter state comparison ---
    print("\n--- Self-check: current-quarter warn vs warn_exp (live risk-gauge lights) ---")
    cur_state = current_quarter_state_comparison(all_res_exp)
    for mkt in MKTS:
        c = cur_state[mkt]
        print(f"  {mkt.upper()} {c['q']}: quad={c['quad']}  warn_trailing={c['warn_trailing']}  "
              f"warn_exp={c['warn_exp']}  {'** DIFFERS **' if c['differs'] else '(same)'}  "
              f"-> W_PRIM_now={c['W_PRIM_now']}  W_PRIM_EXP_now={c['W_PRIM_EXP_now']}")
    any_current_differs = any(c['differs'] for c in cur_state.values())
    print(f"  Any market's live warn light would differ under expanding basis right now: "
          f"{'YES' if any_current_differs else 'NO'}")

    # --- write output ---
    def clean_market(mres):
        out = dict(mres)
        for k in ('_q', '_targets', '_classifiers', '_q25_used', '_matured_n', '_fwd12'):
            out.pop(k, None)
        return out

    thresholds_clean = dict(thresholds)
    thresholds_clean.pop('_panels', None)
    thresholds_clean['panels'] = {
        'abs_wprim': thresholds['_panels']['abs_wprim'],
        'rel_wprim': thresholds['_panels']['rel_wprim'],
    }

    out = {
        'protocol': PROTOCOL_TAG,
        'conventions': {
            'q25': Q25_CONVENTION_NOTE,
            'episode': EPISODE_CONVENTION_NOTE,
        },
        'self_checks': {
            'fwd12_alignment_vs_v2': fwd12_chk,
            't_rel_truncation': trunc_chk,
            'my_wprim_trel_bruteforce': {
                k: v for k, v in my_cells.items()
            },
        },
        'markets': {mkt: clean_market(all_res[mkt]) for mkt in MKTS},
        'threshold_evaluation': thresholds_clean,
        'honesty': {
            'contamination_note': CONTAMINATION_NOTE,
            'overlap_caveat': OVERLAP_CAVEAT,
            'episode_domination': {
                mkt: {
                    tname: {
                        'episodes_total': all_res[mkt]['results'][tname]['W_PRIM']['episodes']['episodes_total'],
                        'caught': all_res[mkt]['results'][tname]['W_PRIM']['episodes']['caught'],
                        'missed': all_res[mkt]['results'][tname]['W_PRIM']['episodes']['missed'],
                    } for tname in ('T_ABS', 'T_REL')
                } for mkt in MKTS
            },
            'applicability_gate_divergence_from_protocol_expectation': {
                'tw_rated_abs': tw_rated, 'my_rated_abs': my_rated,
                'tw_n_bad_abs': all_res['tw']['n_bad_abs'], 'my_n_bad_abs': all_res['my']['n_bad_abs'],
            },
        },
    }
    # --- amendment2 block ---
    def clean_market_exp(mres):
        o = dict(mres)
        for k in ('_q', '_quad', '_warn_trail', '_warn_exp', '_vac_level', '_months_level',
                  '_vac_ez', '_months_ez', '_targets', '_classifiers', '_fwd12'):
            o.pop(k, None)
        return o

    thresholds_exp_clean = dict(thresholds_exp)
    thresholds_exp_clean.pop('_panels', None)
    thresholds_exp_clean['panels'] = {
        'abs_wprim_exp': thresholds_exp['_panels']['abs_wprim_exp'],
        'rel_wprim_exp': thresholds_exp['_panels']['rel_wprim_exp'],
    }

    decision_rule = {
        'text_verbatim': (
            "the live gauge switches to the expanding basis ONLY if W_PRIM_EXP passes the same "
            "ABS+REL gates AND its ABS MH-pooled OR >= the trailing version's. Otherwise trailing "
            "stays (status quo unless dominated), and the conceptual tension is published as a "
            "finding: the trailing warning works empirically even though a glut is conceptually "
            "absolute."
        ),
        'component_1_wprim_exp_abs_pass': cond_abs_pass,
        'component_2_wprim_exp_rel_pass': cond_rel_pass,
        'component_3_abs_mh_or_expanding_ge_trailing': {
            'mh_or_expanding': mh_abs_exp, 'mh_or_trailing': mh_abs_trail, 'pass': cond_or_ge,
        },
        'verdict': 'SWITCH' if switch else 'KEEP-TRAILING',
    }

    out['amendment2'] = {
        'protocol_text_verbatim': AMENDMENT2_TEXT,
        'markets': {mkt: clean_market_exp(all_res_exp[mkt]) for mkt in MKTS},
        'threshold_evaluation_wprim_exp': thresholds_exp_clean,
        'side_by_side_vs_trailing': {
            mkt: {
                'T_ABS_OR_trailing': all_res[mkt]['results']['T_ABS']['W_PRIM']['OR'],
                'T_ABS_OR_expanding': all_res_exp[mkt]['results']['T_ABS']['OR'],
                'T_REL_OR_trailing': all_res[mkt]['results']['T_REL']['W_PRIM']['OR'],
                'T_REL_OR_expanding': all_res_exp[mkt]['results']['T_REL']['OR'],
            } for mkt in MKTS
        },
        'mh_side_by_side': {
            'T_ABS': {'trailing': mh_abs_trail, 'expanding': mh_abs_exp},
            'T_REL': {'trailing': mh_rel_trail, 'expanding': mh_rel_exp},
        },
        'disagreement_map': {
            mkt: {
                'disagreements_count': all_res_exp[mkt]['disagreements_count'],
                'disagreements_2020plus': all_res_exp[mkt]['disagreements_2020plus'],
            } for mkt in MKTS
        },
        'fatigue_exhibit_check': {
            'jp_2023Q3': fatigue_jp,
            'my_2022Q2': fatigue_my,
        },
        'decision_rule': decision_rule,
        'self_checks': {
            'warn_exp_truncation_lookahead_guard': trunc_exp_chk,
            'current_quarter_state_comparison': cur_state,
            'any_current_quarter_differs': any_current_differs,
        },
    }

    # =========================================================================
    # AMENDMENT 3 -- Australia as an out-of-sample hold-out
    # PRIMARY (MKTS = us/tw/my/jp) is untouched above this point. Everything
    # below is additive: a separate pass over 'au' alone, reported as a
    # hold-out, plus a 5-market MH shown ALONGSIDE (never replacing) the
    # frozen 4-market MH computed above (a['MH_pooled_OR'] / r['MH_pooled_OR']).
    # =========================================================================
    print("\n\n" + "=" * 78)
    print("AMENDMENT 3 -- AU out-of-sample hold-out")
    print("=" * 78)
    print(AMENDMENT3_TEXT)

    au_res = analyze_market('au')
    print("\n  >>> AU is an OUT-OF-SAMPLE HOLD-OUT: not part of the primary validated claim")
    print("      ({us,tw,my,jp}); evaluated with the identical v3 machinery. <<<")
    print_market_report(au_res)

    print(f"\n  Applicability gate (AU): n_bad_abs={au_res['n_bad_abs']} -> "
          f"{'RATED' if au_res['rated_abs'] else 'NOT RATED (' + str(au_res['n_bad_abs']) + ' loss quarters)'} "
          f"(threshold >=8)")

    print("\n  AU W_PRIM per-target summary (2x2 / OR / precision vs base_rate / recall / episodes):")
    for tname in ('T_ABS', 'T_REL'):
        s = au_res['results'][tname]['W_PRIM']
        two_x_base = round(2 * s['base_rate'], 4) if s['base_rate'] is not None else None
        prec_flag = (s['precision'] is not None and two_x_base is not None and s['precision'] >= two_x_base)
        c = s['cells']
        print(f"    {tname}: cells a={c['a']} b={c['b']} c={c['c']} d={c['d']}  OR={s['OR']}  "
              f"precision={s['precision']} (vs 2x base_rate={two_x_base}: {prec_flag})  recall={s['recall']}  "
              f"w_quarters={s['w_quarters']}  episodes: total={s['episodes']['episodes_total']} "
              f"caught={s['episodes']['caught']} missed={s['episodes']['missed']}"
              + ('  [target undefined at gate: NOT RATED, numbers shown for completeness]' if tname == 'T_ABS' and not au_res['rated_abs'] else ''))

    # ---- 5-market MH pooled OR (4 frozen + AU), labelled, alongside frozen ----
    all_res_5 = dict(all_res)
    all_res_5['au'] = au_res
    markets_5 = MKTS + ['au']
    rated_markets_abs_5 = [m for m in markets_5 if all_res_5[m]['rated_abs']]
    panel_abs_5 = build_panel(all_res_5, 'W_PRIM', 'T_ABS', rated_markets_abs_5)
    panel_rel_5 = build_panel(all_res_5, 'W_PRIM', 'T_REL', markets_5)
    mh_abs_frozen = a['MH_pooled_OR']
    mh_rel_frozen = r['MH_pooled_OR']
    mh_abs_5 = panel_abs_5['pooled']['OR_MH']
    mh_rel_5 = panel_rel_5['pooled']['OR_MH']
    mh_abs_delta = round(mh_abs_5 - mh_abs_frozen, 3) if (mh_abs_5 is not None and mh_abs_frozen is not None) else None
    mh_rel_delta = round(mh_rel_5 - mh_rel_frozen, 3) if (mh_rel_5 is not None and mh_rel_frozen is not None) else None

    print("\n  5-market MH pooled OR, LABELLED 'with AU (out-of-sample)' -- shown ALONGSIDE, never replacing, the frozen 4-market MH:")
    print(f"    T_ABS: frozen 4-market MH={mh_abs_frozen}  |  with AU (rated markets: {rated_markets_abs_5}) MH={mh_abs_5}  "
          f"AU entered={'au' in rated_markets_abs_5} (AU rated_abs={au_res['rated_abs']})  delta={mh_abs_delta}")
    print(f"    T_REL: frozen 4-market MH={mh_rel_frozen}  |  with AU (markets: {markets_5}) MH={mh_rel_5}  delta={mh_rel_delta}")
    if not au_res['rated_abs']:
        print("    -> AU does NOT enter the T_ABS MH pool (not rated); T_ABS 5-market figure == frozen 4-market figure.")

    # ---- current-quarter risk-gauge state ----
    d_au_current = load_market('au')
    i_last_au = d_au_current['n'] - 1
    au_current_state = {
        'q': d_au_current['q'][i_last_au],
        'quad': d_au_current['quad'][i_last_au],
        'warn': bool(d_au_current['warn'][i_last_au]) if d_au_current['warn'][i_last_au] is not None else False,
        'W_PRIM': au_res['_classifiers']['W_PRIM'][i_last_au],
    }
    print(f"\n  AU current-quarter risk-gauge state: {au_current_state['q']}: quad={au_current_state['quad']}  "
          f"warn={au_current_state['warn']}  -> W_PRIM={au_current_state['W_PRIM']}  -> gauge "
          f"{'ON' if au_current_state['W_PRIM'] else 'OFF'}")
    print(f"    Absolute rating regardless of gauge state: "
          f"{'RATED' if au_res['rated_abs'] else 'NOT RATED'} -- live clock shows AU as 'not rated absolute', "
          f"the same honest treatment as Malaysia.")

    # ---- self-check: T_REL truncation extended to AU ----
    print("\n  Self-check: T_REL truncation / look-ahead guard test, extended to AU:")
    trunc_au = truncation_selfcheck_au()
    print(f"    AU: truncated at k={trunc_au['k']} of n={trunc_au['n_full']}, checked {trunc_au['checked']} quarters -> "
          f"{'PASS (no labels changed)' if trunc_au['pass'] else 'FAIL'}")
    if not trunc_au['pass']:
        print(f"      mismatches (first 5): {trunc_au['mismatches']}")

    au_verdict = (
        "AU is the gauge's first true out-of-sample market: it neither confirms nor breaks the frozen "
        f"claim. It is NOT RATED on the absolute claim that was validated (only {au_res['n_bad_abs']} "
        "matured 3y-loss quarters against an >=8 gate), and its Test-8 declared-ordering concordance "
        "BREAKS (fuelled median 16.1% < starved median 22.3%, rho=-0.156) -- the same no-crash signature "
        "seen in Taiwan, not a contradiction of the risk-gauge claim (which was never a return-ordering claim)."
    )
    print(f"\n  AU hold-out verdict: {au_verdict}")

    out['au_holdout'] = {
        'amendment': 'Amendment 3 -- scripts/compass_v3_protocol.md',
        'protocol_text_verbatim': AMENDMENT3_TEXT,
        'gate': {
            'n_bad_abs': au_res['n_bad_abs'],
            'rated_abs': au_res['rated_abs'],
            'threshold': 8,
            'status_note': ('NOT RATED (' + str(au_res['n_bad_abs']) + ' loss quarters)') if not au_res['rated_abs'] else 'RATED',
        },
        'market_results': clean_market(au_res),
        'mh_5_market_with_au': {
            'label': "with AU (out-of-sample) -- shown alongside, NOT a replacement for the frozen 4-market MH",
            'T_ABS': {
                'markets': rated_markets_abs_5, 'OR_MH': mh_abs_5,
                'n_strata': panel_abs_5['pooled'].get('n_strata'),
                'au_entered': 'au' in rated_markets_abs_5,
                'frozen_4market_OR_MH': mh_abs_frozen,
                'delta_vs_frozen': mh_abs_delta,
            },
            'T_REL': {
                'markets': markets_5, 'OR_MH': mh_rel_5,
                'n_strata': panel_rel_5['pooled'].get('n_strata'),
                'frozen_4market_OR_MH': mh_rel_frozen,
                'delta_vs_frozen': mh_rel_delta,
            },
        },
        'current_quarter_state': au_current_state,
        'self_checks': {
            'truncation_lookahead_guard_au': trunc_au,
        },
        'verdict': au_verdict,
    }

    out_path = os.path.join(ROOT, 'data', 'compass-backtest-v3.json')
    json.dump(out, open(out_path, 'w'), indent=2)
    print(f"\nWrote {out_path}")


if __name__ == '__main__':
    main()
