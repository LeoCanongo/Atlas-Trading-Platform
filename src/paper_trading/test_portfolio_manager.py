from src.paper_trading.portfolio_manager import get_portfolio_summary

price_lookup = {
    "AAPL": 320.00,
}

portfolio = get_portfolio_summary(price_lookup)

print("\nPortfolio Summary")
print("-" * 40)
print(f"Cash: ${portfolio['cash']:.2f}")
print(f"Market Value: ${portfolio['market_value']:.2f}")
print(f"Total Value: ${portfolio['total_value']:.2f}")
print(f"Unrealized P/L: ${portfolio['unrealized_pl']:.2f}")

print("\nPositions")
print("-" * 40)

for p in portfolio["positions"]:
    print(
        f"{p['ticker']} | "
        f"{p['shares']} shares | "
        f"Current ${p['current']:.2f} | "
        f"P/L ${p['pnl']:.2f}"
    )