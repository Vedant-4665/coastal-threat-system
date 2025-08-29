import os
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from db.models import Alert, WeatherData, TideData
from ml.anomaly_detector import AnomalyDetector

load_dotenv()

class AlertService:
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        
    def process_data_and_generate_alerts(self, db: Session, weather_data: Dict, tide_data: Dict) -> List[Dict]:
        """Process new data and generate alerts if anomalies detected"""
        alerts = []
        
        try:
            # Store new data in database
            self._store_weather_data(db, weather_data)
            self._store_tide_data(db, tide_data)
            
            # Get historical data for anomaly detection
            recent_weather = self._get_recent_weather_data(db, hours=24)
            recent_tide = self._get_recent_tide_data(db, hours=24)
            
            # Detect anomalies
            anomalies = self.anomaly_detector.detect_anomalies(recent_weather, recent_tide)
            
            # Generate and store alerts
            for anomaly in anomalies:
                alert = self._create_alert(db, anomaly, weather_data, tide_data)
                if alert:
                    alerts.append(alert)
                    
                    # Send notifications
                    self._send_sms_alert(alert)
                    self._send_push_notification(alert)
            
            # Commit database changes
            db.commit()
            
        except Exception as e:
            print(f"Error processing data and generating alerts: {e}")
            db.rollback()
        
        return alerts
    
    def _store_weather_data(self, db: Session, weather_data: Dict):
        """Store weather data in database"""
        db_weather = WeatherData(**weather_data)
        db.add(db_weather)
        db.flush()  # Get the ID without committing
    
    def _store_tide_data(self, db: Session, tide_data: Dict):
        """Store tide data in database"""
        db_tide = TideData(**tide_data)
        db.add(db_tide)
        db.flush()  # Get the ID without committing
    
    def _get_recent_weather_data(self, db: Session, hours: int = 24) -> List[Dict]:
        """Get recent weather data from database"""
        from datetime import timedelta
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        db_data = db.query(WeatherData).filter(
            WeatherData.timestamp >= cutoff_time
        ).order_by(WeatherData.timestamp.asc()).all()
        
        return [self._db_to_dict(item) for item in db_data]
    
    def _get_recent_tide_data(self, db: Session, hours: int = 24) -> List[Dict]:
        """Get recent tide data from database"""
        from datetime import timedelta
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        db_data = db.query(TideData).filter(
            TideData.timestamp >= cutoff_time
        ).order_by(TideData.timestamp.asc()).all()
        
        return [self._db_to_dict(item) for item in db_data]
    
    def _db_to_dict(self, db_obj) -> Dict:
        """Convert database object to dictionary"""
        return {
            "id": db_obj.id,
            "timestamp": db_obj.timestamp,
            "location": db_obj.location,
            "temperature": getattr(db_obj, 'temperature', None),
            "humidity": getattr(db_obj, 'humidity', None),
            "wind_speed": getattr(db_obj, 'wind_speed', None),
            "wind_direction": getattr(db_obj, 'wind_direction', None),
            "pressure": getattr(db_obj, 'pressure', None),
            "description": getattr(db_obj, 'description', None),
            "tide_height": getattr(db_obj, 'tide_height', None),
            "tide_type": getattr(db_obj, 'tide_type', None),
            "source": db_obj.source
        }
    
    def _create_alert(self, db: Session, anomaly: Dict, weather_data: Dict, tide_data: Dict) -> Optional[Dict]:
        """Create and store alert in database"""
        try:
            # Check if similar alert already exists
            existing_alert = db.query(Alert).filter(
                Alert.alert_type == anomaly["type"],
                Alert.location == weather_data.get("location", "unknown"),
                Alert.is_active == True
            ).first()
            
            if existing_alert:
                # Update existing alert
                existing_alert.timestamp = datetime.utcnow()
                existing_alert.description = anomaly["description"]
                existing_alert.severity = anomaly["severity"]
                db.flush()
                return self._db_to_dict(existing_alert)
            else:
                # Create new alert
                alert_data = {
                    "alert_type": anomaly["type"],
                    "severity": anomaly["severity"],
                    "location": weather_data.get("location", "unknown"),
                    "description": anomaly["description"],
                    "is_active": True,
                    "triggered_by": anomaly["triggered_by"],
                    "data_sources": anomaly["data_sources"]
                }
                
                db_alert = Alert(**alert_data)
                db.add(db_alert)
                db.flush()
                
                return self._db_to_dict(db_alert)
                
        except Exception as e:
            print(f"Error creating alert: {e}")
            return None
    
    def _send_sms_alert(self, alert: Dict):
        """Send SMS alert via Twilio"""
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
            print("Twilio credentials not configured, skipping SMS")
            return
        
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            message = client.messages.create(
                body=f"🚨 COASTAL ALERT: {alert['alert_type'].upper()}\n"
                     f"Severity: {alert['severity']}\n"
                     f"Location: {alert['location']}\n"
                     f"Description: {alert['description']}\n"
                     f"Time: {alert['timestamp']}",
                from_=self.twilio_phone_number,
                to="+1234567890"  # Replace with actual recipient number
            )
            
            print(f"SMS alert sent: {message.sid}")
            
        except Exception as e:
            print(f"Error sending SMS alert: {e}")
    
    def _send_push_notification(self, alert: Dict):
        """Send push notification via Firebase"""
        try:
            # This is a placeholder for Firebase push notifications
            # In a real implementation, you would use firebase-admin SDK
            print(f"Push notification would be sent for alert: {alert['id']}")
            
        except Exception as e:
            print(f"Error sending push notification: {e}")
    
    def get_active_alerts(self, db: Session) -> List[Dict]:
        """Get all active alerts"""
        db_alerts = db.query(Alert).filter(Alert.is_active == True).order_by(Alert.timestamp.desc()).all()
        return [self._db_to_dict(alert) for alert in db_alerts]
    
    def deactivate_alert(self, db: Session, alert_id: int) -> bool:
        """Deactivate an alert"""
        try:
            alert = db.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                alert.is_active = False
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deactivating alert: {e}")
            db.rollback()
            return False
    
    def simulate_cyclone_alert(self, db: Session) -> Dict:
        """Simulate a cyclone alert for testing purposes"""
        cyclone_alert = {
            "type": "cyclone",
            "severity": "critical",
            "description": "Cyclone detected approaching coastal region - immediate evacuation recommended",
            "triggered_by": "simulation",
            "data_sources": "weather,tide,pressure"
        }
        
        weather_data = {
            "timestamp": datetime.utcnow(),
            "location": "19.0760,72.8777",
            "temperature": 25.0,
            "humidity": 95.0,
            "wind_speed": 45.0,
            "wind_direction": 180.0,
            "pressure": 950.0,
            "description": "cyclone conditions",
            "source": "simulation"
        }
        
        tide_data = {
            "timestamp": datetime.utcnow(),
            "location": "19.0760,72.8777",
            "tide_height": 4.2,
            "tide_type": "rising",
            "source": "simulation"
        }
        
        return self.process_data_and_generate_alerts(db, weather_data, tide_data)
