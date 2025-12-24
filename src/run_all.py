# run_all.py
# Orchestrator: scrape live price, fetch history, analyze, plot, and optionally alert.

import os
from scraper import scrape_yahoo_quote, append_to_csv
from hist_fetcher import fetch_history
from analyzer import add_indicators, generate_signals
from dashboard import plot_with_indicators
import pandas as pd

DATA_DIR = "data"
OUT_DIR = "outputs/charts"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def run(ticker="RELIANCE.NS"):
    print("Scraping live price...")
    rec = scrape_yahoo_quote(ticker)
    append_to_csv(rec, path=f"{DATA_DIR}/live_prices.csv")

    print("Fetching history...")
    hist_path = f"{DATA_DIR}/historical_{ticker}.csv"
    hist = fetch_history(ticker, period="6mo", out_csv=hist_path)

    print("Analyzing...")
    hist = add_indicators(hist, price_col="Close")
    hist = generate_signals(hist, price_col="Close")

    # Save analysis
    hist.to_csv(f"{DATA_DIR}/analysis_{ticker}.csv", index=False)

    print("Plotting dashboard...")
    chart_file = plot_with_indicators(hist, ticker, outpath=OUT_DIR)

    # Simple: print most recent signal
    last = hist.iloc[-1]
    sig = hist.iloc[-1]['signal']
    if sig == 1:
        result = f"🟢 BUY Signal for {ticker}"
    elif sig == -1:
        result = f"🔴 SELL Signal for {ticker}"
    else:
        result = f"⚪ HOLD / No Action"


    print("Done. Chart saved to:", chart_file)

if __name__ == "__main__":
    run("RELIANCE.NS")
