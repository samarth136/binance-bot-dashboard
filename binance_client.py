# binance_client.py

from binance.client import Client
from config import API_KEY, API_SECRET

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Mock strategy state (should ideally be stored in a persistent database)
current_strategy = "auto"
auto_trading_enabled = True

# --- Price Fetching ---
def get_latest_price(symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])
    except Exception as e:
        print(f"[ERROR] get_latest_price: {e}")
        return None

# --- Auto-Trading Status ---
def get_auto_trading_status():
    global auto_trading_enabled
    return auto_trading_enabled

def toggle_auto_trading():
    global auto_trading_enabled
    auto_trading_enabled = not auto_trading_enabled
    return auto_trading_enabled

# --- Strategy Storage ---
def get_strategy():
    global current_strategy
    return current_strategy

def set_strategy(name):
    global current_strategy
    current_strategy = name

# --- Strategy Execution Dispatcher ---
from strategies import (
    auto_trade_strategy,
    scalping_strategy,
    trend_following_strategy,
    grid_trading_strategy
)

def execute_strategy(strategy_name):
    print(f"[BINANCE_CLIENT] Executing strategy: {strategy_name}")
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
