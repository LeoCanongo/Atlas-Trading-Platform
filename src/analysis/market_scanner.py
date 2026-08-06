from pathlib import Path
import pandas as pd

from src.indicators.sma import add_sma
from src.indicators.rsi import add_rsi
from src.indicators.macd import add_macd
from src.indicators.adx import add_adx
from src.indicators.volume import add_volume
from src.indicators.atr import add_atr

from src.analysis.scorer import score_stock
from src.analysis.quality_filter import QualityFilter
from src.analysis.ranking_engine import RankingEngine
from src.analysis.trade_quality import TradeQuality
from src.analysis.position_quality import PositionQuality
from src.analysis.trade_validator import TradeValidator
from src.analysis.watchlist_manager import WatchlistManager

from src.strategies.strategy_manager import get_active_strategy
from src.reports.watchlist_report import WatchlistReport

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

watchlist = WatchlistManager()

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
        # Market Data
        # -----------------------------------------

        market_data = {
            "open": latest["Open"],
            "previous_close": df.iloc[-2]["Close"],
            "daily_range_percent": (
                (latest["High"] - latest["Low"])
                / latest["Close"]
            ) * 100,
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

        # -----------------------------------------
        # Quality Filter
        # -----------------------------------------

        if not QualityFilter.passes(score, market_data):
            print("   Rejected by Quality Filter")
            continue

        # -----------------------------------------
        # Strategy Evaluation
        # -----------------------------------------

        signal = strategy.evaluate(score, market_data)        

        # -----------------------------------------
        # Advanced Ranking
        # -----------------------------------------

        atlas_rank = RankingEngine.calculate(
            score=score,
            confidence=confidence,
            signal=signal,
            market_data=market_data,
        )

        # -----------------------------------------
        # Trade Quality
        # -----------------------------------------

        trade_quality = TradeQuality.evaluate(
            score,
            market_data,
        )

        # -----------------------------------------
        # Temporary Trade Levels
        #
        # These will become strategy-specific in
        # Phase 6.
        # -----------------------------------------

        entry = latest["Close"]
        stop = entry - (latest["ATR"] * 2)
        target = entry + (latest["ATR"] * 4)

        # -----------------------------------------
        # Position Quality
        # -----------------------------------------

        position_quality = PositionQuality.evaluate(
            entry,
            stop,
            target,
        )

        # -----------------------------------------
        # Trade Validation
        # -----------------------------------------

        validation = TradeValidator.validate(
            entry,
            stop,
            target,
        )

        if not validation["valid"]:

            print("   Rejected by Trade Validator")
            continue

        # -----------------------------------------
        # Add To Watchlist
        # -----------------------------------------

        watchlist.add(
            ticker=ticker,
            signal=signal,
            atlas_score=score,
            confidence=confidence,
            trade_quality=trade_quality,
            position_quality=position_quality,
            atlas_rank=atlas_rank,
            price=latest["Close"],
        )

        print(
            f"   ✓ "
            f"Score {score}/7   "
            f"{signal}   "
            f"Quality {trade_quality['grade']}   "
            f"RR {position_quality['rr']}"
        )

    except Exception as e:

        print(f"   ERROR: {e}")

# -------------------------------------------------
# Sort Watchlist
# -------------------------------------------------

watchlist.sort()

results = watchlist.get_all()
# -------------------------------------------------
# Results
# -------------------------------------------------

print()
print("=" * 60)
print("SCAN COMPLETE")
print("=" * 60)

print(f"Universe Size   : {total}")
print(f"Valid Setups    : {watchlist.count()}")

if watchlist.count() == 0:

    print()
    print("No valid trading opportunities found.")

else:

    WatchlistReport.display(
        results,
        total,
    )

print()
print("=" * 60)
print(f"Active Strategy : {strategy.name}")
print("=" * 60)