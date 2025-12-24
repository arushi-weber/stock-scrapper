# analyzer.py
# Compute SMA, EMA and simple buy/sell signals.

import pandas as pd
import numpy as np

def add_indicators(df: pd.DataFrame, price_col="Close"):
    df = df.copy()
    df['SMA20'] = df[price_col].rolling(window=20, min_periods=1).mean()
    df['SMA50'] = df[price_col].rolling(window=50, min_periods=1).mean()
    df['EMA20'] = df[price_col].ewm(span=20, adjust=False).mean()
    return df

def generate_signals(df: pd.DataFrame, price_col="Close"):
    df = df.copy()
    # Simple signal: when SMA20 crosses above SMA50 -> buy; below -> sell
    df['signal'] = 0
    df.loc[(df['SMA20'] > df['SMA50']) & (df[price_col] > df['SMA50']), 'signal'] = 1  # BUY
    df.loc[(df['SMA20'] < df['SMA50']) & (df[price_col] < df['SMA50']), 'signal'] = -1 # SELL
    # Generate signal changes
    df['signal_change'] = df['signal'].diff().fillna(0)
    return df

if __name__ == "__main__":
    import hist_fetcher as hf
    df = hf.fetch_history("RELIANCE.NS", period="3mo")
    df = add_indicators(df, price_col="Close")
    df = generate_signals(df, price_col="Close")
    print(df[['Date','Close','SMA20','SMA50','EMA20','signal']].tail(10))
