import pandas as pd

def add_sma(dataframe, period):
    """
    Adds a Simple Moving Average (SMA) column.

    Example:
    period = 20
    creates a column called SMA_20
    """

    column_name = f"SMA_{period}"

    dataframe[column_name] = (
        dataframe["Close"]
        .rolling(window=period)
        .mean()
    )

    return dataframe