import pandas as pd

def add_macd(dataframe):
    ema12 = dataframe["Close"].ewm(span=12, adjust=False).mean()
    ema26 = dataframe["Close"].ewm(span=26, adjust=False).mean()

    dataframe["MACD"] = ema12 - ema26
    dataframe["MACD_SIGNAL"] = (
        dataframe["MACD"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    return dataframe