import React, { useEffect, useState } from 'react';

const strategies = ['scalping', 'trend-following', 'grid'];

function Dashboard() {
  const [balances, setBalances] = useState({ SOL: 0, ARB: 0 });
  const [prices, setPrices] = useState({ SOL: 0, ARB: 0 });
  const [strategy, setStrategy] = useState('');
  const [autoTradingStatus, setAutoTradingStatus] = useState(false);
  const [profit, setProfit] = useState({ value: 0, percentage: 0 });
  const [tradeHistory, setTradeHistory] = useState([]);

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 10000);
    return () => clearInterval(interval);
  }, []);

  async function fetchAllData() {
    await Promise.all([
      fetchBalances(),
      fetchPrices(),
      fetchStrategy(),
      fetchAutoTradingStatus(),
      fetchProfit(),
      // fetchTradeHistory() // add later if needed
    ]);
  }

  async function fetchBalances() {
    const res = await fetch('/api/balances');
    const data = await res.json();
    setBalances(data);
  }

  async function fetchPrices() {
    const res = await fetch('/api/prices');
    const data = await res.json();
    setPrices(data);
  }

  async function fetchStrategy() {
    const res = await fetch('/api/strategy');
    const data = await res.json();
    setStrategy(data.strategy);
  }

  async function fetchAutoTradingStatus() {
    const res = await fetch('/api/auto-trading-status');
    const data = await res.json();
    setAutoTradingStatus(data.status);
  }

  async function fetchProfit() {
    const res = await fetch('/api/profit');
    const data = await res.json();
    setProfit(data);
  }

  async function changeStrategy(newStrategy) {
    const res = await fetch('/api/strategy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ strategy: newStrategy }),
    });
    if (res.ok) {
      setStrategy(newStrategy);
    } else {
      alert('Failed to change strategy');
    }
  }

  async function startAutoTrading() {
    const res = await fetch('/api/start-auto-trading', { method: 'POST' });
    if (res.ok) {
      setAutoTradingStatus(true);
    }
  }

  async function stopAutoTrading() {
    const res = await fetch('/api/stop-auto-trading', { method: 'POST' });
    if (res.ok) {
      setAutoTradingStatus(false);
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: 'auto', fontFamily: 'Arial, sans-serif' }}>
      <h2>Crypto Trading Bot Dashboard</h2>

      <section>
        <h3>Balances</h3>
        <p>SOL: {balances.SOL.toFixed(4)}</p>
        <p>ARB: {balances.ARB.toFixed(4)}</p>
      </section>

      <section>
        <h3>Prices (USDT)</h3>
        <p>SOL: ${prices.SOL.toFixed(2)}</p>
        <p>ARB: ${prices.ARB.toFixed(2)}</p>
      </section>

      <section>
        <h3>Strategy</h3>
        <select
          value={strategy}
          onChange={e => changeStrategy(e.target.value)}
          style={{ padding: '5px', fontSize: '16px' }}
        >
          {strategies.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </section>

      <section>
        <h3>Auto-Trading Status</h3>
        <p>{autoTradingStatus ? 'Running' : 'Stopped'}</p>
        <button onClick={startAutoTrading} disabled={autoTradingStatus}>Start</button>
        <button onClick={stopAutoTrading} disabled={!autoTradingStatus}>Stop</button>
      </section>

      <section>
        <h3>Profit</h3>
        <p>Value: ${profit.value}</p>
        <p>Percentage: {profit.percentage}%</p>
      </section>
    </div>
  );
}

export default Dashboard;
