import React, { useState, useEffect } from 'react';
import { 
  getStakeholderDashboard, 
  getEmergencyCoordination, 
  getHabitatAssessment,
  getFishingZoneSafety,
  getCivilDefenceCoordination,
  getPolicyRecommendations
} from '../services/api';

// Helper functions moved outside component
const getStakeholderTitle = (stakeholderType) => {
  const titles = {
    'disaster_management': 'Disaster Management Department',
    'coastal_government': 'Coastal City Government',
    'environmental_ngo': 'Environmental NGO',
    'fisherfolk': 'Fisherfolk Community',
    'civil_defence': 'Civil Defence Team'
  };
  return titles[stakeholderType] || 'Stakeholder Dashboard';
};

const getStakeholderIcon = (stakeholderType) => {
  const icons = {
    'disaster_management': '🚨',
    'coastal_government': '🏛️',
    'environmental_ngo': '🌿',
    'fisherfolk': '🐟',
    'civil_defence': '🛡️'
  };
  return icons[stakeholderType] || '👥';
};

const getStakeholderDescription = (stakeholderType) => {
  const descriptions = {
    'disaster_management': 'Coordinate emergency response, manage resources, and ensure public safety during coastal disasters.',
    'coastal_government': 'Make data-driven decisions, develop policies, and manage coastal development for sustainable growth.',
    'environmental_ngo': 'Monitor habitat health, protect biodiversity, and advocate for coastal conservation.',
    'fisherfolk': 'Access fishing zone safety information, weather alerts, and emergency protocols for safe fishing operations.',
    'civil_defence': 'Coordinate emergency response teams, manage evacuation plans, and ensure public safety.'
  };
  return descriptions[stakeholderType] || 'Access stakeholder-specific information and tools.';
};

const StakeholderDashboard = ({ stakeholderType, location, onBack }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchDashboardData();
  }, [stakeholderType, location]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const data = await getStakeholderDashboard(stakeholderType, location);
      setDashboardData(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error('Dashboard fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-100 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-20">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-lg text-gray-600">Loading {getStakeholderTitle(stakeholderType)}...</p>
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
              onClick={fetchDashboardData}
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
                onClick={onBack}
                className="text-gray-500 hover:text-gray-700 transition-colors"
              >
                ← Back
              </button>
              <div className="flex items-center space-x-3">
                <span className="text-3xl">{getStakeholderIcon(stakeholderType)}</span>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">{getStakeholderTitle(stakeholderType)}</h1>
                  <p className="text-sm text-gray-600">Monitoring: {location}</p>
                </div>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Last Updated</p>
              <p className="text-sm font-medium text-gray-900">
                {new Date().toLocaleTimeString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {['overview', 'alerts', 'coordination', 'reports', 'tools'].map((tab) => (
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
          <OverviewTab 
            stakeholderType={stakeholderType} 
            location={location}
            dashboardData={dashboardData}
          />
        )}
        {activeTab === 'alerts' && (
          <AlertsTab 
            stakeholderType={stakeholderType} 
            location={location}
          />
        )}
        {activeTab === 'coordination' && (
          <CoordinationTab 
            stakeholderType={stakeholderType} 
            location={location}
          />
        )}
        {activeTab === 'reports' && (
          <ReportsTab 
            stakeholderType={stakeholderType} 
            location={location}
          />
        )}
        {activeTab === 'tools' && (
          <ToolsTab 
            stakeholderType={stakeholderType} 
            location={location}
          />
        )}
      </div>
    </div>
  );
};

// Overview Tab Component
const OverviewTab = ({ stakeholderType, location, dashboardData }) => {
  return (
    <div className="space-y-6">
      {/* Stakeholder Description */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">About This Dashboard</h2>
        <p className="text-gray-600 leading-relaxed">
          {getStakeholderDescription(stakeholderType)}
        </p>
      </div>

      {/* Current Conditions */}
      {dashboardData?.stakeholder_dashboard?.current_conditions && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Weather Conditions</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Temperature:</span>
                <span className="font-medium">
                  {dashboardData.stakeholder_dashboard.current_conditions.weather.temperature}°C
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Wind Speed:</span>
                <span className="font-medium">
                  {dashboardData.stakeholder_dashboard.current_conditions.weather.wind_speed} km/h
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Conditions:</span>
                <span className="font-medium">
                  {dashboardData.stakeholder_dashboard.current_conditions.weather.description}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Ocean Conditions</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Wave Height:</span>
                <span className="font-medium">
                  {dashboardData.stakeholder_dashboard.current_conditions.ocean.wave_height} m
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Current Speed:</span>
                <span className="font-medium">
                  {dashboardData.stakeholder_dashboard.current_conditions.ocean.current_speed} knots
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Water Temp:</span>
                <span className="font-medium">
                  {dashboardData.stakeholder_dashboard.current_conditions.ocean.water_temperature}°C
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Active Alerts</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Alerts:</span>
                <span className="font-medium">
                  {dashboardData.stakeholder_dashboard.current_conditions.alerts.length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Critical:</span>
                <span className="font-medium text-red-600">
                  {dashboardData.stakeholder_dashboard.current_conditions.alerts.filter(a => a.severity === 'critical').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">High:</span>
                <span className="font-medium text-orange-600">
                  {dashboardData.stakeholder_dashboard.current_conditions.alerts.filter(a => a.severity === 'high').length}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Stakeholder-Specific Information */}
      {dashboardData?.stakeholder_dashboard?.stakeholder_info && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Stakeholder Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.entries(dashboardData.stakeholder_dashboard.stakeholder_info).map(([key, value]) => (
              <div key={key}>
                <h3 className="text-lg font-medium text-gray-900 mb-2 capitalize">
                  {key.replace(/_/g, ' ')}
                </h3>
                {Array.isArray(value) ? (
                  <ul className="list-disc list-inside space-y-1 text-gray-600">
                    {value.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                ) : typeof value === 'object' && value !== null ? (
                  <div className="space-y-2">
                    {Object.entries(value).map(([subKey, subValue]) => (
                      <div key={subKey} className="flex justify-between">
                        <span className="text-gray-600 capitalize">{subKey.replace(/_/g, ' ')}:</span>
                        <span className="text-gray-900 font-medium">{subValue}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-600">{value}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Alerts Tab Component
const AlertsTab = ({ stakeholderType, location }) => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
  }, [stakeholderType, location]);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const data = await getStakeholderDashboard(stakeholderType, location);
      setAlerts(data.stakeholder_dashboard.current_conditions.alerts || []);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading alerts...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Active Alerts</h2>
        {alerts.length === 0 ? (
          <p className="text-gray-600">No active alerts at this time.</p>
        ) : (
          <div className="space-y-4">
            {alerts.map((alert, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border ${
                  alert.severity === 'critical'
                    ? 'bg-red-50 border-red-200'
                    : alert.severity === 'high'
                    ? 'bg-orange-50 border-orange-200'
                    : 'bg-yellow-50 border-yellow-200'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900 capitalize">
                      {alert.alert_type?.replace(/_/g, ' ')}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {alert.description}
                    </p>
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                      <span>Severity: {alert.severity}</span>
                      <span>Confidence: {Math.round((alert.confidence || 0) * 100)}%</span>
                    </div>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    alert.severity === 'critical'
                      ? 'bg-red-100 text-red-800'
                      : alert.severity === 'high'
                      ? 'bg-orange-100 text-orange-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {alert.severity}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Coordination Tab Component
const CoordinationTab = ({ stakeholderType, location }) => {
  const [coordinationData, setCoordinationData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleEmergencyCoordination = async (emergencyType, severity = 'medium') => {
    try {
      setLoading(true);
      const data = await getEmergencyCoordination(emergencyType, location, severity, 10000);
      setCoordinationData(data);
    } catch (error) {
      console.error('Error fetching coordination data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Emergency Coordination</h2>
        <p className="text-gray-600 mb-6">
          Access emergency coordination plans and response protocols for different disaster scenarios.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {['tsunami', 'cyclone', 'storm_surge', 'habitat_degradation'].map((emergency) => (
            <button
              key={emergency}
              onClick={() => handleEmergencyCoordination(emergency)}
              disabled={loading}
              className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors disabled:opacity-50"
            >
              <h3 className="font-medium text-gray-900 capitalize mb-2">
                {emergency.replace(/_/g, ' ')}
              </h3>
              <p className="text-sm text-gray-600">
                Get coordination plan
              </p>
            </button>
          ))}
        </div>

        {loading && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading coordination plan...</p>
          </div>
        )}

        {coordinationData && (
          <div className="border-t border-gray-200 pt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Coordination Plan</h3>
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-2">
                {coordinationData.coordination_plan.emergency_type} - {coordinationData.coordination_plan.severity}
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h5 className="font-medium text-gray-700 mb-2">Response Plan</h5>
                  <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                    {coordinationData.coordination_plan.response_plan.immediate_actions?.map((action, index) => (
                      <li key={index}>{action}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h5 className="font-medium text-gray-700 mb-2">Team Coordination</h5>
                  <div className="space-y-2 text-sm text-gray-600">
                    {Object.entries(coordinationData.coordination_plan.team_coordination || {}).map(([team, info]) => (
                      <div key={team} className="flex justify-between">
                        <span className="capitalize">{team.replace(/_/g, ' ')}:</span>
                        <span className={`px-2 py-1 rounded text-xs ${
                          info.deployment_status === 'deploying' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          {info.deployment_status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Reports Tab Component
const ReportsTab = ({ stakeholderType, location }) => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateReport = async (reportType) => {
    try {
      setLoading(true);
      let reportData;
      
      switch (reportType) {
        case 'habitat':
          reportData = await getHabitatAssessment('mangrove_forest', location);
          break;
        case 'fishing':
          reportData = await getFishingZoneSafety(location);
          break;
        case 'policy':
          reportData = await getPolicyRecommendations(location);
          break;
        default:
          return;
      }
      
      setReports(prev => [reportData, ...prev]);
    } catch (error) {
      console.error('Error generating report:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Reports & Assessments</h2>
        <p className="text-gray-600 mb-6">
          Generate comprehensive reports and assessments for your specific stakeholder needs.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <button
            onClick={() => generateReport('habitat')}
            disabled={loading}
            className="p-4 border border-gray-200 rounded-lg hover:border-green-300 hover:bg-green-50 transition-colors disabled:opacity-50"
          >
            <h3 className="font-medium text-gray-900 mb-2">Habitat Assessment</h3>
            <p className="text-sm text-gray-600">
              Assess coastal habitat health and conservation status
            </p>
          </button>
          
          <button
            onClick={() => generateReport('fishing')}
            disabled={loading}
            className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors disabled:opacity-50"
          >
            <h3 className="font-medium text-gray-900 mb-2">Fishing Safety</h3>
            <p className="text-sm text-gray-600">
              Get fishing zone safety assessment and recommendations
            </p>
          </button>
          
          <button
            onClick={() => generateReport('policy')}
            disabled={loading}
            className="p-4 border border-gray-200 rounded-lg hover:border-purple-300 hover:bg-purple-50 transition-colors disabled:opacity-50"
          >
            <h3 className="font-medium text-gray-900 mb-2">Policy Analysis</h3>
            <p className="text-sm text-gray-600">
              Generate policy recommendations and impact analysis
            </p>
          </button>
        </div>

        {loading && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Generating report...</p>
          </div>
        )}

        {reports.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-900">Generated Reports</h3>
            {reports.map((report, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-2">
                  {report.report_type || 'Report'} - {new Date().toLocaleDateString()}
                </h4>
                <div className="text-sm text-gray-600">
                  <p>Location: {report.location}</p>
                  <p>Status: {report.status}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Tools Tab Component
const ToolsTab = ({ stakeholderType, location }) => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Tools & Resources</h2>
        <p className="text-gray-600 mb-6">
          Access specialized tools and resources for your stakeholder role.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-medium text-gray-900 mb-2">Emergency Protocols</h3>
            <p className="text-sm text-gray-600 mb-3">
              Access emergency response protocols and coordination guidelines.
            </p>
            <button className="btn-secondary text-sm">
              View Protocols
            </button>
          </div>
          
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-medium text-gray-900 mb-2">Resource Management</h3>
            <p className="text-sm text-gray-600 mb-3">
              Manage emergency resources and coordinate team deployments.
            </p>
            <button className="btn-secondary text-sm">
              Manage Resources
            </button>
          </div>
          
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-medium text-gray-900 mb-2">Communication Hub</h3>
            <p className="text-sm text-gray-600 mb-3">
              Access emergency communication channels and coordination tools.
            </p>
            <button className="btn-secondary text-sm">
              Open Hub
            </button>
          </div>
          
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="font-medium text-gray-900 mb-2">Training & Documentation</h3>
            <p className="text-sm text-gray-600 mb-3">
              Access training materials and operational documentation.
            </p>
            <button className="btn-secondary text-sm">
              View Materials
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StakeholderDashboard;
