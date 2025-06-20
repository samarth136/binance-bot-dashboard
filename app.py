# app.py

from flask import Flask
import threading
from bot_runner import run_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "Binance Trading Bot is running!"

# Start bot in a separate thread
bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    app.run(debug=True, port=10000)
