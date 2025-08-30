import requests
import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta

class RealTideService:
    """Real tide service using NOAA Tides & Currents API (No API key needed)"""
    
    def __init__(self):
        self.base_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        self.logger = logging.getLogger(__name__)
        
        # Major coastal cities with NOAA station IDs
        self.station_mapping = {
            'miami': '8724580',
            'san_francisco': '9410230',
            'seattle': '9447130',
            'boston': '8443970',
            'new_york': '8518750',
            'charleston': '8665530',
            'galveston': '8771450',
            'los_angeles': '9410660',
            'portland_or': '9447130',
            'anchorage': '9455920',
            'honolulu': '1612340',
            'panama_city': '8729108',
            'pensacola': '8729840',
            'mobile': '8737048',
            'new_orleans': '8761927',
            'santa_barbara': '9411340',
            'monterey': '9413450',
            'crescent_city': '9419750',
            'garibaldi': '9437540'
        }
    
    def get_station_id(self, city_name: str) -> Optional[str]:
        """Get NOAA station ID for a city"""
        normalized_name = city_name.lower().replace(' ', '_').replace('-', '_')
        
        # Direct match
        if normalized_name in self.station_mapping:
            return self.station_mapping[normalized_name]
        
        # Partial match
        for key, station_id in self.station_mapping.items():
            if normalized_name in key or key in normalized_name:
                return station_id
        
        return None
    
    def get_current_water_level(self, city_name: str) -> Optional[Dict]:
        """Get real current water level from NOAA"""
        station_id = self.get_station_id(city_name)
        if not station_id:
            self.logger.warning(f"No NOAA station found for {city_name}")
            return None
        
        try:
            params = {
                'station': station_id,
                'product': 'water_level',
                'datum': 'MLLW',
                'time_zone': 'lst_ldt',
                'units': 'metric',
                'format': 'json'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data']:
                latest = data['data'][0]
                return {
                    'tide_height': float(latest['v']),
                    'tide_type': self._determine_tide_type(latest['v']),
                    'location': city_name,
                    'timestamp': latest['t'],
                    'station_id': station_id,
                    'source': 'noaa_real'
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error fetching water level for {city_name}: {e}")
            return None
    
    def get_tide_predictions(self, city_name: str, hours: int = 24) -> Optional[Dict]:
        """Get tide predictions for next N hours"""
        station_id = self.get_station_id(city_name)
        if not station_id:
            return None
        
        try:
            params = {
                'station': station_id,
                'product': 'predictions',
                'datum': 'MLLW',
                'time_zone': 'lst_ldt',
                'units': 'metric',
                'format': 'json',
                'interval': 'h',  # Hourly predictions
                'range': hours
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'predictions' in data:
                predictions = []
                for pred in data['predictions']:
                    predictions.append({
                        'time': pred['t'],
                        'height': float(pred['v']),
                        'type': self._determine_tide_type(pred['v'])
                    })
                
                return {
                    'predictions': predictions,
                    'location': city_name,
                    'station_id': station_id,
                    'source': 'noaa_real'
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error fetching predictions for {city_name}: {e}")
            return None
    
    def _determine_tide_type(self, height: float) -> str:
        """Determine tide type based on height (simplified logic)"""
        # This is a simplified approach - real tide prediction is more complex
        if height > 2.0:
            return 'high'
        elif height < 0.5:
            return 'low'
        elif height > 1.5:
            return 'rising'
        else:
            return 'falling'
    
    def get_available_stations(self) -> List[Dict]:
        """Get list of available NOAA stations"""
        stations = []
        for city, station_id in self.station_mapping.items():
            stations.append({
                'city': city.replace('_', ' ').title(),
                'station_id': station_id,
                'country': 'USA'
            })
        return stations
