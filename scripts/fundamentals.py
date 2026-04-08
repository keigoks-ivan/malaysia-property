#!/usr/bin/env python3
"""
Fetch fundamental data for screener stocks.
Run manually each quarter: python3 scripts/fundamentals.py

Metrics: Fwd 2Y Revenue CAGR, Fwd 2Y EPS CAGR, ROIC, FCF Margin
"""
import json, time, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import yfinance as yf

SCREENER_PATH = Path(__file__).parent.parent / "docs" / "screener"
INPUT = SCREENER_PATH / "latest.json"
OUTPUT = SCREENER_PATH / "fundamentals.json"

def safe_get(df, labels, col=0):
    if df is None or len(df.columns) == 0 or col >= len(df.columns):
        return None
    for lbl in (labels if isinstance(labels, list) else [labels]):
        if lbl in df.index:
            v = df.loc[lbl].iloc[col]
            if v is not None and str(v) != 'nan':
                return float(v)
    return None

def find_valid_col(df, labels):
    """Find first column index with valid data for given labels."""
    if df is None:
        return None
    for i in range(len(df.columns)):
        v = safe_get(df, labels, i)
        if v is not None and v != 0:
            return i
    return None

def fetch_one(ticker_str, retry=2):
    for attempt in range(retry + 1):
        try:
            tk = yf.Ticker(ticker_str)
            result = {"ticker": ticker_str}

            # === Forward estimates ===
            ge = tk.growth_estimates   # EPS growth estimates
            re = tk.revenue_estimate   # Revenue estimates

            # --- Fwd Revenue CAGR 2Y ---
            # (estimated revenue +1y / last actual revenue) ^ 0.5 - 1
            result["rev_cagr"] = None
            if re is not None and '0y' in re.index and '+1y' in re.index:
                try:
                    rev_1y = float(re.loc['+1y', 'avg'])
                    rev_ago = float(re.loc['0y', 'yearAgoRevenue'])
                    if rev_ago > 0 and rev_1y > 0:
                        result["rev_cagr"] = (rev_1y / rev_ago) ** 0.5 - 1
                except:
                    pass

            # --- Fwd EPS CAGR 2Y ---
            # compound 0y growth and +1y growth
            result["eps_cagr"] = None
            if ge is not None and '0y' in ge.index and '+1y' in ge.index:
                try:
                    g0 = float(ge.loc['0y', 'stockTrend'])
                    g1 = float(ge.loc['+1y', 'stockTrend'])
                    if str(g0) != 'nan' and str(g1) != 'nan':
                        product = (1 + g0) * (1 + g1)
                        if product > 0:
                            result["eps_cagr"] = product ** 0.5 - 1
                        else:
                            result["eps_cagr"] = (g0 + g1) / 2  # avg annual growth
                except:
                    pass

            # === Historical financials for ROIC + FCF ===
            fins = tk.financials
            bs = tk.balance_sheet
            cf = tk.cashflow

            has_fins = fins is not None and len(fins.columns) >= 1 and len(fins.index) > 5
            has_bs = bs is not None and len(bs.columns) >= 1 and len(bs.index) > 3
            has_cf = cf is not None and len(cf.columns) >= 1 and len(cf.index) > 3

            if not has_fins and attempt < retry:
                time.sleep(1)
                continue

            # Find most recent valid column
            rev_col = find_valid_col(fins, "Total Revenue") if has_fins else None

            # --- FCF Margin ---
            result["fcf_margin"] = None
            if has_cf and rev_col is not None:
                rev = safe_get(fins, "Total Revenue", rev_col)
                fcf = safe_get(cf, "Free Cash Flow", rev_col)
                if fcf is None and rev_col < (len(cf.columns) if cf is not None else 0):
                    ocf = safe_get(cf, "Operating Cash Flow", rev_col)
                    capex = safe_get(cf, ["Capital Expenditure"], rev_col)
                    if ocf is not None and capex is not None:
                        fcf = ocf + capex
                if fcf is not None and rev and rev != 0:
                    result["fcf_margin"] = fcf / rev

            # --- ROIC ---
            result["roic"] = None
            col = rev_col if rev_col is not None else 0
            if has_fins and has_bs:
                ebit = safe_get(fins, ["EBIT", "Operating Income"], col)
                use_net_income = False
                if ebit is None:
                    ebit = safe_get(fins, "Net Income", col)
                    use_net_income = True

                tax_rate = 0.21
                if not use_net_income:
                    tax_prov = safe_get(fins, "Tax Provision", col)
                    pretax = safe_get(fins, "Pretax Income", col)
                    if tax_prov is not None and pretax and pretax != 0:
                        tr = tax_prov / pretax
                        tax_rate = tr if 0 <= tr <= 0.5 else 0.21

                equity = safe_get(bs, ["Stockholders Equity", "Total Stockholders Equity", "Common Stock Equity"], col)
                lt_debt = safe_get(bs, ["Long Term Debt", "Long Term Debt And Capital Lease Obligation"], col) or 0

                if ebit is not None and equity is not None:
                    invested = equity + lt_debt
                    if invested > 0:
                        nopat = ebit if use_net_income else ebit * (1 - tax_rate)
                        result["roic"] = nopat / invested

            return result

        except Exception as e:
            if attempt < retry:
                time.sleep(3)
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

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(fetch_one, t): t for t in tickers}
        for future in as_completed(futures):
            r = future.result()
            if r:
                results[r["ticker"]] = r
            done += 1
            if done % 50 == 0 or done == total:
                print(f"  {done}/{total} done")

    for tk, r in results.items():
        for k in ["rev_cagr", "eps_cagr", "fcf_margin", "roic"]:
            v = r[k]
            if v is not None:
                if isinstance(v, complex) or str(v) == 'nan':
                    r[k] = None
                else:
                    r[k] = round(float(v), 4)

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
