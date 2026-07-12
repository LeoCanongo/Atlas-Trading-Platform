import json
from pathlib import Path

ACCOUNT_FILE = Path("paper_account.json")


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

    print(f"✅ Bought {shares} shares of {ticker} @ ${price:.2f}")


def sell_stock(ticker, price):

    account = load_account()

    for position in account["positions"]:

        if position["ticker"] == ticker:

            proceeds = position["shares"] * price

            account["cash"] += proceeds

            account["positions"].remove(position)

            save_account(account)

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

    buy_stock("AAPL", 5, 316.22)

    show_account()