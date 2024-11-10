import React, { useState, useEffect } from 'react';
import './App.css';

function IsMyHouseOnFire() {
    const [deviceCode, setDeviceCode] = useState('');
    const [deviceCode2, setDeviceCode2] = useState('');
    const [isConnected, setIsConnected] = useState(false);
    const [incorrectCode, setIncorrectCode] = useState(false);
    const [ovenOnDuration, setOvenOnDuration] = useState(0);
    const [ovenOnDetected, setOvenOnDetected] = useState(true);
    const [easterEgg, setEasterEgg] = useState(false);

    const handleConnect = () => {
        try {
            console.log(`Connecting to device with code: ${deviceCode}`);
            setDeviceCode("");
            if (deviceCode === '51413' || deviceCode2 === '51413') {
                setIsConnected(true);
                setIncorrectCode(false);
            } else {
                setIncorrectCode(true);
            }
        } catch (error) {
            console.error("Error in handleConnect:", error);
        }
    };

    const handleDisconnect = () => {
        console.log(`Disconnected from device with code: ${deviceCode}`);
        setIsConnected(false);
    };

    const handleHiddenButton = () => {
        setEasterEgg(true);
    };

    useEffect(() => {
        let interval;
        if (isConnected && ovenOnDetected) {
            interval = setInterval(() => {
                setOvenOnDuration(prevDuration => prevDuration + 1);
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [isConnected]);

    const getStatusMessage = () => {
        if (ovenOnDuration < 5) {
            return "Probably Not";
        } else if(ovenOnDuration < 30) {
            return "Probably";
        } else {
            return "For Sure";
        }
    };

    const getGradientColor = () => {
        const maxDuration = 30;
        const duration = Math.min(ovenOnDuration, maxDuration);
        const ratio = duration / maxDuration;

        const startColor = { r: 222, g: 219, b: 210 };
        const endColor = { r: 174, g: 32, b: 18 };

        const r = Math.round(startColor.r + (endColor.r - startColor.r) * ratio);
        const g = Math.round(startColor.g + (endColor.g - startColor.g) * ratio);
        const b = Math.round(startColor.b + (endColor.b - startColor.b) * ratio);

        return `rgb(${r}, ${g}, ${b})`;
    };

    return (
        <div className="container">
            {!easterEgg ? (
                !isConnected ? (
                    // Connect Page
                    <div className="connect-page">
                        <div className="Header">
                            <img src="/logo.png" alt="Logo" className="logo" />
                            <h2 className="header-text">IsMyHouseOnFire.tech</h2>
                            <button onClick={() => handleHiddenButton()} className="hidden-button"></button>

                            <div className="right-section">
                                <input
                                    type="text"
                                    placeholder="Enter your device code"
                                    value={deviceCode2}
                                    onChange={(e) => setDeviceCode2(e.target.value)}
                                    className="header-input"
                                />
                                <button onClick={handleConnect} className="header-button">Connect</button>
                            </div>
                        </div>
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
                        {incorrectCode && (
                            <div className="wrong_code">
                                <h3>Incorrect Code, Try Again!</h3>
                            </div>
                        )}
                        <div className="funny_text">
                            <h2>Enter Your Device Code to Find Out!</h2>
                        </div>
                        <div className="empty-space"></div>
                        <div className="banner">
                            <img src="/flames.png" alt="Banner" />
                        </div>
                    </div>
                ) : (
                    // Main Content Page
                    <div className="main-content">
                        <div className="Header">
                            <img src="/logo.png" alt="Logo" className="logo" />
                            <h2 className="header-text">IsMyHouseOnFire.tech</h2>

                            <div className="right-section-main">
                                <button onClick={handleDisconnect}>Disconnect</button>
                            </div>
                        </div>
                        <div className="title">
                            <h1>{getStatusMessage()}</h1>
                        </div>
                        <div className="oven_on_text" style={{ color: getGradientColor() }}>
                            <h2>Oven Has Been On For: {ovenOnDuration} Seconds</h2>
                        </div>
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
                        <div className="disconnect_button">
                            <button onClick={handleDisconnect}>Disconnect</button>
                        </div>
                        <div
                            className="adaptive_banner"
                            style={{
                                maxWidth: '100%',
                                height: `${Math.min(10 * ovenOnDuration + 100, 500)}px`,
                                width: '100%',
                                objectFit: 'fill',
                                animation: 'flicker 1.5s infinite ease-in-out',
                            }}
                        >
                            <img src="/flames.png" alt="Banner" />
                        </div>
                    </div>
                )
            ) : (
                // Easter Egg Page
                <div className="EasterEgg">
                    <h1>Hello!</h1>
                    <h1>You've Found the Hidden Page!</h1>
                    <img src="/liza.jpg" alt="Liza" className="liza" />
                    <div className="ReturnButton">
                    <button onClick={() => setEasterEgg(false)}>Return</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default IsMyHouseOnFire;
