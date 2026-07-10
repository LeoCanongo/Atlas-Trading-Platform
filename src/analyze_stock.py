from pathlib import Path
import pandas as pd
from indicators.sma import add_sma
from analysis.scorer import score_stock
print("=" * 60)
print("Atlas Trading Platform")
print("Stock Analyzer")
print("=" * 60)

project_root = Path(__file__).parent.parent

stock_file = project_root / "data" / "historical" / "AAPL.csv"

# Load stock data
df = pd.read_csv(stock_file)

# Calculate indicators
df = add_sma(df, 20)
df = add_sma(df, 50)

# Latest values
latest = df.iloc[-1]

price = latest["Close"]
sma20 = latest["SMA_20"]
sma50 = latest["SMA_50"]
score = 0
reasons = []

if not pd.isna(sma50):
    score, reasons = score_stock(price, sma20, sma50)
print(f"\nCurrent Price : ${price:.2f}")
print(f"20 Day SMA    : ${sma20:.2f}")

if pd.isna(sma50):
    print("50 Day SMA    : Not enough data yet")
else:
    print(f"50 Day SMA    : ${sma50:.2f}")

print("\nMarket Analysis")
print("-" * 30)

if price > sma20:
    print("✅ Price is ABOVE the 20-day moving average.")
else:
    print("❌ Price is BELOW the 20-day moving average.")

if not pd.isna(sma50):
    if sma20 > sma50:
        print("📈 Short-term trend is stronger than the long-term trend.")
    else:
        print("📉 Short-term trend is weaker than the long-term trend.")

print("\nAtlas Score")
print("-" * 30)

print(f"Score: {score}/3")

print("\nReasoning:")

for reason in reasons:
    print(f"• {reason}")

print("\nAnalysis Complete.")