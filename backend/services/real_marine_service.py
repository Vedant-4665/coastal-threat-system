import requests
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta

class RealMarineService:
    """Real marine weather service using Stormglass API"""
    
    def __init__(self):
        self.api_key = "b076d0e4-8560-11f0-a59f-0242ac130006-b076d152-8560-11f0-a59f-0242ac130006"
        self.base_url = "https://api.stormglass.io/v2"
        self.logger = logging.getLogger(__name__)
    
    def get_marine_weather(self, lat: float, lon: float) -> Optional[Dict]:
        """Get real marine weather data including waves, currents, and sea conditions"""
        try:
            # Get current marine data
            params = {
                'lat': lat,
                'lng': lon,
                'params': 'waveHeight,waveDirection,wavePeriod,currentSpeed,currentDirection,waterTemperature,visibility,airTemperature,pressure,windSpeed,windDirection,humidity',
                'source': 'sg'
            }
            
            headers = {
                'Authorization': self.api_key
            }
            
            response = requests.get(
                f"{self.base_url}/weather/point", 
                params=params, 
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data']:
                current = data['data']
                
                return {
                    'wave_height': current.get('waveHeight', {}).get('sg', 0),
                    'wave_direction': current.get('waveDirection', {}).get('sg', 0),
                    'wave_period': current.get('wavePeriod', {}).get('sg', 0),
                    'current_speed': current.get('currentSpeed', {}).get('sg', 0),
                    'current_direction': current.get('currentDirection', {}).get('sg', 0),
                    'water_temperature': current.get('waterTemperature', {}).get('sg', 0),
                    'visibility': current.get('visibility', {}).get('sg', 0),
                    'air_temperature': current.get('airTemperature', {}).get('sg', 0),
                    'pressure': current.get('pressure', {}).get('sg', 0),
                    'wind_speed': current.get('windSpeed', {}).get('sg', 0),
                    'wind_direction': current.get('windDirection', {}).get('sg', 0),
                    'humidity': current.get('humidity', {}).get('sg', 0),
                    'location': f"{lat},{lon}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'source': 'stormglass_real'
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching marine weather: {e}")
            return None
        except KeyError as e:
            self.logger.error(f"Error parsing marine weather data: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in marine service: {e}")
            return None
    
    def get_wave_forecast(self, lat: float, lon: float, hours: int = 24) -> Optional[Dict]:
        """Get wave forecast for next N hours"""
        try:
            params = {
                'lat': lat,
                'lng': lon,
                'params': 'waveHeight,waveDirection,wavePeriod',
                'source': 'sg',
                'start': datetime.utcnow().isoformat(),
                'end': (datetime.utcnow() + timedelta(hours=hours)).isoformat()
            }
            
            headers = {
                'Authorization': self.api_key
            }
            
            response = requests.get(
                f"{self.base_url}/forecast/point", 
                params=params, 
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'hours' in data and data['hours']:
                forecasts = []
                for hour_data in data['hours']:
                    forecasts.append({
                        'time': hour_data['time'],
                        'wave_height': hour_data.get('waveHeight', {}).get('sg', 0),
                        'wave_direction': hour_data.get('waveDirection', {}).get('sg', 0),
                        'wave_period': hour_data.get('wavePeriod', {}).get('sg', 0)
                    })
                
                return {
                    'forecasts': forecasts,
                    'location': f"{lat},{lon}",
                    'source': 'stormglass_real'
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error fetching wave forecast: {e}")
            return None
    
    def get_current_conditions(self, lat: float, lon: float) -> Optional[Dict]:
        """Get simplified current conditions summary"""
        marine_data = self.get_marine_weather(lat, lon)
        if not marine_data:
            return None
        
        # Determine sea conditions based on wave height
        wave_height = marine_data.get('wave_height', 0)
        if wave_height < 0.5:
            sea_condition = 'calm'
        elif wave_height < 1.0:
            sea_condition = 'slight'
        elif wave_height < 2.0:
            sea_condition = 'moderate'
        elif wave_height < 3.0:
            sea_condition = 'rough'
        else:
            sea_condition = 'very_rough'
        
        return {
            'sea_condition': sea_condition,
            'wave_height': wave_height,
            'water_temperature': marine_data.get('water_temperature'),
            'visibility': marine_data.get('visibility'),
            'wind_speed': marine_data.get('wind_speed'),
            'location': marine_data['location'],
            'timestamp': marine_data['timestamp'],
            'source': 'stormglass_real'
        }
