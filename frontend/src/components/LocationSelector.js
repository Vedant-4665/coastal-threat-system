import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const LocationSelector = ({ onLocationChange, currentLocation = "mumbai" }) => {
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(currentLocation);
  const [customLocation, setCustomLocation] = useState("");
  const [loading, setLoading] = useState(false);
  const [showCustomInput, setShowCustomInput] = useState(false);

  useEffect(() => {
    fetchLocations();
  }, []);

  const fetchLocations = async () => {
    try {
      setLoading(true);
      const response = await apiService.getAvailableLocations();
      if (response.locations) {
        setLocations(response.locations);
      }
    } catch (error) {
      console.error('Error fetching locations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLocationChange = (locationId) => {
    setSelectedLocation(locationId);
    setShowCustomInput(false);
    setCustomLocation("");
    onLocationChange(locationId);
  };

  const handleCustomLocation = () => {
    if (customLocation.trim()) {
      onLocationChange(customLocation.trim());
      setSelectedLocation("custom");
    }
  };

  const handleCoordinatesInput = () => {
    setShowCustomInput(true);
    setSelectedLocation("custom");
  };

  const popularCities = [
    { id: "mumbai", name: "Mumbai, India", flag: "🇮🇳" },
    { id: "miami", name: "Miami, USA", flag: "🇺🇸" },
    { id: "sydney", name: "Sydney, Australia", flag: "🇦🇺" },
    { id: "tokyo", name: "Tokyo, Japan", flag: "🇯🇵" },
    { id: "london", name: "London, UK", flag: "🇬🇧" },
    { id: "rio", name: "Rio de Janeiro, Brazil", flag: "🇧🇷" },
    { id: "cape_town", name: "Cape Town, South Africa", flag: "🇿🇦" },
    { id: "singapore", name: "Singapore", flag: "🇸🇬" },
    { id: "dubai", name: "Dubai, UAE", flag: "🇦🇪" },
    { id: "vancouver", name: "Vancouver, Canada", flag: "🇨🇦" }
  ];

  return (
    <div className="pro-card p-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
        🌍 Global Coastal Monitoring
      </h3>
      
      <div className="space-y-4">
        {/* Popular Cities Grid */}
        <div>
          <h4 className="font-medium text-gray-700 mb-3">Popular Coastal Cities</h4>
          <div className="location-grid">
            {popularCities.map((city) => (
              <button
                key={city.id}
                onClick={() => handleLocationChange(city.id)}
                className={`location-button ${
                  selectedLocation === city.id ? 'active' : ''
                }`}
              >
                <div className="text-2xl mb-1">{city.flag}</div>
                <div className="text-xs font-medium text-gray-800 leading-tight">
                  {city.name.split(',')[0]}
                </div>
                <div className="text-xs text-gray-500">
                  {city.name.split(',')[1]}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Custom Location Input */}
        <div className="border-t pt-4">
          <h4 className="font-medium text-gray-700 mb-3">Custom Location</h4>
          
          <div className="space-y-3">
            {/* City Name Input */}
            <div className="flex space-x-2">
              <input
                type="text"
                placeholder="Enter city name (e.g., San Francisco, Barcelona)"
                value={customLocation}
                onChange={(e) => setCustomLocation(e.target.value)}
                className="form-input"
                onKeyPress={(e) => e.key === 'Enter' && handleCustomLocation()}
              />
              <button
                onClick={handleCustomLocation}
                disabled={!customLocation.trim()}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Search
              </button>
            </div>

            {/* Coordinates Input */}
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Or use coordinates:</span>
              <button
                onClick={handleCoordinatesInput}
                className="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700"
              >
                📍 Enter Coordinates
              </button>
            </div>

            {/* Coordinates Input Fields */}
            {showCustomInput && (
              <div className="grid grid-cols-2 gap-2 p-3 bg-gray-50 rounded-lg">
                <div>
                  <label className="block text-xs text-gray-600 mb-1">Latitude</label>
                  <input
                    type="number"
                    step="any"
                    placeholder="e.g., 19.0760"
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs text-gray-600 mb-1">Longitude</label>
                  <input
                    type="number"
                    step="any"
                    placeholder="e.g., 72.8777"
                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                <div className="col-span-2">
                  <button
                    onClick={() => {
                      // Handle coordinates input
                      setShowCustomInput(false);
                    }}
                    className="w-full px-3 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700"
                  >
                    Use Coordinates
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Current Location Display */}
        <div className="border-t pt-4">
          <h4 className="font-medium text-gray-700 mb-2">Current Location</h4>
          <div className="flex items-center space-x-2 p-3 bg-blue-50 rounded-lg">
            <span className="text-blue-600">📍</span>
            <span className="font-medium text-blue-800">
              {selectedLocation === "custom" && customLocation 
                ? customLocation 
                : popularCities.find(city => city.id === selectedLocation)?.name || "Mumbai, India"
              }
            </span>
            <span className="text-sm text-blue-600">
              {selectedLocation === "custom" ? "(Custom)" : "(Predefined)"}
            </span>
          </div>
        </div>

        {/* Location Info */}
        <div className="text-xs text-gray-500 text-center">
          <p>🌊 Monitor coastal threats for any location worldwide</p>
          <p>📡 Real-time data from global monitoring networks</p>
          <p>🌍 Support for 190+ countries and territories</p>
        </div>
      </div>
    </div>
  );
};

export default LocationSelector;
