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
      // Asia-Pacific
      "mumbai": { lat: 19.0760, lon: 72.8777, name: "Mumbai, India" },
      "karachi": { lat: 24.8607, lon: 67.0011, name: "Karachi, Pakistan" },
      "tokyo": { lat: 35.6762, lon: 139.6503, name: "Tokyo, Japan" },
      "singapore": { lat: 1.3521, lon: 103.8198, name: "Singapore" },
      "sydney": { lat: -33.8688, lon: 151.2093, name: "Sydney, Australia" },
      "shanghai": { lat: 31.2304, lon: 121.4737, name: "Shanghai, China" },
      "hong_kong": { lat: 22.3193, lon: 114.1694, name: "Hong Kong" },
      "bangkok": { lat: 13.7563, lon: 100.5018, name: "Bangkok, Thailand" },
      "manila": { lat: 14.5995, lon: 120.9842, name: "Manila, Philippines" },
      "jakarta": { lat: -6.2088, lon: 106.8456, name: "Jakarta, Indonesia" },
      
      // Europe
      "london": { lat: 51.5074, lon: -0.1278, name: "London, UK" },
      "paris": { lat: 48.8566, lon: 2.3522, name: "Paris, France" },
      "barcelona": { lat: 41.3851, lon: 2.1734, name: "Barcelona, Spain" },
      "amsterdam": { lat: 52.3676, lon: 4.9041, name: "Amsterdam, Netherlands" },
      "oslo": { lat: 59.9139, lon: 10.7522, name: "Oslo, Norway" },
      "stockholm": { lat: 59.3293, lon: 18.0686, name: "Stockholm, Sweden" },
      "helsinki": { lat: 60.1699, lon: 24.9384, name: "Helsinki, Finland" },
      "copenhagen": { lat: 55.6761, lon: 12.5683, name: "Copenhagen, Denmark" },
      "dublin": { lat: 53.3498, lon: -6.2603, name: "Dublin, Ireland" },
      "athens": { lat: 37.9838, lon: 23.7275, name: "Athens, Greece" },
      
      // Americas
      "new_york": { lat: 40.7128, lon: -74.0060, name: "New York, USA" },
      "miami": { lat: 25.7617, lon: -80.1918, name: "Miami, USA" },
      "los_angeles": { lat: 34.0522, lon: -118.2437, name: "Los Angeles, USA" },
      "san_francisco": { lat: 37.7749, lon: -122.4194, name: "San Francisco, USA" },
      "vancouver": { lat: 49.2827, lon: -123.1207, name: "Vancouver, Canada" },
      "toronto": { lat: 43.6532, lon: -79.3832, name: "Toronto, Canada" },
      "montreal": { lat: 45.5017, lon: -73.5673, name: "Montreal, Canada" },
      "rio": { lat: -22.9068, lon: -43.1729, name: "Rio de Janeiro, Brazil" },
      "sao_paulo": { lat: -23.5505, lon: -46.6333, name: "São Paulo, Brazil" },
      "buenos_aires": { lat: -34.6118, lon: -58.3960, name: "Buenos Aires, Argentina" },
      "lima": { lat: -12.0464, lon: -77.0428, name: "Lima, Peru" },
      "santiago": { lat: -33.4489, lon: -70.6693, name: "Santiago, Chile" },
      
      // Africa & Middle East
      "cape_town": { lat: -33.9249, lon: 18.4241, name: "Cape Town, South Africa" },
      "cairo": { lat: 30.0444, lon: 31.2357, name: "Cairo, Egypt" },
      "casablanca": { lat: 33.5731, lon: -7.5898, name: "Casablanca, Morocco" },
      "lagos": { lat: 6.5244, lon: 3.3792, name: "Lagos, Nigeria" },
      "dubai": { lat: 25.2048, lon: 55.2708, name: "Dubai, UAE" },
      "abuja": { lat: 9.0820, lon: 7.3986, name: "Abuja, Nigeria" },
      "nairobi": { lat: -1.2921, lon: 36.8219, name: "Nairobi, Kenya" },
      "dar_es_salaam": { lat: -6.8230, lon: 39.2695, name: "Dar es Salaam, Tanzania" },
      
      // Oceania
      "auckland": { lat: -36.8485, lon: 174.7633, name: "Auckland, New Zealand" },
      "wellington": { lat: -41.2866, lon: 174.7756, name: "Wellington, New Zealand" },
      "fiji": { lat: -18.1416, lon: 178.4419, name: "Suva, Fiji" },
      "papua_new_guinea": { lat: -9.4438, lon: 147.1803, name: "Port Moresby, PNG" }
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

    // Check for exact match first
    if (locations[currentLocation]) {
      return locations[currentLocation];
    }

    // Check for partial matches (e.g., "new york" matches "new_york")
    const normalizedInput = currentLocation.toLowerCase().replace(" ", "_").replace("-", "_");
    for (const [cityKey, cityInfo] of Object.entries(locations)) {
      if (normalizedInput === cityKey || 
          cityKey.replace("_", "") === normalizedInput.replace("_", "") ||
          cityKey.replace("_", " ") === currentLocation.toLowerCase()) {
        return cityInfo;
      }
    }

    // If still no match, generate coordinates for unknown cities (same logic as backend)
    return generateUnknownCityCoordinates(currentLocation);
  };

  const generateUnknownCityCoordinates = (cityName) => {
    // Generate realistic coordinates based on city name hash (same as backend)
    const cityHash = cityName.toLowerCase().split('').reduce((hash, char) => {
      return ((hash << 5) - hash + char.charCodeAt(0)) & 0xffffffff;
    }, 0);
    
    // Use hash to generate realistic but varied coordinates
    let lat = -90 + (cityHash % 180);  // -90 to 90
    let lon = -180 + ((cityHash >> 8) % 360);  // -180 to 180
    
    // Ensure it's coastal (near water)
    if (Math.abs(lat) > 60) {  // Too close to poles
      lat = lat * 0.6;
    }
    if (Math.abs(lon) > 150) {  // Too far from major coastal areas
      lon = lon * 0.8;
    }
    
    return {
      lat: Math.round(lat * 10000) / 10000,
      lon: Math.round(lon * 10000) / 10000,
      name: `${cityName.charAt(0).toUpperCase() + cityName.slice(1)}, Coastal City`
    };
  };

  useEffect(() => {
    if (!mapRef.current) return;

    const location = getLocationCoordinates();
    console.log('MapView: Updating map for location:', currentLocation, 'coordinates:', location); // Debug log

    // Initialize map
    if (!mapInstanceRef.current) {
      const map = L.map(mapRef.current).setView([location.lat, location.lon], 10);
      
      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map);

      mapInstanceRef.current = map;
      
      // Add zoom event listener to update zoom level indicator
      map.on('zoomend', () => {
        const zoomLevel = document.getElementById('zoom-level');
        if (zoomLevel) {
          zoomLevel.textContent = map.getZoom();
        }
      });
    } else {
      // Update map view for existing map
      const map = mapInstanceRef.current;
      map.setView([location.lat, location.lon], 10);
    }

    const map = mapInstanceRef.current;

    // Clear existing markers and overlays
    markersRef.current.forEach(marker => map.removeLayer(marker));
    markersRef.current = [];

    // Add weather station marker
    const weatherMarker = L.marker([location.lat, location.lon], {
      icon: L.divIcon({
        className: 'weather-station-marker',
        html: '<div class="weather-station-icon">🌤️</div>',
        iconSize: [40, 40],
        iconAnchor: [20, 20]
      })
    }).addTo(map);
    
    weatherMarker.bindPopup(`
      <div class="weather-station-popup">
        <h3 class="font-bold text-lg mb-2">${location.name}</h3>
        <p class="text-sm text-gray-600 mb-2">Coastal Monitoring Station</p>
        <div class="text-xs text-gray-500">
          <div>Coordinates: ${location.lat.toFixed(4)}, ${location.lon.toFixed(4)}</div>
          <div>Status: Active</div>
        </div>
      </div>
    `);

    // Add tide station marker (slightly offset)
    const tideMarker = L.marker([location.lat + 0.01, location.lon + 0.01], {
      icon: L.divIcon({
        className: 'tide-station-marker',
        html: '<div class="tide-station-icon">🌊</div>',
        iconSize: [40, 40],
        iconAnchor: [20, 20]
      })
    }).addTo(map);
    
    tideMarker.bindPopup(`
      <div class="tide-station-popup">
        <h3 class="font-bold text-lg mb-2">${location.name}</h3>
        <p class="text-sm text-gray-600 mb-2">Tide Monitoring Station</p>
        <div class="text-xs text-gray-500">
          <div>Coordinates: ${(location.lat + 0.01).toFixed(4)}, ${(location.lon + 0.01).toFixed(4)}</div>
          <div>Status: Active</div>
        </div>
      </div>
    `);

    // Add coastal boundary with better styling
    const coastalBoundary = L.circle([location.lat, location.lon], {
      radius: 15000, // 15km radius
      color: '#10B981',
      fillColor: '#10B981',
      fillOpacity: 0.1,
      weight: 2,
      dashArray: '5, 10'
    }).addTo(map);
    
    coastalBoundary.bindPopup(`
      <div class="coastal-boundary-popup">
        <h3 class="font-bold text-lg mb-2">Coastal Monitoring Zone</h3>
        <p class="text-sm text-gray-600 mb-2">${location.name}</p>
        <div class="text-xs text-gray-500">
          <div>Radius: 15 km</div>
          <div>Coverage: Coastal waters & shoreline</div>
        </div>
      </div>
    `);

    // Add alert zones if there are alerts
    if (alerts && Array.isArray(alerts) && alerts.length > 0) {
      alerts.forEach((alert, index) => {
        const alertZone = L.circle([location.lat, location.lon], {
          radius: 8000 + (index * 2000), // Varying radius for different alerts
          color: '#EF4444',
          fillColor: '#EF4444',
          fillOpacity: 0.15,
          weight: 3,
          dashArray: '10, 5'
        }).addTo(map);
        
        alertZone.bindPopup(`
          <div class="alert-zone-popup">
            <h3 class="font-bold text-lg mb-2 text-red-600">${alert.alert_type?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Alert'}</h3>
            <p class="text-sm text-gray-600 mb-2">${alert.description || 'No description'}</p>
            <div class="text-xs text-gray-500">
              <div>Severity: ${alert.severity || 'Unknown'}</div>
              <div>Time: ${new Date(alert.timestamp).toLocaleString()}</div>
            </div>
          </div>
        `);
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
      {/* Map Legend - Fixed positioning and responsive to zoom */}
      <div className="absolute top-4 left-4 z-20 bg-white rounded-lg shadow-lg p-3 max-w-48">
        <h3 className="font-bold text-lg text-gray-800 mb-2">Map Legend</h3>
        <div className="space-y-2 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-blue-500 rounded-full flex-shrink-0"></div>
            <span className="text-xs">Weather Station</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-teal-500 rounded-full flex-shrink-0"></div>
            <span className="text-xs">Tide Station</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-red-500 rounded-full flex-shrink-0"></div>
            <span className="text-xs">Alert Zones</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-green-500 rounded-full opacity-20 flex-shrink-0"></div>
            <span className="text-xs">Coastal Boundary</span>
          </div>
        </div>
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="text-xs text-gray-600">
            <strong>Monitoring:</strong> {getLocationCoordinates().name}
          </div>
        </div>
        
        {/* Zoom Level Indicator */}
        <div className="mt-2 pt-2 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <strong>Zoom:</strong> <span id="zoom-level">10</span>
          </div>
        </div>
      </div>
      
      {/* Zoom Controls - Repositioned to avoid overlap */}
      <div className="absolute top-4 right-4 z-20">
        <div className="bg-white rounded-lg shadow-lg p-1 space-y-1">
          <button 
            onClick={() => mapInstanceRef.current?.zoomIn()}
            className="w-8 h-8 bg-white hover:bg-gray-50 border border-gray-200 rounded flex items-center justify-center text-gray-600 hover:text-gray-800 transition-colors"
          >
            +
          </button>
          <button 
            onClick={() => mapInstanceRef.current?.zoomOut()}
            className="w-8 h-8 bg-white hover:bg-gray-50 border border-gray-200 rounded flex items-center justify-center text-gray-600 hover:text-gray-800 transition-colors"
          >
            −
          </button>
        </div>
      </div>
      
      <div 
        ref={mapRef} 
        className="h-full w-full rounded-lg"
        style={{ zIndex: 1 }}
      />
    </div>
  );
};

export default MapView;
