from src.analysis.market_scanner import results
from src.paper_trading.paper_trader import buy_stock
from src.analysis.trade_planner import create_trade_plan
from src.risk.position_sizer import calculate_position_size

print("=" * 50)
print("ATLAS AUTO PAPER TRADER")
print("=" * 50)

if len(results) == 0:
    print("No trading opportunities found.")
    quit()

# Highest scoring stock
best = results[0]

ticker = best["Ticker"]
price = best["Price"]
score = best["Score"]
atr = best["ATR"]

print(f"\nSelected Stock: {ticker}")
print(f"Current Price : ${price:.2f}")
print(f"Atlas Score   : {score}/7")

# Build trade plan
plan = create_trade_plan(
    price,
    atr,
    score
)

# Position sizing
position = calculate_position_size(
    account_size=10000,
    risk_percent=1,
    entry_price=plan["entry"],
    stop_loss=plan["stop_loss"]
)

shares = position["shares"]
print(f"Risk Amount : ${position['dollar_risk']:.2f}")
print(f"Position Val: ${position['position_value']:.2f}")

print("\nExecuting Paper Trade...\n")

buy_stock(
    ticker,
    shares,
    plan["entry"]
)

print("\nTrade Summary")
print("-" * 40)
print(f"Ticker      : {ticker}")
print(f"Entry       : ${plan['entry']:.2f}")
print(f"Stop Loss   : ${plan['stop_loss']:.2f}")
print(f"Take Profit : ${plan['take_profit']:.2f}")
print(f"Shares      : {shares}")
print(f"Confidence  : {plan['confidence']}%")