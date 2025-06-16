import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [price, setPrice] = useState(null);
  const [strategy, setStrategy] = useState("");
  const [auto, setAuto] = useState(false);
  const [newStrategy, setNewStrategy] = useState("");

  const fetchStatus = async () => {
    const res = await axios.get("http://localhost:5000/status?symbol=SOLUSDT");
    setPrice(res.data.price);
    setStrategy(res.data.strategy);
    setAuto(res.data.auto_trading);
  };

  const toggleAuto = async () => {
    await axios.post("http://localhost:5000/toggle_auto");
    fetchStatus();
  };

  const updateStrategy = async () => {
    await axios.post("http://localhost:5000/set_strategy", {
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
