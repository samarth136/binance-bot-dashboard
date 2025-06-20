from auto_trading import auto_trading_loop
from scalping import scalping_loop
from trend_following import trend_following_loop
from grid_trading import grid_trading_loop

def auto_trade_strategy():
    auto_trading_loop()

def scalping_strategy():
    scalping_loop()

def trend_following_strategy():
    trend_following_loop()

def grid_trading_strategy():
    grid_trading_loop()
