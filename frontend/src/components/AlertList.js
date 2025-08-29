import React from 'react';

const AlertList = ({ alerts = [] }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'alert-critical';
      case 'high':
        return 'alert-high';
      case 'medium':
        return 'alert-medium';
      case 'low':
        return 'alert-low';
      default:
        return 'border-l-4 border-l-gray-500 bg-gradient-to-r from-gray-50 to-gray-100 shadow-lg';
    }
  };

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-600 text-white';
      case 'high':
        return 'bg-orange-500 text-white';
      case 'medium':
        return 'bg-yellow-500 text-yellow-900';
      case 'low':
        return 'bg-green-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const getAlertIcon = (alertType) => {
    switch (alertType) {
      case 'cyclone':
        return '🌪️';
      case 'high_wind':
        return '💨';
      case 'high_tide':
        return '🌊';
      case 'low_pressure':
        return '🌫️';
      case 'storm_risk':
        return '🌊💨';
      case 'rough_seas':
        return '🌊';
      case 'pollution':
        return '🚨';
      case 'flooding_risk':
        return '🌊🏠';
      default:
        return '⚠️';
    }
  };

  const getAlertTitle = (alertType) => {
    switch (alertType) {
      case 'high_wind':
        return 'High Wind Warning';
      case 'high_tide':
        return 'High Tide Alert';
      case 'storm_risk':
        return 'Storm Risk Warning';
      case 'rough_seas':
        return 'Rough Sea Conditions';
      case 'pollution':
        return 'Water Quality Alert';
      case 'flooding_risk':
        return 'Flooding Risk Warning';
      default:
        return alertType?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Alert';
    }
  };

  return (
    <div className="space-y-6">
      {/* System Status Overview */}
      <div className="pro-card p-4 bg-gradient-to-r from-blue-50 to-indigo-50">
        <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
          <span className="mr-2">📊</span>
          System Overview
        </h4>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="flex items-center space-x-2">
            <div className="status-indicator online"></div>
            <span className="text-gray-700">Real-time monitoring</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="status-indicator online"></div>
            <span className="text-gray-700">AI threat detection</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="status-indicator online"></div>
            <span className="text-gray-700">Coastal surveillance</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="status-indicator online"></div>
            <span className="text-gray-700">Last update: {new Date().toLocaleTimeString()}</span>
          </div>
        </div>
      </div>

      {/* Alerts Display */}
      {(!alerts || alerts.length === 0) ? (
        <div className="text-center py-12">
          <div className="text-8xl mb-4">✅</div>
          <h3 className="heading-3 text-gray-700 mb-2">All Clear!</h3>
          <p className="text-gray-500 mb-4">No active alerts at the moment.</p>
          <div className="pro-card p-4 bg-green-50 border border-green-200">
            <p className="text-sm text-green-700">
              <strong>System Status:</strong> All monitoring systems operational
            </p>
          </div>
        </div>
      ) : (
        <div className="space-y-4 max-h-96 overflow-y-auto custom-scrollbar">
          {alerts?.map((alert) => (
            <div
              key={alert.id}
              className={`${getSeverityColor(alert.severity)} p-4 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02]`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <div className="text-3xl">
                    {getAlertIcon(alert.alert_type)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-3">
                      <h4 className="font-semibold text-gray-800 text-lg">
                        {getAlertTitle(alert.alert_type)}
                      </h4>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${getSeverityBadge(alert.severity)}`}>
                        {alert.severity}
                      </span>
                    </div>
                    <p className="text-gray-700 text-sm mb-3 leading-relaxed">
                      {alert.description}
                    </p>
                    <div className="grid grid-cols-1 gap-2 text-xs text-gray-500">
                      <div className="flex items-center space-x-4">
                        <span className="flex items-center">
                          <span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                          <strong>Location:</strong> {alert.location}
                        </span>
                        <span className="flex items-center">
                          <span className="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                          <strong>Triggered:</strong> {alert.triggered_by}
                        </span>
                      </div>
                      <div className="flex items-center">
                        <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                        <strong>Time:</strong> {new Date(alert.timestamp).toLocaleString()}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Help Information */}
      <div className="pro-card p-4 bg-gradient-to-r from-gray-50 to-blue-50">
        <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
          <span className="mr-2">ℹ️</span>
          Understanding Alerts
        </h4>
        <div className="text-sm text-gray-600 space-y-2">
          <p><strong>Critical:</strong> Immediate action required. Evacuate if necessary.</p>
          <p><strong>High:</strong> Exercise extreme caution. Monitor local authorities.</p>
          <p><strong>Medium:</strong> Stay alert. Avoid risky activities.</p>
          <p><strong>Low:</strong> Be aware. Normal precautions recommended.</p>
        </div>
      </div>
    </div>
  );
};

export default AlertList;
