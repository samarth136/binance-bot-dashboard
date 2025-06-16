import time
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

class CompoundingManager:
    def __init__(self, principal=100.0, daily_return_percent=5.4):
        self.principal = principal
        self.daily_return_percent = daily_return_percent
        self.last_compound_date = datetime.now().date()

    def compound_if_needed(self):
        today = datetime.now().date()
        if today > self.last_compound_date:
            days_passed = (today - self.last_compound_date).days
            for _ in range(days_passed):
                self.principal += self.principal * (self.daily_return_percent / 100)
            self.last_compound_date = today
            print(f"[Compounding] Capital updated to ${self.principal:.2f} on {today}")

    def get_principal(self):
        self.compound_if_needed()
        return round(self.principal, 2)

class StrategyManager:
    def __init__(self):
        self.active_strategy = "scalping"  # default strategy
        self.auto_trading = False

    def switch_strategy(self, strategy_name):
        allowed = ["scalping", "trend_following", "grid_trading"]
        if strategy_name in allowed:
            self.active_strategy = strategy_name
            print(f"[Strategy] Switched to {strategy_name}")
            return True
        else:
            print(f"[Strategy] Invalid strategy: {strategy_name}")
            return False

    def get_active_strategy(self):
        return self.active_strategy

    def toggle_auto_trading(self, status: bool):
        self.auto_trading = status
        print(f"[Auto-Trading] Set to {self.auto_trading}")

    def get_auto_trading_status(self):
        return self.auto_trading

compounding_manager = CompoundingManager(principal=100, daily_return_percent=5.4)
strategy_manager = StrategyManager()

@app.route('/capital', methods=['GET'])
def get_capital():
    capital = compounding_manager.get_principal()
    return jsonify({"compounded_capital": capital})

@app.route('/strategy', methods=['GET', 'POST'])
def strategy():
    if request.method == 'GET':
        return jsonify({"active_strategy": strategy_manager.get_active_strategy()})
    elif request.method == 'POST':
        data = request.get_json()
        strategy_name = data.get('strategy')
        if strategy_manager.switch_strategy(strategy_name):
            return jsonify({"message": f"Strategy switched to {strategy_name}"})
        else:
            return jsonify({"error": "Invalid strategy name"}), 400

@app.route('/auto_trading', methods=['GET', 'POST'])
def auto_trading():
    if request.method == 'GET':
        status = strategy_manager.get_auto_trading_status()
        return jsonify({"auto_trading": status})
    elif request.method == 'POST':
        data = request.get_json()
        status = data.get('status')
        if isinstance(status, bool):
            strategy_manager.toggle_auto_trading(status)
            return jsonify({"message": f"Auto trading set to {status}"})
        else:
            return jsonify({"error": "Status must be boolean"}), 400

def bot_main_loop():
    while True:
        current_capital = compounding_manager.get_principal()
        active_strategy = strategy_manager.get_active_strategy()
        auto_trading = strategy_manager.get_auto_trading_status()

        print(f"Capital: ${current_capital} | Strategy: {active_strategy} | Auto-Trading: {auto_trading}")

        if auto_trading:
            # Here add your trading logic based on the active_strategy
            # For now, just simulate with prints
            print(f"Running {active_strategy} strategy trades...")

        # Run daily cycle (set to shorter sleep for testing if needed)
        time.sleep(60 * 60 * 24)

if __name__ == "__main__":
    # Run Flask in a separate thread so bot_main_loop can also run
    from threading import Thread
    flask_thread = Thread(target=app.run, kwargs={"debug": True, "use_reloader": False})
    flask_thread.start()

    bot_main_loop()
