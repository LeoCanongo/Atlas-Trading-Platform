from pathlib import Path
import pandas as pd

from src.indicators.sma import add_sma
from src.indicators.rsi import add_rsi
from src.indicators.macd import add_macd
from src.indicators.adx import add_adx
from src.indicators.volume import add_volume
from src.indicators.atr import add_atr

from src.analysis.scorer import score_stock
from src.strategies.strategy_manager import get_active_strategy

print("=" * 60)
print("ATLAS MARKET SCANNER")
print("=" * 60)

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

project_root = Path(__file__).parent.parent.parent

data_folder = project_root / "data" / "historical"
universe_file = project_root / "data" / "universe.csv"

strategy = get_active_strategy()

results = []

# -------------------------------------------------
# Load Universe
# -------------------------------------------------

if not universe_file.exists():
    raise FileNotFoundError(
        f"Universe file not found:\n{universe_file}"
    )

universe = pd.read_csv(universe_file)

total = len(universe)

print(f"\nScanning {total} symbols...\n")

# -------------------------------------------------
# Scan Universe
# -------------------------------------------------

for index, ticker in enumerate(universe["Ticker"], start=1):

    ticker = str(ticker).strip().upper()

    print(f"[{index}/{total}] {ticker}")

    stock_file = data_folder / f"{ticker}.csv"

    if not stock_file.exists():
        print("   Missing historical data")
        continue

    try:

        df = pd.read_csv(stock_file)

        if len(df) < 50:
            print("   Not enough historical data")
            continue

        # -----------------------------------------
        # Technical Indicators
        # -----------------------------------------

        df = add_sma(df, 20)
        df = add_sma(df, 50)

        df = add_rsi(df, 14)
        df = add_macd(df)
        df = add_adx(df)

        df = add_volume(df)
        df = add_atr(df)

        latest = df.iloc[-1]

        # -----------------------------------------
        # Market Statistics
        # -----------------------------------------

        twenty_day_high = df["High"].tail(20).max()
        twenty_day_low = df["Low"].tail(20).min()

        average_volume = df["Volume"].tail(20).mean()

        # -----------------------------------------
        # Atlas Score
        # -----------------------------------------

        score, reasons = score_stock(
            latest["Close"],
            latest["SMA_20"],
            latest["SMA_50"],
            latest["RSI_14"],
            latest["MACD"],
            latest["MACD_SIGNAL"],
            latest["ADX"],
            latest["VOL_RATIO"],
        )

        confidence = round(score / 7 * 100)

        # -----------------------------------------
        # Market Data For Strategy
        # -----------------------------------------

        market_data = {
            "close": latest["Close"],
            "high": latest["High"],
            "low": latest["Low"],

            "sma20": latest["SMA_20"],
            "sma50": latest["SMA_50"],

            "rsi": latest["RSI_14"],

            "macd": latest["MACD"],
            "macd_signal": latest["MACD_SIGNAL"],

            "adx": latest["ADX"],

            "volume": latest["Volume"],
            "average_volume": average_volume,
            "vol_ratio": latest["VOL_RATIO"],

            "atr": latest["ATR"],

            "twenty_day_high": twenty_day_high,
            "twenty_day_low": twenty_day_low,
        }

        signal = strategy.evaluate(score, market_data)

        # -----------------------------------------
        # Atlas Ranking
        # -----------------------------------------

        signal_bonus = {
            "BUY": 25,
            "WATCH": 10,
            "AVOID": 0,
        }[signal]

        atlas_rank = (
            score * 100
            + confidence
            + signal_bonus
        )

        results.append({
            "Ticker": ticker,
            "Price": latest["Close"],
            "ATR": latest["ATR"],
            "Score": score,
            "Confidence": confidence,
            "Signal": signal,
            "Rank": atlas_rank,
        })

        print(
            f"   ✓ Score: {score}/7"
            f"   Signal: {signal}"
        )

    except Exception as e:

        print(f"   ERROR: {e}")

# -------------------------------------------------
# Sort Results
# -------------------------------------------------

results = sorted(
    results,
    key=lambda x: x["Rank"],
    reverse=True,
)# -------------------------------------------------
# Results
# -------------------------------------------------

print()
print("=" * 60)
print("SCAN COMPLETE")
print("=" * 60)

print(f"Stocks Scanned : {len(results)}")
print()

if not results:
    print("No valid trading opportunities were found.")
else:

    print(
        f"{'Rank':<6}"
        f"{'Ticker':<10}"
        f"{'Score':<10}"
        f"{'Confidence':<15}"
        f"{'Signal':<10}"
        f"{'Atlas Rank'}"
    )

    print("-" * 70)

    for position, stock in enumerate(results, start=1):

        print(
            f"{position:<6}"
            f"{stock['Ticker']:<10}"
            f"{str(stock['Score']) + '/7':<10}"
            f"{str(stock['Confidence']) + '%':<15}"
            f"{stock['Signal']:<10}"
            f"{stock['Rank']}"
        )

print()
print("=" * 60)
print(f"Active Strategy : {strategy.name}")
print("=" * 60)