from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/signals")
def get_signals():
    # Example dummy data for testing
    return [
        {"pair": "EUR/USD", "signal": "CALL", "confidence": 80},
        {"pair": "GBP/USD", "signal": "PUT", "confidence": 65}
    ]

# THIS IS CRITICAL FOR RENDER
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # <-- Use Render dynamic port
    uvicorn.run(app, host="0.0.0.0", port=port)
    