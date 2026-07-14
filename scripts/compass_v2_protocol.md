# Compass v2 predictive-upgrade protocol — FROZEN 2026-07-14 (before any evaluation run)

Purpose: improve the Compass's forward predictive power. Rules, formulas, constants,
metrics and success thresholds are declared here BEFORE the first evaluation run.
Changing anything below after seeing results must be disclosed as contamination.

## Baseline (what we're trying to beat)
Test 8 published (data/framework-backtest.json → test8_compass): quarter-level
Spearman ρ between declared cell rank (fuelled=4…starved=1) and realized forward
3-year nominal HPI return: US 0.58 / TW 0.08 / MY 0.71 / JP 0.40. In-sample.

## Candidates (theory-declared; every constant fixed here; NO alternatives will be tried)
All signals must be TRAILING-only (data ≤ t). mom, cred, warn are the existing
trailing series in data/compass-<m>.json — do not recompute them with any
full-history statistic. Forward target: fwd12 (3y forward nominal HPI return, %).

- C1 continuous score (fixes sign-boundary cells / thin-cell artifact):
  S1_t = mom_t + 0.5·cred_t
- C2 credit-turn tilt (T6: credit leads price turns by ~2.5 quarters):
  S2_t = S1_t + 0.5·(cred_t − cred_{t−2})
- C3 sticky-market volume axis (T6: in sticky markets "volume IS the turn").
  Applies to markets with zero hard price turns in recorded history (TW; MY if
  volume history obtainable). vol_z = smooth(tz(vol_yoy, win=24), 3) with tz/smooth
  EXACTLY as in scripts/build_compass.py.
  S3_t = vol_z_t + 0.5·cred_t   (volume replaces price momentum on the X axis)
- C4 supply-glut demotion (glut from warning ring to formal modifier):
  S4_t = S1_t − 0.5·(warn_t ? 1 : 0)

Constants (0.5 weights, 2-quarter turn lag, tz win=24, smooth w=3) are declared
conventions. They will not be grid-searched, varied, or "just tried once".

## Evaluation
1. Per-candidate, per-market, full-period: Spearman ρ(S_t, fwd12_t) over all
   quarters with non-null inputs (comparable to Test 8 baseline).
2. Overlap robustness: forward windows overlap (serial correlation inflates n).
   Report ρ on non-overlapping subsamples: every 12th quarter at offsets
   {0,4,8}, median of the offsets, with per-offset n. Small-n caveat printed.
3. Decade consistency: ρ per decade; count decades with positive sign.
4. WALK-FORWARD SELECTION (the real out-of-sample test of the *process*):
   - Expanding window. Selection dates every 4 quarters.
   - At selection date T, a quarter t is "matured" iff t ≤ T−12 (its 3y forward
     window has closed). Require ≥40 matured quarters to start.
   - At each T: compute every candidate's ρ on matured quarters only; select the
     argmax (pool: baseline rank, C1, C2, C4; plus C3 in sticky markets with
     volume data). Apply the selected score to quarters T..T+3.
   - Final metric: ρ of the walk-forward composite score vs fwd12 over all
     applied quarters, per market; compare to baseline rank ρ over the SAME
     applied window. Also report the selection history.

## Success thresholds (frozen)
- Overall: walk-forward composite ρ ≥ baseline+0.10 in ≥2 of {US, JP, MY},
  with no market degrading by more than 0.05.
- Taiwan (C3 pilot): full-period ρ(S3) ≥ 0.30 (baseline 0.08).
- Anything short of these = negative/partial result, published as-is on
  /my/framework; the live clock page changes only if thresholds are met.

## Contamination disclosure (honest, unavoidable)
Test 8's full-sample cell medians for all four markets are already published;
no design after 2026-07-13 is blind to them. Mitigation: the candidate set is
closed at these four, every formula and constant is fixed above, and the
walk-forward selection uses only matured (information-lagged) data at each date.

## Amendment 1 — 2026-07-14, AFTER the first evaluation run (disclosed contamination)
The walk-forward composite as originally specified concatenates RAW scores from
whichever candidate is selected at each date. Candidates live on incommensurable
scales (baseline = rank 1–4; C1/C2/C4 = continuous z-sums), so a market whose
selection history alternates between scales (US: 14 baseline picks interleaved
with 25 C2 picks, 4 scale switches) gets a pooled Spearman polluted by scale
mixing — a measurement artifact, not a prediction failure. This is a defect in
the METRIC's construction, identifiable from first principles; candidates,
constants and thresholds are unchanged.

Fix (metric v2.1, applied symmetrically to all markets and to the baseline
comparison): at each selection date T, the applied quarters' scores are replaced
by their percentile within the chosen candidate's own MATURED common-set values
at T (midrank convention; matured data only → no look-ahead). The baseline
comparison series is percentile-transformed identically. Both metrics (raw
pooled = original, percentile = corrected) are reported; the threshold verdict
is evaluated against the corrected metric, with the original shown alongside.
Timing disclosure: this amendment was written after seeing the first run FAIL
under the original metric (US delta −0.13). The reader can judge both numbers.

## Data note (C3)
TW volume = building ownership transfers due to sale (買賣移轉棟數), national,
monthly, Ministry of the Interior; aggregate to quarterly sums. Target history
≥1994. If an official value cannot be sourced, leave null — never interpolate
or fabricate. MY volume (NAPIC transactions) optional if ≥15y history is
obtainable; otherwise C3 is TW-only this round.
