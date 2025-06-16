from binance.client import Client

api_key = "YOUR_API_KEY_HERE"
api_secret = "YOUR_API_SECRET_HERE"

client = Client(api_key, api_secret)

try:
    sol_balance = client.get_asset_balance(asset="SOL")
    print("SOL Balance:", sol_balance)
except Exception as e:
    print("Error:", e)
