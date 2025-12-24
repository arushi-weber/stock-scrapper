# dashboard.py
# Plot price with SMA/EMA and save a PNG file.
import matplotlib
matplotlib.use("Agg")  # Disable GUI backend (Tkinter)

import matplotlib.pyplot as plt
import pandas as pd
from src.analyzer import add_indicators

def plot_with_indicators(df: pd.DataFrame, ticker:str, outpath="outputs/charts"):
    df = df.copy()
    df = add_indicators(df, price_col="Close")
    plt.figure(figsize=(12,6))
    plt.plot(df['Date'], df['Close'], label='Close')
    plt.plot(df['Date'], df['SMA20'], label='SMA20')
    plt.plot(df['Date'], df['SMA50'], label='SMA50')
    plt.plot(df['Date'], df['EMA20'], label='EMA20')
    plt.title(f"{ticker} - Price & Indicators")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    fname = f"{outpath}/{ticker}_indicators.png"
    plt.savefig(fname)
    plt.close()
    return fname

def plot_prediction_vs_actual(df, ticker, outpath="outputs/charts"):
    plt.figure(figsize=(12, 6))

    # Plot actual close prices
    plt.plot(df['Date'], df['Close'], label="Actual Price", linewidth=2)

    # Plot ML predictions if column exists
    if 'ml_signal' in df.columns:
        plt.plot(df['Date'], df['ml_signal'], label="ML Prediction Trend", linestyle="dashed")

    # Mark buy/sell points
    buys = df[df['signal'] == 1]
    sells = df[df['signal'] == -1]

    plt.scatter(buys['Date'], buys['Close'], color='green', label='Buy', marker='^', s=100)
    plt.scatter(sells['Date'], sells['Close'], color='red', label='Sell', marker='v', s=100)

    plt.title(f"{ticker} - ML Prediction vs Actual Price")
    plt.xlabel("Date")
    plt.ylabel("Price / Model Output")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    fname = f"{outpath}/{ticker}_prediction_vs_actual.png"
    plt.savefig(fname)
    plt.close()

    return fname

if __name__ == "__main__":
    import hist_fetcher as hf
    df = hf.fetch_history("RELIANCE.NS", period="3mo")
    p = plot_with_indicators(df, "RELIANCE.NS")
    print("Saved chart to", p)
