from src.analysis.market_scanner import results
from src.paper_trading.paper_trader import (
    buy_stock,
    load_account,
)
from src.paper_trading.position_manager import check_positions
from src.analysis.trade_planner import create_trade_plan
from src.risk.position_sizer import calculate_position_size
from src.config.settings import load_settings


def main():

    SETTINGS = load_settings()

    print("=" * 50)
    print("ATLAS AUTO PAPER TRADER")
    print("=" * 50)

    # ------------------------------------------
    # Load account
    # ------------------------------------------

    account = load_account()

    # ------------------------------------------
    # Build latest price lookup
    # ------------------------------------------

    price_lookup = {}

    for stock in results:
        price_lookup[stock["Ticker"]] = stock["Price"]

    # ------------------------------------------
    # Manage existing positions
    # ------------------------------------------

    check_positions(price_lookup)

    # ------------------------------------------
    # Find a stock we don't already own
    # ------------------------------------------

    best = None

    for stock in results:

        already_owned = False

        for position in account["positions"]:

            if position["ticker"] == stock["Ticker"]:
                already_owned = True
                break

        if not already_owned:
            best = stock
            break

    if best is None:

        print("\nNo new trading opportunities.")
        return

    ticker = best["Ticker"]
    price = best["Price"]
    score = best["Score"]
    atr = best["ATR"]

    print(f"\nSelected Stock: {ticker}")

    plan = create_trade_plan(
        price,
        atr,
        score,
    )

    position = calculate_position_size(
        account_size=SETTINGS["account_size"],
        risk_percent=SETTINGS["risk_percent"],
        entry_price=plan["entry"],
        stop_loss=plan["stop_loss"],
    )

    shares = position["shares"]

    buy_stock(
        ticker=ticker,
        shares=shares,
        price=plan["entry"],
        stop_loss=plan["stop_loss"],
        take_profit=plan["take_profit"],
    )

    print("\nTrade Complete")


if __name__ == "__main__":
    main()