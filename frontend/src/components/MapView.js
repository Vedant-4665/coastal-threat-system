import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const MapView = ({ weatherData, tideData, alerts = [], onLocationClick, currentLocation = "mumbai" }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef([]);

  // Get coordinates for the current location
  const getLocationCoordinates = () => {
    const locations = {
      "mumbai": { lat: 19.0760, lon: 72.8777, name: "Mumbai, India" },
      "miami": { lat: 25.7617, lon: -80.1918, name: "Miami, USA" },
      "sydney": { lat: -33.8688, lon: 151.2093, name: "Sydney, Australia" },
      "tokyo": { lat: 35.6762, lon: 139.6503, name: "Tokyo, Japan" },
      "london": { lat: 51.5074, lon: -0.1278, name: "London, UK" },
      "rio": { lat: -22.9068, lon: -43.1729, name: "Rio de Janeiro, Brazil" },
      "cape_town": { lat: -33.9249, lon: 18.4241, name: "Cape Town, South Africa" },
      "singapore": { lat: 1.3521, lon: 103.8198, name: "Singapore" },
      "dubai": { lat: 25.2048, lon: 55.2708, name: "Dubai, UAE" },
      "vancouver": { lat: 49.2827, lon: -123.1207, name: "Vancouver, Canada" }
    };

    // Check if it's a custom location with coordinates
    if (currentLocation.includes(',')) {
      try {
        const [lat, lon] = currentLocation.split(',').map(Number);
        return { lat, lon, name: `Custom Location (${lat.toFixed(4)}, ${lon.toFixed(4)})` };
      } catch (e) {
        return locations.mumbai; // fallback
      }
    }

    return locations[currentLocation] || locations.mumbai;
  };

  useEffect(() => {
    if (!mapRef.current) return;

    const location = getLocationCoordinates();

    // Initialize map
    if (!mapInstanceRef.current) {
      const map = L.map(mapRef.current).setView([location.lat, location.lon], 10);
      
      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map);

      mapInstanceRef.current = map;
    } else {
      // Update map view for existing map
      const map = mapInstanceRef.current;
      map.setView([location.lat, location.lon], 10);
    }

    const map = mapInstanceRef.current;

    // Clear existing markers and overlays
    markersRef.current.forEach(marker => map.removeLayer(marker));
    markersRef.current = [];

    // Add coastal boundary based on location
    const coastalBoundary = L.circle([location.lat, location.lon], {
      color: '#0d9488',
      weight: 2,
      fillColor: '#0d9488',
      fillOpacity: 0.1,
      radius: 50000 // 50km radius
    }).addTo(map);

    // Add location title
    const locationTitle = L.divIcon({
      className: 'location-title',
      html: `
        <div class="bg-white bg-opacity-90 px-3 py-2 rounded-lg shadow-lg border border-gray-200">
          <h3 class="font-bold text-lg text-gray-800">${location.name}</h3>
          <p class="text-sm text-gray-600">Coastal Monitoring Station</p>
        </div>
      `,
      iconSize: [200, 60],
      iconAnchor: [100, 0]
    });

    const titleMarker = L.marker([location.lat + 0.05, location.lon], { icon: locationTitle })
      .addTo(map);
    markersRef.current.push(titleMarker);

    // Add weather station marker
    if (weatherData) {
      const [lat, lon] = weatherData.location.split(',').map(Number);
      
      const weatherIcon = L.divIcon({
        className: 'weather-marker',
        html: `
          <div class="bg-blue-500 text-white rounded-full p-2 text-xs font-bold shadow-lg">
            🌤️
          </div>
        `,
        iconSize: [40, 40],
        iconAnchor: [20, 20]
      });

      const weatherMarker = L.marker([lat, lon], { icon: weatherIcon })
        .addTo(map)
        .bindPopup(`
          <div class="p-2">
            <h3 class="font-bold text-lg">Weather Station</h3>
            <p><strong>Temperature:</strong> ${weatherData.temperature}°C</p>
            <p><strong>Wind:</strong> ${weatherData.wind_speed} m/s</p>
            <p><strong>Pressure:</strong> ${weatherData.pressure} hPa</p>
            <p><strong>Humidity:</strong> ${weatherData.humidity}%</p>
          </div>
        `);

      markersRef.current.push(weatherMarker);
    }

    // Add tide station marker
    if (tideData) {
      const [lat, lon] = tideData.location.split(',').map(Number);
      
      const tideIcon = L.divIcon({
        className: 'tide-marker',
        html: `
          <div class="bg-teal-500 text-white rounded-full p-2 text-xs font-bold shadow-lg">
            🌊
          </div>
        `,
        iconSize: [40, 40],
        iconAnchor: [20, 20]
      });

      const tideMarker = L.marker([lat, lon], { icon: tideIcon })
        .addTo(map)
        .bindPopup(`
          <div class="p-2">
            <h3 class="font-bold text-lg">Tide Station</h3>
            <p><strong>Height:</strong> ${tideData.tide_height} m</p>
            <p><strong>Type:</strong> ${tideData.tide_type}</p>
            <p><strong>Source:</strong> ${tideData.source}</p>
          </div>
        `);

      markersRef.current.push(tideMarker);
    }

    // Add alert markers
    if (alerts && Array.isArray(alerts)) {
      alerts.forEach(alert => {
        const [lat, lon] = alert.location.split(',').map(Number);
        
        let alertColor, alertIcon;
        switch (alert.severity) {
          case 'critical':
            alertColor = 'bg-red-600';
            alertIcon = '🚨';
            break;
          case 'high':
            alertColor = 'bg-orange-500';
            alertIcon = '⚠️';
            break;
          case 'medium':
            alertColor = 'bg-yellow-500';
            alertIcon = '⚡';
            break;
          default:
            alertColor = 'bg-green-500';
            alertIcon = 'ℹ️';
        }

        const alertMarkerIcon = L.divIcon({
          className: 'alert-marker',
          html: `
            <div class="${alertColor} text-white rounded-full p-2 text-xs font-bold shadow-lg animate-pulse">
              ${alertIcon}
            </div>
          `,
          iconSize: [40, 40],
          iconAnchor: [20, 20]
        });

        const alertMarker = L.marker([lat, lon], { icon: alertMarkerIcon })
          .addTo(map)
          .bindPopup(`
            <div class="p-3 max-w-xs">
              <h3 class="font-bold text-lg text-red-600">${alert.alert_type?.toUpperCase() || 'ALERT'}</h3>
              <p class="text-sm mb-2"><strong>Severity:</strong> 
                <span class="px-2 py-1 rounded text-xs font-bold ${alertColor} text-white">
                  ${alert.severity}
                </span>
              </p>
              <p class="text-sm mb-2">${alert.description || 'No description available'}</p>
              <p class="text-xs text-gray-600">
                <strong>Triggered:</strong> ${alert.triggered_by || 'Unknown'}<br/>
                <strong>Time:</strong> ${new Date(alert.timestamp).toLocaleString()}
              </p>
            </div>
          `);

        markersRef.current.push(alertMarker);

        // Add risk zone overlay for high/critical alerts
        if (alert.severity === 'high' || alert.severity === 'critical') {
          const riskZone = L.circle([lat, lon], {
            color: alert.severity === 'critical' ? '#dc2626' : '#ea580c',
            fillColor: alert.severity === 'critical' ? '#dc2626' : '#ea580c',
            fillOpacity: 0.2,
            radius: 5000 // 5km radius
          }).addTo(map);

          markersRef.current.push(riskZone);
        }
      });
    }

    // Add click handler for map
    map.on('click', (e) => {
      if (onLocationClick) {
        onLocationClick(e.latlng);
      }
    });

  }, [weatherData, tideData, alerts, onLocationClick, currentLocation]);

  return (
    <div className="relative h-full w-full">
      <div className="absolute top-4 left-4 z-10 bg-white rounded-lg shadow-lg p-3">
        <h3 className="font-bold text-lg text-gray-800 mb-2">Map Legend</h3>
        <div className="space-y-2 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-blue-500 rounded-full"></div>
            <span>Weather Station</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-teal-500 rounded-full"></div>
            <span>Tide Station</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-red-500 rounded-full"></div>
            <span>Alert Zones</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-green-500 rounded-full opacity-20"></div>
            <span>Coastal Boundary</span>
          </div>
        </div>
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="text-xs text-gray-600">
            <strong>Monitoring:</strong> {getLocationCoordinates().name}
          </div>
        </div>
      </div>
      
      <div 
        ref={mapRef} 
        className="h-full w-full rounded-lg overflow-hidden"
        style={{ minHeight: '400px' }}
      />
    </div>
  );
};

export default MapView;
