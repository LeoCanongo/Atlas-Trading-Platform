from src.paper_trading.position_manager import check_positions

# Fake market prices for testing
price_lookup = {
    "AAPL": 345.00,
    "MSFT": 500.00,
    "NVDA": 180.00,
    "META": 700.00,
}

check_positions(price_lookup)