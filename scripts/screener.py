"""
RS + VCP Screener (Mark Minervini Style)
Computes Relative Strength + Volatility Contraction Pattern scores
for ~200 US stocks. Outputs JSON for web display.

Usage:
  python scripts/screener.py          # full run
  python scripts/screener.py --quick  # skip fundamentals (faster)
"""

import json, os, sys, math, warnings
from datetime import datetime, timezone, timedelta
from pathlib import Path

warnings.filterwarnings('ignore')

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance', 'pandas', 'numpy', '-q'])
    import numpy as np
    import pandas as pd
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
SCREENER_DIR = ROOT / 'docs' / 'screener'
HISTORY_DIR = SCREENER_DIR / 'history'
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# ── Watchlist ────────────────────────────────────────────────────────────
# ~200 liquid US stocks across sectors
WATCHLIST = {
    # Technology
    'AAPL':'Technology','MSFT':'Technology','NVDA':'Technology','GOOG':'Technology',
    'META':'Technology','AVGO':'Technology','ORCL':'Technology','CRM':'Technology',
    'AMD':'Technology','ADBE':'Technology','NOW':'Technology','INTU':'Technology',
    'AMAT':'Technology','KLAC':'Technology','LRCX':'Technology','MRVL':'Technology',
    'SNPS':'Technology','CDNS':'Technology','PANW':'Technology','CRWD':'Technology',
    'FTNT':'Technology','PLTR':'Technology','APP':'Technology','MSTR':'Technology',
    'DELL':'Technology','HPE':'Technology','MU':'Technology','QCOM':'Technology',
    'TXN':'Technology','NXPI':'Technology','ON':'Technology','ARM':'Technology',
    # Financials
    'JPM':'Financials','V':'Financials','MA':'Financials','BAC':'Financials',
    'GS':'Financials','MS':'Financials','BLK':'Financials','SCHW':'Financials',
    'AXP':'Financials','SPGI':'Financials','ICE':'Financials','MCO':'Financials',
    'PGR':'Financials','TRV':'Financials','AIG':'Financials','COIN':'Financials',
    # Health Care
    'LLY':'Health Care','UNH':'Health Care','JNJ':'Health Care','ABBV':'Health Care',
    'MRK':'Health Care','TMO':'Health Care','ABT':'Health Care','ISRG':'Health Care',
    'DHR':'Health Care','BSX':'Health Care','SYK':'Health Care','VRTX':'Health Care',
    'REGN':'Health Care','GILD':'Health Care','ELV':'Health Care','HCA':'Health Care',
    # Consumer Discretionary
    'AMZN':'Consumer Disc','TSLA':'Consumer Disc','HD':'Consumer Disc','MCD':'Consumer Disc',
    'NKE':'Consumer Disc','LOW':'Consumer Disc','SBUX':'Consumer Disc','TJX':'Consumer Disc',
    'BKNG':'Consumer Disc','CMG':'Consumer Disc','ORLY':'Consumer Disc','AZO':'Consumer Disc',
    'ROST':'Consumer Disc','DHI':'Consumer Disc','LEN':'Consumer Disc','DECK':'Consumer Disc',
    # Industrials
    'GE':'Industrials','CAT':'Industrials','RTX':'Industrials','HON':'Industrials',
    'UNP':'Industrials','DE':'Industrials','LMT':'Industrials','NOC':'Industrials',
    'GD':'Industrials','BA':'Industrials','MMM':'Industrials','EMR':'Industrials',
    'ETN':'Industrials','ITW':'Industrials','PH':'Industrials','UBER':'Industrials',
    'AXON':'Industrials','TT':'Industrials','CARR':'Industrials','PWR':'Industrials',
    # Energy
    'XOM':'Energy','CVX':'Energy','COP':'Energy','SLB':'Energy',
    'EOG':'Energy','MPC':'Energy','PSX':'Energy','VLO':'Energy',
    'OXY':'Energy','HES':'Energy','DVN':'Energy','FANG':'Energy',
    # Communication
    'GOOGL':'Communication','NFLX':'Communication','DIS':'Communication','CMCSA':'Communication',
    'TMUS':'Communication','VZ':'Communication','T':'Communication','SPOT':'Communication',
    # Consumer Staples
    'PG':'Consumer Staples','KO':'Consumer Staples','PEP':'Consumer Staples','COST':'Consumer Staples',
    'WMT':'Consumer Staples','PM':'Consumer Staples','MO':'Consumer Staples','CL':'Consumer Staples',
    'MDLZ':'Consumer Staples','STZ':'Consumer Staples','KHC':'Consumer Staples','GIS':'Consumer Staples',
    # Utilities
    'NEE':'Utilities','SO':'Utilities','DUK':'Utilities','CEG':'Utilities',
    'VST':'Utilities','AEP':'Utilities','D':'Utilities','SRE':'Utilities',
    # Real Estate
    'PLD':'Real Estate','AMT':'Real Estate','EQIX':'Real Estate','CCI':'Real Estate',
    'DLR':'Real Estate','WELL':'Real Estate','SPG':'Real Estate','O':'Real Estate',
    # Materials
    'LIN':'Materials','APD':'Materials','SHW':'Materials','ECL':'Materials',
    'FCX':'Materials','NEM':'Materials','NUE':'Materials','DOW':'Materials',
}

BENCHMARK = 'SPY'
EMA_ALPHA = 0.2


def fetch_all_data(tickers, period='300d'):
    """Fetch price data for all tickers."""
    print(f"  Fetching {len(tickers)} tickers...")
    all_tickers = list(tickers) + [BENCHMARK]
    data = yf.download(all_tickers, period=period, interval='1d', group_by='ticker', progress=False, threads=True)
    return data


def calc_return(closes, days):
    """Calculate return over N trading days."""
    if len(closes) < days + 1:
        return None
    return (closes.iloc[-1] / closes.iloc[-(days+1)] - 1) * 100


def percentile_rank(values):
    """Compute percentile rank (0-100) for each value."""
    arr = np.array(values, dtype=float)
    valid = ~np.isnan(arr)
    ranks = np.full_like(arr, np.nan)
    if valid.sum() == 0:
        return ranks
    for i in range(len(arr)):
        if np.isnan(arr[i]):
            continue
        ranks[i] = np.nansum(arr[valid] <= arr[i]) / valid.sum() * 100
    return ranks


def load_previous_history():
    """Load most recent history JSON for EMA smoothing."""
    files = sorted(HISTORY_DIR.glob('*.json'))
    if not files:
        return {}
    try:
        with open(files[-1]) as f:
            data = json.load(f)
        return {r['ticker']: r for r in data.get('rankings', [])}
    except:
        return {}


def find_local_highs(highs, window=90):
    """Find local high points in the last `window` days."""
    if len(highs) < window:
        return []
    segment = highs.iloc[-window:]
    peaks = []
    for i in range(10, len(segment) - 5):
        left = max(0, i - 10)
        right = min(len(segment), i + 6)
        if segment.iloc[i] == segment.iloc[left:right].max():
            peaks.append((segment.index[i], segment.iloc[i], i))
    # Merge peaks within 10 days
    merged = []
    for p in peaks:
        if merged and (p[2] - merged[-1][2]) < 10:
            if p[1] > merged[-1][1]:
                merged[-1] = p
        else:
            merged.append(p)
    return merged


def calc_vcp(closes, highs, lows, volumes):
    """Calculate VCP Score."""
    if len(closes) < 200:
        return {'score': 0, 'pullback_count': 0, 'last_pullback_pct': 0,
                'dist_from_high_pct': 0, 'atr_ratio': 1.0, 'trend_ok': False}

    price = closes.iloc[-1]
    ma150 = closes.iloc[-150:].mean()
    ma200 = closes.iloc[-200:].mean()
    trend_ok = price > ma150 > ma200
    score = 20 if trend_ok else 0

    # Find local highs in last 90 days
    peaks = find_local_highs(highs, 90)

    # Build pullback sequence
    pullbacks = []
    for i in range(1, len(peaks)):
        idx_start = peaks[i-1][2]
        idx_end = peaks[i][2]
        seg_low = lows.iloc[-90:].iloc[idx_start:idx_end+1]
        seg_vol = volumes.iloc[-90:].iloc[idx_start:idx_end+1]
        if len(seg_low) == 0:
            continue
        low_val = seg_low.min()
        high_val = peaks[i-1][1]
        pullback_pct = (high_val - low_val) / high_val * 100
        if pullback_pct < 3:
            continue
        avg_vol = seg_vol.mean() if len(seg_vol) > 0 else 0
        pullbacks.append({
            'high': high_val, 'low': low_val,
            'pullback_pct': pullback_pct, 'avg_vol': avg_vol
        })

    n = len(pullbacks)

    # Contraction count
    if 2 <= n <= 4:
        score += 20
    elif n == 1:
        score += 8
    elif n > 4:
        score += 10

    # Pullback magnitude decreasing
    if n >= 2 and all(pullbacks[i]['pullback_pct'] < pullbacks[i-1]['pullback_pct'] for i in range(1, n)):
        score += 15

    # Higher lows
    if n >= 2 and all(pullbacks[i]['low'] > pullbacks[i-1]['low'] for i in range(1, n)):
        score += 15

    # Volume decreasing
    if n >= 2 and all(pullbacks[i]['avg_vol'] < pullbacks[i-1]['avg_vol'] for i in range(1, n)):
        score += 10

    # Last pullback magnitude
    last_pb = pullbacks[-1]['pullback_pct'] if pullbacks else 0
    if last_pb > 0:
        if last_pb < 4: score += 15
        elif last_pb < 6: score += 10
        elif last_pb < 10: score += 5

    # Distance from 90-day high
    high_90d = highs.iloc[-90:].max()
    dist_pct = (high_90d - price) / high_90d * 100
    if dist_pct < 3: score += 15
    elif dist_pct < 5: score += 10
    elif dist_pct < 10: score += 5
    elif dist_pct >= 10: score -= 5

    # ATR contraction
    def atr(h, l, c, n):
        tr = pd.concat([h-l, (h-c.shift(1)).abs(), (l-c.shift(1)).abs()], axis=1).max(axis=1)
        return tr.rolling(n).mean().iloc[-1]

    atr10 = atr(highs, lows, closes, 10)
    atr60 = atr(highs, lows, closes, 60)
    atr_ratio = atr10 / atr60 if atr60 > 0 else 1.0
    if atr_ratio < 0.5: score += 10
    elif atr_ratio < 0.7: score += 5

    # Volume ratio
    vol_10 = volumes.iloc[-10:].mean()
    vol_60 = volumes.iloc[-60:].mean()
    vol_ratio = vol_10 / vol_60 if vol_60 > 0 else 1.0

    return {
        'score': max(0, min(100, score)),
        'pullback_count': n,
        'last_pullback_pct': round(last_pb, 1),
        'dist_from_high_pct': round(dist_pct, 1),
        'atr_ratio': round(atr_ratio, 2),
        'vol_ratio': round(vol_ratio, 2),
        'trend_ok': trend_ok
    }


def fetch_fundamentals(ticker):
    """Fetch basic fundamentals for a single ticker."""
    try:
        info = yf.Ticker(ticker).info
        return {
            'mktCap': round((info.get('marketCap') or 0) / 1e9, 1),
            'epsTTM': info.get('trailingEps'),
            'epsFwd': info.get('forwardEps'),
            'peRatio': info.get('forwardPE') or info.get('trailingPE'),
            'revGrowth': round((info.get('revenueGrowth') or 0) * 100, 1),
            'opMargin': round((info.get('operatingMargins') or 0) * 100, 1),
            'roe': round((info.get('returnOnEquity') or 0) * 100, 1),
        }
    except:
        return {}


def main():
    quick = '--quick' in sys.argv
    now = datetime.now(timezone.utc)
    today = now.strftime('%Y-%m-%d')
    print(f"=== RS+VCP Screener: {today} ===\n")

    # ── Fetch data ──────────────────────────────────────────────────────
    data = fetch_all_data(WATCHLIST.keys())
    prev = load_previous_history()

    # ── Calculate RS for all stocks ─────────────────────────────────────
    print("  Calculating RS scores...")
    rs_raw = {}  # {ticker: {r1w, r4w, r13w}}
    for ticker in WATCHLIST:
        try:
            closes = data[ticker]['Close'].dropna()
            r1w = calc_return(closes, 5)
            r4w = calc_return(closes, 21)
            r13w = calc_return(closes, 63)
            if r1w is not None and r4w is not None and r13w is not None:
                rs_raw[ticker] = {'r1w': r1w, 'r4w': r4w, 'r13w': r13w}
        except:
            pass

    if not rs_raw:
        print("ERROR: No valid data")
        return

    # Percentile ranks
    tickers_list = list(rs_raw.keys())
    r1w_vals = [rs_raw[t]['r1w'] for t in tickers_list]
    r4w_vals = [rs_raw[t]['r4w'] for t in tickers_list]
    r13w_vals = [rs_raw[t]['r13w'] for t in tickers_list]

    pr1w = percentile_rank(r1w_vals)
    pr4w = percentile_rank(r4w_vals)
    pr13w = percentile_rank(r13w_vals)

    # ── EMA smooth + trend + final RS ───────────────────────────────────
    results = []
    for i, ticker in enumerate(tickers_list):
        raw_1w, raw_4w, raw_13w = pr1w[i], pr4w[i], pr13w[i]

        # EMA smoothing
        prev_data = prev.get(ticker, {})
        if prev_data:
            s1w = prev_data.get('rs_1w', raw_1w) * (1 - EMA_ALPHA) + raw_1w * EMA_ALPHA
            s4w = prev_data.get('rs_4w', raw_4w) * (1 - EMA_ALPHA) + raw_4w * EMA_ALPHA
            s13w = prev_data.get('rs_13w', raw_13w) * (1 - EMA_ALPHA) + raw_13w * EMA_ALPHA
        else:
            s1w, s4w, s13w = raw_1w, raw_4w, raw_13w

        # Persistence
        persistence = s1w * 0.2 + s4w * 0.3 + s13w * 0.5

        # Trend bonus
        if s1w > s4w > s13w:
            trend = 'accelerating'
            bonus = 5
        elif s1w >= s4w >= s13w:
            trend = 'steady'
            bonus = 2
        elif s1w < s4w < s13w:
            trend = 'fading'
            bonus = -5
        else:
            trend = 'choppy'
            bonus = 0

        rs_score = min(100, persistence + bonus)

        # ── VCP ─────────────────────────────────────────────────────────
        try:
            closes = data[ticker]['Close'].dropna()
            highs = data[ticker]['High'].dropna()
            lows = data[ticker]['Low'].dropna()
            volumes = data[ticker]['Volume'].dropna()
            price = float(closes.iloc[-1])
            ma200 = closes.iloc[-200:].mean() if len(closes) >= 200 else price
            vs_200ma = (price - ma200) / ma200 * 100

            vcp = calc_vcp(closes, highs, lows, volumes)
        except:
            price = 0
            vs_200ma = 0
            vcp = {'score': 0, 'pullback_count': 0, 'last_pullback_pct': 0,
                   'dist_from_high_pct': 0, 'atr_ratio': 1.0, 'vol_ratio': 1.0, 'trend_ok': False}

        combined = round(rs_score * 0.6 + vcp['score'] * 0.4, 1)

        results.append({
            'ticker': ticker,
            'sector': WATCHLIST[ticker],
            'rs_score': round(rs_score, 1),
            'rs_trend': trend,
            'rs_1w': round(s1w, 1),
            'rs_4w': round(s4w, 1),
            'rs_13w': round(s13w, 1),
            'vcp_score': vcp['score'],
            'pullback_count': vcp['pullback_count'],
            'last_pullback_pct': vcp['last_pullback_pct'],
            'dist_from_high_pct': vcp['dist_from_high_pct'],
            'atr_ratio': vcp['atr_ratio'],
            'vol_ratio': vcp.get('vol_ratio', 1.0),
            'combined': combined,
            'price': round(price, 2),
            'vs_200ma_pct': round(vs_200ma, 1),
            'trend_ok': bool(vcp['trend_ok']),
        })

    # Sort by combined score
    results.sort(key=lambda x: x['combined'], reverse=True)

    # Assign ranks + rank change
    for i, r in enumerate(results):
        r['rank'] = i + 1
        prev_r = prev.get(r['ticker'], {})
        prev_rank = prev_r.get('rank')
        if prev_rank:
            diff = prev_rank - r['rank']
            if diff > 0: r['rank_change'] = f'+{diff}'
            elif diff < 0: r['rank_change'] = str(diff)
            else: r['rank_change'] = '—'
        else:
            r['rank_change'] = 'NEW'

    # ── Top Picks ───────────────────────────────────────────────────────
    print("  Selecting top picks...")
    picks = {}

    # Minervini best
    for cond in [
        lambda r: r['rs_score']>=80 and r['vcp_score']>=75 and r['rs_trend']=='accelerating' and r['dist_from_high_pct']<5 and r['vol_ratio']<0.8,
        lambda r: r['rs_score']>=80 and r['vcp_score']>=75 and r['rs_trend']=='accelerating' and r['dist_from_high_pct']<8,
        lambda r: r['rs_score']>=78 and r['vcp_score']>=70 and r['rs_trend'] in ('accelerating','steady'),
        lambda r: r['rs_score']>=75 and r['vcp_score']>=65,
    ]:
        for r in results:
            if r['ticker'] not in picks.values() and cond(r):
                picks['minervini'] = r['ticker']
                break
        if 'minervini' in picks:
            break

    # Momentum (biggest rank improvement)
    momentum_candidates = [r for r in results if r['rs_score'] >= 65 and r['rank_change'] not in ('—', 'NEW') and int(r['rank_change'].replace('+','')) > 0]
    momentum_candidates.sort(key=lambda r: int(r['rank_change'].replace('+','')), reverse=True)
    for r in momentum_candidates:
        if r['ticker'] not in picks.values():
            picks['momentum'] = r['ticker']
            break

    # VCP best
    vcp_candidates = [r for r in results if r['vcp_score'] >= 75 and r['rs_score'] >= 70]
    vcp_candidates.sort(key=lambda r: r['vcp_score'] * 0.7 + r['rs_score'] * 0.3, reverse=True)
    for r in vcp_candidates:
        if r['ticker'] not in picks.values():
            picks['vcp_best'] = r['ticker']
            break

    # ── Fundamentals for top 30 ─────────────────────────────────────────
    if not quick:
        print("  Fetching fundamentals for top 30...")
        for r in results[:30]:
            r['fundamentals'] = fetch_fundamentals(r['ticker'])
    else:
        print("  Skipping fundamentals (--quick mode)")

    # ── Sector ranking ──────────────────────────────────────────────────
    sector_scores = {}
    for r in results:
        sec = r['sector']
        if sec not in sector_scores:
            sector_scores[sec] = []
        sector_scores[sec].append(r['rs_score'])
    sector_ranking = [{'sector': s, 'avg_rs': round(np.mean(v), 1), 'count': len(v)}
                      for s, v in sector_scores.items()]
    sector_ranking.sort(key=lambda x: x['avg_rs'], reverse=True)

    # ── Output JSON ─────────────────────────────────────────────────────
    output = {
        'date': today,
        'total_stocks': len(results),
        'benchmark': BENCHMARK,
        'top_picks': picks,
        'sector_ranking': sector_ranking,
        'rankings': results,
    }

    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)): return int(obj)
            if isinstance(obj, (np.floating,)): return float(obj)
            if isinstance(obj, (np.bool_,)): return bool(obj)
            if isinstance(obj, np.ndarray): return obj.tolist()
            return super().default(obj)

    latest_path = SCREENER_DIR / 'latest.json'
    with open(latest_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NpEncoder)

    history_path = HISTORY_DIR / f'{today}.json'
    with open(history_path, 'w') as f:
        json.dump(output, f, cls=NpEncoder)

    print(f"\n  ✓ Output: {latest_path}")
    print(f"  ✓ History: {history_path}")
    print(f"  ✓ Top 5: {', '.join(r['ticker'] for r in results[:5])}")
    print(f"  ✓ Top picks: {picks}")
    print(f"  ✓ Top sector: {sector_ranking[0]['sector']} (avg RS {sector_ranking[0]['avg_rs']})")

    # GitHub Actions output
    gh_output = os.environ.get('GITHUB_OUTPUT')
    if gh_output:
        with open(gh_output, 'a') as f:
            f.write("has_changes=true\n")
            f.write(f"summary=screener {today} top={results[0]['ticker']}\n")


if __name__ == '__main__':
    main()
