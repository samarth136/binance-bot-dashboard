import time
import logging
import sys
from strategy_core import execute_active_strategy

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

LOOP_INTERVAL = 10  # seconds

def main():
    logging.info("🚀 Trading bot loop started")
    while True:
        try:
            execute_active_strategy()
        except Exception as e:
            logging.error(f"❌ Error: {e}")
        time.sleep(LOOP_INTERVAL)

if __name__ == "__main__":
    main()
