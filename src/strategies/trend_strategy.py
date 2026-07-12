def should_buy(score):
    """
    Returns True if the Atlas score is high enough to buy.
    """
    return score >= 6


def evaluate_trend_strategy(score):
    """
    Returns a trading signal based on the Atlas score.
    """

    if score >= 6:
        return "BUY"

    elif score >= 4:
        return "WATCH"

    else:
        return "AVOID"