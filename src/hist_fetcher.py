# hist_fetcher.py
# Uses yfinance to download historical OHLC data for analysis.

import yfinance as yf
import pandas as pd

def fetch_history(ticker: str, period="1y", interval="1d", out_csv=None):
    t = yf.Ticker(ticker)
    hist = t.history(period=period, interval=interval)
    hist = hist.reset_index()
    if out_csv:
        hist.to_csv(out_csv, index=False)
    return hist

if __name__ == "__main__":
    df = fetch_history("RELIANCE.NS", period="6mo", out_csv="data/historical_RELIANCE.NS.csv")
    print(df.tail())
