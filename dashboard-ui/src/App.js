import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = "https://binance-bot-dashboard.onrender.com";

function App() {
  const [price, setPrice] = useState(null);
  const [strategy, setStrategy] = useState("");
  const [auto, setAuto] = useState(false);
  const [newStrategy, setNewStrategy] = useState("");

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/status?symbol=SOLUSDT`);
      setPrice(res.data.price);
      setStrategy(res.data.strategy);
      setAuto(res.data.auto_trading);
    } catch (err) {
      console.error("Error fetching status:", err);
    }
  };

  const toggleAuto = async () => {
    await axios.post(`${BASE_URL}/toggle_auto`);
    fetchStatus();
  };

  const updateStrategy = async () => {
    await axios.post(`${BASE_URL}/set_strategy`, {
      strategy: newStrategy
    });
    fetchStatus();
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Trading Dashboard</h2>
      <p><strong>Price:</strong> {price}</p>
      <p><strong>Current Strategy:</strong> {strategy}</p>
      <p><strong>Auto-Trading:</strong> {auto ? "Enabled" : "Disabled"}</p>

      <button onClick={toggleAuto}>
        {auto ? "Disable Auto" : "Enable Auto"}
      </button>

      <div style={{ marginTop: 20 }}>
        <input
          placeholder="Enter strategy"
          value={newStrategy}
          onChange={(e) => setNewStrategy(e.target.value)}
        />
        <button onClick={updateStrategy}>Update Strategy</button>
      </div>
    </div>
  );
}

export default App;
