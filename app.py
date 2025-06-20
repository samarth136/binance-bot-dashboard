from flask import Flask
from bot_runner import run_bot

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is deployed and running!"

@app.route('/run')
def run():
    run_bot()
    return "Bot has executed the selected strategy."

if __name__ == '__main__':
    app.run(debug=True)
