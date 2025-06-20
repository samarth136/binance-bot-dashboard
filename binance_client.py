import os
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

from strategy_core import (
    auto_trade_strategy,
    scalping_strategy,
    trend_following_strategy,
    grid_trading_strategy
)

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

def get_price(symbol):
    return float(client.get_symbol_ticker(symbol=symbol)["price"])

def get_balance(asset):
    balance_info = client.get_asset_balance(asset=asset)
    return float(balance_info["free"]) if balance_info else 0.0

def get_auto_trading_status():
    return os.getenv("AUTO_TRADING", "off") == "on"

def run_strategy(strategy_name):
    if strategy_name == "auto":
        auto_trade_strategy()
    elif strategy_name == "scalping":
        scalping_strategy()
    elif strategy_name == "trend":
        trend_following_strategy()
    elif strategy_name == "grid":
        grid_trading_strategy()
    else:
        print(f"[ERROR] Unknown strategy: {strategy_name}")
