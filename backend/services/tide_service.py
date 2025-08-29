import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class TideService:
    def __init__(self):
        self.api_key = os.getenv("NOAA_API_KEY")
        self.base_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        
    def get_tide_data(self, station_id: str = "9447130", hours: int = 24) -> Dict:
        """Fetch tide data from NOAA API or return mock data"""
        if self.api_key:
            try:
                end_date = datetime.utcnow()
                begin_date = end_date - timedelta(hours=hours)
                
                params = {
                    "begin_date": begin_date.strftime("%Y%m%d %H:%M"),
                    "end_date": end_date.strftime("%Y%m%d %H:%M"),
                    "station": station_id,
                    "product": "predictions",
                    "datum": "MLLW",
                    "time_zone": "lst_ldt",
                    "interval": "h",
                    "units": "metric",
                    "format": "json"
                }
                
                response = requests.get(self.base_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_tide_data(data, station_id)
            except Exception as e:
                print(f"Error fetching tide data: {e}")
        
        # Return mock data if API fails or no key
        return self._get_mock_tide_data(station_id)
    
    def _parse_tide_data(self, data: Dict, station_id: str) -> Dict:
        """Parse NOAA API response"""
        if "predictions" not in data:
            return self._get_mock_tide_data(station_id)
            
        predictions = data["predictions"]
        if not predictions:
            return self._get_mock_tide_data(station_id)
            
        # Get the most recent prediction
        latest = predictions[-1]
        
        return {
            "timestamp": datetime.utcnow(),
            "location": station_id,
            "tide_height": float(latest["v"]),
            "tide_type": self._determine_tide_type(predictions),
            "source": "noaa"
        }
    
    def _determine_tide_type(self, predictions: List[Dict]) -> str:
        """Determine if tide is high, low, rising, or falling"""
        if len(predictions) < 2:
            return "unknown"
            
        current = float(predictions[-1]["v"])
        previous = float(predictions[-2]["v"])
        
        if current > previous:
            return "rising"
        elif current < previous:
            return "falling"
        else:
            return "stable"
    
    def _get_mock_tide_data(self, station_id: str) -> Dict:
        """Generate mock tide data for testing"""
        import random
        
        # Simulate tide height variation (typical range 0.5 to 3.0 meters)
        tide_height = 1.5 + random.uniform(-1.0, 1.5)
        tide_types = ["rising", "falling", "high", "low"]
        
        return {
            "timestamp": datetime.utcnow(),
            "location": station_id,
            "tide_height": round(tide_height, 2),
            "tide_type": random.choice(tide_types),
            "source": "mock"
        }
    
    def get_station_info(self, station_id: str = "9447130") -> Dict:
        """Get information about a tide station"""
        # Mock station info for now
        stations = {
            "9447130": {
                "name": "Seattle, WA",
                "lat": 47.6023,
                "lon": -122.3393,
                "state": "WA"
            },
            "9447130": {
                "name": "Mumbai, India",
                "lat": 19.0760,
                "lon": 72.8777,
                "state": "Maharashtra"
            }
        }
        
        return stations.get(station_id, {
            "name": f"Station {station_id}",
            "lat": 0.0,
            "lon": 0.0,
            "state": "Unknown"
        })
