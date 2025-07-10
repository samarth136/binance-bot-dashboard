# === config.py ===
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Fetch API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Coins to trade
COINS = ["SOLUSDT", "ARBUSDT", "INJUSDT", "SEIUSDT", "PEPEUSDT", "DOGEUSDT"]

# Entry prices per coin
BUY_THRESHOLD = {
    "SOLUSDT": 140.0,
    "ARBUSDT": 0.75,
    "INJUSDT": 23.0,
    "SEIUSDT": 0.40,
    "PEPEUSDT": 0.000001,
    "DOGEUSDT": 0.12
}

# Profit margin and cycle interval
SELL_MARGIN = 2.5
CHECK_INTERVAL = 15
