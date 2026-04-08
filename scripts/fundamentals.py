#!/usr/bin/env python3
"""
Fetch fundamental data for screener stocks.
Run manually each quarter: python3 scripts/fundamentals.py

Metrics: 2Y Revenue CAGR, 2Y EPS CAGR, ROIC, FCF Margin
"""
import json, time, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import yfinance as yf

SCREENER_PATH = Path(__file__).parent.parent / "docs" / "screener"
INPUT = SCREENER_PATH / "latest.json"
OUTPUT = SCREENER_PATH / "fundamentals.json"

def calc_cagr(old_val, new_val, years=2):
    if old_val is None or new_val is None or old_val <= 0 or new_val <= 0:
        return None
    return (new_val / old_val) ** (1 / years) - 1

def safe_get(df, labels, col=0):
    """Try multiple row labels, return first match or None."""
    if df is None or len(df.columns) == 0:
        return None
    for lbl in (labels if isinstance(labels, list) else [labels]):
        if lbl in df.index:
            v = df.loc[lbl].iloc[col]
            if v is not None and str(v) != 'nan':
                return float(v)
    return None

def fetch_one(ticker_str, retry=2):
    """Fetch fundamentals for one ticker with retries."""
    for attempt in range(retry + 1):
        try:
            tk = yf.Ticker(ticker_str)
            fins = tk.financials
            bs = tk.balance_sheet
            cf = tk.cashflow

            # Check if we got real data
            has_fins = fins is not None and len(fins.columns) >= 3 and len(fins.index) > 5
            has_bs = bs is not None and len(bs.columns) >= 1 and len(bs.index) > 3
            has_cf = cf is not None and len(cf.columns) >= 1 and len(cf.index) > 3

            if not has_fins and attempt < retry:
                time.sleep(1)
                continue

            result = {"ticker": ticker_str}

            # --- Revenue CAGR 2Y ---
            rev_new = safe_get(fins, "Total Revenue", 0)
            rev_old = safe_get(fins, "Total Revenue", 2) if has_fins else None
            result["rev_cagr"] = calc_cagr(rev_old, rev_new)

            # --- EPS CAGR 2Y ---
            eps_new = safe_get(fins, ["Diluted EPS", "Basic EPS"], 0)
            eps_old = safe_get(fins, ["Diluted EPS", "Basic EPS"], 2) if has_fins else None
            result["eps_cagr"] = calc_cagr(eps_old, eps_new)

            # --- FCF Margin ---
            result["fcf_margin"] = None
            if has_cf and rev_new and rev_new != 0:
                fcf = safe_get(cf, "Free Cash Flow", 0)
                if fcf is None:
                    ocf = safe_get(cf, "Operating Cash Flow", 0)
                    capex = safe_get(cf, ["Capital Expenditure"], 0)
                    if ocf is not None and capex is not None:
                        fcf = ocf + capex  # capex is negative in yfinance
                if fcf is not None:
                    result["fcf_margin"] = fcf / rev_new

            # --- ROIC ---
            result["roic"] = None
            if has_fins and has_bs:
                ebit = safe_get(fins, ["EBIT", "Operating Income"], 0)
                tax_prov = safe_get(fins, "Tax Provision", 0)
                pretax = safe_get(fins, "Pretax Income", 0)
                tax_rate = 0.21
                if tax_prov is not None and pretax and pretax != 0:
                    tr = tax_prov / pretax
                    tax_rate = tr if 0 <= tr <= 0.5 else 0.21

                equity = safe_get(bs, ["Stockholders Equity", "Total Stockholders Equity", "Common Stock Equity"], 0)
                lt_debt = safe_get(bs, ["Long Term Debt", "Long Term Debt And Capital Lease Obligation"], 0) or 0

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
    print(f"Fetching fundamentals for {total} stocks...")

    results = {}
    done = 0

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(fetch_one, t): t for t in tickers}
        for future in as_completed(futures):
            r = future.result()
            if r:
                results[r["ticker"]] = r
            done += 1
            if done % 50 == 0 or done == total:
                print(f"  {done}/{total} done")

    # Round values
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
