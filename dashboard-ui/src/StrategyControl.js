import React, { useState, useEffect } from "react";

const StrategyControl = () => {
  const [strategy, setStrategy] = useState("");
  const [autoTrading, setAutoTrading] = useState(false);
  const [newStrategy, setNewStrategy] = useState("");

  useEffect(() => {
    fetch("/strategy")
      .then((res) => res.json())
      .then((data) => setStrategy(data.strategy))
      .catch(console.error);

    fetch("/auto_trading")
      .then((res) => res.json())
      .then((data) => setAutoTrading(data.auto_trading_enabled))
      .catch(console.error);
  }, []);

  const handleStrategyChange = (e) => {
    setNewStrategy(e.target.value);
  };

  const updateStrategy = () => {
    fetch("/strategy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ strategy: newStrategy }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.error) setStrategy(newStrategy);
        else alert(data.error);
      })
      .catch(console.error);
  };

  const toggleAutoTrading = () => {
    fetch("/auto_trading", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enabled: !autoTrading }),
    })
      .then((res) => res.json())
      .then(() => setAutoTrading((prev) => !prev))
      .catch(console.error);
  };

  return (
    <div style={{ padding: "20px", maxWidth: "400px", margin: "auto" }}>
      <h2>Trading Strategy Control</h2>
      <p>
        <b>Current Strategy:</b> {strategy}
      </p>

      <input
        type="text"
        placeholder="Enter new strategy"
        value={newStrategy}
        onChange={handleStrategyChange}
        style={{ width: "100%", marginBottom: "10px" }}
      />
      <button onClick={updateStrategy} style={{ width: "100%" }}>
        Update Strategy
      </button>

      <hr style={{ margin: "20px 0" }} />

      <p>
        <b>Auto-Trading:</b> {autoTrading ? "Enabled" : "Disabled"}
      </p>
      <button onClick={toggleAutoTrading} style={{ width: "100%" }}>
        {autoTrading ? "Disable" : "Enable"} Auto-Trading
      </button>
    </div>
  );
};

export default StrategyControl;
