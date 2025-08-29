import React, { useState, useEffect } from 'react';
import MapView from '../components/MapView';
import AlertList from '../components/AlertList';
import Charts from '../components/Charts';
import LocationSelector from '../components/LocationSelector';
import HelpTooltip from '../components/HelpTooltip';
import { apiService } from '../services/api';

const Dashboard = ({ onBackToWelcome }) => {
  const [weatherData, setWeatherData] = useState(null);
  const [tideData, setTideData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [currentLocation, setCurrentLocation] = useState('mumbai');

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, [currentLocation]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const data = await apiService.getDataForLocation(currentLocation);
      
      if (data.data) {
        setWeatherData(data.data.weather);
        setTideData(data.data.tide);
        setError(null);
      }
      const alertsRes = await apiService.getAlerts();
      setAlerts(alertsRes.alerts || []);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch data. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const handleLocationChange = (newLocation) => {
    setCurrentLocation(newLocation);
    setLoading(true);
    setWeatherData(null);
    setTideData(null);
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: '📊', description: 'Real-time coastal monitoring' },
    { id: 'charts', name: 'Analytics', icon: '📈', description: 'Historical trends & patterns' },
    { id: 'locations', name: 'Locations', icon: '🌍', description: 'Global coastal cities' }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-8 fade-in-up">
            {/* Location Header Card */}
            <div className="pro-card p-8 bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-l-blue-500">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="text-5xl">🌊</div>
                  <div>
                    <h2 className="heading-1 text-gradient">
                      {weatherData?.city_name || 'Mumbai, India'}
                    </h2>
                    <p className="text-xl text-gray-600 font-medium">
                      {weatherData?.country || 'India'} • Coastal Threat Monitoring Station
                    </p>
                    <div className="flex items-center space-x-4 mt-2">
                      <div className="flex items-center space-x-2">
                        <div className="status-indicator online"></div>
                        <span className="text-sm text-gray-600">Real-time monitoring active</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="status-indicator online"></div>
                        <span className="text-sm text-gray-600">AI threat detection enabled</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-6xl font-bold text-blue-600 mb-2">
                    {weatherData?.temperature ? `${weatherData.temperature}°C` : '--'}
                  </div>
                  <div className="text-lg text-gray-600 font-medium">
                    {weatherData?.description || 'Loading weather data...'}
                  </div>
                  <div className="text-sm text-gray-500 mt-1">
                    Last updated: {new Date().toLocaleTimeString()}
                  </div>
                </div>
              </div>
            </div>

            {/* Map and Alerts Row */}
            <div className="dashboard-grid cols-2">
              <div className="pro-card p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="heading-3">🗺️ Coastal Threat Map</h3>
                  <div className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                    {currentLocation.toUpperCase()}
                  </div>
                </div>
                <div className="h-96">
                  <MapView 
                    weatherData={weatherData} 
                    tideData={tideData} 
                    alerts={alerts} 
                    currentLocation={currentLocation} 
                  />
                </div>
              </div>
              
              <div className="pro-card p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="heading-3">🚨 Active Alerts</h3>
                  <div className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                    {alerts?.length || 0} Active
                  </div>
                </div>
                <AlertList alerts={alerts} />
              </div>
            </div>

            {/* Data Cards Row */}
            <div className="dashboard-grid cols-4">
              {/* Weather Card */}
              <HelpTooltip title="Current weather conditions including temperature, humidity, wind speed, and atmospheric pressure">
                <div className="data-card">
                  <div className="icon">🌤️</div>
                  <div className="value">
                    {weatherData?.temperature ? `${weatherData.temperature}°C` : '--'}
                  </div>
                  <div className="label">Temperature</div>
                  <div className="mt-3 space-y-1 text-xs text-gray-500">
                    <div>Humidity: {weatherData?.humidity ? `${weatherData.humidity}%` : '--'}</div>
                    <div>Wind: {weatherData?.wind_speed ? `${weatherData.wind_speed} m/s` : '--'}</div>
                    <div>Pressure: {weatherData?.pressure ? `${weatherData.pressure} hPa` : '--'}</div>
                  </div>
                </div>
              </HelpTooltip>

              {/* Tide Card */}
              <HelpTooltip title="Current tide information including height, type (rising/falling), and source">
                <div className="data-card border-l-green-500">
                  <div className="icon">🌊</div>
                  <div className="value">
                    {tideData?.tide_height ? `${tideData.tide_height}m` : '--'}
                  </div>
                  <div className="label">Tide Height</div>
                  <div className="mt-3 space-y-1 text-xs text-gray-500">
                    <div>Type: {tideData?.tide_type || '--'}</div>
                    <div>Status: {tideData?.tide_type === 'rising' ? '↗️ Rising' : '↘️ Falling'}</div>
                    <div>Source: {tideData?.source || '--'}</div>
                  </div>
                </div>
              </HelpTooltip>

              {/* Ocean Card */}
              <HelpTooltip title="Ocean conditions including wave height, current speed, and sea surface temperature">
                <div className="data-card border-l-teal-500">
                  <div className="icon">🌊</div>
                  <div className="value">
                    {weatherData?.wave_height ? `${weatherData.wave_height}m` : '--'}
                  </div>
                  <div className="label">Wave Height</div>
                  <div className="mt-3 space-y-1 text-xs text-gray-500">
                    <div>Current: {weatherData?.current_speed ? `${weatherData.current_speed} m/s` : '--'}</div>
                    <div>Temp: {weatherData?.sea_surface_temp ? `${weatherData.sea_surface_temp}°C` : '--'}</div>
                    <div>Period: {weatherData?.wave_period ? `${weatherData.wave_period}s` : '--'}</div>
                  </div>
                </div>
              </HelpTooltip>

              {/* Alerts Card */}
              <HelpTooltip title="Active alerts showing current coastal threats and their severity levels">
                <div className="data-card border-l-red-500">
                  <div className="icon">🚨</div>
                  <div className="value">
                    {alerts?.length || 0}
                  </div>
                  <div className="label">Active Alerts</div>
                  <div className="mt-3 space-y-1 text-xs text-gray-500">
                    <div>Critical: {alerts?.filter(a => a.severity === 'critical').length || 0}</div>
                    <div>High: {alerts?.filter(a => a.severity === 'high').length || 0}</div>
                    <div>Medium: {alerts?.filter(a => a.severity === 'medium').length || 0}</div>
                  </div>
                </div>
              </HelpTooltip>
            </div>

            {/* System Status Row */}
            <div className="pro-card p-6 bg-gradient-to-r from-green-50 to-blue-50">
              <h3 className="heading-3 mb-4">⚡ System Status</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <HelpTooltip title="Backend API status and availability">
                  <div className="status-card success">
                    <div className="text-2xl mb-2">✅</div>
                    <div className="font-semibold text-green-800">Backend API</div>
                    <div className="text-sm text-green-600">Operational</div>
                  </div>
                </HelpTooltip>
                <HelpTooltip title="Data sources and connectivity for weather, tide, and ocean data">
                  <div className="status-card success">
                    <div className="text-2xl mb-2">✅</div>
                    <div className="font-semibold text-green-800">Data Sources</div>
                    <div className="text-sm text-green-600">Connected</div>
                  </div>
                </HelpTooltip>
                <HelpTooltip title="AI threat detection and alert generation functionality">
                  <div className="status-card success">
                    <div className="text-2xl mb-2">✅</div>
                    <div className="font-semibold text-green-800">AI Detection</div>
                    <div className="text-sm text-green-600">Active</div>
                  </div>
                </HelpTooltip>
                <HelpTooltip title="Real-time coastal monitoring and alerting system operation">
                  <div className="status-card success">
                    <div className="text-2xl mb-2">✅</div>
                    <div className="font-semibold text-green-800">Monitoring</div>
                    <div className="text-sm text-green-600">Active</div>
                  </div>
                </HelpTooltip>
              </div>
            </div>
          </div>
        );
      
      case 'charts':
        return (
          <div className="pro-card p-8">
            <h2 className="heading-2 mb-6">📈 Historical Trends & Analytics</h2>
            <Charts weatherData={weatherData} tideData={tideData} />
          </div>
        );
      
      case 'locations':
        return <LocationSelector onLocationChange={handleLocationChange} currentLocation={currentLocation} />;
      
      default:
        return null;
    }
  };

  return (
    <div className="dashboard-container">
      {/* Professional Header */}
      <header className="dashboard-header">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={onBackToWelcome}
                className="text-gray-500 hover:text-gray-700 transition-colors duration-200 p-2 hover:bg-gray-100 rounded-lg"
                title="Back to Welcome"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
              </button>
              <div className="text-4xl">🌊</div>
              <div>
                <h1 className="heading-1 text-gradient mb-1">Coastal Threat Alert System</h1>
                <p className="text-lg text-gray-600 font-medium">AI-Powered Global Coastal Monitoring & Early Warning</p>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <div className="text-right">
                <div className="text-sm text-gray-500 font-medium">System Status</div>
                <div className="flex items-center space-x-2">
                  <div className="status-indicator online"></div>
                  <span className="text-green-600 font-semibold">All Systems Operational</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-500 font-medium">Last Updated</div>
                <div className="font-mono text-gray-800">{new Date().toLocaleTimeString()}</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="dashboard-content">
        {/* Professional Tab Navigation */}
        <div className="mb-8">
          <nav className="tab-nav">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
              >
                <span className="mr-2">{tab.icon}</span>
                <div className="text-left">
                  <div className="font-semibold">{tab.name}</div>
                  <div className="text-xs opacity-75">{tab.description}</div>
                </div>
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {loading && activeTab === 'overview' ? (
          <div className="loading-container">
            <div className="loading-content">
              <div className="loading-spinner-large"></div>
              <p className="loading-text">Loading coastal monitoring data...</p>
              <p className="text-sm text-gray-500 mt-2">Fetching real-time updates from global sources</p>
            </div>
          </div>
        ) : (
          renderTabContent()
        )}

        {/* Error Display */}
        {error && (
          <div className="error-container">
            <div className="error-content">
              <div className="error-icon">⚠️</div>
              <p className="error-message">{error}</p>
            </div>
          </div>
        )}
      </div>

      {/* Professional Footer */}
      <footer className="footer-gradient text-white mt-16">
        <div className="container mx-auto px-6 py-8">
          <div className="text-center">
            <p className="text-lg font-semibold mb-2">🌊 Coastal Threat Alert System</p>
            <p className="opacity-75 mb-4">AI-Powered Global Coastal Monitoring for Community Safety</p>
            <div className="text-sm opacity-60">
              Built with FastAPI, React, and Machine Learning • Real-time data from worldwide coastal monitoring networks
            </div>
            <div className="mt-4 text-xs opacity-50">
              HackOut'25 • Team Titans • Protecting Coastal Communities Worldwide
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
