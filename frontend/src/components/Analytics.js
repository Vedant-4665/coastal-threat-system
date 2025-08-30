import React, { useState, useEffect } from 'react';
import { Line, Bar, Doughnut, Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import 'chartjs-adapter-date-fns';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Analytics = ({ location = 'mumbai' }) => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedTimeframe, setSelectedTimeframe] = useState('7d');
  const [selectedMetric, setSelectedMetric] = useState('temperature');

  useEffect(() => {
    generateAnalyticsData();
  }, [location, selectedTimeframe]);

  const generateAnalyticsData = () => {
    setLoading(true);
    
    // Simulate API call delay
    setTimeout(() => {
      const data = generateComprehensiveAnalytics(location, selectedTimeframe);
      setAnalyticsData(data);
      setLoading(false);
    }, 1000);
  };

  const generateComprehensiveAnalytics = (location, timeframe) => {
    const days = timeframe === '7d' ? 7 : timeframe === '30d' ? 30 : 90;
    const baseDate = new Date();
    
    const labels = [];
    const temperatureData = [];
    const humidityData = [];
    const windSpeedData = [];
    const tideHeightData = [];
    const waveHeightData = [];
    const alertCounts = [];
    
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(baseDate);
      date.setDate(date.getDate() - i);
      labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
      
      // Generate realistic data with trends
      const baseTemp = 25 + Math.sin(i * 0.3) * 5 + (Math.random() - 0.5) * 3;
      const baseHumidity = 70 + Math.sin(i * 0.2) * 15 + (Math.random() - 0.5) * 10;
      const baseWind = 8 + Math.sin(i * 0.4) * 4 + (Math.random() - 0.5) * 2;
      const baseTide = 2.5 + Math.sin(i * 0.5) * 1.5 + (Math.random() - 0.5) * 0.5;
      const baseWave = 1.2 + Math.sin(i * 0.3) * 0.8 + (Math.random() - 0.5) * 0.3;
      
      temperatureData.push(Math.round(baseTemp * 10) / 10);
      humidityData.push(Math.round(baseHumidity * 10) / 10);
      windSpeedData.push(Math.round(baseWind * 10) / 10);
      tideHeightData.push(Math.round(baseTide * 10) / 10);
      waveHeightData.push(Math.round(baseWave * 10) / 10);
      
      // Generate alert counts based on conditions
      const alertCount = Math.floor(
        (baseWind > 12 ? 2 : 0) +
        (baseTide > 3.5 ? 1 : 0) +
        (baseWave > 1.8 ? 1 : 0) +
        (Math.random() > 0.7 ? 1 : 0)
      );
      alertCounts.push(alertCount);
    }

    return {
      timeSeries: {
        labels,
        datasets: [
          {
            label: 'Temperature (°C)',
            data: temperatureData,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            tension: 0.4,
            fill: true,
          },
          {
            label: 'Humidity (%)',
            data: humidityData,
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.1)',
            tension: 0.4,
            fill: true,
          },
          {
            label: 'Wind Speed (km/h)',
            data: windSpeedData,
            borderColor: 'rgb(255, 205, 86)',
            backgroundColor: 'rgba(255, 205, 86, 0.1)',
            tension: 0.4,
            fill: true,
          },
        ],
      },
      tideWaveData: {
        labels,
        datasets: [
          {
            label: 'Tide Height (m)',
            data: tideHeightData,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.1)',
            tension: 0.4,
            fill: true,
          },
          {
            label: 'Wave Height (m)',
            data: waveHeightData,
            borderColor: 'rgb(153, 102, 255)',
            backgroundColor: 'rgba(153, 102, 255, 0.1)',
            tension: 0.4,
            fill: true,
          },
        ],
      },
      alertTrends: {
        labels,
        datasets: [
          {
            label: 'Daily Alerts',
            data: alertCounts,
            backgroundColor: 'rgba(255, 99, 132, 0.8)',
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1,
          },
        ],
      },
      threatDistribution: {
        labels: ['High Wind', 'High Tide', 'Storm Surge', 'Pollution', 'Habitat Degradation'],
        datasets: [
          {
            data: [35, 25, 20, 15, 5],
            backgroundColor: [
              'rgba(255, 99, 132, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(153, 102, 255, 0.8)',
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(153, 102, 255)',
            ],
            borderWidth: 2,
          },
        ],
      },
      riskAssessment: {
        labels: ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'],
        datasets: [
          {
            label: 'Risk Level Distribution',
            data: [40, 35, 20, 5],
            backgroundColor: [
              'rgba(75, 192, 192, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(255, 159, 64, 0.8)',
              'rgba(255, 99, 132, 0.8)',
            ],
            borderColor: [
              'rgb(75, 192, 192)',
              'rgb(255, 205, 86)',
              'rgb(255, 159, 64)',
              'rgb(255, 99, 132)',
            ],
            borderWidth: 2,
          },
        ],
      },
      predictiveInsights: {
        next24h: {
          temperature: { min: 22, max: 28, trend: 'stable' },
          windSpeed: { min: 6, max: 12, trend: 'decreasing' },
          tideHeight: { min: 2.1, max: 3.2, trend: 'rising' },
          riskLevel: 'moderate',
          recommendations: [
            'Monitor wind conditions for fishing activities',
            'Prepare for moderate tide changes',
            'Continue normal coastal operations'
          ]
        },
        next7d: {
          temperature: { min: 20, max: 30, trend: 'warming' },
          windSpeed: { min: 5, max: 15, trend: 'variable' },
          tideHeight: { min: 1.8, max: 3.5, trend: 'mixed' },
          riskLevel: 'moderate',
          recommendations: [
            'Prepare for potential storm conditions',
            'Monitor long-term weather patterns',
            'Update emergency response protocols'
          ]
        }
      },
      stakeholderMetrics: {
        disasterManagement: { responseTime: '2.3 min', coordinationScore: 94, readinessLevel: 'high' },
        coastalGovernment: { policyEffectiveness: 87, resourceAllocation: 92, communityEngagement: 89 },
        environmentalNGO: { habitatMonitoring: 91, conservationEfforts: 88, researchQuality: 93 },
        fisherfolk: { safetyCompliance: 96, weatherAwareness: 89, emergencyResponse: 87 },
        civilDefence: { responseCapability: 95, equipmentStatus: 93, trainingLevel: 91 }
      }
    };
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading comprehensive analytics...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header Controls */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Analytics & Insights</h2>
            <p className="text-gray-600 mt-1">Comprehensive coastal monitoring analytics and predictive insights</p>
          </div>
          <div className="flex gap-3">
            <select
              value={selectedTimeframe}
              onChange={(e) => setSelectedTimeframe(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
            <select
              value={selectedMetric}
              onChange={(e) => setSelectedMetric(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="temperature">Temperature</option>
              <option value="humidity">Humidity</option>
              <option value="wind">Wind Speed</option>
              <option value="tide">Tide Height</option>
            </select>
          </div>
        </div>
      </div>

      {/* Time Series Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Environmental Trends</h3>
          <Line 
            data={analyticsData.timeSeries}
            options={{
              responsive: true,
              plugins: {
                legend: { position: 'top' },
                title: { display: false }
              },
              scales: {
                y: { beginAtZero: false }
              }
            }}
          />
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Ocean Conditions</h3>
          <Line 
            data={analyticsData.tideWaveData}
            options={{
              responsive: true,
              plugins: {
                legend: { position: 'top' },
                title: { display: false }
              },
              scales: {
                y: { beginAtZero: false }
              }
            }}
          />
        </div>
      </div>

      {/* Alert Trends and Risk Assessment */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Alert Trends</h3>
          <Bar 
            data={analyticsData.alertTrends}
            options={{
              responsive: true,
              plugins: {
                legend: { position: 'top' },
                title: { display: false }
              },
              scales: {
                y: { beginAtZero: true, ticks: { stepSize: 1 } }
              }
            }}
          />
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Level Distribution</h3>
          <Doughnut 
            data={analyticsData.riskAssessment}
            options={{
              responsive: true,
              plugins: {
                legend: { position: 'bottom' },
                title: { display: false }
              }
            }}
          />
        </div>
      </div>

      {/* Threat Distribution and Predictive Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Threat Distribution</h3>
          <Doughnut 
            data={analyticsData.threatDistribution}
            options={{
              responsive: true,
              plugins: {
                legend: { position: 'bottom' },
                title: { display: false }
              }
            }}
          />
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Predictive Insights</h3>
          <div className="space-y-4">
            <div className="border-l-4 border-blue-500 pl-4">
              <h4 className="font-medium text-gray-900">Next 24 Hours</h4>
              <p className="text-sm text-gray-600">Risk Level: <span className="font-medium text-orange-600">{analyticsData.predictiveInsights.next24h.riskLevel}</span></p>
              <ul className="text-sm text-gray-600 mt-2 space-y-1">
                {analyticsData.predictiveInsights.next24h.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
            <div className="border-l-4 border-purple-500 pl-4">
              <h4 className="font-medium text-gray-900">Next 7 Days</h4>
              <p className="text-sm text-gray-600">Risk Level: <span className="font-medium text-orange-600">{analyticsData.predictiveInsights.next7d.riskLevel}</span></p>
              <ul className="text-sm text-gray-600 mt-2 space-y-1">
                {analyticsData.predictiveInsights.next7d.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-purple-500 mr-2">•</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Stakeholder Performance Metrics */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Stakeholder Performance Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {Object.entries(analyticsData.stakeholderMetrics).map(([stakeholder, metrics]) => (
            <div key={stakeholder} className="text-center p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900 capitalize mb-3">
                {stakeholder.replace(/([A-Z])/g, ' $1').trim()}
              </h4>
              <div className="space-y-2">
                {Object.entries(metrics).map(([metric, value]) => (
                  <div key={metric}>
                    <p className="text-xs text-gray-600 capitalize">
                      {metric.replace(/([A-Z])/g, ' $1').trim()}
                    </p>
                    <p className="text-sm font-semibold text-gray-900">
                      {typeof value === 'number' ? `${value}%` : value}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Key Insights Summary */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200 p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-4">Key Insights Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 mb-2">
              {analyticsData.predictiveInsights.next24h.riskLevel === 'critical' ? '🔴' : 
               analyticsData.predictiveInsights.next24h.riskLevel === 'high' ? '🟠' : 
               analyticsData.predictiveInsights.next24h.riskLevel === 'moderate' ? '🟡' : '🟢'}
            </div>
            <p className="text-sm font-medium text-blue-900">Current Risk Level</p>
            <p className="text-xs text-blue-700 capitalize">{analyticsData.predictiveInsights.next24h.riskLevel}</p>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 mb-2">
              {Math.max(...analyticsData.alertTrends.datasets[0].data)}
            </div>
            <p className="text-sm font-medium text-blue-900">Peak Daily Alerts</p>
            <p className="text-xs text-blue-700">Last {selectedTimeframe}</p>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 mb-2">
              {Math.round(analyticsData.stakeholderMetrics.disasterManagement.responseTime.split(' ')[0])} min
            </div>
            <p className="text-sm font-medium text-blue-900">Avg Response Time</p>
            <p className="text-xs text-blue-700">Disaster Management</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
