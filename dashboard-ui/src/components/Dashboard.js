// Dashboard.js (React)
import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [balances, setBalances] = useState({SOL: 0, ARB: 0});
  const [prices, setPrices] = useState({SOL: 0, ARB: 0});
  const [strategy, setStrategy] = useState('scalping');
  const [autoTrading, setAutoTrading] = useState(false);
  const [profit, setProfit] = useState({value: 0, percentage: 0});
  const [tradeHistory, setTradeHistory] = useState([]);

  // Fetch balances, prices, strategy, auto-trading status, profit periodically
  useEffect(() => {
    async function fetchData() {
      const balRes = await fetch('/api/balances');
      setBalances(await balRes.json());

      const priceRes = await fetch('/api/prices');
      setPrices(await priceRes.json());

      const stratRes = await fetch('/api/strategy');
      setStrategy((await stratRes.json()).strategy);

      const autoRes = await fetch('/api/auto-trading-status');
      setAutoTrading((await autoRes.json()).status);

      const profitRes = await fetch('/api/profit');
      setProfit(await profitRes.json());

      const historyRes = await fetch('/api/trade-history');
      setTradeHistory(await historyRes.json());
    }

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  // Change strategy handler
  async function changeStrategy(e) {
    const newStrategy = e.target.value;
    await fetch('/api/set-strategy', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({strategy: newStrategy})
    });
    setStrategy(newStrategy);
  }

  // Toggle auto trading handler
  async function toggleAutoTrading() {
    await fetch('/api/toggle-auto-trading', {method: 'POST'});
    // Refresh status after toggle
    const res = await fetch('/api/auto-trading-status');
    setAutoTrading((await res.json()).status);
  }

  return (
    <div>
      <h2>Balances</h2>
      <p>SOL: {balances.SOL}</p>
      <p>ARB: {balances.ARB}</p>

      <h2>Prices</h2>
      <p>SOL: ${prices.SOL}</p>
      <p>ARB: ${prices.ARB}</p>

      <h2>Strategy</h2>
      <select value={strategy} onChange={changeStrategy}>
        <option value="scalping">Scalping</option>
        <option value="trend-following">Trend Following</option>
        <option value="grid">Grid</option>
      </select>

      <h2>Auto Trading</h2>
      <button onClick={toggleAutoTrading}>{autoTrading ? 'Stop' : 'Start'}</button>

      <h2>Profit</h2>
      <p>Value: ${profit.value.toFixed(2)}</p>
      <p>Percentage: {profit.percentage.toFixed(2)}%</p>

      <h2>Trade History</h2>
      <ul>
        {tradeHistory.map((trade, idx) => (
          <li key={idx}>{trade.timestamp}: {trade.details}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
