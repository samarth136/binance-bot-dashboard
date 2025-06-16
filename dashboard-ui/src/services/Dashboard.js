import React, { useState, useEffect } from 'react';
import { getSpotBalance, getFuturesBalance } from '../services/api';

const Dashboard = () => {
    const [spotBalance, setSpotBalance] = useState(null);
    const [futuresBalance, setFuturesBalance] = useState(null);

    // Fetch spot balance on component mount
    useEffect(() => {
        const fetchBalances = async () => {
            const spot = await getSpotBalance();
            setSpotBalance(spot);
            const futures = await getFuturesBalance();
            setFuturesBalance(futures);
        };

        fetchBalances();
    }, []);

    return (
        <div>
            <h1>Crypto Trading Dashboard</h1>
            <div>
                <h2>Spot Balance</h2>
                <p>{spotBalance ? `${spotBalance} USDT` : 'Loading...'}</p>
            </div>
            <div>
                <h2>Futures Balance</h2>
                <p>{futuresBalance ? `${futuresBalance} USDT` : 'Loading...'}</p>
            </div>
            {/* Add more sections as necessary */}
        </div>
    );
};

export default Dashboard;
