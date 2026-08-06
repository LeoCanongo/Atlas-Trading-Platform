class RankingEngine:

    @staticmethod
    def calculate(score, confidence, signal, market_data):

        rank = score * 100
        rank += confidence

        # -------------------------
        # Signal Bonus
        # -------------------------

        signal_bonus = {
            "BUY": 25,
            "WATCH": 10,
            "AVOID": 0,
        }

        rank += signal_bonus.get(signal, 0)

        # -------------------------
        # Trend Strength
        # -------------------------

        adx = market_data["adx"]

        if adx >= 40:
            rank += 30
        elif adx >= 30:
            rank += 20
        elif adx >= 25:
            rank += 10

        # -------------------------
        # Relative Volume
        # -------------------------

        vol_ratio = market_data["vol_ratio"]

        if vol_ratio >= 2:
            rank += 20
        elif vol_ratio >= 1.5:
            rank += 10

        # -------------------------
        # RSI Preference
        # -------------------------

        rsi = market_data["rsi"]

        if 55 <= rsi <= 65:
            rank += 15
        elif 50 <= rsi <= 70:
            rank += 8

        # -------------------------
        # SMA20 Distance
        # -------------------------

        distance = (
            (market_data["close"] - market_data["sma20"])
            / market_data["sma20"]
        ) * 100

        if distance <= 3:
            rank += 10

        # -------------------------
        # ATR %
        # -------------------------

        atr_percent = (
            market_data["atr"]
            / market_data["close"]
        ) * 100

        if 2 <= atr_percent <= 5:
            rank += 10

        return round(rank, 2)