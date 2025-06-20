from strategies import auto_trade_strategy, scalping_strategy, trend_following_strategy
from binance_client import get_auto_trading_status, get_selected_strategy

def execute_selected_strategy():
    auto_mode = get_auto_trading_status()
    selected_strategy = get_selected_strategy()

    print(f"[STRATEGY] Auto mode: {auto_mode} | Selected: {selected_strategy}")

    if auto_mode:
        auto_trade_strategy()
    elif selected_strategy == 'scalping':
        scalping_strategy()
    elif selected_strategy == 'trend':
        trend_following_strategy()
    else:
        print(f"[STRATEGY] Unknown strategy: {selected_strategy}")
