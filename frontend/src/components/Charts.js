import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

const Charts = ({ weatherData, tideData, alerts }) => {
  const [chartData, setChartData] = useState(null);
  const [selectedChart, setSelectedChart] = useState('tide');

  useEffect(() => {
    if (!weatherData || !tideData) return;

    // Generate mock historical data for demonstration
    const generateHistoricalData = () => {
      const now = new Date();
      const data = [];
      
      for (let i = 23; i >= 0; i--) {
        const time = new Date(now.getTime() - i * 60 * 60 * 1000);
        const baseTide = 1.5 + Math.sin((i / 12) * Math.PI) * 1.0; // Simulate tide cycle
        const baseWind = 15 + Math.sin((i / 24) * Math.PI) * 10; // Simulate wind variation
        
        data.push({
          time,
          tide: baseTide + (Math.random() - 0.5) * 0.3,
          wind: Math.max(0, baseWind + (Math.random() - 0.5) * 5),
          pressure: 1013 + (Math.random() - 0.5) * 20
        });
      }
      
      return data;
    };

    const historicalData = generateHistoricalData();
    
    // Add current data
    const currentTime = new Date();
    historicalData.push({
      time: currentTime,
      tide: tideData.tide_height,
      wind: weatherData.wind_speed,
      pressure: weatherData.pressure
    });

    setChartData(historicalData);
  }, [weatherData, tideData]);

  const getTideChartData = () => {
    if (!chartData) return null;

    const anomalyPoints = alerts
      .filter(alert => alert.alert_type === 'high_tide' || alert.alert_type === 'storm_surge_risk')
      .map(alert => {
        const [lat, lon] = alert.location.split(',').map(Number);
        return { x: new Date(alert.timestamp), y: 2.5, r: 8 }; // Mark anomaly points
      });

    return {
      labels: chartData.map(d => d.time),
      datasets: [
        {
          label: 'Tide Height (m)',
          data: chartData.map(d => ({ x: d.time, y: d.tide })),
          borderColor: '#0d9488',
          backgroundColor: 'rgba(13, 148, 136, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'High Tide Threshold',
          data: chartData.map(d => ({ x: d.time, y: 2.5 })),
          borderColor: '#dc2626',
          backgroundColor: 'rgba(220, 38, 38, 0.1)',
          borderWidth: 2,
          borderDash: [5, 5],
          fill: false,
          pointRadius: 0,
        },
        ...(anomalyPoints.length > 0 ? [{
          label: 'Anomaly Detected',
          data: anomalyPoints,
          backgroundColor: '#dc2626',
          pointRadius: 8,
          pointHoverRadius: 10,
          showLine: false,
        }] : [])
      ]
    };
  };

  const getWindChartData = () => {
    if (!chartData) return null;

    const anomalyPoints = alerts
      .filter(alert => alert.alert_type === 'high_wind')
      .map(alert => {
        return { x: new Date(alert.timestamp), y: 25, r: 8 }; // Mark anomaly points
      });

    return {
      labels: chartData.map(d => d.time),
      datasets: [
        {
          label: 'Wind Speed (m/s)',
          data: chartData.map(d => ({ x: d.time, y: d.wind })),
          borderColor: '#0891b2',
          backgroundColor: 'rgba(8, 145, 178, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'High Wind Threshold',
          data: chartData.map(d => ({ x: d.time, y: 25 })),
          borderColor: '#dc2626',
          backgroundColor: 'rgba(220, 38, 38, 0.1)',
          borderWidth: 2,
          borderDash: [5, 5],
          fill: false,
          pointRadius: 0,
        },
        ...(anomalyPoints.length > 0 ? [{
          label: 'Anomaly Detected',
          data: anomalyPoints,
          backgroundColor: '#dc2626',
          pointRadius: 8,
          pointHoverRadius: 10,
          showLine: false,
        }] : [])
      ]
    };
  };

  const getPressureChartData = () => {
    if (!chartData) return null;

    const anomalyPoints = alerts
      .filter(alert => alert.alert_type === 'low_pressure')
      .map(alert => {
        return { x: new Date(alert.timestamp), y: 1000, r: 8 }; // Mark anomaly points
      });

    return {
      labels: chartData.map(d => d.time),
      datasets: [
        {
          label: 'Atmospheric Pressure (hPa)',
          data: chartData.map(d => ({ x: d.time, y: d.pressure })),
          borderColor: '#7c3aed',
          backgroundColor: 'rgba(124, 58, 237, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'Low Pressure Threshold',
          data: chartData.map(d => ({ x: d.time, y: 1000 })),
          borderColor: '#dc2626',
          backgroundColor: 'rgba(220, 38, 38, 0.1)',
          borderWidth: 2,
          borderDash: [5, 5],
          fill: false,
          pointRadius: 0,
        },
        ...(anomalyPoints.length > 0 ? [{
          label: 'Anomaly Detected',
          data: anomalyPoints,
          backgroundColor: '#dc2626',
          pointRadius: 8,
          pointHoverRadius: 10,
          showLine: false,
        }] : [])
      ]
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            family: 'Inter',
            size: 12,
            weight: '600'
          }
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: '#3b82f6',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
        padding: 12,
        titleFont: {
          family: 'Inter',
          size: 14,
          weight: '600'
        },
        bodyFont: {
          family: 'Inter',
          size: 12
        }
      }
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'hour',
          displayFormats: {
            hour: 'HH:mm'
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
          drawBorder: false
        },
        ticks: {
          font: {
            family: 'Inter',
            size: 11
          },
          color: '#6b7280'
        }
      },
      y: {
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
          drawBorder: false
        },
        ticks: {
          font: {
            family: 'Inter',
            size: 11
          },
          color: '#6b7280'
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    },
    elements: {
      point: {
        hoverRadius: 8,
        hoverBorderWidth: 2,
        hoverBorderColor: '#ffffff'
      }
    }
  };

  const getCurrentChartData = () => {
    switch (selectedChart) {
      case 'tide':
        return getTideChartData();
      case 'wind':
        return getWindChartData();
      case 'pressure':
        return getPressureChartData();
      default:
        return getTideChartData();
    }
  };

  const getChartTitle = () => {
    switch (selectedChart) {
      case 'tide':
        return 'Tide Height Trends & Anomalies';
      case 'wind':
        return 'Wind Speed Patterns & Alerts';
      case 'pressure':
        return 'Atmospheric Pressure Analysis';
      default:
        return 'Coastal Data Analysis';
    }
  };

  if (!chartData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-500">Loading chart data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Chart Type Selector */}
      <div className="flex flex-wrap gap-2">
        {[
          { key: 'tide', label: '🌊 Tide Analysis', icon: '🌊' },
          { key: 'wind', label: '💨 Wind Patterns', icon: '💨' },
          { key: 'pressure', label: '🌫️ Pressure Trends', icon: '🌫️' }
        ].map((chart) => (
          <button
            key={chart.key}
            onClick={() => setSelectedChart(chart.key)}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 ${
              selectedChart === chart.key
                ? 'bg-blue-600 text-white shadow-lg transform scale-105'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:scale-105'
            }`}
          >
            <span>{chart.icon}</span>
            <span>{chart.label}</span>
          </button>
        ))}
      </div>

      {/* Chart Container */}
      <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-xl p-6 border border-white/20">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">{getChartTitle()}</h3>
          <p className="text-sm text-gray-600">
            Real-time monitoring with AI-powered anomaly detection
          </p>
        </div>
        
        <div className="h-80">
          <Line data={getCurrentChartData()} options={chartOptions} />
        </div>
      </div>

      {/* Chart Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-blue-600">📊</span>
            <h4 className="font-semibold text-blue-800">Data Points</h4>
          </div>
          <p className="text-2xl font-bold text-blue-600">{chartData.length}</p>
          <p className="text-sm text-blue-600">24-hour monitoring</p>
        </div>

        <div className="bg-green-50 rounded-lg p-4 border border-green-200">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-green-600">🤖</span>
            <h4 className="font-semibold text-green-800">ML Analysis</h4>
          </div>
          <p className="text-2xl font-bold text-green-600">{alerts.length}</p>
          <p className="text-sm text-green-600">anomalies detected</p>
        </div>

        <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-purple-600">⚡</span>
            <h4 className="font-semibold text-purple-800">Real-time</h4>
          </div>
          <p className="text-2xl font-bold text-purple-600">Live</p>
          <p className="text-sm text-purple-600">continuous monitoring</p>
        </div>
      </div>
    </div>
  );
};

export default Charts;
