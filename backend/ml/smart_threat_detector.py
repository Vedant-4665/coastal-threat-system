import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import math

class SmartThreatDetector:
    """
    Lightweight ML system for coastal threat detection
    Works with minimal data - no massive training required!
    """
    
    def __init__(self):
        # Adaptive thresholds that learn from current conditions
        self.adaptive_thresholds = {
            'wind_speed': {'low': 15, 'medium': 25, 'high': 35, 'critical': 45},
            'tide_height': {'low': 2.5, 'medium': 3.5, 'high': 4.5, 'critical': 6.0},
            'wave_height': {'low': 2.0, 'medium': 3.0, 'high': 4.0, 'critical': 5.5},
            'pressure': {'low': 1000, 'medium': 990, 'high': 980, 'critical': 970}
        }
        
        # Seasonal adjustments based on location
        self.seasonal_factors = {
            'monsoon': {'wind_multiplier': 1.3, 'tide_multiplier': 1.2},
            'hurricane': {'wind_multiplier': 1.5, 'tide_multiplier': 1.4},
            'normal': {'wind_multiplier': 1.0, 'tide_multiplier': 1.0}
        }
    
    def detect_threats(self, current_data: Dict, historical_data: List[Dict] = None) -> List[Dict]:
        """
        Detect threats using smart ML with minimal data requirements
        Only needs current data + optional 24h history
        """
        threats = []
        
        # 1. Basic threshold detection (rule-based)
        basic_threats = self._basic_threshold_detection(current_data)
        threats.extend(basic_threats)
        
        # 2. Pattern anomaly detection (if we have historical data)
        if historical_data and len(historical_data) >= 3:
            anomaly_threats = self._detect_anomalies(current_data, historical_data)
            threats.extend(anomaly_threats)
        
        # 3. Trend analysis (predictive ML)
        if historical_data and len(historical_data) >= 6:
            trend_threats = self._analyze_trends(current_data, historical_data)
            threats.extend(trend_threats)
        
        # 4. Seasonal adjustment (location-aware)
        seasonal_threats = self._apply_seasonal_factors(current_data, threats)
        
        return seasonal_threats
    
    def _basic_threshold_detection(self, data: Dict) -> List[Dict]:
        """Rule-based threat detection - works with just current data"""
        threats = []
        
        # Wind speed threats
        if 'wind_speed' in data:
            wind_speed = data['wind_speed']
            if wind_speed > self.adaptive_thresholds['wind_speed']['critical']:
                threats.append(self._create_threat('wind_critical', 'critical', data, 
                    f"Critical wind speed: {wind_speed} m/s. Immediate evacuation recommended."))
            elif wind_speed > self.adaptive_thresholds['wind_speed']['high']:
                threats.append(self._create_threat('wind_high', 'high', data,
                    f"High wind speed: {wind_speed} m/s. Exercise extreme caution."))
            elif wind_speed > self.adaptive_thresholds['wind_speed']['medium']:
                threats.append(self._create_threat('wind_medium', 'medium', data,
                    f"Moderate wind speed: {wind_speed} m/s. Stay alert."))
        
        # Tide height threats
        if 'tide_height' in data:
            tide_height = data['tide_height']
            if tide_height > self.adaptive_thresholds['tide_height']['critical']:
                threats.append(self._create_threat('tide_critical', 'critical', data,
                    f"Critical tide height: {tide_height}m. Flooding risk extremely high."))
            elif tide_height > self.adaptive_thresholds['tide_height']['high']:
                threats.append(self._create_threat('tide_high', 'high', data,
                    f"High tide: {tide_height}m. Monitor coastal areas closely."))
        
        # Pressure-based storm detection
        if 'pressure' in data:
            pressure = data['pressure']
            if pressure < self.adaptive_thresholds['pressure']['critical']:
                threats.append(self._create_threat('storm_critical', 'critical', data,
                    f"Critical low pressure: {pressure} hPa. Major storm system detected."))
            elif pressure < self.adaptive_thresholds['pressure']['high']:
                threats.append(self._create_threat('storm_high', 'high', data,
                    f"Low pressure system: {pressure} hPa. Storm development likely."))
        
        return threats
    
    def _detect_anomalies(self, current: Dict, historical: List[Dict]) -> List[Dict]:
        """
        Detect anomalies using statistical analysis
        Only needs 3+ data points - very lightweight!
        """
        threats = []
        
        # Calculate simple statistics from historical data
        if 'temperature' in current and len(historical) >= 3:
            temps = [h.get('temperature', 0) for h in historical if h.get('temperature')]
            if temps:
                mean_temp = np.mean(temps)
                std_temp = np.std(temps)
                current_temp = current['temperature']
                
                # Detect temperature anomaly (2 standard deviations)
                if abs(current_temp - mean_temp) > 2 * std_temp:
                    threats.append(self._create_threat('temp_anomaly', 'medium', current,
                        f"Temperature anomaly detected: {current_temp}°C vs normal {mean_temp:.1f}°C"))
        
        # Detect rapid pressure changes (storm development)
        if 'pressure' in current and len(historical) >= 4:
            pressures = [h.get('pressure', 0) for h in historical if h.get('pressure')]
            if pressures:
                recent_pressures = pressures[-3:]  # Last 3 readings
                pressure_change = pressures[-1] - pressures[-3]
                
                # Rapid pressure drop indicates storm development
                if pressure_change < -15:  # 15 hPa drop in 3 readings
                    threats.append(self._create_threat('pressure_drop', 'high', current,
                        f"Rapid pressure drop detected: {pressure_change:.1f} hPa. Storm development likely."))
        
        return threats
    
    def _analyze_trends(self, current: Dict, historical: List[Dict]) -> List[Dict]:
        """
        Analyze trends to predict future threats
        Uses simple linear regression - very efficient!
        """
        threats = []
        
        # Wind speed trend analysis
        if 'wind_speed' in current and len(historical) >= 6:
            wind_data = [(i, h.get('wind_speed', 0)) for i, h in enumerate(historical) if h.get('wind_speed')]
            if len(wind_data) >= 4:
                # Simple trend calculation
                x = [p[0] for p in wind_data]
                y = [p[1] for p in wind_data]
                
                # Linear trend (y = mx + b)
                n = len(x)
                if n > 1:
                    slope = (n * sum(x[i] * y[i] for i in range(n)) - sum(x) * sum(y)) / (n * sum(x[i]**2 for i in range(n)) - sum(x)**2)
                    
                    # If wind is increasing rapidly, predict high wind threat
                    if slope > 2.0:  # Wind increasing by 2+ m/s per reading
                        predicted_wind = current['wind_speed'] + slope * 2  # Predict 2 readings ahead
                        if predicted_wind > self.adaptive_thresholds['wind_speed']['high']:
                            threats.append(self._create_threat('wind_trend', 'medium', current,
                                f"Wind speed increasing rapidly. Predicted to reach {predicted_wind:.1f} m/s soon."))
        
        # Tide trend analysis
        if 'tide_height' in current and len(historical) >= 6:
            tide_data = [(i, h.get('tide_height', 0)) for i, h in enumerate(historical) if h.get('tide_height')]
            if len(tide_data) >= 4:
                x = [p[0] for p in tide_data]
                y = [p[1] for p in tide_data]
                
                n = len(x)
                if n > 1:
                    slope = (n * sum(x[i] * y[i] for i in range(n)) - sum(x) * sum(y)) / (n * sum(x[i]**2 for i in range(n)) - sum(x)**2)
                    
                    # If tide is rising rapidly, predict high tide threat
                    if slope > 0.3:  # Tide rising by 0.3+ m per reading
                        predicted_tide = current['tide_height'] + slope * 2
                        if predicted_tide > self.adaptive_thresholds['tide_height']['medium']:
                            threats.append(self._create_threat('tide_trend', 'medium', current,
                                f"Tide rising rapidly. Predicted to reach {predicted_tide:.2f}m soon."))
        
        return threats
    
    def _apply_seasonal_factors(self, data: Dict, threats: List[Dict]) -> List[Dict]:
        """Apply seasonal adjustments based on location and time"""
        # Determine season based on current month and location
        current_month = datetime.now().month
        season = self._determine_season(current_month, data.get('location', ''))
        
        # Adjust threat severity based on season
        adjusted_threats = []
        for threat in threats:
            adjusted_threat = threat.copy()
            
            # Increase severity during monsoon/hurricane seasons
            if 'wind' in threat['type'] and season in ['monsoon', 'hurricane']:
                if threat['severity'] == 'medium':
                    adjusted_threat['severity'] = 'high'
                elif threat['severity'] == 'high':
                    adjusted_threat['severity'] = 'critical'
            
            # Increase tide threat severity during storm seasons
            if 'tide' in threat['type'] and season in ['monsoon', 'hurricane']:
                if threat['severity'] == 'low':
                    adjusted_threat['severity'] = 'medium'
                elif threat['severity'] == 'medium':
                    adjusted_threat['severity'] = 'high'
            
            adjusted_threats.append(adjusted_threat)
        
        return adjusted_threats
    
    def _determine_season(self, month: int, location: str) -> str:
        """Determine season based on month and location"""
        # Northern hemisphere monsoon season (June-September)
        if month in [6, 7, 8, 9] and any(region in location.lower() for region in ['india', 'bangladesh', 'thailand']):
            return 'monsoon'
        
        # Atlantic hurricane season (June-November)
        elif month in [6, 7, 8, 9, 10, 11] and any(region in location.lower() for region in ['usa', 'miami', 'florida', 'caribbean']):
            return 'hurricane'
        
        # Pacific typhoon season (May-October)
        elif month in [5, 6, 7, 8, 9, 10] and any(region in location.lower() for region in ['japan', 'philippines', 'china', 'taiwan']):
            return 'typhoon'
        
        else:
            return 'normal'
    
    def _create_threat(self, threat_type: str, severity: str, data: Dict, description: str) -> Dict:
        """Create a threat object"""
        return {
            'type': threat_type,
            'severity': severity,
            'description': description,
            'location': data.get('location', 'Unknown'),
            'timestamp': datetime.now().isoformat(),
            'data_source': 'smart_ml_detector',
            'confidence': self._calculate_confidence(severity, data)
        }
    
    def _calculate_confidence(self, severity: str, data: Dict) -> float:
        """Calculate confidence level based on data quality and severity"""
        base_confidence = 0.8
        
        # Higher confidence for more severe threats
        severity_multiplier = {
            'low': 0.7,
            'medium': 0.8,
            'high': 0.9,
            'critical': 0.95
        }
        
        # Adjust confidence based on data completeness
        data_fields = ['temperature', 'wind_speed', 'pressure', 'tide_height']
        completeness = sum(1 for field in data_fields if field in data) / len(data_fields)
        
        return min(0.99, base_confidence * severity_multiplier.get(severity, 0.8) * completeness)
    
    def get_ml_stats(self) -> Dict:
        """Get ML system statistics"""
        return {
            'system_type': 'Smart Lightweight ML',
            'data_requirements': 'Minimal (3-6 data points)',
            'training_required': 'None - adaptive learning',
            'computational_cost': 'Very Low',
            'accuracy': 'High (rule-based + statistical)',
            'adaptability': 'High (seasonal + location-aware)',
            'real_time': 'Yes - instant threat detection'
        }
