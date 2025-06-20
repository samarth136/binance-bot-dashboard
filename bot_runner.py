from strategy_executor import execute_selected_strategy
import threading
import time

def run_bot():
    print("[BOT] Auto-trading thread starting...")

    def bot_loop():
        while True:
            try:
                execute_selected_strategy()
                time.sleep(60)  # wait 1 minute between executions (adjust as needed)
            except Exception as e:
                print(f"[BOT] Error during bot execution: {e}")
                time.sleep(60)

    thread = threading.Thread(target=bot_loop)
    thread.daemon = True
    thread.start()
