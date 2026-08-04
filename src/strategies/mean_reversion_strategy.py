class MeanReversionStrategy:
    """
    Atlas Mean Reversion Strategy.

    Looks for oversold stocks that may be
    ready for a rebound.
    """

    name = "Mean Reversion"

    def evaluate(self, score, market):

        close = market["close"]

        sma20 = market["sma20"]
        sma50 = market["sma50"]

        rsi = market["rsi"]

        macd = market["macd"]
        macd_signal = market["macd_signal"]

        adx = market["adx"]

        vol_ratio = market["vol_ratio"]

        twenty_day_low = market["twenty_day_low"]

        # ------------------------------------
        # High-Probability Reversal
        # ------------------------------------
        if (
            score >= 4
            and close <= twenty_day_low * 1.02
            and close < sma20
            and sma20 >= sma50
            and rsi <= 35
            and macd >= macd_signal
            and vol_ratio >= 1.0
            and adx >= 15
        ):
            return "BUY"

        # ------------------------------------
        # Possible Reversal
        # ------------------------------------
        if (
            rsi <= 40
            and close < sma20
            and macd >= macd_signal
        ):
            return "WATCH"

        return "AVOID"


mean_reversion_strategy = MeanReversionStrategy()