from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pandas as pd
import yfinance as yf
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
import os

app = FastAPI()

# Serve frontend if you have static files
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
    
    return {"pair": pair, "signal": direction, "score": score}

@app.get("/signals")
def get_signals():
    results = []
    for pair in PAIRS:
        results.append(analyze_pair(pair))
    return results

# Critical for Render dynamic port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)