from flask import Flask, render_template, request, send_file
import os
from dotenv import load_dotenv

# ML Model Import
from src.ml_model import train_model, predict_signal, load_model

# Project imports
from src.scraper import scrape_yahoo_quote, append_to_csv
from src.hist_fetcher import fetch_history
from src.analyzer import add_indicators, generate_signals
from src.dashboard import plot_with_indicators, plot_prediction_vs_actual
from src.alert import send_email_alert

# Matplotlib config
import matplotlib
matplotlib.use("Agg")

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    chart_path = None
    prediction_chart = None   # <-- Add this line
    selected_stock = None

    if request.method == "POST":

        ticker = request.form.get("ticker")
        selected_stock = ticker

        try:
            # 1) Live quote → CSV
            record = scrape_yahoo_quote(ticker)
            append_to_csv(record, path="data/live_prices.csv")

            # 2) Historical data
            hist_path = f"data/historical_{ticker}.csv"
            hist = fetch_history(ticker, period="6mo", out_csv=hist_path)

            # 3) Indicators + signals
            hist = add_indicators(hist, price_col="Close")
            hist = generate_signals(hist)   

            last = hist.iloc[-1]
            sig = last["signal"]

            if sig == 1:
                signal_text = "BUY"
                result = f"🟢 BUY Signal for {ticker}"
            elif sig == -1:
                signal_text = "SELL"
                result = f"🔴 SELL Signal for {ticker}"
            else:
                signal_text = "HOLD"
                result = f"⚪ HOLD — No Clear Signal"

            # ---------- ML MODEL SECTION ----------
            model = load_model()
            if model is None:
                print("⚠ Training model for first time...")
                accuracy, path = train_model(hist)
                print(f"✔ Model trained (Accuracy: {accuracy:.2f}) saved at: {path}")

            # ML prediction with confidence
            ml_prediction, confidence = predict_signal(last)

            result = f"{result} | 🤖 ML Prediction: {ml_prediction} ({confidence*100:.2f}% confidence)"

            # 👉 Store ML prediction trend in dataframe for chart
            hist.loc[len(hist)-1, "ml_signal"] = ml_prediction


            # ---------- EMAIL ALERTS ----------
            change = last.get("signal_change", 0)

            if change != 0 and signal_text in ("BUY", "SELL"):
                try:
                    send_email_alert(ticker, float(last["Close"]), signal_text)
                except Exception as mail_err:
                    print("Email error:", mail_err)

            # ---------- CHART ----------
            file_path = plot_with_indicators(hist, ticker, outpath="outputs/charts")
            chart_path = f"/chart?file={file_path}"
            
            # 👉 Create prediction vs actual trend chart
            prediction_file = plot_prediction_vs_actual(hist, ticker)
            prediction_chart = f"/chart?file={prediction_file}"


        except Exception as e:
            result = f"⚠️ Error: {str(e)}"

    return render_template(
    "index.html",
    result=result,
    chart=chart_path,
    prediction_chart=prediction_chart,
    selected_stock=selected_stock)



@app.route("/chart")
def serve_chart():
    file = request.args.get("file")
    file = os.path.abspath(file)
    return send_file(file, mimetype="image/png")


@app.route("/download-chart")
def download_chart():
    file = request.args.get("file")
    file = os.path.abspath(file)
    return send_file(file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
