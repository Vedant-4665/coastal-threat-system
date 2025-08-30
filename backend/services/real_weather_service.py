import requests
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta

class RealWeatherService:
    """Real weather service using OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = "fe0e556968434b261e347b27dd523679"  # Your real API key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.logger = logging.getLogger(__name__)
        
    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict]:
        """Get real current weather data from OpenWeatherMap"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'  # Celsius, m/s, hPa
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'location': f"{lat},{lon}",
                'timestamp': datetime.utcnow(),  # Return datetime object, not ISO string
                'source': 'openweathermap_real'
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching weather data: {e}")
            return None
        except KeyError as e:
            self.logger.error(f"Error parsing weather data: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in weather service: {e}")
            return None
    
    def get_weather_forecast(self, lat: float, lon: float) -> Optional[Dict]:
        """Get 5-day weather forecast"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract next 24 hours forecast
            forecasts = []
            for item in data['list'][:8]:  # 3-hour intervals, 8 = 24 hours
                forecasts.append({
                    'time': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'description': item['weather'][0]['description']
                })
            
            return {
                'forecasts': forecasts,
                'location': f"{lat},{lon}",
                'timestamp': datetime.utcnow(),  # Return datetime object, not ISO string
                'source': 'openweathermap_real'
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching forecast: {e}")
            return None
