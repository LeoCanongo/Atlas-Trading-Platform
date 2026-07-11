from pathlib import Path
import pandas as pd

from src.indicators.sma import add_sma
from src.analysis.scorer import score_stock

print("=" * 60)
print("ATLAS DAILY MARKET SCAN")
print("=" * 60)

project_root = Path(__file__).parent.parent.parent

data_folder = project_root / "data" / "historical"

csv_files = sorted(data_folder.glob("*.csv"))

results = []

for file in csv_files:

    ticker = file.stem

    df = pd.read_csv(file)

    df = add_sma(df,20)
    df = add_sma(df,50)

    latest = df.iloc[-1]

    price = latest["Close"]
    sma20 = latest["SMA_20"]
    sma50 = latest["SMA_50"]

    score = 0

    if not pd.isna(sma50):
        score, reasons = score_stock(price,sma20,sma50)

    results.append({
        "Ticker": ticker,
        "Score": score
    })

results = sorted(results,key=lambda x:x["Score"],reverse=True)

print()

for stock in results:

    print(f"{stock['Ticker']:6}   Score: {stock['Score']}/3")