def score_stock(price, sma20, sma50):
    score = 0
    reasons = []

    # Rule 1
    if price > sma20:
        score += 1
        reasons.append("Price is above the 20-day moving average.")

    # Rule 2
    if price > sma50:
        score += 1
        reasons.append("Price is above the 50-day moving average.")

    # Rule 3
    if sma20 > sma50:
        score += 1
        reasons.append("Short-term trend is stronger than the long-term trend.")

    return score, reasons