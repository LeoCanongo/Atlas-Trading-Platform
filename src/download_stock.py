from pathlib import Path
import yfinance as yf

print("=" * 60)
print("Atlas Trading Platform")
print("Market Data Downloader")
print("=" * 60)

# Find the project root folder
project_root = Path(__file__).parent.parent

# Locate the watchlist
watchlist_file = project_root / "config" / "watchlist.txt"

print(f"\nLooking for watchlist at:\n{watchlist_file}")

# Read all stock tickers from the watchlist
with open(watchlist_file, "r") as file:
    tickers = [line.strip().upper() for line in file if line.strip()]

print("\nWatchlist contains:")
print(tickers)

# Create the historical data folder if it doesn't exist
data_folder = project_root / "data" / "historical"
data_folder.mkdir(parents=True, exist_ok=True)

# Download data for every stock
for ticker in tickers:

    print(f"\nDownloading {ticker}...")

    stock = yf.Ticker(ticker)

    # Download ONE YEAR of historical data
    history = stock.history(period="1y")

    filename = data_folder / f"{ticker}.csv"

    history.to_csv(filename)

    print(f"Saved {ticker}.csv")

print("\n✅ All downloads completed successfully!")