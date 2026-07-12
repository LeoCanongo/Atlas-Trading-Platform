from pathlib import Path
import pandas as pd

from src.indicators.sma import add_sma
from src.indicators.rsi import add_rsi
from src.indicators.macd import add_macd
from src.indicators.adx import add_adx
from src.indicators.volume import add_volume
from src.indicators.atr import add_atr

from src.analysis.scorer import score_stock
from src.strategies.trend_strategy import should_buy
from src.analysis.trade_planner import create_trade_plan


project_root = Path(__file__).parent.parent.parent
stock_file = project_root / "data" / "historical" / "AAPL.csv"

df = pd.read_csv(stock_file)

# Indicators
df = add_sma(df, 20)
df = add_sma(df, 50)
df = add_rsi(df, 14)
df = add_macd(df)
df = add_adx(df)
df = add_volume(df)
df = add_atr(df)

# Remove rows that don't have enough indicator data
df = df.dropna().reset_index(drop=True)

returns = []

for i in range(len(df) - 1):

    row = df.iloc[i]

    score, reasons = score_stock(
        row["Close"],
        row["SMA_20"],
        row["SMA_50"],
        row["RSI_14"],
        row["MACD"],
        row["MACD_SIGNAL"],
        row["ADX"],
        row["VOL_RATIO"],
    )

    if not should_buy(score):
        continue

    plan = create_trade_plan(
        row["Close"],
        row["ATR"],
        score,
    )

    entry = df.iloc[i + 1]["Open"]

    for j in range(i + 1, len(df)):

        high = df.iloc[j]["High"]
        low = df.iloc[j]["Low"]

        # Stop loss
        if low <= plan["stop_loss"]:
            trade_return = (
                (plan["stop_loss"] - entry)
                / entry
                * 100
            )
            returns.append(trade_return)
            break

        # Take profit
        if high >= plan["take_profit"]:
            trade_return = (
                (plan["take_profit"] - entry)
                / entry
                * 100
            )
            returns.append(trade_return)
            break

# ------------------------
# Results
# ------------------------

print("=" * 45)
print("ATLAS BACKTEST")
print("=" * 45)

if returns:

    wins = sum(r > 0 for r in returns)
    losses = len(returns) - wins

    print(f"Trades       : {len(returns)}")
    print(f"Wins         : {wins}")
    print(f"Losses       : {losses}")

    print(f"Win Rate     : {wins / len(returns) * 100:.1f}%")
    print(f"Avg Return   : {sum(returns) / len(returns):.2f}%")
    print(f"Best Trade   : {max(returns):.2f}%")
    print(f"Worst Trade  : {min(returns):.2f}%")
    print(f"Total Return : {sum(returns):.2f}%")

    avg_win = sum(r for r in returns if r > 0) / wins if wins else 0
    avg_loss = abs(sum(r for r in returns if r < 0) / losses) if losses else 0

    print(f"Avg Winner   : {avg_win:.2f}%")
    print(f"Avg Loser    : {avg_loss:.2f}%")

    if avg_loss > 0:
        print(f"Risk/Reward  : {avg_win / avg_loss:.2f}")

    total_profit = sum(r for r in returns if r > 0)
    total_loss = abs(sum(r for r in returns if r < 0))

    if total_loss > 0:
        print(f"Profit Factor: {total_profit / total_loss:.2f}")

else:
    print("No trades found.")