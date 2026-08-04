class MomentumStrategy:
    """
    Atlas Momentum Strategy.

    Finds stocks with strong momentum,
    high volume, and accelerating trends.
    """

    name = "Momentum"

    def evaluate(self, score, market):

        close = market["close"]

        sma20 = market["sma20"]
        sma50 = market["sma50"]

        rsi = market["rsi"]

        macd = market["macd"]
        macd_signal = market["macd_signal"]

        adx = market["adx"]

        vol_ratio = market["vol_ratio"]

        # ------------------------------------
        # Strong Momentum
        # ------------------------------------
        if (
            score >= 6
            and close > sma20
            and sma20 > sma50
            and macd > macd_signal
            and 60 <= rsi <= 80
            and adx >= 25
            and vol_ratio >= 1.3
        ):
            return "BUY"

        # ------------------------------------
        # Momentum Building
        # ------------------------------------
        if (
            score >= 4
            and close > sma20
            and macd > macd_signal
            and vol_ratio >= 1.1
        ):
            return "WATCH"

        return "AVOID"


momentum_strategy = MomentumStrategy()