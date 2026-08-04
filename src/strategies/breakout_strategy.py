class BreakoutStrategy:
    """
    Atlas Breakout Strategy.

    Searches for stocks breaking into new highs with
    strong momentum and increased volume.
    """

    name = "Breakout"

    def evaluate(self, score, market):

        close = market["close"]
        high = market["high"]

        sma20 = market["sma20"]
        sma50 = market["sma50"]

        rsi = market["rsi"]

        adx = market["adx"]

        volume = market["volume"]
        average_volume = market["average_volume"]
        vol_ratio = market["vol_ratio"]

        atr = market["atr"]

        twenty_day_high = market["twenty_day_high"]

        # -------------------------------------------------
        # High-Confidence Breakout
        # -------------------------------------------------
        if (
            score >= 5
            and close >= twenty_day_high
            and close > sma20
            and sma20 > sma50
            and volume > average_volume
            and vol_ratio >= 1.5
            and 55 <= rsi <= 75
            and adx >= 20
        ):
            return "BUY"

        # -------------------------------------------------
        # Breakout Forming
        # -------------------------------------------------
        if (
            score >= 4
            and close > sma20
            and high >= twenty_day_high * 0.99
            and vol_ratio >= 1.2
            and adx >= 18
        ):
            return "WATCH"

        return "AVOID"


breakout_strategy = BreakoutStrategy()