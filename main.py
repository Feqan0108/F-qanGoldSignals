import requests
import pandas as pd
import ta
import schedule
import time

from telegram import Bot
from config import *

bot = Bot(token=TELEGRAM_TOKEN)

SYMBOL = "XAU/USD"
INTERVAL = "5min"

last_signal = None


def get_price_data():

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={SYMBOL}"
        f"&interval={INTERVAL}"
        f"&outputsize=300"
        f"&apikey={TWELVE_DATA_API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    if "values" not in data:
        print("API Error")
        return None

    df = pd.DataFrame(data["values"])

    df = df.iloc[::-1]

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["open"] = df["open"].astype(float)

    return df
def send_signal(signal, price):

    global last_signal

    if signal == last_signal:
        return

    if signal == "BUY":
        sl = round(price - 5, 2)
        tp = round(price + 10, 2)
    else:
        sl = round(price + 5, 2)
        tp = round(price - 10, 2)

    message = f"""
🔥 Fəqan Gold Signals

📊 Symbol: XAU/USD

📈 Signal: {signal}

💰 Entry: {price}

🛑 Stop Loss: {sl}

🎯 Take Profit: {tp}

⏰ Timeframe: M5
"""

    bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

    last_signal = signal


def check_market():

    df = get_price_data()

    if df is None:
        return

    signal = generate_signal(df)

    if signal is None:
        print("No Signal")
        return

    price = float(df.iloc[-1]["close"])

    send_signal(signal, price)
    def run_bot():
    print("🚀 Fəqan Gold Signals Bot Started")

    while True:
        try:
            check_market()
        except Exception as e:
            print(f"Error: {e}")

        # Hər 5 dəqiqədən bir yoxla
        time.sleep(300)


if __name__ == "__main__":
    run_bot()
