from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pandas as pd
import yfinance as yf
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

PAIRS = ["EURUSD=X", "GBPUSD=X", "USDJPY=X"]

def analyze_pair(pair):
    df = yf.download(pair, interval="1m", period="1d")
    df.dropna(inplace=True)

    df["EMA20"] = EMAIndicator(df["Close"], window=20).ema_indicator()
    df["EMA50"] = EMAIndicator(df["Close"], window=50).ema_indicator()
    df["RSI"] = RSIIndicator(df["Close"], window=14).rsi()

    last = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    direction = None

    if last["EMA20"] > last["EMA50"]:
        score += 2
        direction = "CALL"
    elif last["EMA20"] < last["EMA50"]:
        score += 2
        direction = "PUT"

    if last["Low"] < prev["Low"] and last["Close"] > prev["Low"]:
        score += 2
        direction = "CALL"

    if last["High"] > prev["High"] and last["Close"] < prev["High"]:
        score += 2
        direction = "PUT"

    confidence = round((score / 6) * 100, 1)

    if score >= 4:
        return {
            "pair": pair,
            "signal": direction,
            "confidence": confidence
        }

    return None

@app.get("/signals")
def get_signals():
    results = []
    for pair in PAIRS:
        signal = analyze_pair(pair)
        if signal:
            results.append(signal)
    return results