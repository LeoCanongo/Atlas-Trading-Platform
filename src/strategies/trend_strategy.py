def should_buy(score):
    """
    Returns True if the Atlas score is high enough to buy.
    """
    return score >= 6


class TrendStrategy:
    """
    Default Atlas trend-following strategy.
    """

    name = "Trend Following"

    def evaluate(self, score):

        if score >= 6:
            return "BUY"

        elif score >= 4:
            return "WATCH"

        return "AVOID"


trend_strategy = TrendStrategy()


def evaluate_trend_strategy(score):
    """
    Backwards-compatible wrapper.
    Existing code can still call this function.
    """

    return trend_strategy.evaluate(score)