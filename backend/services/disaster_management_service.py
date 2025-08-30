from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import logging
from enum import Enum

class StakeholderType(Enum):
    DISASTER_MANAGEMENT = "disaster_management"
    COASTAL_GOVERNMENT = "coastal_government"
    ENVIRONMENTAL_NGO = "environmental_ngo"
    FISHERFOLK = "fisherfolk"
    CIVIL_DEFENCE = "civil_defence"

class EmergencyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DisasterManagementService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Stakeholder-specific alert configurations
        self.stakeholder_configs = {
            StakeholderType.DISASTER_MANAGEMENT: {
                "alert_types": ["all"],
                "response_time": "immediate",
                "coordination_required": True,
                "evacuation_planning": True
            },
            StakeholderType.COASTAL_GOVERNMENT: {
                "alert_types": ["infrastructure", "economic", "social"],
                "response_time": "within_1_hour",
                "coordination_required": True,
                "evacuation_planning": True
            },
            StakeholderType.ENVIRONMENTAL_NGO: {
                "alert_types": ["habitat", "pollution", "ecosystem"],
                "response_time": "within_2_hours",
                "coordination_required": False,
                "evacuation_planning": False
            },
            StakeholderType.FISHERFOLK: {
                "alert_types": ["fishing_safety", "weather", "tides"],
                "response_time": "within_30_minutes",
                "coordination_required": False,
                "evacuation_planning": False
            },
            StakeholderType.CIVIL_DEFENCE: {
                "alert_types": ["all"],
                "response_time": "immediate",
                "coordination_required": True,
                "evacuation_planning": True
            }
        }
        
        # Emergency response protocols
        self.emergency_protocols = {
            "tsunami": {
                "evacuation_zones": ["coastal_0_500m", "coastal_500m_1km", "coastal_1km_2km"],
                "response_teams": ["coast_guard", "police", "fire", "medical"],
                "communication_channels": ["emergency_broadcast", "mobile_sms", "radio", "social_media"],
                "shelter_locations": ["designated_shelters", "high_ground", "evacuation_centers"]
            },
            "cyclone": {
                "evacuation_zones": ["coastal_0_1km", "coastal_1km_3km", "flood_prone_areas"],
                "response_teams": ["disaster_response", "police", "fire", "medical", "utilities"],
                "communication_channels": ["emergency_broadcast", "mobile_sms", "radio", "tv"],
                "shelter_locations": ["cyclone_shelters", "schools", "community_centers"]
            },
            "storm_surge": {
                "evacuation_zones": ["coastal_0_500m", "low_lying_areas", "river_mouths"],
                "response_teams": ["coast_guard", "police", "fire", "rescue"],
                "communication_channels": ["emergency_broadcast", "mobile_sms", "radio"],
                "shelter_locations": ["high_ground", "multi_story_buildings", "designated_shelters"]
            },
            "habitat_degradation": {
                "evacuation_zones": ["affected_ecosystems", "pollution_impact_zones"],
                "response_teams": ["environmental", "scientific", "cleanup", "monitoring"],
                "communication_channels": ["scientific_alerts", "environmental_reports", "ngo_networks"],
                "shelter_locations": ["not_applicable"]
            }
        }

    def generate_stakeholder_alert(self, 
                                 alert_data: Dict, 
                                 stakeholder_type: StakeholderType,
                                 location: str) -> Dict:
        """Generate stakeholder-specific alerts with appropriate response protocols"""
        
        try:
            config = self.stakeholder_configs[stakeholder_type]
            emergency_level = self._assess_emergency_level(alert_data)
            
            # Filter alert types based on stakeholder
            if config["alert_types"] != ["all"]:
                if alert_data.get("alert_type") not in config["alert_types"]:
                    return None
            
            # Generate stakeholder-specific response plan
            response_plan = self._generate_response_plan(
                alert_data, stakeholder_type, emergency_level, location
            )
            
            return {
                "stakeholder_type": stakeholder_type.value,
                "alert_id": alert_data.get("id"),
                "location": location,
                "emergency_level": emergency_level.value,
                "alert_type": alert_data.get("alert_type"),
                "description": alert_data.get("description"),
                "timestamp": datetime.utcnow().isoformat(),
                "response_time_requirement": config["response_time"],
                "coordination_required": config["coordination_required"],
                "evacuation_planning": config["evacuation_planning"],
                "response_plan": response_plan,
                "stakeholder_actions": self._get_stakeholder_actions(stakeholder_type, emergency_level),
                "communication_priority": self._get_communication_priority(emergency_level)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating stakeholder alert: {str(e)}")
            return None

    def _assess_emergency_level(self, alert_data: Dict) -> EmergencyLevel:
        """Assess emergency level based on alert severity and data"""
        
        severity = alert_data.get("severity", "medium")
        confidence = alert_data.get("confidence", 0.5)
        
        if severity == "critical" and confidence > 0.8:
            return EmergencyLevel.CRITICAL
        elif severity == "high" and confidence > 0.7:
            return EmergencyLevel.HIGH
        elif severity == "medium" and confidence > 0.6:
            return EmergencyLevel.MEDIUM
        else:
            return EmergencyLevel.LOW

    def _generate_response_plan(self, 
                              alert_data: Dict, 
                              stakeholder_type: StakeholderType,
                              emergency_level: EmergencyLevel,
                              location: str) -> Dict:
        """Generate comprehensive response plan for the emergency"""
        
        alert_type = alert_data.get("alert_type", "general")
        
        if alert_type in self.emergency_protocols:
            protocol = self.emergency_protocols[alert_type]
            
            return {
                "emergency_type": alert_type,
                "evacuation_zones": protocol["evacuation_zones"],
                "response_teams": protocol["response_teams"],
                "communication_channels": protocol["communication_channels"],
                "shelter_locations": protocol["shelter_locations"],
                "immediate_actions": self._get_immediate_actions(stakeholder_type, emergency_level),
                "coordination_checklist": self._get_coordination_checklist(stakeholder_type),
                "resource_requirements": self._get_resource_requirements(emergency_level, alert_type)
            }
        else:
            return {
                "emergency_type": "general",
                "immediate_actions": self._get_immediate_actions(stakeholder_type, emergency_level),
                "coordination_checklist": self._get_coordination_checklist(stakeholder_type)
            }

    def _get_stakeholder_actions(self, 
                                stakeholder_type: StakeholderType, 
                                emergency_level: EmergencyLevel) -> List[str]:
        """Get specific actions for each stakeholder type"""
        
        actions = {
            StakeholderType.DISASTER_MANAGEMENT: {
                EmergencyLevel.CRITICAL: [
                    "Activate emergency operations center",
                    "Coordinate all response teams",
                    "Issue evacuation orders",
                    "Deploy emergency resources",
                    "Establish command structure"
                ],
                EmergencyLevel.HIGH: [
                    "Mobilize response teams",
                    "Prepare evacuation plans",
                    "Alert all stakeholders",
                    "Monitor situation closely"
                ],
                EmergencyLevel.MEDIUM: [
                    "Increase monitoring",
                    "Prepare response teams",
                    "Update stakeholders",
                    "Review emergency plans"
                ]
            },
            StakeholderType.COASTAL_GOVERNMENT: {
                EmergencyLevel.CRITICAL: [
                    "Declare emergency",
                    "Activate emergency protocols",
                    "Coordinate with disaster management",
                    "Mobilize local resources",
                    "Communicate with public"
                ],
                EmergencyLevel.HIGH: [
                    "Prepare emergency declaration",
                    "Coordinate local response",
                    "Alert local agencies",
                    "Prepare public communication"
                ]
            },
            StakeholderType.ENVIRONMENTAL_NGO: {
                EmergencyLevel.CRITICAL: [
                    "Assess habitat damage",
                    "Document environmental impact",
                    "Coordinate cleanup efforts",
                    "Alert environmental agencies",
                    "Mobilize volunteer teams"
                ],
                EmergencyLevel.HIGH: [
                    "Monitor environmental changes",
                    "Prepare assessment teams",
                    "Coordinate with partners",
                    "Document initial observations"
                ]
            },
            StakeholderType.FISHERFOLK: {
                EmergencyLevel.CRITICAL: [
                    "Return to port immediately",
                    "Secure vessels",
                    "Move to safe locations",
                    "Monitor weather updates",
                    "Follow evacuation orders"
                ],
                EmergencyLevel.HIGH: [
                    "Prepare to return to port",
                    "Monitor conditions closely",
                    "Secure fishing equipment",
                    "Stay updated on alerts"
                ]
            },
            StakeholderType.CIVIL_DEFENCE: {
                EmergencyLevel.CRITICAL: [
                    "Activate civil defence protocols",
                    "Deploy rescue teams",
                    "Establish emergency communications",
                    "Coordinate with military if needed",
                    "Protect critical infrastructure"
                ],
                EmergencyLevel.HIGH: [
                    "Prepare civil defence response",
                    "Alert rescue teams",
                    "Secure critical facilities",
                    "Prepare emergency communications"
                ]
            }
        }
        
        return actions.get(stakeholder_type, {}).get(emergency_level, ["Monitor situation"])

    def _get_coordination_checklist(self, stakeholder_type: StakeholderType) -> List[str]:
        """Get coordination checklist for stakeholders"""
        
        checklists = {
            StakeholderType.DISASTER_MANAGEMENT: [
                "Contact all response agencies",
                "Establish communication protocols",
                "Coordinate resource allocation",
                "Set up emergency operations center",
                "Establish command hierarchy"
            ],
            StakeholderType.COASTAL_GOVERNMENT: [
                "Contact disaster management",
                "Alert local agencies",
                "Coordinate with neighboring cities",
                "Establish local command center",
                "Prepare public announcements"
            ],
            StakeholderType.ENVIRONMENTAL_NGO: [
                "Contact partner organizations",
                "Coordinate with environmental agencies",
                "Establish assessment protocols",
                "Prepare volunteer coordination",
                "Set up communication networks"
            ],
            StakeholderType.FISHERFOLK: [
                "Contact fishing associations",
                "Coordinate with port authorities",
                "Establish communication networks",
                "Share safety information",
                "Coordinate return to port"
            ],
            StakeholderType.CIVIL_DEFENCE: [
                "Contact military liaison",
                "Coordinate with police",
                "Establish rescue protocols",
                "Set up emergency communications",
                "Coordinate with utilities"
            ]
        }
        
        return checklists.get(stakeholder_type, ["Establish basic coordination"])

    def _get_immediate_actions(self, 
                              stakeholder_type: StakeholderType, 
                              emergency_level: EmergencyLevel) -> List[str]:
        """Get immediate actions for stakeholders"""
        
        if emergency_level in [EmergencyLevel.CRITICAL, EmergencyLevel.HIGH]:
            return [
                "Assess immediate threats",
                "Protect human life first",
                "Establish emergency communications",
                "Mobilize available resources",
                "Coordinate with other agencies"
            ]
        else:
            return [
                "Monitor situation",
                "Prepare response plans",
                "Update stakeholders",
                "Review emergency procedures"
            ]

    def _get_resource_requirements(self, 
                                 emergency_level: EmergencyLevel, 
                                 alert_type: str) -> Dict:
        """Get resource requirements for emergency response"""
        
        base_resources = {
            "personnel": 10 if emergency_level == EmergencyLevel.CRITICAL else 5,
            "vehicles": 5 if emergency_level == EmergencyLevel.CRITICAL else 2,
            "communication_equipment": "Full emergency setup",
            "medical_supplies": "Emergency medical kit",
            "shelter_capacity": "1000+ people" if emergency_level == EmergencyLevel.CRITICAL else "500+ people"
        }
        
        if alert_type == "tsunami":
            base_resources.update({
                "rescue_boats": 10 if emergency_level == EmergencyLevel.CRITICAL else 5,
                "life_jackets": "1000+",
                "flood_rescue_equipment": "Full flood response kit"
            })
        elif alert_type == "cyclone":
            base_resources.update({
                "storm_shelters": "Multiple locations",
                "wind_protection_equipment": "Full storm response kit",
                "debris_clearance": "Heavy machinery"
            })
        
        return base_resources

    def _get_communication_priority(self, emergency_level: EmergencyLevel) -> str:
        """Get communication priority level"""
        
        priorities = {
            EmergencyLevel.CRITICAL: "Immediate broadcast to all channels",
            EmergencyLevel.HIGH: "Priority broadcast within 15 minutes",
            EmergencyLevel.MEDIUM: "Standard broadcast within 1 hour",
            EmergencyLevel.LOW: "Regular update within 4 hours"
        }
        
        return priorities.get(emergency_level, "Standard update")

    def get_emergency_coordination_summary(self, location: str) -> Dict:
        """Get summary of all active emergencies and coordination status"""
        
        return {
            "location": location,
            "timestamp": datetime.utcnow().isoformat(),
            "coordination_status": "active",
            "stakeholders_involved": [s.value for s in StakeholderType],
            "emergency_protocols": list(self.emergency_protocols.keys()),
            "response_capabilities": {
                "evacuation": "Multi-zone evacuation planning",
                "communication": "Multi-channel emergency broadcasting",
                "coordination": "Inter-agency coordination protocols",
                "resources": "Comprehensive resource management"
            }
        }

    def coordinate_emergency_response(self, 
                                   emergency_type: str, 
                                   location: str, 
                                   severity: str = "medium", 
                                   affected_population: int = 10000) -> Dict:
        """Coordinate emergency response for specific emergency type"""
        
        try:
            emergency_level = EmergencyLevel(severity.lower())
            
            # Get emergency protocols
            protocols = self.emergency_protocols.get(emergency_type, {})
            
            # Generate coordination plan
            coordination_plan = {
                "emergency_type": emergency_type,
                "location": location,
                "severity": severity,
                "affected_population": affected_population,
                "timestamp": datetime.utcnow().isoformat(),
                "response_plan": {
                    "immediate_actions": self._get_immediate_actions(StakeholderType.DISASTER_MANAGEMENT, emergency_level),
                    "evacuation_zones": protocols.get("evacuation_zones", []),
                    "shelter_locations": protocols.get("shelter_locations", []),
                    "communication_channels": protocols.get("communication_channels", [])
                },
                "team_coordination": {
                    "coast_guard": {
                        "deployment_status": "deploying" if emergency_level in [EmergencyLevel.CRITICAL, EmergencyLevel.HIGH] else "on_standby",
                        "personnel_count": 20 if emergency_level == EmergencyLevel.CRITICAL else 10,
                        "response_time": "immediate" if emergency_level == EmergencyLevel.CRITICAL else "within_15_minutes"
                    },
                    "police": {
                        "deployment_status": "deploying" if emergency_level in [EmergencyLevel.CRITICAL, EmergencyLevel.HIGH] else "on_standby",
                        "personnel_count": 50 if emergency_level == EmergencyLevel.CRITICAL else 25,
                        "response_time": "immediate" if emergency_level == EmergencyLevel.CRITICAL else "within_15_minutes"
                    },
                    "fire": {
                        "deployment_status": "deploying" if emergency_level in [EmergencyLevel.CRITICAL, EmergencyLevel.HIGH] else "on_standby",
                        "personnel_count": 30 if emergency_level == EmergencyLevel.CRITICAL else 15,
                        "response_time": "immediate" if emergency_level == EmergencyLevel.CRITICAL else "within_15_minutes"
                    },
                    "medical": {
                        "deployment_status": "deploying" if emergency_level in [EmergencyLevel.CRITICAL, EmergencyLevel.HIGH] else "on_standby",
                        "personnel_count": 40 if emergency_level == EmergencyLevel.CRITICAL else 20,
                        "response_time": "immediate" if emergency_level == EmergencyLevel.CRITICAL else "within_15_minutes"
                    }
                },
                "resource_allocation": self._get_resource_requirements(emergency_level, emergency_type),
                "communication_priority": self._get_communication_priority(emergency_level),
                "coordination_checklist": self._get_coordination_checklist(StakeholderType.DISASTER_MANAGEMENT)
            }
            
            return coordination_plan
            
        except Exception as e:
            self.logger.error(f"Error coordinating emergency response: {str(e)}")
            return None
