import React, { useState } from 'react';
import Dashboard from './pages/Dashboard';
import WelcomeScreen from './components/WelcomeScreen';
import './index.css';

function App() {
  const [showDashboard, setShowDashboard] = useState(false);

  const handleGetStarted = () => {
    setShowDashboard(true);
  };

  const handleBackToWelcome = () => {
    setShowDashboard(false);
  };

  if (!showDashboard) {
    return <WelcomeScreen onGetStarted={handleGetStarted} />;
  }

  return (
    <div className="App">
      <Dashboard onBackToWelcome={handleBackToWelcome} />
    </div>
  );
}

export default App;
