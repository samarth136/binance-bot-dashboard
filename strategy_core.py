from auto_trading import auto_trading_loop
from scalping import scalping_loop
from trend_following import trend_following_loop
from grid_trading import grid_trading_loop

def auto_trade_strategy():
    print("[STRATEGY] Auto Trading Strategy Active")
    auto_trading_loop()

def scalping_strategy():
    print("[STRATEGY] Scalping Strategy Active")
    scalping_loop()

def trend_following_strategy():
    print("[STRATEGY] Trend Following Strategy Active")
    trend_following_loop()

def grid_trading_strategy():
    print("[STRATEGY] Grid Trading Strategy Active")
    grid_trading_loop()
