# th_raw.json — provenance and gaps

Raw quarterly series bundle for adding **Thailand (Bangkok)** to the Property Compass.
Schema is a key-for-key copy of `scripts/.audata/au_raw.json`; every array is length **141**,
axis **1991Q1 → 2026Q1**, contiguous, aligned index-for-index.

Fetched **2026-07-31**. Nothing here is interpolated, forward-filled to hide a hole, or invented.
The only forward-fill in the file is `pop` (annual → quarterly step) and it is flagged as such
in `unit_notes` and below.

---

## What is in the file

| field | source | id / key | coverage on axis | n |
|---|---|---|---|---|
| `price` | BIS via FRED | `QTHN628BIS` | 1991Q1–2026Q1 | 141 |
| `cpi` | IMF Data, dataflow `CPI` | `THA.CPI._T.SRP_IX.Q` | 1991Q1–2026Q1 | 141 |
| `rate` | IMF Data, dataflow `MFS_IR` | `THA.MMRT_…` + `THA.MFS166_…` (spliced) | 1991Q1–2026Q1 | 141 |
| `credit` | BIS via FRED | `CRDQTHAHABIS` | 1991Q4–2025Q4 | 137 |
| `gdp` | IMF Data, dataflow `QNEA` | `THA.B1GQ.V.SA.XDC.Q` | 1993Q1–2026Q1 | 133 |
| `pop` | World Bank WDI via FRED | `POPTOTTHA647NWDB` (annual) | 1991Q1–2025Q4 | 140 |
| `unemp` | IMF Data, dataflow `LS` | `THA.U.PT.Q` | 2001Q1–2026Q1, holes | 93 |
| `income` | ILOSTAT | `EAR_EMTA_SEX_NB_Q`, `SEX_T` | 2014Q1–2025Q4, one hole | 47 |
| `pti` | — | — | **all null** | 0 |
| `months` | — | — | **all null** | 0 |
| `vacancy` | — | — | **all null** | 0 |

Country code is `THA` in the IMF API (`TH` silently returns metadata with zero observations —
a trap, because it returns HTTP 200 and a 56 KB body).

## Method notes

- **Frequency conversion**: none was needed. Every series was already published quarterly
  except `pop` (annual). No monthly→quarterly averaging was performed anywhere in this file.
- **`pop` is a step function**: the World Bank annual mid-year value is repeated across all four
  quarters of its year. Within-year quarter-on-quarter population change is therefore identically
  zero by construction; only the Q4→Q1 step carries information. An engine with special handling
  for annual-on-quarterly inputs must apply it here. 2026Q1 is null (2026 WDI not released).
  Thailand's population **peaked in 2022** and has declined every year since — that is real.
- **`rate` is spliced** at 2000Q2/2000Q3: money market (interbank overnight) rate before,
  BOT policy rate after. The join has a ~0.48 pp level step (1.977% → 1.500%), so year-on-year
  change across 2000Q3–2001Q2 is not clean. The pre-2000 leg is a *market* rate and a different
  concept from a policy target; the 1997–98 spike to 20.6% is the genuine crisis squeeze.

## Verification performed

1. **`price` × `cpi` reproduces BIS's own real Bangkok index** (`QTHR628BIS`) to within 0.12%
   at six checkpoints spanning 35 years:

   | | 1991Q1 | 1997Q1 | 2003Q1 | 2010Q1 | 2018Q1 | 2026Q1 |
   |---|---|---|---|---|---|---|
   | price/cpi×100 | 100.816 | 116.740 | 96.320 | 99.145 | 136.465 | 150.650 |
   | BIS published | 100.730 | 116.725 | 96.372 | 99.145 | 136.465 | 150.831 |

   This simultaneously validates the price series, the deflator, the CPI base, and the
   index-for-index alignment of the two arrays.
2. **`credit` ÷ trailing-4Q `gdp` = 87.5% at 2025Q4**, exactly the figure BIS publishes in
   `QTHHAM770A` (household credit, % of GDP). This validates the credit level, the GDP level,
   the units of both, and the alignment, in one check.
3. **CPI base**: the four 2010 quarters average to exactly 100.000, confirming 2010 = 100.
4. **Policy rate against known BOT history**: 0.50% floor 2020Q2–2022Q2, hikes from 2022Q3,
   2.50% peak 2023Q3–2024Q3, cuts through 2025 to **1.00% at 2026Q1**. Matches.
5. **CPI deflation**: index falls 122.677 (2025Q1) → 122.018 (2026Q1), matching the documented
   Thai deflation of 2025–26.
6. **Bangkok nominal index ≈ 182 in 2025** (2025Q3 = 182.574). Matches.
7. FRED's title for `QTHN628BIS` is literally *"Residential Property Prices for Bangkok, Thailand"* —
   confirmed **city**, not nationwide.

## The credit trap, and how it was avoided

The brief flagged this and it was real. FRED carries five different Thai household-credit series:

- `QTHHAM770A` — **% of GDP**, not a level. Using it as `credit` would corrupt the compass Y axis.
- `QTHHAMUSDA` — level, but in **US dollars**. Rejected: it embeds THB/USD, so the 1997 baht float
  would appear as a ~50% credit collapse that never happened.
- `QTHHAMXDCA` / `QTHHAMXDCB` / `QTHPAMXDCA` — **do not exist** (404).
- `CRDQTHAHUBIS` — level in **billions of baht**, but *unadjusted for breaks*.
- `CRDQTHAHABIS` — level in **billions of baht**, *adjusted for breaks*. ← **used**

The unadjusted and adjusted series differ by ~3× at the start (255.9 vs 793.6 bn baht at 1991Q4)
because of a coverage expansion; the unadjusted one would inject an enormous fake credit-growth
spike. The adjusted one is the series that reconciles with the published %-of-GDP ratio at both
ends (see verification 2). No derived/reconstructed series was needed — this is a true published
domestic-currency level.

The real 1997Q2→2002Q2 decline (3,047 → 2,472 bn baht) is genuine post-crisis deleveraging.

## Gaps, and why — what a downstream engine must NOT trust

**`months` and `vacancy` are entirely null, so the Thai supply axis has zero components.**
This is not a fetch failure that a retry will fix. Thailand publishes no official housing
inventory, absorption or rental-vacancy series. REIC (`reic.or.th`) is a JS SPA whose statistics
pages cannot be extracted — already documented as a dead end in
`.claude/notes/market-page-spec.md`, and retried here without success. The private surveys that
exist (AREA, SCB EIC, Knight Frank) are annual, start around 2021, and disagree on the same
"Greater Bangkok unsold units" concept by more than 60% (210,112 vs 213,000 vs 350,000), so they
cannot be chained into anything quarterly. **Do not present a Thai supply reading.**

**Valuation is only possible from 2014Q1, and only reliably from about 2020.** `pti` is null
(no official Thai price-to-income ratio exists), so valuation must fall back to `price`/`income` —
and `income` only starts 2014Q1. With the 24-quarter standardisation window the first trustworthy
valuation z-score is no earlier than ~2020. **Do not report a Thai valuation number before that.**

**`income` is not household income.** It is ILOSTAT *average monthly earnings of employees*
(baht per employee per month) from the NSO Labour Force Survey — a per-worker wage, not a
household aggregate, and **not unit-comparable to the `income` field in `au_raw.json`** (which is
ABS household gross disposable income in A$m). It is included because it is the only genuine
observed quarterly Thai income series obtainable. The NSO Household Socio-Economic Survey — the
proper source — remains unobtainable; it also failed in the earlier `/th` page round.
**2015Q1 is deliberately null**: ILOSTAT publishes 1076.029 there (and 1094.989 / 1052.500 for the
male/female breakdowns), about one thirteenth of both neighbours — an evident source-side unit
error. It was removed, not interpolated.

**`unemp` has seven consecutive missing quarters over COVID.** 2020Q2 and all of
2021Q1–2022Q3 are absent from the IMF source. The COVID labour shock is therefore only half
observed. Separately, Thai unemployment sits structurally near 1% because of the large informal
and agricultural workforce, so its z-score is driven by very small absolute moves — the economy
axis should be read with that in mind.

**Other honest nulls**: `credit` 1991Q1–1991Q3 (BIS series starts 1991Q4) and 2026Q1 (BIS credit
lags BIS prices by a quarter); `gdp` 1991Q1–1992Q4 (IMF QNEA for Thailand starts 1993Q1);
`pop` 2026Q1; `unemp` pre-2001Q1.

**Practical consequence**: before 1993Q1 only `price`, `cpi`, `rate` and `pop` exist (4 series),
and before 2001Q1 there is no `unemp`. If the engine requires ≥3 components per axis, the early
axis readings rest on a thin and uneven base.

## Could not verify

- The exact vintage/revision date of the IMF QNEA and LS extracts (the API returns data without a
  release stamp in the CSV rows requested).
- Whether the 2000Q2/2000Q3 rate splice step reflects a true easing in that quarter or purely the
  change of concept — both legs are plausible, and no overlapping period is published for both.
- BIS's precise deflation method for `QTHR628BIS`; the ~0.1% residual in verification 1 is
  consistent with them using monthly MoC CPI averaged slightly differently, but this was not
  confirmed against BIS documentation.
