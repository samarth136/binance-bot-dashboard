from flask import Flask, jsonify
from binance_client import get_spot_balance, get_futures_balance, get_price

app = Flask(__name__)

@app.route('/spot_balance/<symbol>')
def spot_balance(symbol):
    balance = get_spot_balance(symbol)
    return jsonify({symbol.upper(): balance})

@app.route('/futures_balance/<symbol>')
def futures_balance(symbol):
    balance = get_futures_balance(symbol)
    return jsonify({symbol.upper(): balance})

@app.route('/price/<symbol>')
def price(symbol):
    price = get_price(symbol)
    return jsonify({symbol.upper(): price})

if __name__ == '__main__':
    app.run(debug=True, port=5050)
