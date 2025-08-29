from datetime import datetime, timedelta
from typing import Dict, List
import random
import sys
import os

# Add the ml directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))
from smart_threat_detector import SmartThreatDetector

class SimpleAlertService:
    """
    Simplified alert service for coastal threat monitoring
    Now with SMART ML that works with minimal data!
    """
    
    def __init__(self):
        self.alert_types = {
            "high_wind": "Strong winds detected",
            "high_tide": "High tide warning",
            "storm_risk": "Storm conditions detected",
            "pollution": "Water quality alert",
            "rough_seas": "Rough sea conditions",
            "flooding_risk": "Potential flooding risk"
        }
        
        self.severity_levels = ["low", "medium", "high", "critical"]
        
        # Initialize the smart ML threat detector
        self.ml_detector = SmartThreatDetector()
    
    def generate_alerts_from_data(self, weather_data: Dict, tide_data: Dict, ocean_data: Dict, pollution_data: Dict) -> List[Dict]:
        """Generate alerts using SMART ML with minimal data requirements"""
        alerts = []
        
        # Combine all data for ML analysis
        combined_data = {}
        if weather_data:
            combined_data.update(weather_data)
        if tide_data:
            combined_data.update(tide_data)
        if ocean_data:
            combined_data.update(ocean_data)
        if pollution_data:
            combined_data.update(pollution_data)
        
        # Use SMART ML to detect threats (works with minimal data!)
        ml_threats = self.ml_detector.detect_threats(combined_data)
        
        # Convert ML threats to alerts
        for threat in ml_threats:
            alerts.append(self._create_alert(
                threat['type'],
                threat['severity'],
                threat['location'],
                threat['description'],
                'smart_ml'
            ))
        
        # Add some realistic random alerts for demonstration
        if random.random() < 0.3:  # 30% chance
            alerts.append(self._create_alert(
                "flooding_risk",
                random.choice(["low", "medium"]),
                weather_data.get('location', '19.0760,72.8777') if weather_data else "19.0760,72.8777",
                "Minor flooding risk in low-lying coastal areas. Monitor local conditions.",
                "system_monitoring"
            ))
        
        return alerts
    
    def _create_alert(self, alert_type: str, severity: str, location: str, description: str, triggered_by: str) -> Dict:
        """Create an alert object"""
        return {
            "id": f"alert_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            "alert_type": alert_type,
            "severity": severity,
            "location": location,
            "description": description,
            "is_active": True,
            "triggered_by": triggered_by,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "smart_ml_alert_service"
        }
    
    def get_active_alerts(self) -> List[Dict]:
        """Get currently active alerts (for demo purposes, returns sample alerts)"""
        sample_alerts = [
            {
                "id": "alert_20250830_001",
                "alert_type": "high_wind",
                "severity": "medium",
                "location": "19.0760,72.8777",
                "description": "ML detected moderate winds: 22 m/s. Monitor coastal conditions.",
                "is_active": True,
                "triggered_by": "smart_ml",
                "timestamp": (datetime.utcnow() - timedelta(minutes=15)).isoformat(),
                "source": "smart_ml_alert_service"
            },
            {
                "id": "alert_20250830_002",
                "alert_type": "high_tide",
                "severity": "low",
                "location": "19.0760,72.8777",
                "description": "ML detected high tide approaching: 2.8m expected in next 2 hours.",
                "is_active": True,
                "triggered_by": "smart_ml",
                "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
                "source": "smart_ml_alert_service"
            }
        ]
        return sample_alerts
    
    def deactivate_alert(self, alert_id: str) -> bool:
        """Deactivate an alert (for demo purposes)"""
        # In a real system, this would update the database
        return True
    
    def get_ml_system_info(self) -> Dict:
        """Get information about the ML system"""
        return {
            "ml_system": self.ml_detector.get_ml_stats(),
            "alert_service": {
                "total_alerts_generated": "Dynamic based on data",
                "ml_integration": "Fully integrated",
                "data_efficiency": "Minimal data requirements",
                "real_time_processing": "Yes"
            }
        }
