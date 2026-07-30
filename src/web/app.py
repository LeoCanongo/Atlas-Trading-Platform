from pathlib import Path
from flask import Flask, render_template, request, redirect

from src.analysis.market_scanner import results
from src.config.settings import (
    SETTINGS,
    save_settings,
)
from src.paper_trading.paper_trader import (
    load_account,
    load_history,
)
from src.paper_trading.portfolio_manager import (
    get_portfolio_summary,
)

project_root = Path(__file__).resolve().parent.parent.parent

app = Flask(
    __name__,
    template_folder=str(project_root / "templates"),
    static_folder=str(project_root / "static"),
)


@app.route("/", methods=["GET", "POST"])
def dashboard():

    if request.method == "POST":

        SETTINGS["account_size"] = float(
            request.form["account_size"]
        )

        SETTINGS["risk_percent"] = float(
            request.form["risk_percent"]
        )

        SETTINGS["minimum_score"] = int(
            request.form["minimum_score"]
        )

        save_settings(SETTINGS)

        return redirect("/")

    account = load_account()
    history = load_history()

    price_lookup = {}

    for stock in results:
        price_lookup[stock["Ticker"]] = stock["Price"]

    portfolio = get_portfolio_summary(price_lookup)

    return render_template(
        "dashboard.html",
        stocks=results,
        settings=SETTINGS,
        account=account,
        history=history,
        portfolio=portfolio,
    )


if __name__ == "__main__":
    app.run(debug=True)