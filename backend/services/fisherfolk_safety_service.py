from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import logging
from enum import Enum

class FishingZoneStatus(Enum):
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"
    CLOSED = "closed"

class WeatherCondition(Enum):
    CALM = "calm"
    MODERATE = "moderate"
    ROUGH = "rough"
    STORMY = "stormy"
    EXTREME = "extreme"

class FisherfolkSafetyService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Fishing zone definitions and safety parameters
        self.fishing_zones = {
            "nearshore": {
                "distance_from_shore": "0-5 km",
                "depth_range": "0-20m",
                "typical_species": ["pomfret", "mackerel", "sardines", "prawns"],
                "safety_considerations": ["shallow_water", "tidal_currents", "weather_exposure"],
                "recommended_vessel_types": ["small_boats", "catamarans", "traditional_crafts"]
            },
            "offshore": {
                "distance_from_shore": "5-50 km",
                "depth_range": "20-200m",
                "typical_species": ["tuna", "grouper", "snapper", "deep_sea_fish"],
                "safety_considerations": ["deep_water", "strong_currents", "weather_conditions", "navigation"],
                "recommended_vessel_types": ["medium_trawlers", "longliners", "gillnetters"]
            },
            "deep_sea": {
                "distance_from_shore": "50+ km",
                "depth_range": "200m+",
                "typical_species": ["swordfish", "marlin", "sharks", "deep_sea_species"],
                "safety_considerations": ["extreme_weather", "navigation_challenges", "emergency_response_time"],
                "recommended_vessel_types": ["large_trawlers", "factory_ships", "research_vessels"]
            }
        }
        
        # Safety thresholds for different conditions
        self.safety_thresholds = {
            "wind_speed": {
                "safe": {"max": 15, "unit": "knots"},
                "caution": {"max": 25, "unit": "knots"},
                "dangerous": {"max": 35, "unit": "knots"},
                "closed": {"max": 50, "unit": "knots"}
            },
            "wave_height": {
                "safe": {"max": 1.5, "unit": "meters"},
                "caution": {"max": 2.5, "unit": "meters"},
                "dangerous": {"max": 4.0, "unit": "meters"},
                "closed": {"max": 6.0, "unit": "meters"}
            },
            "visibility": {
                "safe": {"min": 10, "unit": "km"},
                "caution": {"min": 5, "unit": "km"},
                "dangerous": {"min": 2, "unit": "km"},
                "closed": {"min": 0.5, "unit": "km"}
            },
            "current_speed": {
                "safe": {"max": 2, "unit": "knots"},
                "caution": {"max": 4, "unit": "knots"},
                "dangerous": {"max": 6, "unit": "knots"},
                "closed": {"max": 8, "unit": "knots"}
            }
        }
        
        # Emergency protocols for different situations
        self.emergency_protocols = {
            "vessel_distress": {
                "immediate_actions": [
                    "Activate emergency beacon (EPIRB)",
                    "Send distress signal via radio",
                    "Deploy life rafts if necessary",
                    "Secure vessel and crew"
                ],
                "communication": [
                    "Coast Guard emergency frequency",
                    "Marine rescue coordination",
                    "Nearby vessels",
                    "Port authorities"
                ],
                "survival_equipment": [
                    "Life jackets for all crew",
                    "Emergency rations and water",
                    "First aid kit",
                    "Emergency flares and signals"
                ]
            },
            "weather_emergency": {
                "immediate_actions": [
                    "Return to port immediately",
                    "Seek sheltered waters",
                    "Secure all equipment",
                    "Monitor weather updates"
                ],
                "safe_harbors": [
                    "Designated storm shelters",
                    "Protected bays and coves",
                    "Port facilities",
                    "Emergency anchorages"
                ]
            },
            "medical_emergency": {
                "immediate_actions": [
                    "Assess medical situation",
                    "Provide first aid",
                    "Contact medical authorities",
                    "Prepare for evacuation if needed"
                ],
                "emergency_contacts": [
                    "Marine medical services",
                    "Coast Guard medical support",
                    "Port medical facilities",
                    "Emergency air evacuation"
                ]
            }
        }

    def assess_fishing_zone_safety(self, 
                                  location: str,
                                  weather_data: Dict,
                                  ocean_data: Dict) -> Dict:
        """Assess the safety of fishing zones based on current conditions"""
        
        try:
            # Extract relevant data
            wind_speed = weather_data.get("wind_speed", 0)
            wave_height = ocean_data.get("wave_height", 0)
            visibility = weather_data.get("visibility", 10)
            current_speed = ocean_data.get("current_speed", 0)
            
            # Assess each safety parameter
            wind_status = self._assess_parameter("wind_speed", wind_speed)
            wave_status = self._assess_parameter("wave_height", wave_height)
            visibility_status = self._assess_parameter("visibility", visibility)
            current_status = self._assess_parameter("current_speed", current_speed)
            
            # Determine overall zone status
            overall_status = self._determine_overall_status([
                wind_status, wave_status, visibility_status, current_status
            ])
            
            # Generate safety recommendations
            safety_recommendations = self._generate_safety_recommendations(
                overall_status, weather_data, ocean_data
            )
            
            return {
                "location": location,
                "assessment_time": datetime.utcnow().isoformat(),
                "overall_status": overall_status.value,
                "zone_assessments": {
                    "nearshore": self._assess_zone_safety("nearshore", overall_status),
                    "offshore": self._assess_zone_safety("offshore", overall_status),
                    "deep_sea": self._assess_zone_safety("deep_sea", overall_status)
                },
                "condition_details": {
                    "wind": {"speed": wind_speed, "status": wind_status.value, "unit": "knots"},
                    "waves": {"height": wave_height, "status": wave_status.value, "unit": "meters"},
                    "visibility": {"distance": visibility, "status": visibility_status.value, "unit": "km"},
                    "currents": {"speed": current_speed, "status": current_status.value, "unit": "knots"}
                },
                "safety_recommendations": safety_recommendations,
                "emergency_protocols": self._get_relevant_emergency_protocols(overall_status),
                "next_assessment": (datetime.utcnow() + timedelta(hours=2)).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing fishing zone safety: {str(e)}")
            return None

    def _assess_parameter(self, parameter: str, value: float) -> FishingZoneStatus:
        """Assess a specific safety parameter"""
        
        thresholds = self.safety_thresholds.get(parameter, {})
        
        if parameter == "visibility":
            # For visibility, higher is better
            if value >= thresholds.get("safe", {}).get("min", 10):
                return FishingZoneStatus.SAFE
            elif value >= thresholds.get("caution", {}).get("min", 5):
                return FishingZoneStatus.CAUTION
            elif value >= thresholds.get("dangerous", {}).get("min", 2):
                return FishingZoneStatus.DANGEROUS
            else:
                return FishingZoneStatus.CLOSED
        else:
            # For other parameters, lower is better
            if value <= thresholds.get("safe", {}).get("max", 0):
                return FishingZoneStatus.SAFE
            elif value <= thresholds.get("caution", {}).get("max", 0):
                return FishingZoneStatus.CAUTION
            elif value <= thresholds.get("dangerous", {}).get("max", 0):
                return FishingZoneStatus.DANGEROUS
            else:
                return FishingZoneStatus.CLOSED

    def _determine_overall_status(self, statuses: List[FishingZoneStatus]) -> FishingZoneStatus:
        """Determine overall fishing zone status based on individual parameters"""
        
        if any(status == FishingZoneStatus.CLOSED for status in statuses):
            return FishingZoneStatus.CLOSED
        elif any(status == FishingZoneStatus.DANGEROUS for status in statuses):
            return FishingZoneStatus.DANGEROUS
        elif any(status == FishingZoneStatus.CAUTION for status in statuses):
            return FishingZoneStatus.CAUTION
        else:
            return FishingZoneStatus.SAFE

    def _assess_zone_safety(self, zone: str, overall_status: FishingZoneStatus) -> Dict:
        """Assess safety for a specific fishing zone"""
        
        zone_info = self.fishing_zones.get(zone, {})
        
        if overall_status == FishingZoneStatus.SAFE:
            return {
                "status": "safe",
                "recommendation": f"Safe for {zone} fishing",
                "vessel_types": zone_info.get("recommended_vessel_types", []),
                "precautions": ["Standard safety protocols", "Monitor conditions"]
            }
        elif overall_status == FishingZoneStatus.CAUTION:
            return {
                "status": "caution",
                "recommendation": f"Exercise caution for {zone} fishing",
                "vessel_types": zone_info.get("recommended_vessel_types", []),
                "precautions": [
                    "Experienced crews only",
                    "Enhanced safety equipment",
                    "Frequent condition monitoring",
                    "Prepare for rapid return"
                ]
            }
        elif overall_status == FishingZoneStatus.DANGEROUS:
            return {
                "status": "dangerous",
                "recommendation": f"Not recommended for {zone} fishing",
                "vessel_types": ["Large vessels only with experienced crews"],
                "precautions": [
                    "Avoid fishing activities",
                    "Return to port if already at sea",
                    "Monitor emergency broadcasts",
                    "Prepare emergency protocols"
                ]
            }
        else:  # CLOSED
            return {
                "status": "closed",
                "recommendation": f"{zone.title()} fishing zones closed",
                "vessel_types": ["No fishing vessels recommended"],
                "precautions": [
                    "All fishing activities suspended",
                    "Return to port immediately",
                    "Follow emergency protocols",
                    "Monitor official announcements"
                ]
            }

    def _generate_safety_recommendations(self, 
                                       overall_status: FishingZoneStatus,
                                       weather_data: Dict,
                                       ocean_data: Dict) -> List[str]:
        """Generate safety recommendations based on current conditions"""
        
        recommendations = []
        
        if overall_status == FishingZoneStatus.SAFE:
            recommendations.extend([
                "Standard fishing operations can proceed",
                "Maintain regular safety protocols",
                "Monitor weather and ocean conditions",
                "Ensure all safety equipment is functional"
            ])
        
        elif overall_status == FishingZoneStatus.CAUTION:
            recommendations.extend([
                "Increase monitoring frequency",
                "Ensure all crew are experienced",
                "Check emergency equipment",
                "Have evacuation plan ready",
                "Stay within safe distance of port"
            ])
        
        elif overall_status == FishingZoneStatus.DANGEROUS:
            recommendations.extend([
                "Consider postponing fishing activities",
                "If at sea, return to port immediately",
                "Activate emergency protocols",
                "Monitor all communication channels",
                "Prepare for extreme weather conditions"
            ])
        
        else:  # CLOSED
            recommendations.extend([
                "All fishing activities suspended",
                "Return to port immediately",
                "Follow emergency evacuation procedures",
                "Monitor official emergency broadcasts",
                "Prepare for extended port stay"
            ])
        
        # Add specific recommendations based on conditions
        if weather_data.get("wind_speed", 0) > 25:
            recommendations.append("High winds - secure all equipment and vessels")
        
        if ocean_data.get("wave_height", 0) > 3:
            recommendations.append("High waves - avoid exposed areas")
        
        if weather_data.get("visibility", 10) < 5:
            recommendations.append("Low visibility - use navigation aids and radar")
        
        return recommendations

    def _get_relevant_emergency_protocols(self, overall_status: FishingZoneStatus) -> Dict:
        """Get relevant emergency protocols based on current status"""
        
        if overall_status in [FishingZoneStatus.DANGEROUS, FishingZoneStatus.CLOSED]:
            return {
                "weather_emergency": self.emergency_protocols["weather_emergency"],
                "vessel_distress": self.emergency_protocols["vessel_distress"]
            }
        else:
            return {
                "vessel_distress": self.emergency_protocols["vessel_distress"],
                "medical_emergency": self.emergency_protocols["medical_emergency"]
            }

    def generate_fishing_safety_report(self, 
                                     location: str,
                                     weather_data: Dict,
                                     ocean_data: Dict) -> Dict:
        """Generate comprehensive fishing safety report"""
        
        safety_assessment = self.assess_fishing_zone_safety(location, weather_data, ocean_data)
        
        if not safety_assessment:
            return None
        
        return {
            "report_type": "fishing_safety_assessment",
            "location": location,
            "generated_date": datetime.utcnow().isoformat(),
            "summary": {
                "overall_status": safety_assessment["overall_status"],
                "safe_zones": [zone for zone, info in safety_assessment["zone_assessments"].items() 
                              if info["status"] == "safe"],
                "caution_zones": [zone for zone, info in safety_assessment["zone_assessments"].items() 
                                 if info["status"] == "caution"],
                "dangerous_zones": [zone for zone, info in safety_assessment["zone_assessments"].items() 
                                   if info["status"] in ["dangerous", "closed"]]
            },
            "detailed_assessment": safety_assessment,
            "fishing_recommendations": self._get_fishing_recommendations(safety_assessment),
            "safety_checklist": self._generate_safety_checklist(safety_assessment),
            "emergency_contacts": self._get_emergency_contacts(location),
            "weather_forecast": self._get_weather_forecast_summary(weather_data),
            "ocean_conditions": self._get_ocean_conditions_summary(ocean_data)
        }

    def _get_fishing_recommendations(self, safety_assessment: Dict) -> Dict:
        """Get fishing recommendations for different vessel types"""
        
        return {
            "small_boats": {
                "recommendation": "Stay in nearshore zones only",
                "conditions": "Calm weather, good visibility",
                "precautions": ["Check weather forecast", "Stay within sight of shore"]
            },
            "medium_vessels": {
                "recommendation": "Can operate in offshore zones with caution",
                "conditions": "Moderate weather, good navigation",
                "precautions": ["Monitor conditions closely", "Have backup plans"]
            },
            "large_vessels": {
                "recommendation": "Can operate in most conditions",
                "conditions": "All weather conditions",
                "precautions": ["Follow safety protocols", "Monitor emergency channels"]
            }
        }

    def _generate_safety_checklist(self, safety_assessment: Dict) -> List[str]:
        """Generate safety checklist for current conditions"""
        
        checklist = [
            "Check weather forecast and ocean conditions",
            "Ensure all safety equipment is functional",
            "Verify communication systems are working",
            "Check emergency supplies and fuel levels",
            "Review emergency procedures with crew",
            "Monitor official safety broadcasts"
        ]
        
        if safety_assessment["overall_status"] in ["dangerous", "closed"]:
            checklist.extend([
                "Prepare emergency evacuation plan",
                "Secure all equipment and cargo",
                "Establish emergency communication protocols",
                "Monitor emergency frequencies"
            ])
        
        return checklist

    def _get_emergency_contacts(self, location: str) -> Dict:
        """Get emergency contacts for the location"""
        
        return {
            "coast_guard": "+1-800-XXX-XXXX",
            "marine_rescue": "+1-800-XXX-XXXX",
            "port_authority": "+1-800-XXX-XXXX",
            "emergency_medical": "911",
            "weather_service": "+1-800-XXX-XXXX",
            "fishing_association": "+1-800-XXX-XXXX"
        }

    def _get_weather_forecast_summary(self, weather_data: Dict) -> Dict:
        """Get weather forecast summary"""
        
        return {
            "current_conditions": {
                "temperature": weather_data.get("temperature", "N/A"),
                "wind_speed": weather_data.get("wind_speed", "N/A"),
                "wind_direction": weather_data.get("wind_direction", "N/A"),
                "visibility": weather_data.get("visibility", "N/A"),
                "description": weather_data.get("description", "N/A")
            },
            "trend": "Stable" if weather_data.get("wind_speed", 0) < 15 else "Deteriorating",
            "recommendation": "Monitor conditions closely"
        }

    def _get_ocean_conditions_summary(self, ocean_data: Dict) -> Dict:
        """Get ocean conditions summary"""
        
        return {
            "current_conditions": {
                "wave_height": ocean_data.get("wave_height", "N/A"),
                "current_speed": ocean_data.get("current_speed", "N/A"),
                "water_temperature": ocean_data.get("water_temperature", "N/A"),
                "tide_status": ocean_data.get("tide_status", "N/A")
            },
            "trend": "Stable" if ocean_data.get("wave_height", 0) < 2 else "Rough",
            "recommendation": "Exercise caution in rough conditions"
        }
