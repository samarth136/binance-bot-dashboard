import time
import logging
from config import SYMBOL, CHECK_INTERVAL, BUY_THRESHOLD, SELL_MARGIN
from binance_client import (
    get_current_price, get_balance, place_market_order, calculate_trade_quantity
)

BUY_PRICE_FILE = "buy_price.txt"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def save_buy_price(price):
    with open(BUY_PRICE_FILE, "w") as f:
        f.write(str(price))

def load_buy_price():
    try:
        with open(BUY_PRICE_FILE, "r") as f:
            return float(f.read())
    except:
        return None

def should_buy(current_price, threshold):
    return current_price <= threshold

def should_sell(buy_price, current_price):
    target_price = buy_price * (1 + SELL_MARGIN / 100)
    if current_price >= target_price:
        return True, f"Target reached: {current_price:.2f} >= {target_price:.2f}"
    return False, f"Target: {target_price:.2f} | Current: {current_price:.2f}"

def run_strategy():
    logger.info("🚀 Trading bot started")

    while True:
        try:
            current_price = get_current_price()
            usdt_balance = get_balance("USDT")
            sol_balance = get_balance("SOL")
            logger.info(f"📈 Current price: {current_price}")
            logger.info(f"💰 USDT: {usdt_balance} | SOL: {sol_balance}")

            buy_price = load_buy_price()

            if sol_balance == 0:
                if should_buy(current_price, BUY_THRESHOLD):
                    qty = calculate_trade_quantity(usdt_balance, current_price)
                    logger.info(f"🟢 Buying {qty} SOL at {current_price}")
                    order = place_market_order("BUY", qty)
                    if order:
                        save_buy_price(current_price)
            else:
                if buy_price is None:
                    buy_price = current_price  # fallback
                    save_buy_price(buy_price)

                sell_decision, reason = should_sell(buy_price, current_price)
                if sell_decision:
                    logger.info(f"🔴 Selling {sol_balance} SOL — {reason}")
                    place_market_order("SELL", round(sol_balance, 3))
                    save_buy_price("")  # reset

                else:
                    logger.info(f"⏳ Waiting to sell — {reason}")

            logger.info("✅ Cycle complete\n")
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            logger.error(f"⚠️ Error: {e}")
            time.sleep(10)
