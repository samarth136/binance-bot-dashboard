import os
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Load keys from environment variables (set in Render)
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

# Fetch spot balance
def get_balance(symbol):
    try:
        balance_info = client.get_asset_balance(asset=symbol)
        return float(balance_info["free"])
    except Exception as e:
        print(f"Error fetching balance for {symbol}: {e}")
        return 0.0

# Get latest price for a trading pair
def get_price(symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

# Place market order (BUY or SELL)
def place_market_order(symbol, side, quantity):
    try:
        print(f"Placing {side} market order for {quantity} of {symbol}")
        order = client.order_market(
            symbol=symbol,
            side=side.upper(),
            quantity=quantity
        )
        return order
    except BinanceAPIException as e:
        print(f"Binance API error: {e}")
    except Exception as e:
        print(f"Order placement error: {e}")
    return None

# Auto-trading toggle
AUTO_TRADING_STATUS = {"enabled": True}

def get_auto_trading_status():
    return AUTO_TRADING_STATUS["enabled"]

def toggle_auto_trading():
    AUTO_TRADING_STATUS["enabled"] = not AUTO_TRADING_STATUS["enabled"]
    return AUTO_TRADING_STATUS["enabled"]

# Current strategy
CURRENT_STRATEGY = {"strategy": "scalping"}

def get_current_strategy():
    return CURRENT_STRATEGY["strategy"]

def set_current_strategy(new_strategy):
    CURRENT_STRATEGY["strategy"] = new_strategy
