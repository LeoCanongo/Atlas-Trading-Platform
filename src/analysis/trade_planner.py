def create_trade_plan(price, atr, score, max_score=7):

    stop_loss = price - (1.5 * atr)
    take_profit = price + (3 * atr)

    confidence = round((score / max_score) * 100)

    if confidence >= 90:
        recommendation = "STRONG BUY 🟢"
        trend = "Very Strong 🟢"

    elif confidence >= 75:
        recommendation = "BUY 🟢"
        trend = "Strong 🟢"

    elif confidence >= 60:
        recommendation = "WATCH 🟡"
        trend = "Moderate 🟡"

    else:
        recommendation = "AVOID 🔴"
        trend = "Weak 🔴"

    return {
        "recommendation": recommendation,
        "entry": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": confidence,
        "trend": trend,
    }