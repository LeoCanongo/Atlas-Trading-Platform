class QualityFilter:

    # ---------------------------------
    # Score
    # ---------------------------------

    MIN_SCORE = 4

    # ---------------------------------
    # Liquidity
    # ---------------------------------

    MIN_AVG_VOLUME = 500000
    MIN_RELATIVE_VOLUME = 1.20

    # ---------------------------------
    # Volatility
    # ---------------------------------

    MIN_ATR_PERCENT = 1.0
    MAX_ATR_PERCENT = 8.0

    MAX_DAILY_RANGE = 8.0
    MAX_GAP = 5.0

    # ---------------------------------
    # Trend
    # ---------------------------------

    MAX_DISTANCE_FROM_SMA20 = 8.0

    # ---------------------------------
    # Momentum
    # ---------------------------------

    MAX_RSI = 75

    @classmethod
    def passes(cls, score, market):

        # ----------------------------
        # Score
        # ----------------------------

        if score < cls.MIN_SCORE:
            return False

        # ----------------------------
        # Trend
        # ----------------------------

        if market["sma20"] <= market["sma50"]:
            return False

        # ----------------------------
        # Liquidity
        # ----------------------------

        if market["average_volume"] < cls.MIN_AVG_VOLUME:
            return False

        if market["vol_ratio"] < cls.MIN_RELATIVE_VOLUME:
            return False

        # ----------------------------
        # ATR
        # ----------------------------

        atr_percent = (
            market["atr"]
            / market["close"]
        ) * 100

        if atr_percent < cls.MIN_ATR_PERCENT:
            return False

        if atr_percent > cls.MAX_ATR_PERCENT:
            return False

        # ----------------------------
        # Daily Range
        # ----------------------------

        if market["daily_range_percent"] > cls.MAX_DAILY_RANGE:
            return False

        # ----------------------------
        # Gap Filter
        # ----------------------------

        gap = abs(
            (
                market["open"]
                - market["previous_close"]
            )
            / market["previous_close"]
        ) * 100

        if gap > cls.MAX_GAP:
            return False

        # ----------------------------
        # Distance Above SMA20
        # ----------------------------

        distance = (
            (
                market["close"]
                - market["sma20"]
            )
            / market["sma20"]
        ) * 100

        if distance > cls.MAX_DISTANCE_FROM_SMA20:
            return False

        # ----------------------------
        # RSI
        # ----------------------------

        if market["rsi"] > cls.MAX_RSI:
            return False

        return True