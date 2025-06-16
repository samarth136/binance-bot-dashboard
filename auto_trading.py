import time
import statistics
from binance_client import (
    get_latest_price,
    get_auto_trading_status,
    set_strategy,
    get_strategy,
    execute_strategy
)

price_history = []

def calculate_moving_average(data, window):
    if len(data) < window:
        return None
    return sum(data[-window:]) / window

def calculate_volatility(data):
    if len(data) < 2:
        return 0
    return statistics.stdev(data[-10:]) / statistics.mean(data[-10:])

def decide_best_strategy(price_history):
    if len(price_history) < 10:
        return "grid"

    ma_short = calculate_moving_average(price_history, 5)
    ma_long = calculate_moving_average(price_history, 10)
    volatility = calculate_volatility(price_history)

    print(f"5MA: {ma_short:.2f}, 10MA: {ma_long:.2f}, Volatility: {volatility:.4f}")

    if ma_short > ma_long and volatility < 0.01:
        return "trend-following"
    elif volatility >= 0.01:
        return "scalping"
    else:
        return "grid"

def auto_trading_loop():
    print("Starting smart auto-trading loop...")
    while True:
        try:
            if not get_auto_trading_status():
                print("Auto-trading is OFF. Sleeping...")
                time.sleep(5)
                continue

            sol_price = get_latest_price("SOLUSDT")
            print(f"Latest SOL price: {sol_price}")

            price_history.append(sol_price)
            if len(price_history) > 20:
                price_history.pop(0)

            new_strategy = decide_best_strategy(price_history)
            current_strategy = get_strategy()

            if new_strategy != current_strategy:
                print(f"Switching strategy: {current_strategy} → {new_strategy}")
                set_strategy(new_strategy)

            execute_strategy(new_strategy)

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(10)

if __name__ == "__main__":
    auto_trading_loop()
