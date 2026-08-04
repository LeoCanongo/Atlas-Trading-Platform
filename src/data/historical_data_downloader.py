from pathlib import Path
from datetime import timedelta

import pandas as pd
import yfinance as yf

print("=" * 60)
print("ATLAS HISTORICAL DATA DOWNLOADER")
print("=" * 60)

# -------------------------------------------------
# Paths
# -------------------------------------------------

project_root = Path(__file__).parent.parent.parent

data_folder = project_root / "data"
historical_folder = data_folder / "historical"
universe_file = data_folder / "universe.csv"

historical_folder.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Verify Universe
# -------------------------------------------------

if not universe_file.exists():
    raise FileNotFoundError(f"Could not find: {universe_file}")

universe = pd.read_csv(universe_file)

successful = 0
failed = 0

# -------------------------------------------------
# Download Loop
# -------------------------------------------------

for ticker in universe["Ticker"]:

    ticker = str(ticker).strip().upper()

    output_file = historical_folder / f"{ticker}.csv"

    print(f"\n{ticker}")

    try:

        # -----------------------------------------
        # Existing File
        # -----------------------------------------

        existing = None
        start_date = None

        if output_file.exists():

            existing = pd.read_csv(output_file)

            # Remove accidental ticker row from old files
            if (
                len(existing) > 0
                and str(existing.iloc[0]["Date"]).upper() == "AAPL"
            ):
                existing = existing.iloc[1:].reset_index(drop=True)

            if not existing.empty:

                existing["Date"] = pd.to_datetime(existing["Date"])

                last_date = existing["Date"].max()

                start_date = last_date + timedelta(days=1)

                print(f"Updating from {start_date.date()}")

            else:

                existing = None

        else:

            print("Downloading full history")

        # -----------------------------------------
        # Download
        # -----------------------------------------

        kwargs = {
            "tickers": ticker,
            "interval": "1d",
            "progress": False,
            "auto_adjust": False,
            "group_by": "column",
        }

        if start_date is None:
            kwargs["period"] = "5y"
        else:
            kwargs["start"] = start_date.strftime("%Y-%m-%d")

        new_data = yf.download(**kwargs)

        if new_data.empty:

            print("Already up to date.")

            successful += 1

            continue

        # -----------------------------------------
        # Flatten Columns
        # -----------------------------------------

        if isinstance(new_data.columns, pd.MultiIndex):
            new_data.columns = new_data.columns.get_level_values(0)

        new_data.reset_index(inplace=True)

        # Keep only columns Atlas needs
        expected = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
        ]

        new_data = new_data[expected]

        # Ensure numeric columns
        numeric_cols = [
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
        ]

        for col in numeric_cols:
            new_data[col] = pd.to_numeric(new_data[col], errors="coerce")

        new_data = new_data.dropna()

        # -----------------------------------------
        # Merge
        # -----------------------------------------

        if existing is not None:

            combined = pd.concat(
                [existing, new_data],
                ignore_index=True,
            )

            combined = combined.drop_duplicates(
                subset="Date"
            )

            combined = combined.sort_values("Date")

        else:

            combined = new_data

        combined.to_csv(output_file, index=False)

        print(f"Saved {len(combined)} rows")

        successful += 1

    except Exception as e:

        failed += 1

        print(f"Failed: {e}")

# -------------------------------------------------
# Summary
# -------------------------------------------------

print()
print("=" * 60)
print("DOWNLOAD COMPLETE")
print("=" * 60)

print(f"Successful Updates : {successful}")
print(f"Failed Updates     : {failed}")
print(f"Total Symbols      : {len(universe)}")