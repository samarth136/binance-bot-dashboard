from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Binance Client
client = Client(
    api_key=os.getenv("BINANCE_API_KEY"),
    api_secret=os.getenv("BINANCE_API_SECRET")
)

# Globals for storing bot state
strategy_mode = "auto"  # default strategy mode
current_strategy = "grid"  # initial fallback strategy
auto_trading_enabled = True  # Auto-trading toggle

# Get latest price for a given symbol
def get_latest_price(symbol="SOLUSDT"):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

# --- Auto-Trading Status ---
def get_auto_trading_status():
    return auto_trading_enabled

def set_auto_trading_status(status: bool):
    global auto_trading_enabled
    auto_trading_enabled = status

# --- Strategy Get/Set ---
def get_strategy():
    return current_strategy

def set_strategy(strategy_name):
    global current_strategy
    current_strategy = strategy_name

# --- Strategy Execution Logic ---
from strat import (
    auto_trade_strategy,
    scalping_strategy,
    trend_following_strategy,
    grid_trading_strategy
)

def execute_strategy(name):
    print(f"[STRATEGY] Executing: {name}")
    if name == "auto":
        auto_trade_strategy()
    elif name == "scalping":
        scalping_strategy()
    elif name == "trend-following":
        trend_following_strategy()
    elif name == "grid":
        grid_trading_strategy()
    else:
        print(f"[ERROR] Unknown strategy name: {name}")
