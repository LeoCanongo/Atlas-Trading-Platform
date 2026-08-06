class TradeQuality:

    @staticmethod
    def evaluate(score, market_data):

        quality = 0

        # -----------------------------
        # Atlas Score
        # -----------------------------

        quality += score * 10

        # -----------------------------
        # Trend Strength
        # -----------------------------

        adx = market_data["adx"]

        if adx >= 40:
            quality += 15
        elif adx >= 30:
            quality += 10
        elif adx >= 25:
            quality += 5

        # -----------------------------
        # Relative Volume
        # -----------------------------

        vol = market_data["vol_ratio"]

        if vol >= 2:
            quality += 15
        elif vol >= 1.5:
            quality += 10
        elif vol >= 1.2:
            quality += 5

        # -----------------------------
        # RSI
        # -----------------------------

        rsi = market_data["rsi"]

        if 55 <= rsi <= 65:
            quality += 10
        elif 50 <= rsi <= 70:
            quality += 5

        # -----------------------------
        # ATR %
        # -----------------------------

        atr_percent = (
            market_data["atr"]
            / market_data["close"]
        ) * 100

        if 2 <= atr_percent <= 5:
            quality += 10

        # -----------------------------
        # Distance from SMA20
        # -----------------------------

        distance = abs(
            (
                market_data["close"]
                - market_data["sma20"]
            )
            / market_data["sma20"]
        ) * 100

        if distance <= 3:
            quality += 10
        elif distance <= 5:
            quality += 5

        # -----------------------------
        # Grade
        # -----------------------------

        if quality >= 90:
            grade = "A+"
        elif quality >= 80:
            grade = "A"
        elif quality >= 70:
            grade = "B"
        elif quality >= 60:
            grade = "C"
        else:
            grade = "D"

        return {
            "score": round(quality),
            "grade": grade,
        }