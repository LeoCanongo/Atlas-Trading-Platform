class WatchlistReport:

    @staticmethod
    def display(results, universe_size):

        buy = []
        watch = []
        avoid = []

        for stock in results:

            signal = stock["signal"]

            if signal == "BUY":
                buy.append(stock)

            elif signal == "WATCH":
                watch.append(stock)

            else:
                avoid.append(stock)

        print()
        print("=" * 80)
        print("ATLAS WATCHLIST")
        print("=" * 80)

        # -------------------------------------------------
        # BUY
        # -------------------------------------------------

        print("\nBUY")
        print("-" * 80)

        if buy:

            for i, stock in enumerate(buy, start=1):

                tq = stock["trade_quality"]
                pq = stock["position_quality"]

                print(f"{i}. {stock['ticker']}")

                print(
                    f"   Price:            ${stock['price']:.2f}"
                )

                print(
                    f"   Atlas Score:      {stock['atlas_score']}/7"
                )

                print(
                    f"   Confidence:       {stock['confidence']}%"
                )

                print(
                    f"   Trade Quality:    {tq['score']} ({tq['grade']})"
                )

                print(
                    f"   Position Grade:   {pq['grade']}"
                )

                print(
                    f"   Risk/Reward:      {pq['rr']}:1"
                )

                print(
                    f"   Atlas Rank:       {stock['atlas_rank']:.2f}"
                )

                print()

        else:

            print("None")

        # -------------------------------------------------
        # WATCH
        # -------------------------------------------------

        print("\nWATCH")
        print("-" * 80)

        if watch:

            start = len(buy) + 1

            for i, stock in enumerate(watch, start=start):

                tq = stock["trade_quality"]
                pq = stock["position_quality"]

                print(f"{i}. {stock['ticker']}")

                print(
                    f"   Price:            ${stock['price']:.2f}"
                )

                print(
                    f"   Atlas Score:      {stock['atlas_score']}/7"
                )

                print(
                    f"   Confidence:       {stock['confidence']}%"
                )

                print(
                    f"   Trade Quality:    {tq['score']} ({tq['grade']})"
                )

                print(
                    f"   Position Grade:   {pq['grade']}"
                )

                print(
                    f"   Risk/Reward:      {pq['rr']}:1"
                )

                print(
                    f"   Atlas Rank:       {stock['atlas_rank']:.2f}"
                )

                print()

        else:

            print("None")

        # -------------------------------------------------
        # AVOID
        # -------------------------------------------------

        print("\nAVOID")
        print("-" * 80)

        if avoid:

            start = len(buy) + len(watch) + 1

            for i, stock in enumerate(avoid, start=start):

                tq = stock["trade_quality"]
                pq = stock["position_quality"]

                print(f"{i}. {stock['ticker']}")

                print(
                    f"   Price:            ${stock['price']:.2f}"
                )

                print(
                    f"   Atlas Score:      {stock['atlas_score']}/7"
                )

                print(
                    f"   Confidence:       {stock['confidence']}%"
                )

                print(
                    f"   Trade Quality:    {tq['score']} ({tq['grade']})"
                )

                print(
                    f"   Position Grade:   {pq['grade']}"
                )

                print(
                    f"   Risk/Reward:      {pq['rr']}:1"
                )

                print(
                    f"   Atlas Rank:       {stock['atlas_rank']:.2f}"
                )

                print()

        else:

            print("None")

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)

        print(f"Universe Size   : {universe_size}")
        print(f"Passed Filters  : {len(results)}")
        print(f"BUY Candidates  : {len(buy)}")
        print(f"WATCH           : {len(watch)}")
        print(f"AVOID           : {len(avoid)}")
        print(f"Rejected        : {universe_size - len(results)}")