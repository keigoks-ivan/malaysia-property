# gr_raw.json — provenance and gaps

Raw quarterly series bundle for adding **Greece** as the seventh market of the Property Compass.
Schema is a key-for-key copy of `scripts/.thdata/th_raw.json` (itself a copy of
`scripts/.audata/au_raw.json`); every array is length **117**, axis **1997Q1 → 2026Q1**,
contiguous, aligned index-for-index.

Assembled **2026-08-02**. Nothing here is interpolated, forward-filled to hide a hole, or invented.
There is no forward-fill anywhere in this file — unlike Thailand, `pop` is a genuine published
quarterly series, not an annual step.

Most of the underlying facts were already collected in the Greece dossier
(`gr-data.md`, 2026-08-01). What is new here is frequency alignment and four fresh fetches;
see "Dossier vs fresh" below.

---

## What is in the file

| field | source | id / key | coverage on axis | n |
|---|---|---|---|---|
| `price` | BIS via FRED | `QGRN628BIS` | 1997Q1–2026Q1 | **117** |
| `pti` | — | — | **all null** | 0 |
| `months` | Eurostat `sts_cobp_q` | `BPRM_DW / CPA_F41001_X_410014 / NSA / I21` | 1997Q1–2026Q1 | **117** |
| `vacancy` | — | — | **all null** | 0 |
| `pop` | Eurostat `namq_10_pe` | `POP_NC / THS_PER / NSA` | 1997Q1–2026Q1 | **117** |
| `credit` | BIS via FRED | `CRDQGRAHABIS` | 1997Q1–2025Q4 | 116 |
| `rate` | OECD via FRED + ECB via FRED | `IRSTCI01GRM156N` → `ECBDFR` (spliced) | 1997Q1–2026Q1 | **117** |
| `cpi` | Eurostat via FRED | `CP0000GRM086NEST` (HICP) | 1997Q1–2026Q1 | **117** |
| `gdp` | Eurostat via FRED | `CPMNACSCAB1GQEL` | 1997Q1–2026Q1 | **117** |
| `unemp` | OECD/Eurostat via FRED | `LRHUTTTTGRQ156S` | 1998Q2–2026Q1 | 112 |
| `income` | Eurostat `nasq_10_nf_tr` | `B6G / S14_S15 / PAID / CP_MEUR / SCA` | 1999Q1–2026Q1 | 109 |

Nine of eleven fields have **zero interior holes**. The only nulls are leading nulls
(`unemp` before 1998Q2, `income` before 1999Q1), one trailing null (`credit` 2026Q1), and the two
fields that genuinely do not exist for Greece (`pti`, `vacancy`).

**Last actual observation, by field:** `price` 2026Q1 · `months` 2026Q1 · `pop` 2026Q1 ·
`credit` **2025Q4** · `rate` 2026Q1 · `cpi` 2026Q1 · `gdp` 2026Q1 · `unemp` 2026Q1 ·
`income` 2026Q1 · `pti` none · `vacancy` none.

## Why the axis starts at 1997Q1

The axis is pinned to the price series, exactly as Thailand's was. `QGRN628BIS` begins 1997Q1 and
that is the longest Greek house-price series in existence. Four inputs run further back at source
and are therefore truncated, not missing: `credit` from 1994Q4, `gdp` / `pop` / `months` from
1995Q1, `cpi` from 1996Q1. Extending the axis to 1995Q1 would have added eight quarters in which
the compass has no price and therefore no reading. Nothing was shortened to hide a gap.

## Method notes

- **Frequency conversion.** Four series needed it, all by simple arithmetic mean, all documented
  in `unit_notes`:
  - `cpi` — monthly HICP → quarterly, mean of the three months. Every quarter on the axis has all
    three months present, so no quarter is a partial average.
  - `rate` leg 1 — monthly drachma call-money rate → quarterly, mean of three months, no month missing.
  - `rate` leg 2 — **calendar-daily** ECB deposit facility rate → quarterly, mean of every day in the
    quarter. `ECBDFR` has 10,074 daily observations 1999-01-01 → 2026-07-31 with zero nulls.
  - Nothing else. `price`, `credit`, `gdp`, `unemp`, `months`, `pop`, `income` are all published
    quarterly. **No annual series was stepped onto the quarterly axis anywhere in this file.**
- **`pop` is genuinely quarterly, but its within-year shape is the compiler's.** Eurostat's
  quarterly national-accounts population is produced by interpolating annual demographic statistics.
  Quarter-on-quarter change is therefore smooth by construction; only year-on-year change carries
  real information. It is still strictly better than Thailand's annual step, and `build_compass`'s
  special handling for annual-on-quarterly inputs is **not** required for Greece.
- **`rate` is spliced at 2000Q4/2001Q1** — Greece adopted the euro on 1 January 2001 and has had no
  national policy rate since. Drachma overnight interbank rate before, ECB deposit facility rate
  after. Step **7.177% → 3.750% = −3.427pp**, of which −2.333pp is genuine convergence (the same
  OECD call-money concept fell 7.177% → 4.843% across the same join) and −1.093pp is the change of
  concept (market overnight rate vs the floor of a then ~100bp-wide ECB corridor). Year-on-year
  change through 2001 is not clean.
- **Why the deposit facility rate and not the main refinancing rate.** FRED's `ECBMRRFR` is null
  from 2000-06-28 to 2008-10-14 (the variable-rate-tender era, when a minimum bid rate applied
  instead of a fixed rate), covering only 74 of 117 quarters and requiring a second splice; the
  minimum-bid-rate series is not on FRED under any of six probed ids. Beyond availability: since
  18 September 2024 the DFR is the ECB's declared steering rate, and it is the only key rate that
  registers the negative-rate easing — the DFR is negative in 34 quarters (2014Q2–2022Q3, minimum
  −0.50%) while the MRO sat at exactly 0.00%, which would have flattened the rate component of the
  money axis across the entire Greek recovery.

## The supply axis IS populated — and this is the main thing Greece has that Thailand did not

`months` = **Eurostat `sts_cobp_q`, dwellings authorised in residential buildings, quarterly index
(2021 = 100), 1995Q1–2026Q1, 117/117 on the axis with no gaps.** This is the same slot and the same
sign convention as `months` in `au_raw.json` (ABS building approvals): high = more permits = loose
future supply, and `build_compass` applies sign −1.

Consequence: `build_compass` will **not** emit `supply_available: false` for Greece. The
supply-glut ring and the supply gauge both work, from 1997Q1 onwards. **They rest on one component,
not two** — `vacancy` is null — so the supply reading is a pure permits-flow reading and should be
described that way.

Verification that this index is the real thing: converted to counts (index × 22.6/100 = thousands
of dwellings a year), the annual averages reproduce Eurostat's published dwelling counts to within
±0.2k — 2005 174.2k vs 174.4k published, 2015 5.5k, 2021 22.6k, 2024 41.7k, 2025 31.9k. Peak
2005Q4 = 1505.0, trough 2016Q1 = 20.3, a range of 32×; 2026Q1 = 155.7.

Two things a reader of this series must be told, both already in `unit_notes`:

1. **2005Q4 = 1505.0 is a regulatory pull-forward**, not an error — 19% VAT applied to new
   buildings permitted from 1 January 2006, so the whole country filed in Q4 2005.
2. **2025 is depressed by a second regulatory artefact.** The New Building Regulation (ΝΟΚ)
   floor-area and height bonuses were suspended nationwide in December 2024 and only clarified in
   May 2025, freezing filings. The 2026Q1 reading of +70.2% year-on-year (which independently
   corroborates ELSTAT's own +72.5% for Jan–Mar 2026 on its wider definition) is therefore off an
   artificially weak base and is **not** a clean demand signal.

`vacancy` stays null and cannot be rescued. Greece's only tier-1 vacancy observations are the 2011
and 2021 censuses — two points ten years apart. Putting them on a quarterly axis would mean
inventing 38 values between them. (For prose use, not for this array: the narrow 2021 count is
**793,884** nationally, not the widely-quoted 2.2 million / 34.5%, which is the broad definition
including island and rural holiday homes; Attica narrow 255,298; Municipality of Athens 117,137 on
the broad definition out of 437,188 dwellings.)

## Verification performed

1. **`price` × national CPI reproduces BIS's own real index `QGRR628BIS` to 0.045%** across all
   113 overlapping quarters — this simultaneously validates the price series, the deflator concept,
   the base, and index-for-index alignment. The national CPI used for this check
   (`GRCCPIALLMINMEI`) is *exactly* BIS's deflator; it is **not** the `cpi` shipped in the file
   (see gap note below).

   | | 1997Q1 | 2003Q1 | 2008Q3 | 2013Q1 | 2017Q2 | 2021Q1 | 2025Q1 |
   |---|---|---|---|---|---|---|---|
   | price/natCPI (rebased) | 62.994 | 99.476 | 115.914 | 74.467 | 62.128 | 74.982 | 94.511 |
   | BIS published real | 62.996 | 99.476 | 115.915 | 74.467 | 62.127 | 74.983 | 94.511 |

2. **`credit` ÷ trailing-4Q `gdp` reproduces BIS's published household-credit-to-GDP ratio
   `QGRHAM770A` to 0.05pp** at five checkpoints spanning 25 years — 2000Q4 15.18 vs 15.2,
   2010Q3 60.76 vs 60.8, 2014Q1 67.05 vs 67.1, 2020Q4 58.56 vs 58.6, **2025Q4 38.05 vs 38.1**.
   This validates the credit level, the GDP level, the units of both, and their alignment at once,
   and it is the check that proves `credit` is a level and not the %-of-GDP twin.
3. **Real house prices**, from the published real index: peak **2007Q3 = 119.53**, trough
   **2017Q2 = 62.13**, drawdown **−48.0%**, 2026Q1 = 96.98 = **−18.9% vs the 2007 peak**. Matches the
   dossier's stated −48% / −18.9% exactly. Nominal: peak 2008Q3 = 109.50, post-crisis trough
   2017Q3 = 63.08, −42.4%, 2026Q1 **+9.5% above the pre-crisis peak**.
4. **`unemp` peak**: quarterly maximum **2013Q3 = 28.03%**, 2013 four-quarter average **27.80%**,
   matching the published annual peak of 27.8%.
5. **`credit` peak**: **EUR 139.3bn at 2010Q3** → EUR 94.3bn at 2025Q4 = **−32.3%**, matching the
   dossier. The level is flat-to-rising since 2022 (91.8 → 94.3bn) while the ratio kept falling.
6. **`months` reproduces published dwelling counts** — see the supply section above.
7. **`income` against the IMF's own valuation finding**: household gross disposable income rose
   **+48.3%** from its 2014Q1 trough to 2026Q1 (+51.7% per capita on this file's `pop`), against
   BIS nominal prices **+90.0%** from their 2017Q3 trough. The IMF's May 2026 Article IV reports
   roughly +85% prices vs +47% disposable income per capita. Independent corroboration from two
   unrelated sources.
8. **CPI base and deflation**: `cpi` 2025 monthly average = 100.002, confirming base 2025 = 100;
   rebased to 2010 = 100 the index reads 2012 104.18 → 2016 100.76 → 2021 102.51, i.e. about 2.5%
   cumulative inflation across the whole 2010–2021 decade, then 2022 112.04 and 2025 123.66.
   The Greek deflation is present and not smoothed away.
9. **`pop` against the World Bank**: identical to 2020 (1997 10,661.2 vs 10,661.3 thousand;
   2010 11,121.4 vs 11,121.3), diverging by 70–126 thousand from 2021 (definition, see below).
   Peak 2010Q4 = 11,122.9k, 2026Q1 = 10,549.2k, −5.16%. No census step is visible in the series.
10. **`gdp` annual sums**: 1997 EUR 111.0bn, 2008 EUR 238.7bn, 2013 EUR 178.2bn, 2020 EUR 168.0bn,
    2025 EUR 247.9bn — matching the dossier's nominal GDP path.
11. **`rate` against known ECB history**: DFR 3.75% at 2001Q1, 0.25% at 2010Q3, 0.00% at 2013Q3,
    −0.40% at 2017Q3, −0.50% at 2021Q1, 2.00% at 2025Q4 and 2026Q1 (cut to 2.00% on 11 June 2025,
    raised to 2.25% on 17 June 2026, after the last quarter on the axis). Matches.

## Gaps, and why — what a downstream engine must NOT trust

**`pti` is entirely null and cannot be fixed.** No official Greek price-to-income ratio exists.
Greece is absent from Eurostat's house price index collection altogether (`prc_hpi_q` returns zero
observations for `geo=EL`), which also means **there is no independent tier-1 cross-check on the
BIS Greek price series** — the BoG apartment index is the only corroboration and it is a different
concept (valuation-based, Athens, 2006Q1+). No OECD price-to-income indicator for Greece is carried
on FRED (five candidate ids probed, all 404).

**Valuation is only possible from 1999Q1, and only reliably from about 2005.** With `pti` null,
valuation falls back to `price`/`income`, and `income` starts 1999Q1. With a 24-quarter
standardisation window the first trustworthy valuation z-score is no earlier than about 2005Q1.

**`cpi` is HICP, not the deflator BIS uses.** The national/OECD CPI (`GRCCPIALLMINMEI`) is exactly
BIS's deflator and reproduces `QGRR628BIS` to 0.045%, but it is **discontinued at 2025-04** and
therefore cannot cover 2025Q2–2026Q1 or ever be refreshed. Splicing it would have put a join at the
most recent and most-read end of the series, so Eurostat HICP was used throughout instead. The cost
is a maximum level divergence of **2.15%** from BIS's deflator over 29 years — about 0.07pp a year,
immaterial for real growth rates but not zero. If a downstream chart claims to show "the BIS real
house price index", use `QGRR628BIS` directly rather than recomputing it from these two fields.

**`cpi` and `months` are not seasonally adjusted.** Greek HICP has a large January/February sales
effect; the permits index has median seasonal factors of Q1 0.881, Q2 1.018, Q3 0.993, Q4 1.114.
For both fields, **only year-on-year change should be read**; quarter-on-quarter change is partly
seasonal. (For `months` the ±12% seasonal is small against a 32× range, which is why the NSA
variant was preferred over the SCA variant that starts only in 2000Q1.)

**`rate` is not one concept.** See the splice note. Additionally, from 2001Q1 the field is a
euro-area rate, not a Greek one: Greece imports its monetary stance entirely, and during 2010–2018
Greek market rates and credit conditions were violently disconnected from it (the 10-year Greek
government yield peaked at 29.24% in February 2012 while the ECB's policy rate was 1.00%).
**Do not read the Greek money axis as if the policy rate described Greek financial conditions in
the crisis years.** The 10-year yield (`IRLTLT01GRM156N`) is the series that does, and it is not in
this file. Note also that its July 2015 observation prints 0 — the capital-controls month with a
closed market, not a zero yield.

**`credit` measures all lenders, not banks.** BIS credit to households fell −32.3% from its 2010Q3
peak. The ECB bank-balance-sheet housing-loan stock fell −68.6% over roughly the same window
(EUR 80.3bn Aug 2010 → EUR 25.2bn Jun 2026). The difference is almost entirely the Hercules/HAPS
securitisations moving loans from bank books to servicers and SPVs; the households still owe them.
This file deliberately carries the all-lender measure so that transfer does not appear as
repayment. **A downstream page that describes Greek household deleveraging using only the bank
series is wrong, and the %-of-GDP ratio alone hides it too.**

**`credit` 2026Q1 is null** — BIS credit lags BIS prices by one quarter. This is the normal state
of the file at any refresh, not a fetch failure.

**`pop` is the national-accounts concept, and it diverges from the World Bank after 2021** by 70–126
thousand persons (2024: 10,531.3k here vs 10,405.1k WDI). The two agree exactly to 2020 and agree on
direction throughout — peak 2010, 15 straight years of decline, first increase in 2025 — but not on
level. Do not mix this series with WDI-based population figures in the same chart. Also note the
structural fact behind it: Greece's natural change is now about −55,000 a year and the population
has stopped falling only because net migration turned sharply positive from 2023.

**`unemp` 2026Q1 = 9.633% is a quarterly average of a volatile monthly series** (Jan 8.9, Feb 9.9,
Mar 10.1) and the same monthly series printed **8.1% for May 2026**, the lowest since 2008.
Do not quote the 2026Q1 figure as "the current Greek unemployment rate".

**Practical consequence for early quarters**: before 1998Q2 there is no `unemp` and before 1999Q1
no `income`, so 1997Q1–1998Q1 carries six of eleven fields (`price`, `months`, `pop`, `credit`,
`rate`, `cpi`, `gdp` — seven, minus the two all-null ones). If the engine requires ≥3 components
per axis, all axes still qualify from 1997Q1, but the economy axis rests on `gdp` alone until
1998Q2 and the valuation axis does not exist until 1999Q1.

**Provisional tail.** The Bank of Greece flags its own apartment-price indices as Provisional for
2025Q2–2026Q1 and revises them. BIS publishes no status flag, but the underlying data is the same
compilation, so **the last four quarters of `price` should be treated as provisional**. The same
applies to the most recent `gdp`, `income` and `months` observations, which are subject to normal
national-accounts and building-activity revision.

## Dossier vs fresh fetches

**From the dossier (`gr-data.md`, collected 2026-08-01)** — series identified there and re-pulled at
full quarterly resolution here (the dossier printed them at annual or checkpoint resolution):
`QGRN628BIS`, `QGRR628BIS`, `CRDQGRAHABIS`, `QGRHAM770A`, `CPMNACSCAB1GQEL`, `LRHUTTTTGRQ156S`,
`POPTOTGRA647NWDB`, `GRCCPIALLMINMEI`, `ECBDFR`, `ECBMRRFR`, `IRSTCI01GRM156N`. All the sanity
targets (−48% real drawdown, −18.9% vs the 2007 peak, 27.8% unemployment peak, EUR 139.3bn → 94.3bn
credit, EUR 80.3bn → 25.2bn mortgage stock, 793,884 narrow vacancy) came from the dossier and every
one of them reconciled.

**Fresh fetches, four, all made because the dossier's version was the wrong frequency or too short:**

1. **Eurostat `sts_cobp_q`** — quarterly building permits, 1992Q1–2026Q2. The dossier had only the
   *annual* `sts_cobp_a` (2005–2025) and the OECD quarterly indices that **stop in 2023**
   (`GRCPERMITQISMEI` 2023Q4, `ODCNPI03GRQ661N` 2023Q3). This one series is the reason Greece has a
   working supply axis at all; without it the OECD series would have left 2024Q1–2026Q1 null, i.e.
   no supply reading at exactly the point the compass is read.
2. **Eurostat `namq_10_pe`, `na_item=POP_NC`** — quarterly population, 1995Q1–2026Q1. The dossier had
   only annual World Bank population. This removes the annual-step artefact Thailand had to live with.
3. **Eurostat `nasq_10_nf_tr`, `B6G`/`S14_S15`** — quarterly household gross disposable income,
   1999Q1–2026Q1. Not in the dossier at all; it is the field that makes valuation possible.
4. **FRED `CP0000GRM086NEST`** — Greek HICP monthly, 1996-01–2026-06. Not in the dossier; found by
   id probing after the dossier's CPI (`GRCCPIALLMINMEI`) proved to be discontinued at 2025-04.

**Retrieval technique that mattered:** the dossier's §0 documents FRED same-origin browser fetch and
the Bank of Greece SPA/SheetJS route. Neither was needed. On this machine **plain `curl` from bash
reaches both `fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>` and the Eurostat REST dissemination
API directly (HTTP 200, no key, no browser)** — the browser was not opened once. The Eurostat API's
useful property is that requesting a dataset with only `geo=EL` returns the full dimension catalogue
(`d['id']`, `d['dimension'][k]['category']['index']`), so valid dimension codes can be enumerated
rather than guessed; that is how `POP_NC`, `CPA_F41001_X_410014` and the `I21` unit were found. Two
non-obvious traps: a partially-specified Eurostat query returns a *sparse* value map whose integer
keys index the full cross-product, so it must be fully specified before parsing; and
`cpa2_1=CPA_F41001` returns empty for `BPRM_DW` while `CPA_F41001_X_410014` carries the dwelling
counts — the same trap the dossier hit at annual frequency.

**Not fetched, deliberately:** ELSTAT was not touched. The dossier documents that it is reachable
only through the `r.jina.ai` reader proxy, and its two relevant outputs — the Building Activity
Survey (a wider permit definition than Eurostat's, and only usable as a second opinion) and the
census vacancy counts (decadal) — could not improve any field on a quarterly axis. The Bank of
Greece Athens index was not fetched either; the decision to use the BIS national series is recorded
in `unit_notes['price']` and the BoG numbers are already in the dossier at full quarterly resolution
should a page want them.

## Could not verify

- **FRED series titles.** `fred.stlouisfed.org/series/<ID>` returns a JS shell with no `<title>` to
  `curl`, and `fred.stlouisfed.org/data/<ID>.txt` hung. The identity of every FRED series in this
  file was therefore established from its *data* (base year, coverage, reconciliation against a
  published ratio or a known history) rather than from its published title. `CP0000GRM086NEST` in
  particular was confirmed to be Greek HICP by showing its annual averages are a constant 0.81464×
  the published Eurostat 2015=100 Greek HICP at eight separate years.
- **The vintage/revision date of the Eurostat extracts.** The dissemination API returns values
  without a release stamp on the rows requested.
- **Whether the −3.427pp `rate` splice step at 2000Q4/2001Q1 is fully accounted for** by the
  convergence/concept decomposition given above. The decomposition is arithmetic, but no source
  publishes both legs on the same concept across the join, so the attribution is inference.
- **BIS's exact deflation method for `QGRR628BIS`.** The 0.045% residual in verification 1 is
  consistent with monthly-CPI averaging differences, but this was not confirmed against BIS
  documentation.
- **Whether `pop`'s post-2021 divergence from WDI is definitional or a vintage difference.** Both
  series are internally smooth and neither shows a census step, so the cause was inferred, not read
  from a methodological note.
- **The Bank of Greece "Provisional" flag does not exist on the BIS series.** The claim that the
  last four `price` quarters are provisional is transferred from the BoG file's own status column on
  the parallel index; it was not confirmed that BIS revises on the same schedule.
