from flask import Flask, jsonify, send_from_directory
import threading
from bot_runner import run_bot  # ⬅️ Make sure bot_runner.py is in the same directory

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/status')
def status():
    return jsonify({"status": "Bot is running"})

# Start the trading bot in a background thread when Flask starts
def start_bot():
    run_bot()

bot_thread = threading.Thread(target=start_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
