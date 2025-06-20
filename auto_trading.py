import time
from binance_client import run_strategy, get_auto_trading_status

def auto_trading_loop():
    print("[AUTO TRADING] Starting auto trading loop...")
    while get_auto_trading_status():
        run_strategy("auto")
        time.sleep(60)  # wait 1 minute before the next trade cycle
