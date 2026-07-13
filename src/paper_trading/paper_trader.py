import json
from pathlib import Path
from datetime import datetime

ACCOUNT_FILE = Path("paper_account.json")
HISTORY_FILE = Path("paper_trade_history.json")


def load_account():

    if ACCOUNT_FILE.exists():
        with open(ACCOUNT_FILE, "r") as f:
            return json.load(f)

    account = {
        "cash": 10000.0,
        "positions": []
    }

    save_account(account)
    return account


def save_account(account):

    with open(ACCOUNT_FILE, "w") as f:
        json.dump(account, f, indent=4)


def load_history():

    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)

    return []


def save_history(history):

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def record_trade(action, ticker, shares, price):

    history = load_history()

    history.append(
        {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "ticker": ticker,
            "shares": shares,
            "price": price,
        }
    )

    save_history(history)


def buy_stock(ticker, shares, price):

    account = load_account()

    cost = shares * price

    if cost > account["cash"]:
        print("❌ Not enough cash.")
        return

    account["cash"] -= cost

    account["positions"].append(
        {
            "ticker": ticker,
            "shares": shares,
            "entry": price
        }
    )

    save_account(account)

    record_trade(
        "BUY",
        ticker,
        shares,
        price
    )

    print(f"✅ Bought {shares} shares of {ticker} @ ${price:.2f}")


def sell_stock(ticker, price):

    account = load_account()

    for position in account["positions"]:

        if position["ticker"] == ticker:

            proceeds = position["shares"] * price

            account["cash"] += proceeds

            account["positions"].remove(position)

            save_account(account)

            record_trade(
                "SELL",
                ticker,
                position["shares"],
                price
            )

            print(f"✅ Sold {ticker} @ ${price:.2f}")

            return

    print("❌ Position not found.")


def show_account():

    account = load_account()

    print("\n==============================")
    print("      PAPER ACCOUNT")
    print("==============================")

    print(f"Cash: ${account['cash']:.2f}")
    print()

    if not account["positions"]:
        print("No open positions.")
        return

    print("Positions:\n")

    for p in account["positions"]:

        print(
            f"{p['ticker']} | "
            f"{p['shares']} shares | "
            f"Entry ${p['entry']:.2f}"
        )


if __name__ == "__main__":

    show_account()