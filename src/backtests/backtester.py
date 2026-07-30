from pathlib import Path

import math
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


def run_backtest(symbol):

    project_root = Path(__file__).resolve().parent.parent.parent

    stock_file = (
        project_root
        / "data"
        / "historical"
        / f"{symbol}.csv"
    )

    if not stock_file.exists():
        raise FileNotFoundError(
            f"No historical data found for {symbol}"
        )

    df = pd.read_csv(stock_file)

    df = add_sma(df, 20)
    df = add_sma(df, 50)
    df = add_rsi(df, 14)
    df = add_macd(df)
    df = add_adx(df)
    df = add_volume(df)
    df = add_atr(df)

    df = df.dropna().reset_index(drop=True)

    starting_balance = 10000.0
    balance = starting_balance

    peak = starting_balance
    max_drawdown = 0.0

    equity_curve = [starting_balance]

    returns = []
    durations = []
    trade_log = []

    for i in range(len(df) - 1):

        row = df.iloc[i]

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

        if not should_buy(score):
            continue

        plan = create_trade_plan(
            row["Close"],
            row["ATR"],
            score,
        )

        entry = df.iloc[i + 1]["Open"]
        entry_date = pd.to_datetime(df.iloc[i + 1]["Date"])

        for j in range(i + 1, len(df)):

            high = df.iloc[j]["High"]
            low = df.iloc[j]["Low"]

            if low <= plan["stop_loss"]:

                exit_price = plan["stop_loss"]
                exit_date = pd.to_datetime(df.iloc[j]["Date"])

                trade_return = (
                    (exit_price - entry)
                    / entry
                    * 100
                )

                duration = (exit_date - entry_date).days

                durations.append(duration)
                returns.append(trade_return)

                balance *= (1 + trade_return / 100)
                equity_curve.append(balance)

                peak = max(peak, balance)

                drawdown = (
                    (balance - peak)
                    / peak
                    * 100
                )

                max_drawdown = min(
                    max_drawdown,
                    drawdown,
                )

                trade_log.append({
                    "entry_date": entry_date.date(),
                    "exit_date": exit_date.date(),
                    "entry": entry,
                    "exit": exit_price,
                    "return": trade_return,
                    "duration": duration,
                })

                break

            if high >= plan["take_profit"]:

                exit_price = plan["take_profit"]
                exit_date = pd.to_datetime(df.iloc[j]["Date"])

                trade_return = (
                    (exit_price - entry)
                    / entry
                    * 100
                )

                duration = (exit_date - entry_date).days

                durations.append(duration)
                returns.append(trade_return)

                balance *= (1 + trade_return / 100)
                equity_curve.append(balance)

                peak = max(peak, balance)

                drawdown = (
                    (balance - peak)
                    / peak
                    * 100
                )

                max_drawdown = min(
                    max_drawdown,
                    drawdown,
                )

                trade_log.append({
                    "entry_date": entry_date.date(),
                    "exit_date": exit_date.date(),
                    "entry": entry,
                    "exit": exit_price,
                    "return": trade_return,
                    "duration": duration,
                })

                break

    wins = sum(r > 0 for r in returns)
    losses = len(returns) - wins

    avg_return = (
        sum(returns) / len(returns)
        if returns else 0
    )

    avg_win = (
        sum(r for r in returns if r > 0) / wins
        if wins else 0
    )

    avg_loss = (
        abs(sum(r for r in returns if r < 0) / losses)
        if losses else 0
    )

    total_profit = sum(r for r in returns if r > 0)
    total_loss = abs(sum(r for r in returns if r < 0))

    avg_duration = (
        sum(durations) / len(durations)
        if durations else 0
    )

    win_rate = (
        wins / len(returns)
        if returns else 0
    )

    loss_rate = 1 - win_rate

    expectancy = (
        (win_rate * avg_win)
        -
        (loss_rate * avg_loss)
    )

    if len(returns) > 1:

        mean = avg_return

        variance = sum(
            (r - mean) ** 2
            for r in returns
        ) / (len(returns) - 1)

        std_dev = math.sqrt(variance)

        sharpe_ratio = (
            mean / std_dev
            if std_dev > 0 else 0
        )

    else:
        sharpe_ratio = 0
    report = {
        "symbol": symbol,
        "trades": len(returns),
        "wins": wins,
        "losses": losses,
        "win_rate": (
            wins / len(returns) * 100
            if returns else 0
        ),
        "average_return": avg_return,
        "average_winner": avg_win,
        "average_loser": avg_loss,
        "expectancy": expectancy,
        "sharpe_ratio": sharpe_ratio,
        "best_trade": (
            max(returns)
            if returns else 0
        ),
        "worst_trade": (
            min(returns)
            if returns else 0
        ),
        "total_return": sum(returns),
        "profit_factor": (
            total_profit / total_loss
            if total_loss > 0 else 0
        ),
        "starting_balance": starting_balance,
        "ending_balance": balance,
        "max_drawdown": max_drawdown,
        "average_duration": avg_duration,
        "shortest_trade": (
            min(durations)
            if durations else 0
        ),
        "longest_trade": (
            max(durations)
            if durations else 0
        ),
        "equity_curve": equity_curve,
        "returns": returns,
        "trade_log": trade_log,
    }

    return report


def print_report(report):

    print("=" * 55)
    print("ATLAS BACKTEST REPORT")
    print("=" * 55)

    print(f"Symbol            : {report['symbol']}")
    print(f"Trades            : {report['trades']}")
    print(f"Wins              : {report['wins']}")
    print(f"Losses            : {report['losses']}")
    print(f"Win Rate          : {report['win_rate']:.2f}%")
    print(f"Average Return    : {report['average_return']:.2f}%")
    print(f"Average Winner    : {report['average_winner']:.2f}%")
    print(f"Average Loser     : {report['average_loser']:.2f}%")
    print(f"Expectancy        : {report['expectancy']:.2f}%")
    print(f"Sharpe Ratio      : {report['sharpe_ratio']:.2f}")
    print(f"Best Trade        : {report['best_trade']:.2f}%")
    print(f"Worst Trade       : {report['worst_trade']:.2f}%")
    print(f"Total Return      : {report['total_return']:.2f}%")
    print(f"Profit Factor     : {report['profit_factor']:.2f}")

    print()
    print(f"Starting Balance  : ${report['starting_balance']:,.2f}")
    print(f"Ending Balance    : ${report['ending_balance']:,.2f}")
    print(f"Max Drawdown      : {report['max_drawdown']:.2f}%")

    print()
    print(f"Avg Trade Length  : {report['average_duration']:.1f} days")
    print(f"Shortest Trade    : {report['shortest_trade']} days")
    print(f"Longest Trade     : {report['longest_trade']} days")

    print()
    print("Recent Trades")
    print("-" * 85)

    recent_trades = report["trade_log"][-5:]

    if recent_trades:

        for trade in recent_trades:

            print(
                f"{trade['entry_date']} -> "
                f"{trade['exit_date']} | "
                f"{trade['duration']} days | "
                f"Entry: ${trade['entry']:.2f} | "
                f"Exit: ${trade['exit']:.2f} | "
                f"Return: {trade['return']:.2f}%"
            )

    else:
        print("No trades found.")


if __name__ == "__main__":

    report = run_backtest("AAPL")

    print_report(report)
    