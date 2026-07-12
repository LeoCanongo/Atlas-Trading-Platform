from pathlib import Path
import pandas as pd

from src.indicators.sma import add_sma
from src.indicators.rsi import add_rsi
from src.indicators.macd import add_macd
from src.indicators.adx import add_adx
from src.indicators.volume import add_volume
from src.indicators.atr import add_atr

from src.analysis.scorer import score_stock

print("=" * 60)
print("ATLAS BACKTEST")
print("=" * 60)

project_root = Path(__file__).parent.parent.parent
stock_file = project_root / "data" / "historical" / "AAPL.csv"

df = pd.read_csv(stock_file)

df = add_sma(df, 20)
df = add_sma(df, 50)
df = add_rsi(df, 14)
df = add_macd(df)
df = add_adx(df)
df = add_volume(df)
df = add_atr(df)

buy_signals = 0

for _, row in df.iterrows():

    if pd.isna(row["SMA_50"]):
        continue

    score, _ = score_stock(
        row["Close"],
        row["SMA_20"],
        row["SMA_50"],
        row["RSI_14"],
        row["MACD"],
        row["MACD_SIGNAL"],
        row["ADX"],
        row["VOL_RATIO"],
    )

    if score >= 6:
        buy_signals += 1

print()
print(f"Ticker: AAPL")
print(f"Days Tested: {len(df)}")
print(f"Buy Signals: {buy_signals}")