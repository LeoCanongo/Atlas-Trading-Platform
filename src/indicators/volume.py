import pandas as pd


def add_volume(df, period=20):
    df["VOL_AVG"] = df["Volume"].rolling(period).mean()

    df["VOL_RATIO"] = df["Volume"] / df["VOL_AVG"]

    return df