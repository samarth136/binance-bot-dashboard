import time
from binance_client import (
    get_auto_trading_status,
    get_current_strategy,
    get_current_capital
)

def ai_scalping():
    print("Executing AI Scalping Strategy...")

def trend_following():
    print("Executing Trend Following Strategy...")

def grid_trading():
    print("Executing Grid Trading Strategy...")

def execute_strategy():
    strategy = get_current_strategy()
    if strategy == "ai_scalping":
        ai_scalping()
    elif strategy == "trend_following":
        trend_following()
    elif strategy == "grid_trading":
        grid_trading()
    else:
        print(f"Unknown strategy: {strategy}")

if __name__ == '__main__':
    print("Strategy executor started...")
    while True:
        if get_auto_trading_status():
            print(f"\n[Auto Mode ON] Using strategy: {get_current_strategy()}")
            execute_strategy()
        else:
            print("\n[Auto Mode OFF] Waiting...")
        time.sleep(10)  # You can adjust this interval as needed
