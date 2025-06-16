from binance_client import client

# Check account balances for SOL and ARB
def check_balances():
    try:
        balances = client.get_account()["balances"]
        assets = ["SOL", "ARB"]
        for asset in assets:
            balance = next((item for item in balances if item["asset"] == asset), None)
            if balance:
                print(f"{asset} - Free: {balance['free']}, Locked: {balance['locked']}")
            else:
                print(f"{asset} - No balance found.")
    except Exception as e:
        print("Error fetching balances:", e)

# Simple compounding calculation
def calculate_compounded_quantity(start_amount, growth_rate, days):
    # growth_rate as a decimal (e.g., 5.4% -> 0.054)
    for day in range(1, days + 1):
        start_amount *= (1 + growth_rate)
        print(f"Day {day}: {start_amount:.2f}")
    return start_amount

if __name__ == "__main__":
    print("Checking balances...")
    check_balances()
    
    print("\nCalculating compounding growth...")
    initial = 100  # Example starting capital
    rate = 0.054   # 5.4% daily growth
    period = 150   # Target: 5 months (~150 days)
    final = calculate_compounded_quantity(initial, rate, period)
    
    print(f"\nFinal amount after {period} days: {final:.2f}")
