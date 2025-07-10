import time
import logging
import os
from config import COINS, CHECK_INTERVAL, BUY_THRESHOLD, SELL_MARGIN
from binance_client import (
    get_current_price, get_balance, place_market_order,
    calculate_trade_quantity, should_buy, should_sell
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def buy_price_file(symbol):
    return f"buy_price_{symbol}.txt"

def save_buy_price(symbol, price):
    with open(buy_price_file(symbol), "w") as f:
        f.write(str(price))
    logger.info(f"💾 Saved buy price for {symbol}: {price}")

def load_buy_price(symbol):
    path = buy_price_file(symbol)
    if os.path.exists(path):
        with open(path, "r") as f:
            return float(f.read().strip())
    return None

def clear_buy_price(symbol):
    path = buy_price_file(symbol)
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"🗑️ Cleared buy price for {symbol}")

def get_total_balance():
    total_usdt = get_balance("USDT")
    total_value = total_usdt
    for symbol in COINS:
        base_asset = symbol.replace("USDT", "")
        coin_balance = get_balance(base_asset)
        price = get_current_price(symbol)
        coin_value = coin_balance * price
        total_value += coin_value
    return round(total_value, 2)

def trading_bot():
    logger.info("🚀 Multi-coin trading bot started")

    while True:
        for symbol in COINS:
            base_asset = symbol.replace("USDT", "")
            current_price = get_current_price(symbol)
            usdt_balance = get_balance("USDT")
            coin_balance = get_balance(base_asset)
            buy_price = load_buy_price(symbol)

            logger.info(f"📊 {symbol} | Price: {current_price:.6f} | USDT: {usdt_balance:.2f} | {base_asset}: {coin_balance:.6f}")

            if coin_balance < 0.001:
                threshold = BUY_THRESHOLD.get(symbol, 0)
                if should_buy(current_price, threshold):
                    qty = calculate_trade_quantity(usdt_balance, current_price, symbol)
                    if qty >= 0.001:
                        logger.info(f"🟢 Buying {qty} {base_asset} at {current_price}")
                        order = place_market_order("BUY", qty, symbol)
                        if order:
                            save_buy_price(symbol, current_price)
            else:
                if buy_price is None:
                    logger.warning(f"⚠️ Missing buy price for {symbol}, skipping sell.")
                    continue
                sell_decision, reason = should_sell(buy_price, current_price, SELL_MARGIN)
                if sell_decision:
                    logger.info(f"🔴 Selling {coin_balance:.3f} {base_asset} — {reason}")
                    place_market_order("SELL", round(coin_balance, 3), symbol)
                    clear_buy_price(symbol)
                else:
                    logger.info(f"⏳ Waiting to sell {symbol} — {reason}")

        total_balance = get_total_balance()
        logger.info(f"💼 Total Bot Balance: {total_balance:.2f} USDT\n")
        logger.info("✅ Cycle complete\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    trading_bot()
