# Compass + Report Card design-logic audit — charter (2026-07-14)

Scope: /my/clock's two instruments (Compass incl. supply-glut warning; Report Card
incl. cross-country layer) and their full pipeline: build_clock_{us,tw,my,jp}.py →
clock-*.json → build_compass.py → compass-*.json → gen_compass_page.py/compass.js
→ my/clock.html. Question: is the DESIGN LOGIC correct — right basis, right data,
page says what the code does?

## What "correct" means (the standards findings are judged against)
1. BASIS PRINCIPLE (twice-burned lesson): cyclical/predictive quantities use
   TRAILING windows; health/absolute quantities use EXPANDING (whole-history);
   monotone trends (population) use ABSOLUTE direction. Every standardized series
   must be classified: basis used vs basis the principle requires.
2. CLAIMS = CODE: every sentence on the page describing a computation must match
   what the code actually does. A page that says "trailing" where the engine is
   expanding is a bug even if the engine is right.
3. DATA INTEGRITY: every input series must be what it claims — right deflator,
   known frequency (incl. step/interpolated segments), fresh enough, aligned by
   quarter label, documented breaks.
4. VALIDATED-CLAIM PROTECTION: W_PRIM = starved ∧ warn is a VALIDATED claim
   (compass-backtest-v3.json) — validated AS IMPLEMENTED (warn = trailing z ≤ −1
   on vacancy OR months). Any change to any input of W_PRIM invalidates the
   validation: such changes require a disclosed protocol amendment + v3 re-run,
   never a silent fix. Audit may still conclude the design is wrong; the remedy
   path is re-validation.

## Finding classification (every finding gets exactly one)
- BUG — objectively wrong (contradiction, wrong basis per principle, wrong data,
  claim≠code). Fix now; if it touches W_PRIM inputs → NEEDS-REVALIDATION instead.
- NEEDS-REVALIDATION — a defensible fix exists but touches the validated claim;
  fix only via amendment + re-run of the v3 harness, both results published.
- DESIGN-DEBT — defensible as-is but fragile or unmodelled; disclose on page or
  document, don't change behavior.
- OK-AS-DESIGNED — reviewed and correct; record why.

## Known seed findings (verify, don't assume)
- S1: page footer (gen_compass_page.py .src paragraph) says report-card gauges are
  "trailing-z" — engine has been EXPANDING since commit ad23c16. Suspected BUG
  (documentation). Check the whole footer sentence ("standardised on trailing
  windows") for further overreach.
- S2: warn flag basis is TRAILING (czlist win=24 in build_clock_*.py STRUCT) —
  design question: does a chronically glutted market stop warning as the window
  adapts (warning fatigue)? Classify per principle §1 and §4: is a glut warning a
  cyclical or an absolute concept? Whatever the conclusion, remedy path is §4.
