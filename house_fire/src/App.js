import React, { useState } from 'react';
import './App.css';

function IsMyHouseOnFire() {
    const [deviceCode, setDeviceCode] = useState('');
    const [isConnected, setIsConnected] = useState(false); // Track connection status

    const handleConnect = () => {
        console.log(`Connecting to device with code: ${deviceCode}`);
        setIsConnected(true); // Set as connected to display main content
    };

    const handleDisconnect = () => {
        console.log(`Disconnected from device with code: ${deviceCode}`);
        setIsConnected(false);
    }

    return (
        <div className="container">
            {/* Render different views based on the isConnected state */}
            {!isConnected ? (
                // Connect Page
                <div className="connect-page">
                    <div className="title">
                        <h1>Is My House On Fire?</h1>
                    </div>
                    <div className="connection-section">
                        <input
                            type="text"
                            placeholder="Enter your device code"
                            value={deviceCode}
                            onChange={(e) => setDeviceCode(e.target.value)}
                        />
                        <button onClick={handleConnect}>Connect</button>
                    </div>
                    <div className="banner">
                        <img src="/flames.svg" alt="Banner"/>
                    </div>
                </div>
            ) : (
                // Main Content Page
                <div className="main-content">
                    <div className="streaming-section">
                        <h2>Live Stream</h2>
                        <div className="stream-placeholder">
                            <p>Streaming content will appear here.</p>
                        </div>
                    </div>
                    <div className="graphs-section">
                        <h2>Analytics</h2>
                        <div className="graph-placeholder">
                            <p>Graphs will appear here.</p>
                        </div>
                    </div>
                    <button onClick={handleDisconnect}>Disconnect</button>
                </div>
            )}
        </div>
    );
}

export default IsMyHouseOnFire;
