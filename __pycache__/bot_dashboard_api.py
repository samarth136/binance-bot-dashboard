from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from binance_client import get_spot_balance, get_asset_price

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/balance")
def get_balance():
    return {
        "usdt_balance": get_spot_balance("USDT"),
        "sol_price": get_asset_price("SOLUSDT")
    }

@app.get("/status")
def get_status():
    return {"message": "Bot is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
