# strategy_executor.py
from binance_client import place_market_order


def ai_scalping():
    print("Executing AI Scalping Strategy.")
    # Example trade - Buy 0.2 SOL
    place_market_order("SOLUSDT", "BUY", 0.2)


def trend_following():
    print("Executing Trend Following Strategy.")
    # Example trade - Sell 0.2 SOL
    place_market_order("SOLUSDT", "SELL", 0.2)


def grid_trading():
    print("Executing Grid Trading Strategy.")
    # Example grid trade - Buy 0.1 SOL
    place_market_order("SOLUSDT", "BUY", 0.1)
