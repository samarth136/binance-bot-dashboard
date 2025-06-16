class CompoundingEngine:
    def __init__(self, initial_capital, reserve_percent, switch_capital=50000, switch_day=150):
        self.capital = initial_capital
        self.reserve_percent = reserve_percent
        self.reserved_funds = 0
        self.day = 0
        self.switch_capital = switch_capital
        self.switch_day = switch_day
        self.strategy = "aggressive"

    def next_day(self, daily_profit):
        self.day += 1
        if self.capital >= self.switch_capital or self.day >= self.switch_day:
            self.strategy = "conservative"
        reserved = daily_profit * self.reserve_percent
        reinvested = daily_profit - reserved
        self.reserved_funds += reserved
        self.capital += reinvested
        return {
            'day': self.day,
            'capital': round(self.capital, 2),
            'reserved_funds': round(self.reserved_funds, 2),
            'daily_profit': round(daily_profit, 2),
            'reinvested': round(reinvested, 2),
            'reserved_today': round(reserved, 2),
            'total_value': round(self.capital + self.reserved_funds, 2),
            'strategy': self.strategy
        }