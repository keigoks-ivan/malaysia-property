#!/usr/bin/env python3
"""
Fetch fundamental data for TW screener stocks.
Run manually each quarter: python3 scripts/fundamentals_tw.py

Metrics: 2Y Revenue CAGR, 2Y EPS CAGR, ROIC, FCF Margin
"""
import json, time, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import yfinance as yf

SCREENER_PATH = Path(__file__).parent.parent / "docs" / "screener"
INPUT = SCREENER_PATH / "tw_latest.json"
OUTPUT = SCREENER_PATH / "tw_fundamentals.json"

def calc_cagr(old_val, new_val, years=2):
    if old_val is None or new_val is None or old_val <= 0 or new_val <= 0:
        return None
    return (new_val / old_val) ** (1 / years) - 1

def safe_get(df, labels, col=0):
    if df is None or len(df.columns) == 0:
        return None
    for lbl in (labels if isinstance(labels, list) else [labels]):
        if lbl in df.index:
            v = df.loc[lbl].iloc[col]
            if v is not None and str(v) != 'nan':
                return float(v)
    return None

def find_valid_pair(df, labels, span=2):
    """Find newest non-nan value and the one `span` years before it. Returns (new, old, years)."""
    if df is None or len(df.columns) < span + 1:
        return None, None, span
    for lbl in (labels if isinstance(labels, list) else [labels]):
        if lbl in df.index:
            row = df.loc[lbl]
            for i in range(len(row) - span):
                new_v = row.iloc[i]
                old_v = row.iloc[i + span]
                if str(new_v) != 'nan' and str(old_v) != 'nan' and new_v is not None and old_v is not None:
                    return float(new_v), float(old_v), span
    return None, None, span

def fetch_one(ticker_str, retry=2):
    for attempt in range(retry + 1):
        try:
            tk = yf.Ticker(ticker_str)
            fins = tk.financials
            bs = tk.balance_sheet
            cf = tk.cashflow

            has_fins = fins is not None and len(fins.columns) >= 3 and len(fins.index) > 5
            has_bs = bs is not None and len(bs.columns) >= 1 and len(bs.index) > 3
            has_cf = cf is not None and len(cf.columns) >= 1 and len(cf.index) > 3

            if not has_fins and attempt < retry:
                time.sleep(1)
                continue

            result = {"ticker": ticker_str}

            # --- Revenue CAGR 2Y ---
            rev_new, rev_old, yrs = find_valid_pair(fins, "Total Revenue", 2)
            result["rev_cagr"] = calc_cagr(rev_old, rev_new, yrs)

            # --- EPS CAGR 2Y ---
            eps_new, eps_old, yrs = find_valid_pair(fins, ["Diluted EPS", "Basic EPS"], 2)
            result["eps_cagr"] = calc_cagr(eps_old, eps_new, yrs)

            # --- FCF Margin (use most recent valid year) ---
            result["fcf_margin"] = None
            # Find the first column with valid revenue
            rev_col = None
            if has_fins:
                for i in range(len(fins.columns)):
                    v = safe_get(fins, "Total Revenue", i)
                    if v and v != 0:
                        rev_col = i
                        break
            if has_cf and rev_col is not None:
                rev = safe_get(fins, "Total Revenue", rev_col)
                fcf = safe_get(cf, "Free Cash Flow", rev_col)
                if fcf is None and rev_col < len(cf.columns):
                    ocf = safe_get(cf, "Operating Cash Flow", rev_col)
                    capex = safe_get(cf, ["Capital Expenditure"], rev_col)
                    if ocf is not None and capex is not None:
                        fcf = ocf + capex
                if fcf is not None and rev and rev != 0:
                    result["fcf_margin"] = fcf / rev

            # --- ROIC (use same valid column as revenue) ---
            result["roic"] = None
            col = rev_col if rev_col is not None else 0
            if has_fins and has_bs:
                ebit = safe_get(fins, ["EBIT", "Operating Income"], col)
                tax_prov = safe_get(fins, "Tax Provision", col)
                pretax = safe_get(fins, "Pretax Income", col)
                tax_rate = 0.20  # Taiwan corporate tax rate
                if tax_prov is not None and pretax and pretax != 0:
                    tr = tax_prov / pretax
                    tax_rate = tr if 0 <= tr <= 0.5 else 0.20

                equity = safe_get(bs, ["Stockholders Equity", "Total Stockholders Equity", "Common Stock Equity"], col)
                lt_debt = safe_get(bs, ["Long Term Debt", "Long Term Debt And Capital Lease Obligation"], col) or 0

                if ebit is not None and equity is not None:
                    invested = equity + lt_debt
                    if invested > 0:
                        result["roic"] = ebit * (1 - tax_rate) / invested

            return result

        except Exception as e:
            if attempt < retry:
                time.sleep(1)
                continue
            print(f"  ✗ {ticker_str}: {e}", file=sys.stderr)
            return {"ticker": ticker_str, "rev_cagr": None, "eps_cagr": None, "fcf_margin": None, "roic": None}

def main():
    with open(INPUT) as f:
        data = json.load(f)
    tickers = [r["ticker"] for r in data["rankings"]]
    total = len(tickers)
    print(f"Fetching TW fundamentals for {total} stocks...")

    results = {}
    done = 0

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(fetch_one, t): t for t in tickers}
        for future in as_completed(futures):
            r = future.result()
            if r:
                results[r["ticker"]] = r
            done += 1
            if done % 20 == 0 or done == total:
                print(f"  {done}/{total} done")

    for tk, r in results.items():
        for k in ["rev_cagr", "eps_cagr", "fcf_margin", "roic"]:
            if r[k] is not None:
                r[k] = round(float(r[k]), 4)

    output = {
        "date": data["date"],
        "count": len(results),
        "data": results
    }

    with open(OUTPUT, "w") as f:
        json.dump(output, f, indent=None, separators=(",", ":"))

    has = lambda k: sum(1 for r in results.values() if r[k] is not None)
    print(f"\nSaved to {OUTPUT}")
    print(f"  rev_cagr: {has('rev_cagr')}/{total}")
    print(f"  eps_cagr: {has('eps_cagr')}/{total}")
    print(f"  fcf_margin: {has('fcf_margin')}/{total}")
    print(f"  roic: {has('roic')}/{total}")

if __name__ == "__main__":
    main()
