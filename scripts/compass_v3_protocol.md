# Compass v3 protocol — risk retarget + applicability gate + panel + new conditioners
# FROZEN 2026-07-14, before any evaluation run. Changes after first run = disclosed amendment.

Lesson base: v2 (scripts/compass_v2_protocol.md) showed rescoring the same two inputs
against the same 3y-return-ordering target has hit its ceiling. v3 changes the TARGET
(risk avoidance, not return ordering), the SCOPE (applicability gate), the DATA
STRUCTURE (pooled panel), and adds two theory-declared CONDITIONERS.

## Targets (binary; no scale-mixing trap by construction)
- T-ABS (absolute loss): bad_t = 1 iff fwd12_t < 0 (nominal 3y loss). No look-ahead
  issue (fwd12 is the outcome being predicted, evaluated after the fact).
- T-REL (relative weakness): bad_t = 1 iff fwd12_t < Q25 of matured own-history
  outcomes, where Q25 at quarter t uses ONLY {fwd12_u : u ≤ t−12, non-null}
  (expanding, matured; ≥20 matured obs required else target undefined at t).
  Look-ahead guard: the cutoff at t may never include any outcome window that
  overlaps t. u ≤ t−12 guarantees this.

## Warning states (classifiers; all cell/warn series from data/compass-<m>.json, trailing)
- W_MOM  = quad_t == starved                          (momentum alone)
- W_PRIM = quad_t == starved AND warn_t == true       (no fuel + supply glut; primary)
Conditioners (path 4; each tested ONLY as W_PRIM ∧ condition, fixed cut, no search):
- W_AFS  = W_PRIM ∧ (AFS_z_t > 0), where AFS_t = r_t − r_{t−4}, r = real rate
  (nominal mortgage/policy rate − CPI YoY, from the market's raw series),
  AFS_z = smooth(tz(AFS, 24), 3) with tz/smooth exactly as build_compass.py.
  Theory: an affordability shock (real financing cost rising) on top of a starved
  market deepens downside (T2: floating share governs drawdown).
- W_DEMO = W_PRIM ∧ (demo_yoy_t < 0), demo_yoy = YoY % change of the 25–39
  population (first-buyer cohort; regime study: ρ=+0.44 in easing regimes).
  Data granularity per market disclosed (quarterly where published; annual step
  where only annual exists — a step function of published values, never
  interpolated). If a market's cohort series cannot be sourced, W_DEMO is
  NOT EVALUATED there — never proxied.

## Applicability gate (path 2 — honesty as a feature)
A market is RATED for the absolute claim iff its matured history contains ≥8
quarters with fwd12 < 0. Otherwise: NOT RATED (absolute) — published as such,
with the reason (no loss events in recorded history to learn from or verify
against). Expected: US, JP rated; TW, MY not rated (T6: zero hard turns / no 8%
drawdown in 27y). All four markets are rated for the relative claim.

## Metrics (2×2 per market per classifier per target)
- Odds ratio OR = [P(bad|W)/(1−P(bad|W))] / [P(bad|¬W)/(1−P(bad|¬W))]
  (Haldane correction +0.5 per cell when any cell is 0; flagged when applied).
- precision = P(bad|W); recall = P(W|bad); base rate = P(bad). All with counts.
- Overlap robustness: same metrics on non-overlapping subsamples (every 12th
  quarter, offsets {0,4,8}, median), with per-offset event counts.
- PANEL (path 3): pooled Mantel–Haenszel OR across market strata (rated markets
  only for T-ABS; all four for T-REL). No fitted model; stratified counts only.

## Success thresholds (frozen)
- ABS claim: W_PRIM OR ≥ 3 with ≥8 W-quarters and precision ≥ 2× base rate, in
  BOTH US and JP; MH pooled OR ≥ 3.
- REL claim: W_PRIM OR ≥ 2 in ≥3 of 4 markets; MH pooled OR ≥ 2.5.
- Conditioners: adopt W_AFS / W_DEMO only if it raises OR ≥ +50% over W_PRIM
  without recall falling below 0.67× W_PRIM's recall, in both US and JP (T-ABS).
  Otherwise discarded (result still published).
- The live clock page is re-framed as a risk gauge ONLY if both the ABS claim
  (US+JP) and the REL claim pass. Anything less = negative/partial result
  published on /my/framework; clock unchanged.

## Multiple-comparison discipline
Two classifiers (W_MOM, W_PRIM), two conditioners, two targets — all declared
here; nothing else will be tried. W_MOM exists to isolate the glut term's
contribution (W_PRIM vs W_MOM), not as a rescue candidate: the verdict rides on
W_PRIM alone.

## Contamination disclosure
v2's published results (cell medians, decade decay, C3 refutation) inform this
design; the gate/targets/cuts are frozen before computing any 2×2 table. The
known clustering of loss events (2006–08 US, 1990s JP) means OR estimates are
dominated by few episodes; episode counts (distinct contiguous bad-spells
caught vs missed) are reported alongside quarter counts for exactly this reason.

## Data note
- AFS inputs exist in-repo: scripts/.{tw,my,jp}data/*_raw.json (rate, cpi),
  US real_rate in data/clock-us.json raw.
- demo 25–39 cohort: to be sourced per market from official statistics only
  (US: Census/FRED; TW: MOI household registration age tables; JP: e-Stat;
  MY: DOSM if obtainable, else NOT EVALUATED). Same no-fabrication rule as v2's
  volume fetch: unsourced = null.
