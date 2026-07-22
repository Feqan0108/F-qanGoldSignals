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
