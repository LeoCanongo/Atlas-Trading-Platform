from src.paper_trading.paper_trader import load_history


def get_trade_statistics():

    history = load_history()

    buys = [t for t in history if t["action"] == "BUY"]
    sells = [t for t in history if t["action"] == "SELL"]

    completed = min(len(buys), len(sells))

    profits = []

    for i in range(completed):

        buy = buys[i]
        sell = sells[i]

        entry = buy["price"]
        exit_price = sell["price"]

        pnl_percent = ((exit_price - entry) / entry) * 100

        profits.append(pnl_percent)

    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p <= 0]

    stats = {
        "total_trades": len(profits),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": (
            len(wins) / len(profits) * 100
            if profits else 0
        ),
        "average_gain": (
            sum(wins) / len(wins)
            if wins else 0
        ),
        "average_loss": (
            sum(losses) / len(losses)
            if losses else 0
        ),
        "largest_winner": (
            max(profits)
            if profits else 0
        ),
        "largest_loser": (
            min(profits)
            if profits else 0
        ),
        "average_return": (
            sum(profits) / len(profits)
            if profits else 0
        ),
    }

    return stats