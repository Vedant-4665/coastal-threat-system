import React, { useState } from 'react';

const AlertList = ({ alerts = [], onRefresh }) => {
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const handleRefresh = () => {
    if (onRefresh) {
      onRefresh();
      setLastUpdate(new Date());
    }
  };

  const getAlertTitle = (alertType) => {
    if (!alertType) return 'Unknown Alert';
    
    const titles = {
      'high_wind': 'High Wind Warning',
      'high_tide': 'High Tide Alert',
      'storm_surge': 'Storm Surge Warning',
      'tsunami': 'Tsunami Alert',
      'cyclone': 'Cyclone Warning',
      'pollution': 'Water Pollution Alert',
      'habitat_degradation': 'Habitat Degradation Alert'
    };
    
    return titles[alertType] || alertType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  const getAlertColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'bg-red-600 text-white';
      case 'high':
        return 'bg-orange-500 text-white';
      case 'medium':
        return 'bg-yellow-500 text-white';
      case 'low':
        return 'bg-green-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  return (
    <div className="space-y-4">
      {/* Header with refresh button */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Active Alerts</h3>
        <div className="flex items-center space-x-3">
          <button
            onClick={handleRefresh}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors flex items-center space-x-1"
          >
            <span>🔄</span>
            <span>Refresh</span>
          </button>
          <div className="text-xs text-gray-500">
            Last: {lastUpdate.toLocaleTimeString()}
          </div>
        </div>
      </div>

      {/* System Overview Card */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <h4 className="font-semibold text-gray-900 mb-3">System Overview</h4>
        <div className="grid grid-cols-2 gap-3">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Real-time monitoring</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600">AI threat detection</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Coastal surveillance</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Last update: {new Date().toLocaleTimeString()}</span>
          </div>
        </div>
      </div>

      {/* Alerts */}
      {(!alerts || alerts.length === 0) ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-4">✅</div>
          <p className="text-gray-600">No active alerts at this time</p>
          <p className="text-sm text-gray-500 mt-2">System is monitoring coastal conditions</p>
        </div>
      ) : (
        <div className="space-y-3">
          {alerts.map((alert, index) => (
            <div
              key={alert.id || index}
              className={`border-l-4 border-l-${getAlertColor(alert.severity).split('-')[1]}-500 bg-white rounded-lg shadow-sm border border-gray-200 p-4`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h4 className="font-semibold text-gray-900">
                      {getAlertTitle(alert.alert_type)}
                    </h4>
                    <span className={`px-2 py-1 rounded text-xs font-bold ${getAlertColor(alert.severity)}`}>
                      {alert.severity || 'unknown'}
                    </span>
                  </div>
                  
                  <p className="text-gray-600 mb-3">
                    {alert.description || 'No description available'}
                  </p>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm text-gray-500">
                    <div>
                      <strong>Location:</strong> {alert.location || 'Unknown'}
                    </div>
                    <div>
                      <strong>Time:</strong> {new Date(alert.timestamp).toLocaleString()}
                    </div>
                    <div>
                      <strong>Triggered:</strong> {alert.triggered_by || 'Unknown'}
                    </div>
                    <div>
                      <strong>Source:</strong> {alert.source || 'Unknown'}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Understanding Alerts Section */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <div className="text-blue-600 text-xl">ℹ️</div>
          <div>
            <h4 className="font-semibold text-blue-900 mb-2">Understanding Alerts</h4>
            <div className="text-sm text-blue-800 space-y-1">
              <p><strong>Critical:</strong> Immediate action required - evacuate if necessary</p>
              <p><strong>High:</strong> Take precautions - monitor conditions closely</p>
              <p><strong>Medium:</strong> Stay alert - prepare for potential changes</p>
              <p><strong>Low:</strong> Informational - no immediate action needed</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AlertList;
