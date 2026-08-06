from datetime import datetime


class WatchlistManager:

    def __init__(self):

        self.watchlist = []

    # -------------------------------------------------
    # Add Opportunity
    # -------------------------------------------------

    def add(
        self,
        ticker,
        signal,
        atlas_score,
        confidence,
        trade_quality,
        position_quality,
        atlas_rank,
        price,
    ):

        self.watchlist.append({
            "timestamp": datetime.now(),
            "ticker": ticker,
            "signal": signal,
            "atlas_score": atlas_score,
            "confidence": confidence,
            "trade_quality": trade_quality,
            "position_quality": position_quality,
            "atlas_rank": atlas_rank,
            "price": price,
        })

    # -------------------------------------------------
    # Sort
    # -------------------------------------------------

    def sort(self):

        self.watchlist.sort(
            key=lambda trade: trade["atlas_rank"],
            reverse=True,
        )

    # -------------------------------------------------
    # Get All
    # -------------------------------------------------

    def get_all(self):

        return self.watchlist

    # -------------------------------------------------
    # Get BUY Signals
    # -------------------------------------------------

    def get_buy_signals(self):

        return [
            trade
            for trade in self.watchlist
            if trade["signal"] == "BUY"
        ]

    # -------------------------------------------------
    # Get WATCH Signals
    # -------------------------------------------------

    def get_watch_signals(self):

        return [
            trade
            for trade in self.watchlist
            if trade["signal"] == "WATCH"
        ]

    # -------------------------------------------------
    # Get AVOID Signals
    # -------------------------------------------------

    def get_avoid_signals(self):

        return [
            trade
            for trade in self.watchlist
            if trade["signal"] == "AVOID"
        ]

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        self.watchlist.clear()

    # -------------------------------------------------
    # Count
    # -------------------------------------------------

    def count(self):

        return len(self.watchlist)