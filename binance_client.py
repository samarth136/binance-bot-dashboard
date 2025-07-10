from binance.client import Client
from binance.helpers import round_step_size
from binance.exceptions import BinanceAPIException
import logging
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("binance_client")

client = Client(config.API_KEY, config.API_SECRET)

def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def get_balance(asset):
    try:
        balance = client.get_asset_balance(asset=asset)
        return float(balance['free']) if balance else 0.0
    except Exception as e:
        logger.error(f"❌ Error fetching balance for {asset}: {e}")
        return 0.0

def place_market_order(side, quantity, symbol):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        logger.info(f"✅ Order placed: {side} {quantity} {symbol}")
        return order
    except Exception as e:
        logger.error(f"❌ Order failed for {symbol}: {e}")
        return None

def get_lot_size(symbol):
    try:
        exchange_info = client.get_symbol_info(symbol)
        for f in exchange_info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                return float(f['stepSize'])
    except BinanceAPIException as e:
        logger.error(f"❌ Couldn't fetch lot size for {symbol}: {e}")
    return 0.001  # default fallback

def calculate_trade_quantity(usdt_balance, current_price, symbol):
    raw_qty = usdt_balance / current_price
    step_size = get_lot_size(symbol)
    return round_step_size(raw_qty, step_size)

def should_buy(current_price, threshold):
    return current_price <= threshold
def should_sell(buy_price, current_price, margin_percent=2.5):
    target_price = buy_price * (1 + margin_percent / 100)
    return current_price >= target_price, f"Target: {current_price:.6f} >= {target_price:.6f}"
