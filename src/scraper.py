import requests
from datetime import datetime
import csv
import os


def scrape_yahoo_quote(ticker: str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    # Ensure response is valid JSON
    if not response.text.strip():
        raise ValueError("Empty response from Yahoo Finance")

    data = response.json()

    result = data.get("chart", {}).get("result", [])
    if not result:
        raise ValueError(f"Invalid ticker or blocked request: {ticker}")

    price = result[0]["meta"]["regularMarketPrice"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"ticker": ticker, "price": float(price), "time": timestamp}


def append_to_csv(record: dict, path="data/live_prices.csv"):
    file_exists = os.path.isfile(path)

    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ticker", "price", "time"])
        
        if not file_exists:
            writer.writeheader()

        writer.writerow(record)

    print("✔ Recorded Price:", record)
