# binance_client.py (integrated with phase logic)

from flask import Flask, jsonify, request
from binance.client import Client
import json
from datetime import datetime

app = Flask(__name__)

# --- Binance API Setup ---
API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'
client = Client(API_KEY, API_SECRET)

# --- Phase + State Management ---
PHASE_FILE = "phase_state.json"
STATE_FILE = "bot_state.json"

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "starting_balance": 48,
            "current_balance": 48,
            "total_withdrawn": 0
        }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_phase():
    try:
        with open(PHASE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"phase": 0, "day": 0, "withdrawals": 0}

def save_phase(data):
    with open(PHASE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_investment_state(daily_growth=0.06):
    state = load_state()
    phase = load_phase()

    state["current_balance"] *= (1 + daily_growth)
    phase["day"] += 1

    if phase["phase"] == 0 and phase["day"] >= 74:
        if state["current_balance"] >= 7300:
            withdrawal = state["current_balance"] - 1000
            state["current_balance"] = 1000
            state["total_withdrawn"] += withdrawal
            phase["phase"] = 1

    elif phase["phase"] == 1 and state["current_balance"] >= 50000:
        withdrawal = state["current_balance"] - 10000
        state["current_balance"] = 10000
        state["total_withdrawn"] += withdrawal
        phase["phase"] = 2
        phase["day"] = 0

    elif phase["phase"] == 2:
        if phase["day"] % 30 == 0:
            if state["current_balance"] >= 1200:
                state["current_balance"] -= 1200
                state["total_withdrawn"] += 1200

    save_state(state)
    save_phase(phase)
    return {**state, **phase}

# --- Trading Strategies ---
def trend_following(current_price, short_ma, long_ma):
    if short_ma > long_ma:
        return "buy"
    elif short_ma < long_ma:
        return "sell"
    return "hold"

def scalping(price, bid_price, ask_price, spread_threshold=0.001):
    spread = ask_price - bid_price
    if spread >= spread_threshold:
        if price <= bid_price:
            return "buy"
        elif price >= ask_price:
            return "sell"
    return "hold"

def grid_trading(price, grid_levels, last_trade_price):
    for level in grid_levels:
        if price <= level and last_trade_price > level:
            return "buy"
        elif price >= level and last_trade_price < level:
            return "sell"
    return "hold"

# --- API Routes ---
@app.route('/')
def home():
    return "Welcome to Binance Bot API!"

@app.route('/prices')
def prices():
    symbols = ["SOLUSDT", "ARBUSDT"]
    prices = {}
    for symbol in symbols:
        ticker = client.get_symbol_ticker(symbol=symbol)
        prices[symbol] = ticker["price"]
    return jsonify(prices)

@app.route('/bot_state')
def bot_state():
    state = load_state()
    return jsonify(state)

@app.route('/phase_status')
def phase_status():
    return jsonify(load_phase())

@app.route('/run_daily')
def run_daily():
    updated_state = update_investment_state(daily_growth=0.06)
    return jsonify(updated_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)