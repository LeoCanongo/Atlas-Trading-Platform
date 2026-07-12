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
print("ATLAS MARKET SCANNER")
print("=" * 60)

project_root = Path(__file__).parent.parent.parent
data_folder = project_root / "data" / "historical"

results = []

for stock_file in data_folder.glob("*.csv"):

    ticker = stock_file.stem

    df = pd.read_csv(stock_file)

    df = add_sma(df, 20)
    df = add_sma(df, 50)
    df = add_rsi(df, 14)
    df = add_macd(df)
    df = add_adx(df)
    df = add_volume(df)
    df = add_atr(df)

    latest = df.iloc[-1]

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

    results.append({
        "Ticker": ticker,
        "Score": score,
        "Confidence": confidence
    })

results = sorted(
    results,
    key=lambda x: x["Score"],
    reverse=True
)

print()

print(f"{'Ticker':<10}{'Score':<10}{'Confidence':<15}{'Signal'}")
print("-" * 50)

for stock in results:

    if stock["Score"] >= 6:
        signal = "BUY 🟢"
    elif stock["Score"] >= 4:
        signal = "WATCH 🟡"
    else:
        signal = "AVOID 🔴"

    print(
        f"{stock['Ticker']:<10}"
        f"{str(stock['Score']) + '/7':<10}"
        f"{str(stock['Confidence']) + '%':<15}"
        f"{signal}"
    )