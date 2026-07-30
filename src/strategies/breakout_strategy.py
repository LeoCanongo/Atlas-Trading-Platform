class BreakoutStrategy:
    """
    Simple breakout strategy.
    """

    name = "Breakout"

    def evaluate(self, score):

        if score >= 7:
            return "BUY"

        elif score >= 5:
            return "WATCH"

        return "AVOID"


breakout_strategy = BreakoutStrategy()