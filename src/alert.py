import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("ALERT_EMAIL")
PASSWORD = os.getenv("ALERT_PASS")
TO = os.getenv("ALERT_TO")

def send_email_alert(stock, price, signal):
    subject = f"📈 Stock Alert: {stock} - {signal}"
    message = f"""
Hello,

Stock: {stock}
Current Price: ₹{price}
Signal: {signal}

Action: {"👉 BUY" if signal == "BUY" else "⚠ SELL"}

Stay updated 🚀
"""

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = TO

    try:
        print("📡 Connecting to Gmail...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.ehlo()  # required for some Gmail accounts
            server.login(str(EMAIL), str(PASSWORD))
            server.sendmail(EMAIL, TO, msg.as_string())
            print("📬 Email Sent Successfully!")

    except Exception as e:
        print(f"❌ Email Error: {e}")
