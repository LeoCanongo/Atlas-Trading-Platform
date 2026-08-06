class WatchlistReport:

    @staticmethod
    def display(results, universe_size):

        buy = []
        watch = []
        avoid = []

        for stock in results:

            if stock["Signal"] == "BUY":
                buy.append(stock)

            elif stock["Signal"] == "WATCH":
                watch.append(stock)

            else:
                avoid.append(stock)

        print()
        print("=" * 70)
        print("ATLAS WATCHLIST")
        print("=" * 70)

        # ------------------------------------------------
        # BUY
        # ------------------------------------------------

        print("\nBUY")
        print("-" * 70)

        if buy:
            for i, stock in enumerate(buy, start=1):

                print(
                    f"{i}. "
                    f"{stock['Ticker']:<8}"
                    f"Score {stock['Score']}/7   "
                    f"Confidence {stock['Confidence']}%"
                )
        else:
            print("None")

        # ------------------------------------------------
        # WATCH
        # ------------------------------------------------

        print("\nWATCH")
        print("-" * 70)

        if watch:
            start = len(buy) + 1

            for i, stock in enumerate(watch, start=start):

                print(
                    f"{i}. "
                    f"{stock['Ticker']:<8}"
                    f"Score {stock['Score']}/7   "
                    f"Confidence {stock['Confidence']}%"
                )
        else:
            print("None")

        # ------------------------------------------------
        # AVOID
        # ------------------------------------------------

        print("\nAVOID")
        print("-" * 70)

        if avoid:

            start = len(buy) + len(watch) + 1

            for i, stock in enumerate(avoid, start=start):

                print(
                    f"{i}. "
                    f"{stock['Ticker']}"
                )

        else:
            print("None")

        # ------------------------------------------------
        # Summary
        # ------------------------------------------------

        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)

        print(f"Universe Size   : {universe_size}")
        print(f"Passed Filters  : {len(results)}")
        print(f"BUY Candidates  : {len(buy)}")
        print(f"WATCH           : {len(watch)}")
        print(f"AVOID           : {len(avoid)}")
        print(f"Rejected        : {universe_size - len(results)}")