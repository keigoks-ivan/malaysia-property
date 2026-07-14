#!/usr/bin/env python3
"""Assemble scripts/.audata/au_raw.json from vetted official sources. No interpolation:
a quarter is non-null only if fully sourced (flows need all 3 months). See unit_notes."""
import csv, json, os, datetime
import openpyxl

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'au_raw.json')

# ---- axis 1975Q1 .. 2026Q1 ----
AXIS = []
for y in range(1975, 2027):
    for q in range(1, 5):
        AXIS.append(f'{y}Q{q}')
        if y == 2026 and q == 1:
            break
IDX = {q: i for i, q in enumerate(AXIS)}
N = len(AXIS)

def blank():
    return [None] * N

def mon_to_q(y, m):
    return f'{y}Q{(m-1)//3 + 1}'

# ---------- price: FRED BIS QAUN628BIS (quarterly, obs date = first month of quarter) ----------
price = blank()
for r in csv.DictReader(open(os.path.join(SRC, 'price_bis.csv'))):
    d = r['observation_date']; v = r['QAUN628BIS']
    if v in ('', '.'):
        continue
    y, m, _ = d.split('-')
    q = f'{int(y)}Q{(int(m)-1)//3 + 1}'
    if q in IDX:
        price[IDX[q]] = round(float(v), 4)

# ---------- ABS quarterly CSVs (TIME_PERIOD like 1959-Q3) ----------
def abs_q(fname, mult=1.0, rnd=4):
    out = blank()
    for r in csv.DictReader(open(os.path.join(SRC, fname))):
        tp = r['TIME_PERIOD']; v = r['OBS_VALUE']
        if v == '' or 'Q' not in tp:
            continue
        y, qq = tp.split('-Q')
        q = f'{y}Q{qq}'
        if q in IDX:
            out[IDX[q]] = round(float(v) * mult, rnd)
    return out

cpi = abs_q('cpi.csv')                       # index, Australia, All groups, Original
gdp = abs_q('gdp.csv')                       # $m, current prices, SA (unit_mult 6 = $m)
pop = abs_q('pop.csv', mult=1000.0, rnd=0)   # ERP in '000 -> persons

# ---------- ABS monthly: unemployment (quarter-average, need 3 months) ----------
def abs_monthly(fname, agg):
    buckets = {}
    for r in csv.DictReader(open(os.path.join(SRC, fname))):
        tp = r['TIME_PERIOD']; v = r['OBS_VALUE']
        if v == '' or '-' not in tp:
            continue
        y, m = tp.split('-')
        if not m.isdigit():
            continue
        q = mon_to_q(int(y), int(m))
        buckets.setdefault(q, []).append(float(v))
    out = blank()
    for q, vals in buckets.items():
        if q in IDX and len(vals) == 3:
            out[IDX[q]] = round(agg(vals), 4)
    return out

unemp  = abs_monthly('unemp.csv', lambda v: sum(v)/3)          # rate %, quarter-avg
months = abs_monthly('appr_orig.csv', lambda v: sum(v))        # dwelling approvals, quarter-SUM
months = [None if x is None else int(round(x)) for x in months]

# ---------- income: ABS 5206.0 Table 20, A2302939L (household GDI, current prices, SA, $m) ----------
income = blank()
wb = openpyxl.load_workbook(os.path.join(SRC, 'income_t20.xlsx'), read_only=True, data_only=True)
ws = wb['Data1']
COL = 74  # 0-based index of A2302939L (Seasonally Adjusted GROSS DISPOSABLE INCOME)
for row in ws.iter_rows(min_row=11):
    d = row[0].value; v = row[COL].value
    if d is None or v is None:
        continue
    if isinstance(d, datetime.datetime):
        q = mon_to_q(d.year, d.month)
        if q in IDX:
            income[IDX[q]] = round(float(v), 1)

# ---------- RBA credit / rate / SQM vacancy (pre-aggregated tails) ----------
def load_tail(fname):
    line = open(os.path.join(SRC, fname)).read().strip().split('\n')[-1]
    parts = line.split('|')
    start = parts[-2] if len(parts) >= 3 else parts[0]
    vals = parts[-1].split(',')
    return start, [float(x) for x in vals]

def place(series_start, vals, rnd=None):
    out = blank()
    si = IDX[series_start]
    for k, v in enumerate(vals):
        j = si + k
        if 0 <= j < N and AXIS[j][:4].isdigit():
            # advance by quarter respecting axis contiguity (axis is contiguous, so linear)
            out[j] = v if rnd is None else round(v, rnd)
    return out

# credit tail: "CREDIT|1990Q1|.." -> start token is parts[1]
def load_named(fname):
    line = open(os.path.join(SRC, fname)).read().strip().split('\n')[-1]
    p = line.split('|')
    # find the Qx start token
    start = next(t for t in p if len(t) >= 6 and t[4] == 'Q')
    vals = [float(x) for x in p[-1].split(',')]
    return start, vals

cst, cvals = load_named('rba_credit.txt')
credit = place(cst, cvals, rnd=1)

# rate: splice CRI (<=1990Q3) with CRT (>=1990Q4)
cria_s, cria = None, None
line = open(os.path.join(SRC, 'rba_cri_a.txt')).read().strip()
cria_s = line.split('|')[0]; cria = [float(x) for x in line.split('|')[1].split(',')]
line = open(os.path.join(SRC, 'rba_cri_b.txt')).read().strip()
crib_s = line.split('|')[0]; crib = [float(x) for x in line.split('|')[1].split(',')]
line = open(os.path.join(SRC, 'rba_crt.txt')).read().strip()
crt_s = line.split('|')[0]; crt = [float(x) for x in line.split('|')[1].split(',')]

rate = blank()
# CRI part A 1976Q3.. then part B 2003Q1.. (full interbank); then overwrite 1990Q4+ with CRT
for s, vals in [(cria_s, cria), (crib_s, crib)]:
    si = IDX[s]
    for k, v in enumerate(vals):
        if si + k < N:
            rate[si + k] = round(v, 3)
si = IDX[crt_s]
for k, v in enumerate(crt):
    if si + k < N:
        rate[si + k] = round(v, 3)

# vacancy: SQM quarter-avg 2005Q1..
line = open(os.path.join(SRC, 'sqm_vacancy.txt')).read().strip()
vac_s = line.split('|')[0]; vacv = [float(x) for x in line.split('|')[1].split(',')]
vacancy = blank()
si = IDX[vac_s]
for k, v in enumerate(vacv):
    if si + k < N:
        vacancy[si + k] = round(v, 2)

def first_last(a):
    idx = [i for i, v in enumerate(a) if v is not None]
    if not idx:
        return None
    return AXIS[idx[0]], AXIS[idx[-1]], len(idx)

raw = {
    'q': AXIS,
    'price': price, 'gdp': gdp, 'unemp': unemp, 'cpi': cpi, 'pop': pop,
    'income': income, 'credit': credit, 'rate': rate, 'months': months,
    'vacancy': vacancy,
    'unit_notes': {
        'price': 'BIS Residential Property Prices, Australia, nominal, index 2010=100 (FRED mirror id QAUN628BIS; underlying source Bank for International Settlements selected property-price series). Quarterly level. Range 1970Q1-2026Q1 (axis truncated to 1975Q1+). https://fred.stlouisfed.org/series/QAUN628BIS',
        'cpi': 'ABS Consumer Price Index (6401.0), All groups CPI, Australia (weighted average of eight capital cities), Index Numbers, Original. ABS Data API dataflow CPI key 1.10001.10.50.Q. Quarterly index (re-referenced base; continuous chain since 1948Q3). Range 1948Q3-2026Q1. https://data.api.abs.gov.au/rest/data/CPI/1.10001.10.50.Q',
        'gdp': 'ABS National Accounts (5206.0) Gross domestic product, Current prices, Seasonally Adjusted, $ millions. ABS Data API dataflow ANA_AGG key M3.GPM.20.AUS.Q (measure M3=Current prices, item GPM, TSEST 20=SA). Quarterly nominal level. Range 1959Q3-2026Q1.',
        'pop': "ABS Estimated Resident Population (3101.0 / National, state and territory population), total ERP, Australia. ABS Data API dataflow ERP_COMP_Q key 10.AUS.Q (measure 10=Estimated Resident Population). Source unit '000 persons; stored here x1000 = persons. Quarter-end level. Range 1981Q2-2025Q4 (quarterly ERP begins 1981Q2; earlier quarters null). 2026Q1 not yet released -> null.",
        'income': 'ABS National Accounts (5206.0) Table 20 Household Income Account: Households GROSS DISPOSABLE INCOME, Current prices, Seasonally Adjusted, $ millions, series ID A2302939L. Downloaded xlsx 5206020_Household_Income.xlsx (Mar-2026 release). Quarterly nominal level. Range 1959Q3-2026Q1. Used as denominator for price/income valuation.',
        'unemp': 'ABS Labour Force (6202.0) Unemployment rate, Persons, total (15+), Seasonally Adjusted, per cent. ABS Data API dataflow LF key M13.3.1599.20.AUS.M. Monthly -> quarter-AVERAGE (all 3 months required, else null). Range 1978Q1-2026Q1 (monthly LF survey begins 1978-02; 1978Q1 needs Jan which is absent -> first full quarter 1978Q2).',
        'months': 'ABS Building Approvals (8731.0) Number of dwelling units, New, Total Residential, Total Sectors, Australia, ORIGINAL (no seasonally adjusted series is published at this dwelling-unit/total-residential cut in the API). ABS Data API dataflow BA_GCCSA key 1.1.9.1.100.10.AUS.M. Monthly -> quarter-SUM (all 3 months required, else null). Unit: dwelling units approved per quarter. Range 1983Q1-2026Q1. NOTE: Original (not SA) -> retains within-year seasonality; downstream supply z-score should be read with that caveat.',
        'vacancy': 'SQM Research national residential rental vacancy rate, per cent (listings advertised >=3 weeks vs total established rentals). Monthly -> quarter-AVERAGE (all 3 months required). Range 2005Q1-2026Q1; pre-2005 null (series begins Jan 2005). https://sqmresearch.com.au/property/vacancy-rates?national=1',
        'credit': 'RBA Statistical Table D2 (Lending and Credit Aggregates): Housing credit = Owner-occupier housing (series DLCACOHN) + Investor housing (DLCACIHN), Original, $ billion, monthly, taken at quarter-END month. Sum of the two published levels equals total housing credit. Range 1990Q1-2026Q1 (owner-occ/investor split begins 1990-01; earlier housing credit not available in current D2 -> null). BREAK: RBA adopted the EFS collection in Jul-2019 causing a one-off downward reclassification of the housing credit level (2019Q2=1836.4 -> 2019Q3=1797.3, ~-2.1%); YoY credit growth spanning 2019Q3-2020Q2 is distorted by this break. A separate minor owner/investor purpose reclassification occurred 2015 but does not affect the summed total. https://www.rba.gov.au/statistics/tables/',
        'rate': 'RBA cash rate, per cent, monthly-average -> quarter-AVERAGE (all 3 months required). SPLICE: Interbank Overnight Cash Rate (series FIRMMCRI, RBA Table F1.1) for 1976Q3-1990Q3, then Cash Rate Target (series FIRMMCRT) for 1990Q4-2026Q1 (explicit target published from 1990Q4; the two agree within a few bps post-1990 except during 2020-21 when the interbank rate traded a few bps below the 0.10% target). Range 1976Q3-2026Q1. https://www.rba.gov.au/statistics/tables/',
        'pti': 'Not sourced (no clean official price-to-income ratio used); all null. Valuation is computed downstream as price/income.',
    },
    'pti': blank(),
    'fetched': '2026-07-14',
}

json.dump(raw, open(OUT, 'w'), separators=(',', ':'))

# ---- report ----
print('axis', AXIS[0], '..', AXIS[-1], 'N=', N)
for k in ['price', 'cpi', 'gdp', 'pop', 'income', 'unemp', 'months', 'credit', 'rate', 'vacancy']:
    fl = first_last(raw[k])
    print(f'  {k:9}', fl)
print('wrote', OUT, os.path.getsize(OUT), 'bytes')
