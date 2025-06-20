from strategy_executor import execute_selected_strategy

def run_bot():
    print("[BOT RUNNER] Starting the trading bot...")
    # You can set your default or selected strategy here
    selected_strategy = "auto"  # Replace with dynamic choice if needed
    execute_selected_strategy(selected_strategy)
