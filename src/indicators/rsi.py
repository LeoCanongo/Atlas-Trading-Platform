import pandas as pd


def add_rsi(dataframe, period=14):
    """
    Adds a Relative Strength Index (RSI) column.

    Example:
        period = 14

        Creates:
            RSI_14
    """

    delta = dataframe["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    dataframe[f"RSI_{period}"] = rsi

    return dataframe