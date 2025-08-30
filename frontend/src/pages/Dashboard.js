import React, { useState, useEffect } from 'react';
import MapView from '../components/MapView';
import AlertList from '../components/AlertList';
import LocationSelector from '../components/LocationSelector';
import HelpTooltip from '../components/HelpTooltip';
import StakeholderDashboard from '../components/StakeholderDashboard';
import Analytics from '../components/Analytics';
import { getDataForLocation, getAvailableLocations, getAlerts } from '../services/api';

const Dashboard = ({ onBackToWelcome }) => {
  const [currentLocation, setCurrentLocation] = useState('mumbai');
  const [data, setData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showStakeholderDashboard, setShowStakeholderDashboard] = useState(false);
  const [selectedStakeholder, setSelectedStakeholder] = useState(null);

  useEffect(() => {
    fetchData();
  }, [currentLocation]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [locationData, alertsData] = await Promise.all([
        getDataForLocation(currentLocation),
        getAlerts()
      ]);
      
      setData(locationData);
      setAlerts(alertsData.alerts || []);
    } catch (err) {
      setError('Failed to fetch data');
      console.error('Data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLocationChange = (location) => {
    setCurrentLocation(location);
  };

  const handleStakeholderSelect = (stakeholderType) => {
    setSelectedStakeholder(stakeholderType);
    setShowStakeholderDashboard(true);
  };

  const handleBackToMain = () => {
    setShowStakeholderDashboard(false);
    setSelectedStakeholder(null);
  };

  if (showStakeholderDashboard && selectedStakeholder) {
    return (
      <StakeholderDashboard
        stakeholderType={selectedStakeholder}
        location={currentLocation}
        onBack={handleBackToMain}
      />
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-100 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-20">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-lg text-gray-600">Loading coastal threat data...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-100 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-20">
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
            <button
              onClick={fetchData}
              className="btn-primary"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={onBackToWelcome}
                className="text-gray-500 hover:text-gray-700 transition-colors"
              >
                ← Back to Welcome
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Coastal Threat Alert System</h1>
                <p className="text-sm text-gray-600">Real-time monitoring and early warning system</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Monitoring</p>
              <p className="text-sm font-medium text-gray-900 capitalize">{currentLocation}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {['overview', 'stakeholders', 'analytics', 'locations'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Map and Alerts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <HelpTooltip title="Interactive Coastal Map" position="top">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">Coastal Monitoring Map</h2>
                  <div className="h-96">
                    <MapView 
                      currentLocation={currentLocation}
                      alerts={alerts}
                    />
                  </div>
                </div>
              </HelpTooltip>

              <HelpTooltip title="Active Threat Alerts" position="top">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">Active Alerts</h2>
                  <AlertList alerts={alerts} />
                </div>
              </HelpTooltip>
            </div>

            {/* Data Cards Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <HelpTooltip title="Current Weather Conditions" position="top">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                        <span className="text-blue-600 text-lg">🌤️</span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Weather</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {data?.weather?.temperature}°C
                      </p>
                    </div>
                  </div>
                </div>
              </HelpTooltip>

              <HelpTooltip title="Ocean Wave Conditions" position="top">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-cyan-100 rounded-lg flex items-center justify-center">
                        <span className="text-cyan-600 text-lg">🌊</span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Waves</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {data?.ocean?.wave_height} m
                      </p>
                    </div>
                  </div>
                </div>
              </HelpTooltip>

              <HelpTooltip title="Current Tide Status" position="top">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                        <span className="text-green-600 text-lg">🌊</span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Tide</p>
                      <p className="text-lg font-semibold text-gray-900 capitalize">
                        {data?.ocean?.tide_status || 'N/A'}
                      </p>
                    </div>
                  </div>
                </div>
              </HelpTooltip>

              <HelpTooltip title="Active Threat Alerts" position="top">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                        <span className="text-red-600 text-lg">🚨</span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Alerts</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {alerts?.length || 0}
                      </p>
                    </div>
                  </div>
                </div>
              </HelpTooltip>
            </div>

            {/* System Status Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <HelpTooltip title="System Health and Status" position="top">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">System Status</h2>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Monitoring System</span>
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                        Active
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Data Collection</span>
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                        Operational
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Alert System</span>
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                        Functional
                      </span>
                    </div>
                  </div>
                </div>
              </HelpTooltip>

              <HelpTooltip title="Understanding the Alert System" position="top">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">Understanding Alerts</h2>
                  <div className="space-y-3 text-sm text-gray-600">
                    <p><strong>Critical:</strong> Immediate action required, life-threatening conditions</p>
                    <p><strong>High:</strong> Urgent attention needed, significant risk</p>
                    <p><strong>Medium:</strong> Monitor closely, moderate risk</p>
                    <p><strong>Low:</strong> Stay informed, minimal risk</p>
                  </div>
                </div>
              </HelpTooltip>
            </div>
          </div>
        )}

        {activeTab === 'stakeholders' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Stakeholder Dashboards</h2>
              <p className="text-gray-600 mb-6">
                Access specialized dashboards designed for different stakeholder groups to support disaster management, 
                habitat protection, fisherfolk safety, civil defence, and coastal government decision-making.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="border border-gray-200 rounded-lg p-6 hover:border-blue-300 hover:shadow-md transition-all">
                  <div className="text-center">
                    <span className="text-4xl mb-4 block">🚨</span>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Disaster Management</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Coordinate emergency response, manage resources, and ensure public safety during coastal disasters.
                    </p>
                    <button
                      onClick={() => handleStakeholderSelect('disaster_management')}
                      className="btn-primary w-full"
                    >
                      Access Dashboard
                    </button>
                  </div>
                </div>

                <div className="border border-gray-200 rounded-lg p-6 hover:border-green-300 hover:shadow-md transition-all">
                  <div className="text-center">
                    <span className="text-4xl mb-4 block">🏛️</span>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Coastal Government</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Make data-driven decisions, develop policies, and manage coastal development for sustainable growth.
                    </p>
                    <button
                      onClick={() => handleStakeholderSelect('coastal_government')}
                      className="btn-primary w-full"
                    >
                      Access Dashboard
                    </button>
                  </div>
                </div>

                <div className="border border-gray-200 rounded-lg p-6 hover:border-green-300 hover:shadow-md transition-all">
                  <div className="text-center">
                    <span className="text-4xl mb-4 block">🌿</span>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Environmental NGO</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Monitor habitat health, protect biodiversity, and advocate for coastal conservation.
                    </p>
                    <button
                      onClick={() => handleStakeholderSelect('environmental_ngo')}
                      className="btn-primary w-full"
                    >
                      Access Dashboard
                    </button>
                  </div>
                </div>

                <div className="border border-gray-200 rounded-lg p-6 hover:border-blue-300 hover:shadow-md transition-all">
                  <div className="text-center">
                    <span className="text-4xl mb-4 block">🐟</span>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Fisherfolk Community</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Access fishing zone safety information, weather alerts, and emergency protocols for safe fishing operations.
                    </p>
                    <button
                      onClick={() => handleStakeholderSelect('fisherfolk')}
                      className="btn-primary w-full"
                    >
                      Access Dashboard
                    </button>
                  </div>
                </div>

                <div className="border border-gray-200 rounded-lg p-6 hover:border-purple-300 hover:shadow-md transition-all">
                  <div className="text-center">
                    <span className="text-4xl mb-4 block">🛡️</span>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Civil Defence Team</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Coordinate emergency response teams, manage evacuation plans, and ensure public safety.
                    </p>
                    <button
                      onClick={() => handleStakeholderSelect('civil_defence')}
                      className="btn-primary w-full"
                    >
                      Access Dashboard
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <Analytics location={currentLocation} />
          </div>
        )}

        {activeTab === 'locations' && (
          <div className="space-y-6">
            <HelpTooltip title="Select Monitoring Location" position="top">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Location Selection</h2>
                <LocationSelector 
                  currentLocation={currentLocation}
                  onLocationChange={handleLocationChange}
                />
              </div>
            </HelpTooltip>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
