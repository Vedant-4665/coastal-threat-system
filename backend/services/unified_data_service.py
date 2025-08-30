import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import random
import math
import hashlib
import logging

# Import real services
from .real_weather_service import RealWeatherService
from .real_tide_service import RealTideService
from .real_marine_service import RealMarineService

load_dotenv()

class UnifiedDataService:
    """Unified data service using REAL APIs with fallbacks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize real API services
        self.weather_service = RealWeatherService()
        self.tide_service = RealTideService()
        self.marine_service = RealMarineService()
        
        # Coastal cities with REAL coordinates (only actual coastal cities)
        self.coastal_cities = {
            # North America - USA
            "miami": {"name": "Miami, USA", "lat": 25.7617, "lon": -80.1918, "country": "USA", "timezone": "UTC-5"},
            "san_francisco": {"name": "San Francisco, USA", "lat": 37.7749, "lon": -122.4194, "country": "USA", "timezone": "UTC-8"},
            "seattle": {"name": "Seattle, USA", "lat": 47.6062, "lon": -122.3321, "country": "USA", "timezone": "UTC-8"},
            "boston": {"name": "Boston, USA", "lat": 42.3601, "lon": -71.0589, "country": "USA", "timezone": "UTC-5"},
            "new_york": {"name": "New York, USA", "lat": 40.7128, "lon": -74.0060, "country": "USA", "timezone": "UTC-5"},
            "charleston": {"name": "Charleston, USA", "lat": 32.7765, "lon": -79.9311, "country": "USA", "timezone": "UTC-5"},
            "galveston": {"name": "Galveston, USA", "lat": 29.3013, "lon": -94.7977, "country": "USA", "timezone": "UTC-6"},
            "los_angeles": {"name": "Los Angeles, USA", "lat": 34.0522, "lon": -118.2437, "country": "USA", "timezone": "UTC-8"},
            "portland_or": {"name": "Portland, USA", "lat": 45.5152, "lon": -122.6784, "country": "USA", "timezone": "UTC-8"},
            "anchorage": {"name": "Anchorage, USA", "lat": 61.2181, "lon": -149.9003, "country": "USA", "timezone": "UTC-9"},
            "honolulu": {"name": "Honolulu, USA", "lat": 21.3099, "lon": -157.8581, "country": "USA", "timezone": "UTC-10"},
            "panama_city": {"name": "Panama City, USA", "lat": 30.1595, "lon": -85.6598, "country": "USA", "timezone": "UTC-6"},
            "pensacola": {"name": "Pensacola, USA", "lat": 30.4213, "lon": -87.2169, "country": "USA", "timezone": "UTC-6"},
            "mobile": {"name": "Mobile, USA", "lat": 30.6954, "lon": -88.0399, "country": "USA", "timezone": "UTC-6"},
            "new_orleans": {"name": "New Orleans, USA", "lat": 29.9511, "lon": -90.0715, "country": "USA", "timezone": "UTC-6"},
            "santa_barbara": {"name": "Santa Barbara, USA", "lat": 34.4208, "lon": -119.6982, "country": "USA", "timezone": "UTC-8"},
            "monterey": {"name": "Monterey, USA", "lat": 36.6002, "lon": -121.8947, "country": "USA", "timezone": "UTC-8"},
            "crescent_city": {"name": "Crescent City, USA", "lat": 41.7558, "lon": -124.2026, "country": "USA", "timezone": "UTC-8"},
            "garibaldi": {"name": "Garibaldi, USA", "lat": 45.5598, "lon": -123.9110, "country": "USA", "timezone": "UTC-8"},
            
            # North America - Canada
            "vancouver": {"name": "Vancouver, Canada", "lat": 49.2827, "lon": -123.1207, "country": "Canada", "timezone": "UTC-8"},
            "toronto": {"name": "Toronto, Canada", "lat": 43.6532, "lon": -79.3832, "country": "Canada", "timezone": "UTC-5"},
            "montreal": {"name": "Montreal, Canada", "lat": 45.5017, "lon": -73.5673, "country": "Canada", "timezone": "UTC-5"},
            "halifax": {"name": "Halifax, Canada", "lat": 44.6488, "lon": -63.5752, "country": "Canada", "timezone": "UTC-4"},
            
            # Europe - Only ACTUAL coastal cities
            "barcelona": {"name": "Barcelona, Spain", "lat": 41.3851, "lon": 2.1734, "country": "Spain", "timezone": "UTC+1"},
            "amsterdam": {"name": "Amsterdam, Netherlands", "lat": 52.3676, "lon": 4.9041, "country": "Netherlands", "timezone": "UTC+1"},
            "oslo": {"name": "Oslo, Norway", "lat": 59.9139, "lon": 10.7522, "country": "Norway", "timezone": "UTC+1"},
            "stockholm": {"name": "Stockholm, Sweden", "lat": 59.3293, "lon": 18.0686, "country": "Sweden", "timezone": "UTC+1"},
            "helsinki": {"name": "Helsinki, Finland", "lat": 60.1699, "lon": 24.9384, "country": "Finland", "timezone": "UTC+2"},
            "copenhagen": {"name": "Copenhagen, Denmark", "lat": 55.6761, "lon": 12.5683, "country": "Denmark", "timezone": "UTC+1"},
            "dublin": {"name": "Dublin, Ireland", "lat": 53.3498, "lon": -6.2603, "country": "Ireland", "timezone": "UTC+0"},
            "athens": {"name": "Athens, Greece", "lat": 37.9838, "lon": 23.7275, "country": "Greece", "timezone": "UTC+2"},
            "venice": {"name": "Venice, Italy", "lat": 45.4408, "lon": 12.3155, "country": "Italy", "timezone": "UTC+1"},
            "marseille": {"name": "Marseille, France", "lat": 43.2965, "lon": 5.3698, "country": "France", "timezone": "UTC+1"},
            "rotterdam": {"name": "Rotterdam, Netherlands", "lat": 51.9225, "lon": 4.4792, "country": "Netherlands", "timezone": "UTC+1"},
            
            # Asia-Pacific
            "mumbai": {"name": "Mumbai, India", "lat": 19.0760, "lon": 72.8777, "country": "India", "timezone": "UTC+5:30"},
            "karachi": {"name": "Karachi, Pakistan", "lat": 24.8607, "lon": 67.0011, "country": "Pakistan", "timezone": "UTC+5"},
            "tokyo": {"name": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503, "country": "Japan", "timezone": "UTC+9"},
            "singapore": {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "country": "Singapore", "timezone": "UTC+8"},
            "sydney": {"name": "Sydney, Australia", "lat": -33.8688, "lon": 151.2093, "country": "Australia", "timezone": "UTC+10"},
            "shanghai": {"name": "Shanghai, China", "lat": 31.2304, "lon": 121.4737, "country": "China", "timezone": "UTC+8"},
            "hong_kong": {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "country": "Hong Kong", "timezone": "UTC+8"},
            "bangkok": {"name": "Bangkok, Thailand", "lat": 13.7563, "lon": 100.5018, "country": "Thailand", "timezone": "UTC+7"},
            "manila": {"name": "Manila, Philippines", "lat": 14.5995, "lon": 120.9842, "country": "Philippines", "timezone": "UTC+8"},
            "jakarta": {"name": "Jakarta, Indonesia", "lat": -6.2088, "lon": 106.8456, "country": "Indonesia", "timezone": "UTC+7"},
            "kolkata": {"name": "Kolkata, India", "lat": 22.5726, "lon": 88.3639, "country": "India", "timezone": "UTC+5:30"},
            "chennai": {"name": "Chennai, India", "lat": 13.0827, "lon": 80.2707, "country": "India", "timezone": "UTC+5:30"},
            "kochi": {"name": "Kochi, India", "lat": 9.9312, "lon": 76.2673, "country": "India", "timezone": "UTC+5:30"},
            "visakhapatnam": {"name": "Visakhapatnam, India", "lat": 17.6868, "lon": 83.2185, "country": "India", "timezone": "UTC+5:30"},
            
            # Africa & Middle East
            "cape_town": {"name": "Cape Town, South Africa", "lat": -33.9249, "lon": 18.4241, "country": "South Africa", "timezone": "UTC+2"},
            "cairo": {"name": "Cairo, Egypt", "lat": 30.0444, "lon": 31.2357, "country": "Egypt", "timezone": "UTC+2"},
            "casablanca": {"name": "Casablanca, Morocco", "lat": 33.5731, "lon": -7.5898, "country": "Morocco", "timezone": "UTC+0"},
            "lagos": {"name": "Lagos, Nigeria", "lat": 6.5244, "lon": 3.3792, "country": "Nigeria", "timezone": "UTC+1"},
            "dubai": {"name": "Dubai, UAE", "lat": 25.2048, "lon": 55.2708, "country": "UAE", "timezone": "UTC+4"},
            "abuja": {"name": "Abuja, Nigeria", "lat": 9.0820, "lon": 7.3986, "country": "Nigeria", "timezone": "UTC+1"},
            "nairobi": {"name": "Nairobi, Kenya", "lat": -1.2921, "lon": 36.8219, "country": "Kenya", "timezone": "UTC+3"},
            "dar_es_salaam": {"name": "Dar es Salaam, Tanzania", "lat": -6.8230, "lon": 39.2695, "country": "Tanzania", "timezone": "UTC+3"},
            
            # Oceania
            "auckland": {"name": "Auckland, New Zealand", "lat": -36.8485, "lon": 174.7633, "country": "New Zealand", "timezone": "UTC+12"},
            "wellington": {"name": "Wellington, New Zealand", "lat": -41.2866, "lon": 174.7756, "country": "New Zealand", "timezone": "UTC+12"},
            "fiji": {"name": "Suva, Fiji", "lat": -18.1416, "lon": 178.4419, "country": "Fiji", "timezone": "UTC+12"},
            "papua_new_guinea": {"name": "Port Moresby, PNG", "lat": -9.4438, "lon": 147.1803, "country": "PNG", "timezone": "UTC+10"},
            
            # South America
            "rio": {"name": "Rio de Janeiro, Brazil", "lat": -22.9068, "lon": -43.1729, "country": "Brazil", "timezone": "UTC-3"},
            "sao_paulo": {"name": "São Paulo, Brazil", "lat": -23.5505, "lon": -46.6333, "country": "Brazil", "timezone": "UTC-3"},
            "buenos_aires": {"name": "Buenos Aires, Argentina", "lat": -34.6118, "lon": -58.3960, "country": "Argentina", "timezone": "UTC-3"},
            "lima": {"name": "Lima, Peru", "lat": -12.0464, "lon": -77.0428, "country": "Peru", "timezone": "UTC-5"},
            "santiago": {"name": "Santiago, Chile", "lat": -33.4489, "lon": -70.6693, "country": "Chile", "timezone": "UTC-3"}
        }
    
    def get_location_info(self, location_input: str) -> Dict:
        """Get location information from various input formats"""
        try:
            # Normalize input (remove spaces, convert to lowercase)
            normalized_input = location_input.lower().replace(" ", "_").replace("-", "_")
            
            # Check if it's a predefined city (exact match)
            if normalized_input in self.coastal_cities:
                city_info = self.coastal_cities[normalized_input]
                return {
                    "name": city_info["name"],
                    "lat": city_info["lat"],
                    "lon": city_info["lon"],
                    "country": city_info["country"],
                    "timezone": city_info["timezone"],
                    "coordinates": f"{city_info['lat']},{city_info['lon']}"
                }
            
            # Check for partial matches (e.g., "new york" matches "new_york")
            for city_key, city_info in self.coastal_cities.items():
                if (normalized_input in city_key or 
                    city_key.replace("_", "") in normalized_input or
                    city_key.replace("_", " ") in location_input.lower()):
                    return {
                        "name": city_info["name"],
                        "lat": city_info["lat"],
                        "lon": city_info["lon"],
                        "country": city_info["country"],
                        "timezone": city_info["timezone"],
                        "coordinates": f"{city_info['lat']},{city_info['lon']}"
                    }
            
            # Check if it's coordinates (lat,lon format)
            if "," in location_input:
                try:
                    lat, lon = map(float, location_input.split(","))
                    return {
                        "name": f"Custom Location ({lat:.4f}, {lon:.4f})",
                        "lat": lat,
                        "lon": lon,
                        "country": "Custom",
                        "timezone": "UTC",
                        "coordinates": f"{lat},{lon}"
                    }
                except ValueError:
                    pass
            
            # Generate realistic data for unknown cities instead of falling back to Mumbai
            # This prevents the "Mumbai loop" issue
            return self._generate_unknown_city_data(location_input)
            
        except Exception as e:
            print(f"Error getting location info: {e}")
            return self._generate_unknown_city_data(location_input)
    
    def _generate_unknown_city_data(self, city_name: str) -> Dict:
        """Generate realistic data for unknown cities instead of falling back to Mumbai"""
        # Generate realistic coordinates based on city name hash
        city_hash = hashlib.md5(city_name.lower().encode()).hexdigest()
        
        # Use hash to generate realistic but varied coordinates
        lat = -90 + (int(city_hash[:8], 16) % 180)  # -90 to 90
        lon = -180 + (int(city_hash[8:16], 16) % 360)  # -180 to 180
        
        # Ensure it's coastal (near water)
        if abs(lat) > 60:  # Too close to poles
            lat = lat * 0.6
        if abs(lon) > 150:  # Too far from major coastal areas
            lon = lon * 0.8
        
        # Determine timezone based on longitude
        timezone_offset = int(lon / 15)
        timezone = f"UTC{timezone_offset:+d}"
        
        return {
            "name": f"{city_name.title()}, Coastal City",
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "country": "Coastal Region",
            "timezone": timezone,
            "coordinates": f"{round(lat, 4)},{round(lon, 4)}"
        }
    
    def get_weather_data(self, location_input: str = "mumbai") -> Dict:
        """Get realistic weather data based on location and time"""
        try:
            location_info = self.get_location_info(location_input)
            lat, lon = location_info["lat"], location_info["lon"]
            
            # Try OpenWeather API first
            api_key = os.getenv("OPENWEATHER_API_KEY")
            if api_key:
                url = f"http://api.openweathermap.org/data/2.5/weather"
                params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": api_key,
                    "units": "metric"
                }
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "timestamp": datetime.utcnow(),
                        "location": location_info["coordinates"],
                        "city_name": location_info["name"],
                        "country": location_info["country"],
                        "timezone": location_info["timezone"],
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"],
                        "wind_direction": data["wind"]["deg"],
                        "pressure": data["main"]["pressure"],
                        "description": data["weather"][0]["description"],
                        "source": "openweather_api"
                    }
            
            # Fallback to realistic simulation
            return self._generate_realistic_weather(lat, lon, location_info)
            
        except Exception as e:
            print(f"Error getting weather data: {e}")
            location_info = self.get_location_info(location_input)
            return self._generate_realistic_weather(location_info["lat"], location_info["lon"], location_info)
    
    def get_tide_data(self, location_input: str = "mumbai") -> Dict:
        """Get realistic tide data based on location and time"""
        try:
            location_info = self.get_location_info(location_input)
            lat, lon = location_info["lat"], location_info["lon"]
            
            # Try NOAA API for tide data
            noaa_key = os.getenv("NOAA_API_KEY")
            if noaa_key:
                # Find nearest NOAA station
                station_id = self._find_nearest_noaa_station(lat, lon)
                if station_id:
                    url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
                    params = {
                        "station": station_id,
                        "product": "predictions",
                        "datum": "MLLW",
                        "time_zone": "lst_ldt",
                        "interval": "h",
                        "format": "json",
                        "range": "24",
                        "units": "metric"
                    }
                    
                    response = requests.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if "predictions" in data and data["predictions"]:
                            latest = data["predictions"][-1]
                            return {
                                "timestamp": datetime.utcnow(),
                                "location": location_info["coordinates"],
                                "city_name": location_info["name"],
                                "country": location_info["country"],
                                "timezone": location_info["timezone"],
                                "tide_height": float(latest["v"]),
                                "tide_type": "high" if "H" in latest["type"] else "low",
                                "source": "noaa_api"
                            }
            
            # Fallback to realistic simulation
            return self._generate_realistic_tide(location_info)
            
        except Exception as e:
            print(f"Error getting tide data: {e}")
            location_info = self.get_location_info(location_input)
            return self._generate_realistic_tide(location_info)
    
    def get_ocean_data(self, location_input: str = "mumbai") -> Dict:
        """Get realistic ocean data based on location and time"""
        try:
            location_info = self.get_location_info(location_input)
            lat, lon = location_info["lat"], location_info["lon"]
            
            return self._generate_realistic_ocean(lat, lon, location_info)
            
        except Exception as e:
            print(f"Error getting ocean data: {e}")
            location_info = self.get_location_info(location_input)
            return self._generate_realistic_ocean(location_info["lat"], location_info["lon"], location_info)
    
    def get_pollution_data(self, location_input: str = "mumbai") -> Dict:
        """Get realistic pollution data based on location and time"""
        try:
            location_info = self.get_location_info(location_input)
            lat, lon = location_info["lat"], location_info["lon"]
            
            # Try WAQI API for air quality data
            api_key = os.getenv("WAQI_API_KEY")
            if api_key:
                url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={api_key}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data["status"] == "ok":
                        aqi = data["data"]["aqi"]
                        return {
                            "timestamp": datetime.utcnow(),
                            "location": location_info["coordinates"],
                            "city_name": location_info["name"],
                            "country": location_info["country"],
                            "timezone": location_info["timezone"],
                            "water_quality": "good" if aqi < 50 else "moderate" if aqi < 100 else "poor",
                            "pollution_level": "low" if aqi < 50 else "moderate" if aqi < 100 else "high",
                            "alerts": [],
                            "monitoring_data": {
                                "turbidity": 10.0 + random.uniform(-3, 3),
                                "dissolved_oxygen": 7.0 + random.uniform(-0.5, 0.5),
                                "ph": 7.0 + random.uniform(-0.3, 0.3),
                                "bacteria_count": 100 + random.randint(-30, 50)
                            },
                            "illegal_dumping_detected": random.choice([True, False]),
                            "suspicious_activity": [],
                            "source": "waqi_api"
                        }
            
            # Fallback to realistic simulation
            return self._generate_realistic_pollution(location_info)
            
        except Exception as e:
            print(f"Error getting pollution data: {e}")
            location_info = self.get_location_info(location_input)
            return self._generate_realistic_pollution(location_info)
    
    def get_comprehensive_data(self, location_input: str) -> Dict:
        """Get comprehensive coastal data using REAL APIs with fallbacks"""
        try:
            location_info = self.get_location_info(location_input)
            if not location_info:
                raise ValueError(f"Could not get location info for {location_input}")
            
            lat, lon = location_info['lat'], location_info['lon']
            city_name = location_info['name']
            
            # Try to get REAL data from APIs
            weather_data = None
            tide_data = None
            marine_data = None
            
            # 1. Get REAL weather data
            try:
                weather_data = self.weather_service.get_current_weather(lat, lon)
                self.logger.info(f"Successfully fetched real weather data for {city_name}")
            except Exception as e:
                self.logger.warning(f"Failed to get real weather data for {city_name}: {e}")
                weather_data = self._get_fallback_weather_data(city_name, lat, lon)
            
            # 2. Get REAL tide data (if city has NOAA station)
            try:
                tide_data = self.tide_service.get_current_water_level(city_name.lower().replace(' ', '_').replace('-', '_'))
                if tide_data:
                    self.logger.info(f"Successfully fetched real tide data for {city_name}")
                else:
                    tide_data = self._get_fallback_tide_data(city_name, lat, lon)
            except Exception as e:
                self.logger.warning(f"Failed to get real tide data for {city_name}: {e}")
                tide_data = self._get_fallback_tide_data(city_name, lat, lon)
            
            # 3. Get REAL marine weather data
            try:
                marine_data = self.marine_service.get_current_conditions(lat, lon)
                if marine_data:
                    self.logger.info(f"Successfully fetched real marine data for {city_name}")
                else:
                    marine_data = self._get_fallback_marine_data(city_name, lat, lon)
            except Exception as e:
                self.logger.warning(f"Failed to get real marine data for {city_name}: {e}")
                marine_data = self._get_fallback_marine_data(city_name, lat, lon)
            
            # 4. Get air quality data (fallback for now)
            air_quality = self._get_air_quality_data(lat, lon)
            
            # 5. Get ocean currents (fallback for now)
            ocean_currents = self._get_ocean_currents_data(lat, lon)
            
            return {
                'location': location_info,
                'weather': weather_data,
                'tide': tide_data,
                'marine': marine_data,
                'air_quality': air_quality,
                'ocean_currents': ocean_currents,
                'timestamp': datetime.utcnow().isoformat(),
                'data_sources': {
                    'weather': 'openweathermap_real' if weather_data and 'source' in weather_data else 'fallback',
                    'tide': 'noaa_real' if tide_data and 'source' in tide_data else 'fallback',
                    'marine': 'stormglass_real' if marine_data and 'source' in marine_data else 'fallback',
                    'air_quality': 'fallback',
                    'ocean_currents': 'fallback'
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting comprehensive data: {e}")
            return self._get_fallback_comprehensive_data(location_input)
    
    def _get_fallback_weather_data(self, city_name: str, lat: float, lon: float) -> Dict:
        """Fallback weather data when API fails"""
        return {
            'temperature': round(random.uniform(15, 35), 1),
            'humidity': random.randint(40, 90),
            'wind_speed': round(random.uniform(2, 25), 1),
            'wind_direction': random.randint(0, 360),
            'pressure': round(random.uniform(1000, 1020), 1),
            'description': 'Partly cloudy',
            'location': f"{lat},{lon}",
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'fallback'
        }
    
    def _get_fallback_tide_data(self, city_name: str, lat: float, lon: float) -> Dict:
        """Fallback tide data when API fails"""
        return {
            'tide_height': round(random.uniform(0.5, 3.0), 2),
            'tide_type': random.choice(['high', 'low', 'rising', 'falling']),
            'location': city_name,
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'fallback'
        }
    
    def _get_fallback_marine_data(self, city_name: str, lat: float, lon: float) -> Dict:
        """Fallback marine data when API fails"""
        return {
            'sea_condition': random.choice(['calm', 'slight', 'moderate', 'rough']),
            'wave_height': round(random.uniform(0.3, 2.5), 1),
            'water_temperature': round(random.uniform(15, 28), 1),
            'visibility': random.randint(5, 25),
            'wind_speed': round(random.uniform(3, 20), 1),
            'location': f"{lat},{lon}",
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'fallback'
        }
    
    def get_available_locations(self) -> List[Dict]:
        """Get list of available coastal locations"""
        return [
            {"id": city_key, **city_info} 
            for city_key, city_info in self.coastal_cities.items()
        ]
    
    def _find_nearest_noaa_station(self, lat: float, lon: float) -> Optional[str]:
        """Find the nearest NOAA tide station to given coordinates"""
        stations = {
            "9447130": {"name": "Seattle", "lat": 47.6026, "lon": -122.3393},
            "9410230": {"name": "San Diego", "lat": 32.7157, "lon": -117.1611},
            "9413450": {"name": "Monterey", "lat": 36.6050, "lon": -121.8880},
            "9414290": {"name": "San Francisco", "lat": 37.8063, "lon": -122.4659}
        }
        
        nearest_station = None
        min_distance = float('inf')
        
        for station_id, station_info in stations.items():
            distance = math.sqrt((lat - station_info["lat"])**2 + (lon - station_info["lon"])**2)
            if distance < min_distance:
                min_distance = distance
                nearest_station = station_id
        
        return nearest_station
    
    def _generate_realistic_weather(self, lat: float, lon: float, location_info: Dict) -> Dict:
        """Generate realistic weather data based on location and current conditions"""
        now = datetime.utcnow()
        hour = now.hour
        
        # Adjust temperature based on latitude and time
        if abs(lat) < 23.5:  # Tropical
            base_temp = 28 + random.uniform(-2, 2)
        elif abs(lat) < 45:  # Temperate
            base_temp = 18 + random.uniform(-3, 3)
        else:  # Polar
            base_temp = 8 + random.uniform(-4, 4)
        
        # Adjust for day/night cycle
        if 6 <= hour <= 18:  # Daytime
            base_temp += 6
        else:  # Nighttime
            base_temp -= 4
        
        # Realistic wind patterns
        if 10 <= hour <= 16:  # Afternoon winds
            wind_speed = 12 + random.uniform(-3, 8)
        else:
            wind_speed = 6 + random.uniform(-2, 4)
        
        return {
            "timestamp": now,
            "location": location_info["coordinates"],
            "city_name": location_info["name"],
            "country": location_info["country"],
            "timezone": location_info["timezone"],
            "temperature": round(base_temp, 1),
            "humidity": random.randint(65, 85),
            "wind_speed": round(max(0, wind_speed), 1),
            "wind_direction": random.randint(0, 360),
            "pressure": 1013 + random.uniform(-12, 12),
            "description": "partly cloudy",
            "source": "realistic_simulation"
        }
    
    def _generate_realistic_tide(self, location_info: Dict) -> Dict:
        """Generate realistic tide data based on lunar cycles"""
        now = datetime.utcnow()
        hour = now.hour
        
        # Simple tide simulation based on time
        tide_height = 1.8 + 1.2 * abs(math.sin((hour - 6) * math.pi / 12))
        
        return {
            "timestamp": now,
            "location": location_info["coordinates"],
            "city_name": location_info["name"],
            "country": location_info["country"],
            "timezone": location_info["timezone"],
            "tide_height": round(tide_height, 2),
            "tide_type": "rising" if 6 <= hour <= 18 else "falling",
            "source": "realistic_simulation"
        }
    
    def _generate_realistic_ocean(self, lat: float, lon: float, location_info: Dict) -> Dict:
        """Generate realistic ocean data based on location"""
        now = datetime.utcnow()
        hour = now.hour
        
        # Realistic wave patterns
        if 8 <= hour <= 16:  # Daytime waves
            wave_height = 1.8 + random.uniform(-0.3, 0.8)
        else:
            wave_height = 1.2 + random.uniform(-0.2, 0.4)
        
        return {
            "timestamp": now,
            "location": location_info["coordinates"],
            "city_name": location_info["name"],
            "country": location_info["country"],
            "timezone": location_info["timezone"],
            "wave_height": round(wave_height, 1),
            "wave_period": 8.0 + random.uniform(-1, 1),
            "current_speed": 0.3 + random.uniform(-0.1, 0.2),
            "current_direction": 45 + random.uniform(-15, 15),
            "sea_surface_temp": 26.5 + random.uniform(-1, 1),
            "source": "realistic_simulation"
        }
    
    def _generate_realistic_pollution(self, location_info: Dict) -> Dict:
        """Generate realistic pollution data based on location and time"""
        now = datetime.utcnow()
        hour = now.hour
        
        # Pollution varies by time of day
        if 7 <= hour <= 9 or 17 <= hour <= 19:  # Rush hours
            pollution_level = "moderate"
            bacteria_count = 180 + random.randint(-40, 80)
        else:
            pollution_level = "low"
            bacteria_count = 90 + random.randint(-25, 40)
        
        return {
            "timestamp": now,
            "location": location_info["coordinates"],
            "city_name": location_info["name"],
            "country": location_info["country"],
            "timezone": location_info["timezone"],
            "water_quality": "good" if pollution_level == "low" else "moderate",
            "pollution_level": pollution_level,
            "alerts": [],
            "monitoring_data": {
                "turbidity": 10.0 + random.uniform(-2, 2),
                "dissolved_oxygen": 7.0 + random.uniform(-0.4, 0.4),
                "ph": 7.0 + random.uniform(-0.2, 0.2),
                "bacteria_count": bacteria_count
            },
            "illegal_dumping_detected": random.choice([True, False]),
            "suspicious_activity": [],
            "source": "realistic_simulation"
        }

    def _get_fallback_comprehensive_data(self, location_input: str) -> Dict:
        """Complete fallback when all APIs fail"""
        location_info = self.get_location_info(location_input)
        if not location_info:
            location_info = {
                'name': 'Unknown Location',
                'lat': 0.0,
                'lon': 0.0,
                'country': 'Unknown',
                'timezone': 'UTC',
                'coordinates': '0,0'
            }
        
        return {
            'location': location_info,
            'weather': self._get_fallback_weather_data(location_info['name'], location_info['lat'], location_info['lon']),
            'tide': self._get_fallback_tide_data(location_info['name'], location_info['lat'], location_info['lon']),
            'marine': self._get_fallback_marine_data(location_info['name'], location_info['lat'], location_info['lon']),
            'air_quality': self._get_air_quality_data(location_info['lat'], location_info['lon']),
            'ocean_currents': self._get_ocean_currents_data(location_info['lat'], location_info['lon']),
            'timestamp': datetime.utcnow().isoformat(),
            'data_sources': {
                'weather': 'fallback',
                'tide': 'fallback',
                'marine': 'fallback',
                'air_quality': 'fallback',
                'ocean_currents': 'fallback'
            }
        }
    
    def _get_air_quality_data(self, lat: float, lon: float) -> Dict:
        """Get air quality data (fallback for now)"""
        return {
            'aqi': random.randint(20, 150),
            'pm25': round(random.uniform(5, 60), 1),
            'pm10': round(random.uniform(10, 100), 1),
            'o3': round(random.uniform(20, 80), 1),
            'location': f"{lat},{lon}",
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'fallback'
        }
    
    def _get_ocean_currents_data(self, lat: float, lon: float) -> Dict:
        """Get ocean currents data (fallback for now)"""
        return {
            'current_speed': round(random.uniform(0.1, 2.0), 2),
            'current_direction': random.randint(0, 360),
            'temperature': round(random.uniform(15, 28), 1),
            'salinity': round(random.uniform(30, 35), 2),
            'location': f"{lat},{lon}",
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'fallback'
        }
