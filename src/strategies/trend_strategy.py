class TrendStrategy:
    """
    Atlas Trend Following Strategy.

    This strategy favors stocks that are already in
    strong established uptrends.
    """

    name = "Trend Following"

    def evaluate(self, score, market):

        close = market["close"]
        sma20 = market["sma20"]
        sma50 = market["sma50"]
        rsi = market["rsi"]
        adx = market["adx"]
        macd = market["macd"]
        macd_signal = market["macd_signal"]

        # -------------------------------------------------
        # High-Confidence Trend Trade
        # -------------------------------------------------
        if (
            score >= 6
            and close > sma20
            and sma20 > sma50
            and macd > macd_signal
            and 50 <= rsi <= 70
            and adx >= 25
        ):
            return "BUY"

        # -------------------------------------------------
        # Trend Developing
        # -------------------------------------------------
        if (
            score >= 4
            and close > sma20
            and sma20 > sma50
            and macd > macd_signal
        ):
            return "WATCH"

        return "AVOID"


trend_strategy = TrendStrategy()


def should_buy(score):
    """
    Backwards compatibility.
    """
    return score >= 6


def evaluate_trend_strategy(score):
    """
    Legacy wrapper for older Atlas code.

    New code should use:
        strategy.evaluate(score, market)
    """

    dummy_market = {
        "close": 1,
        "sma20": 0,
        "sma50": 0,
        "rsi": 60,
        "adx": 30,
        "macd": 1,
        "macd_signal": 0,
    }

    return trend_strategy.evaluate(score, dummy_market)