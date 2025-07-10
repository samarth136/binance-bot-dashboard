import time
import logging
from config import SYMBOL, CHECK_INTERVAL, BUY_THRESHOLD, SELL_MARGIN
from binance_client import (
    get_current_price, get_balance, place_market_order,
    calculate_trade_quantity, should_buy, should_sell
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

buy_price_file = "buy_price.txt"

def save_buy_price(price):
    with open(buy_price_file, "w") as f:
        f.write(str(price))

def load_buy_price():
    try:
        with open(buy_price_file, "r") as f:
            return float(f.read().strip())
    except:
        return None

def run_strategy():
    logger.info("🚀 Trading bot started")

    buy_price = load_buy_price()

    while True:
        try:
            current_price = get_current_price()
            usdt = get_balance("USDT")
            sol = get_balance("SOL")

            logger.info(f"📈 Current price: {current_price}")
            logger.info(f"💰 USDT: {usdt} | SOL: {sol}")

            if sol == 0:
                if should_buy(current_price, BUY_THRESHOLD):
                    qty = calculate_trade_quantity(usdt, current_price)
                    if qty >= 0.01:
                        logger.info(f"🟢 Buying {qty} SOL at {current_price}")
                        order = place_market_order("BUY", qty)
                        if order:
                            buy_price = current_price
                            save_buy_price(buy_price)
            else:
                if buy_price is None:
                    buy_price = current_price
                sell, reason = should_sell(buy_price, current_price, SELL_MARGIN)
                if sell:
                    logger.info(f"🔴 Selling {sol} SOL because {reason}")
                    place_market_order("SELL", round(sol, 3))
                    buy_price = None
                    save_buy_price("")  # reset file

            logger.info("✅ Cycle complete\n")
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            logger.error(f"⚠️ Error in bot loop: {e}")
            time.sleep(10)
