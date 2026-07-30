from src.paper_trading.paper_trader import (
    load_account,
    sell_stock,
)


def check_positions(price_lookup):
    """
    Checks all open positions against their stop-loss
    and take-profit levels.

    Parameters
    ----------
    price_lookup : dict

    Example:
    {
        "AAPL": 320.15,
        "MSFT": 505.20
    }
    """

    account = load_account()

    if not account["positions"]:
        print("No open positions.")
        return

    print("\nChecking Positions...")
    print("-" * 40)

    for position in account["positions"]:

        ticker = position["ticker"]

        if ticker not in price_lookup:
            print(f"{ticker}: No current price available.")
            continue

        current_price = price_lookup[ticker]

        stop_loss = position["stop_loss"]
        take_profit = position["take_profit"]

        print(
            f"{ticker}: "
            f"Current ${current_price:.2f} | "
            f"SL ${stop_loss:.2f} | "
            f"TP ${take_profit:.2f}"
        )

        if current_price <= stop_loss:

            print(f"➡ Stop loss triggered for {ticker}")

            sell_stock(
                ticker,
                current_price,
            )

        elif current_price >= take_profit:

            print(f"➡ Take profit triggered for {ticker}")

            sell_stock(
                ticker,
                current_price,
            )

        else:

            print("Holding position.")