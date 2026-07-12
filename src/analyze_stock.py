from pathlib import Path
import pandas as pd
from src.indicators.sma import add_sma
from src.indicators.rsi import add_rsi
from src.analysis.scorer import score_stock
from src.indicators.macd import add_macd
from src.indicators.adx import add_adx
from src.indicators.volume import add_volume
from src.indicators.atr import add_atr
from src.analysis.trade_planner import create_trade_plan
from src.risk.position_sizer import calculate_position_size
from src.strategies.trend_strategy import evaluate_trend_strategy
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
df = add_rsi(df, 14)
df = add_macd(df)
df = add_adx(df)
df = add_volume(df)
df = add_atr(df)
# Latest values
latest = df.iloc[-1]
rsi = latest["RSI_14"]
macd = latest["MACD"]
signal = latest["MACD_SIGNAL"]
adx = latest["ADX"]
volume_ratio = latest["VOL_RATIO"]
atr = latest["ATR"]
price = latest["Close"]
sma20 = latest["SMA_20"]
sma50 = latest["SMA_50"]
score = 0
reasons = []

if not pd.isna(sma50):
 score, reasons = score_stock(
    price,
    sma20,
    sma50,
    rsi,
    macd,
    signal,
    adx,
    volume_ratio,
)
 plan = create_trade_plan(price, atr, score)
 signal = evaluate_trend_strategy(score)
print(f"\nCurrent Price : ${price:.2f}")
print(f"20 Day SMA    : ${sma20:.2f}")

if pd.isna(sma50):
    print("50 Day SMA    : Not enough data yet")
else:
    print(f"50 Day SMA    : ${sma50:.2f}")
print(f"14 Day RSI : {rsi:.2f}")
print(f"MACD       : {macd:.2f}")
if adx > 25:
    print("💪 ADX shows a strong trend.")
else:
    print("😴 ADX shows a weak or sideways market.")
print(f"Signal     : {signal:.2f}")
print(f"ADX         : {adx:.2f}")
print(f"Volume Ratio : {volume_ratio:.2f}")
print(f"14 Day ATR   : ${atr:.2f}")
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
if rsi > 70:
    print("🔴 RSI indicates the stock may be OVERBOUGHT.")
elif rsi < 30:
    print("🟢 RSI indicates the stock may be OVERSOLD.")
else:
    print("🟡 RSI is in a healthy range.")
print("\nAtlas Score")
print("-" * 30)

print(f"Score: {score}/7")

print("\nReasoning:")

for reason in reasons:
    print(f"• {reason}")

print("\nAnalysis Complete.")
print("\n" + "=" * 30)
print("TRADE PLAN")
print("=" * 30)

print(f"Recommendation : {signal}")
print(f"Entry Price    : ${plan['entry']:.2f}")
print(f"Stop Loss      : ${plan['stop_loss']:.2f}")
print(f"Take Profit    : ${plan['take_profit']:.2f}")
print(f"Confidence     : {plan['confidence']}%")
print(f"Trend Strength : {plan['trend']}")
position = calculate_position_size(
    account_size=10000,
    risk_percent=1,
    entry_price=plan["entry"],
    stop_loss=plan["stop_loss"],
)

print("\n" + "=" * 30)
print("POSITION SIZING")
print("=" * 30)

print(f"Account Size    : ${position['account_size']:,.2f}")
print(f"Risk Per Trade  : {position['risk_percent']}%")
print(f"Dollar Risk     : ${position['dollar_risk']:.2f}")
print(f"Risk Per Share  : ${position['risk_per_share']:.2f}")
print(f"Shares          : {position['shares']}")
print(f"Position Value  : ${position['position_value']:.2f}")