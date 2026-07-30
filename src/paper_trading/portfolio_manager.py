from src.paper_trading.paper_trader import load_account


def get_portfolio_summary(price_lookup):
    """
    Calculate portfolio statistics.

    price_lookup example:
    {
        "AAPL": 320.15,
        "META": 705.20
    }
    """

    account = load_account()

    cash = account["cash"]

    market_value = 0.0
    unrealized_pl = 0.0

    positions = []

    for position in account["positions"]:

        ticker = position["ticker"]
        shares = position["shares"]
        entry = position["entry"]

        current = price_lookup.get(ticker, entry)

        value = shares * current
        cost = shares * entry
        pnl = value - cost

        market_value += value
        unrealized_pl += pnl

        positions.append({
            "ticker": ticker,
            "shares": shares,
            "entry": entry,
            "current": current,
            "value": value,
            "pnl": pnl,
        })

    total_value = cash + market_value

    return {
        "cash": cash,
        "market_value": market_value,
        "total_value": total_value,
        "unrealized_pl": unrealized_pl,
        "positions": positions,
    }