def calculate_compounded_quantity(initial_amount, daily_growth_rate, days, reserve_percent=0.2):
    quantities = []
    current = initial_amount

    for _ in range(days):
        profit = current * daily_growth_rate
        reserved = profit * reserve_percent
        reinvest = profit - reserved
        current += reinvest
        quantities.append(current)

    return quantities
