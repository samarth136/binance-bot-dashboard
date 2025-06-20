from strategies import auto_trade_strategy, scalping_strategy, trend_following_strategy, grid_trading_strategy

def execute_selected_strategy(strategy_name):
    if strategy_name == 'auto':
        auto_trade_strategy()
    elif strategy_name == 'scalping':
        scalping_strategy()
    elif strategy_name == 'trend':
        trend_following_strategy()
    elif strategy_name == 'grid':
        grid_trading_strategy()
    else:
        print(f"[ERROR] Unknown strategy: {strategy_name}")
