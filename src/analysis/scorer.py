def score_stock(price, sma20, sma50, rsi, macd, signal, adx, volume_ratio):
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

    # Rule 4
    if 40 <= rsi <= 70:
        score += 1
        reasons.append(f"RSI is healthy ({rsi:.2f}).")
    elif rsi > 70:
        reasons.append(f"RSI is overbought ({rsi:.2f}).")
    else:
        reasons.append(f"RSI is oversold ({rsi:.2f}).")

    # Rule 5
    if macd > signal:
        score += 1
        reasons.append("MACD is above its signal line (bullish momentum).")
    else:
        reasons.append("MACD is below its signal line (bearish momentum).")

    # Rule 6
    if adx > 25:
        score += 1
        reasons.append(f"ADX confirms a strong trend ({adx:.2f}).")
    else:
        reasons.append(f"ADX indicates a weak trend ({adx:.2f}).")

    # Rule 7
    if volume_ratio >= 1.2:
        score += 1
        reasons.append(
            f"Volume is {volume_ratio:.2f}x above average (strong confirmation)."
        )
    else:
        reasons.append(
            f"Volume is only {volume_ratio:.2f}x average."
        )

    return score, reasons