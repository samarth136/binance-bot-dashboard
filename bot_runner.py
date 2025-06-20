# bot_runner.py

import time
from strategy_executor import execute_selected_strategy

def run_bot():
    print("[BOT] Starting trading bot...")

    strategy_name = "auto"  # default strategy for now
    while True:
        print("[BOT] Running strategy execution loop...")
        execute_selected_strategy(strategy_name)
        time.sleep(60)  # run once per minute
