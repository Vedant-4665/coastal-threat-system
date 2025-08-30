from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import logging
from enum import Enum

class ResponseTeamType(Enum):
    SEARCH_AND_RESCUE = "search_and_rescue"
    MEDICAL = "medical"
    FIRE_AND_SAFETY = "fire_and_safety"
    INFRASTRUCTURE = "infrastructure"
    COMMUNICATION = "communication"
    LOGISTICS = "logistics"
    SECURITY = "security"

class EmergencyPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class CivilDefenceService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Response team configurations
        self.response_teams = {
            ResponseTeamType.SEARCH_AND_RESCUE: {
                "capabilities": ["water_rescue", "land_rescue", "evacuation", "first_aid"],
                "equipment": ["rescue_boats", "diving_gear", "ropes", "medical_supplies"],
                "personnel_required": 8,
                "response_time": "immediate",
                "coordination_required": True
            },
            ResponseTeamType.MEDICAL: {
                "capabilities": ["emergency_medical", "triage", "evacuation", "field_hospital"],
                "equipment": ["ambulances", "medical_kits", "stretchers", "medications"],
                "personnel_required": 12,
                "response_time": "within_15_minutes",
                "coordination_required": True
            },
            ResponseTeamType.FIRE_AND_SAFETY: {
                "capabilities": ["fire_suppression", "hazard_control", "structural_assessment", "evacuation"],
                "equipment": ["fire_trucks", "firefighting_gear", "safety_equipment", "communication_devices"],
                "personnel_required": 10,
                "response_time": "within_10_minutes",
                "coordination_required": True
            },
            ResponseTeamType.INFRASTRUCTURE: {
                "capabilities": ["damage_assessment", "repair", "utilities_restoration", "structural_support"],
                "equipment": ["assessment_tools", "repair_equipment", "generators", "construction_materials"],
                "personnel_required": 15,
                "response_time": "within_1_hour",
                "coordination_required": True
            },
            ResponseTeamType.COMMUNICATION: {
                "capabilities": ["emergency_broadcasting", "coordination", "public_information", "inter_agency_communication"],
                "equipment": ["radio_systems", "satellite_phones", "broadcasting_equipment", "coordination_centers"],
                "personnel_required": 6,
                "response_time": "immediate",
                "coordination_required": True
            },
            ResponseTeamType.LOGISTICS: {
                "capabilities": ["supply_management", "transportation", "resource_allocation", "coordination_support"],
                "equipment": ["trucks", "warehouses", "inventory_systems", "coordination_tools"],
                "personnel_required": 8,
                "response_time": "within_30_minutes",
                "coordination_required": True
            },
            ResponseTeamType.SECURITY: {
                "capabilities": ["crowd_control", "access_control", "security_assessment", "law_enforcement"],
                "equipment": ["barriers", "communication_devices", "security_equipment", "coordination_tools"],
                "personnel_required": 10,
                "response_time": "within_20_minutes",
                "coordination_required": True
            }
        }
        
        # Emergency response protocols
        self.emergency_protocols = {
            "tsunami": {
                "immediate_response": [
                    "Activate emergency operations center",
                    "Issue evacuation orders",
                    "Deploy search and rescue teams",
                    "Establish emergency communications"
                ],
                "coordination_requirements": [
                    "Multi-agency coordination",
                    "Evacuation planning",
                    "Resource mobilization",
                    "Public communication"
                ],
                "resource_priorities": [
                    "Search and rescue equipment",
                    "Medical supplies",
                    "Communication systems",
                    "Transportation vehicles"
                ]
            },
            "cyclone": {
                "immediate_response": [
                    "Activate emergency operations center",
                    "Issue storm warnings",
                    "Deploy emergency teams",
                    "Establish shelters"
                ],
                "coordination_requirements": [
                    "Multi-agency coordination",
                    "Shelter management",
                    "Resource mobilization",
                    "Public communication"
                ],
                "resource_priorities": [
                    "Emergency shelters",
                    "Medical supplies",
                    "Communication systems",
                    "Transportation vehicles"
                ]
            },
            "storm_surge": {
                "immediate_response": [
                    "Activate emergency operations center",
                    "Issue flood warnings",
                    "Deploy rescue teams",
                    "Establish evacuation routes"
                ],
                "coordination_requirements": [
                    "Multi-agency coordination",
                    "Evacuation planning",
                    "Resource mobilization",
                    "Public communication"
                ],
                "resource_priorities": [
                    "Rescue boats",
                    "Medical supplies",
                    "Communication systems",
                    "Transportation vehicles"
                ]
            },
            "habitat_degradation": {
                "immediate_response": [
                    "Assess environmental damage",
                    "Deploy assessment teams",
                    "Establish monitoring protocols",
                    "Coordinate with environmental agencies"
                ],
                "coordination_requirements": [
                    "Environmental agency coordination",
                    "Scientific assessment",
                    "Monitoring coordination",
                    "Public communication"
                ],
                "resource_priorities": [
                    "Assessment equipment",
                    "Monitoring tools",
                    "Communication systems",
                    "Scientific expertise"
                ]
            }
        }

    def coordinate_emergency_response(self, 
                                   emergency_type: str,
                                   location: str,
                                   severity: str,
                                   affected_population: int) -> Dict:
        """Coordinate emergency response for a specific emergency"""
        
        try:
            # Get emergency protocol
            protocol = self.emergency_protocols.get(emergency_type, {})
            
            # Assess resource requirements
            resource_assessment = self._assess_resource_requirements(
                emergency_type, severity, affected_population
            )
            
            # Generate response plan
            response_plan = self._generate_response_plan(
                emergency_type, location, severity, protocol, resource_assessment
            )
            
            # Coordinate team deployment
            team_coordination = self._coordinate_team_deployment(
                emergency_type, severity, resource_assessment
            )
            
            return {
                "emergency_type": emergency_type,
                "location": location,
                "severity": severity,
                "affected_population": affected_population,
                "coordination_status": "active",
                "response_plan": response_plan,
                "team_coordination": team_coordination,
                "resource_allocation": resource_assessment,
                "communication_protocols": self._establish_communication_protocols(emergency_type),
                "coordination_timeline": self._generate_coordination_timeline(emergency_type, severity),
                "stakeholder_notifications": self._get_stakeholder_notifications(emergency_type, severity)
            }
            
        except Exception as e:
            self.logger.error(f"Error coordinating emergency response: {str(e)}")
            return None

    def _assess_resource_requirements(self, 
                                    emergency_type: str,
                                    severity: str,
                                    affected_population: int) -> Dict:
        """Assess resource requirements for the emergency"""
        
        # Base resource requirements
        base_resources = {
            "personnel": affected_population // 100,  # 1 person per 100 affected
            "vehicles": max(5, affected_population // 500),  # 1 vehicle per 500 affected
            "medical_supplies": affected_population // 50,  # 1 kit per 50 affected
            "communication_equipment": "Full emergency setup",
            "coordination_centers": max(1, affected_population // 10000)  # 1 center per 10k affected
        }
        
        # Adjust based on emergency type
        if emergency_type == "tsunami":
            base_resources.update({
                "rescue_boats": max(10, affected_population // 1000),
                "life_jackets": affected_population,
                "flood_rescue_equipment": "Full flood response kit"
            })
        elif emergency_type == "cyclone":
            base_resources.update({
                "emergency_shelters": max(5, affected_population // 2000),
                "storm_protection_equipment": "Full storm response kit",
                "debris_clearance": "Heavy machinery"
            })
        elif emergency_type == "storm_surge":
            base_resources.update({
                "rescue_boats": max(8, affected_population // 1500),
                "flood_protection": "Full flood response kit",
                "evacuation_vehicles": max(10, affected_population // 1000)
            })
        
        # Adjust based on severity
        severity_multiplier = {
            "low": 0.5,
            "medium": 1.0,
            "high": 1.5,
            "critical": 2.0
        }
        
        multiplier = severity_multiplier.get(severity, 1.0)
        
        # Apply multiplier to numeric resources
        for key, value in base_resources.items():
            if isinstance(value, (int, float)):
                base_resources[key] = int(value * multiplier)
        
        return base_resources

    def _generate_response_plan(self, 
                              emergency_type: str,
                              location: str,
                              severity: str,
                              protocol: Dict,
                              resource_assessment: Dict) -> Dict:
        """Generate comprehensive response plan"""
        
        return {
            "emergency_type": emergency_type,
            "location": location,
            "severity": severity,
            "immediate_actions": protocol.get("immediate_response", []),
            "coordination_requirements": protocol.get("coordination_requirements", []),
            "resource_priorities": protocol.get("resource_priorities", []),
            "response_phases": self._define_response_phases(emergency_type, severity),
            "evacuation_plan": self._generate_evacuation_plan(emergency_type, location, severity),
            "communication_strategy": self._generate_communication_strategy(emergency_type, severity),
            "resource_mobilization": self._generate_resource_mobilization_plan(resource_assessment)
        }

    def _define_response_phases(self, emergency_type: str, severity: str) -> List[Dict]:
        """Define response phases for the emergency"""
        
        if emergency_type == "tsunami":
            return [
                {
                    "phase": "immediate_response",
                    "duration": "0-2 hours",
                    "actions": ["Evacuation", "Search and rescue", "Emergency communications"],
                    "teams": ["Search and rescue", "Medical", "Communication"]
                },
                {
                    "phase": "stabilization",
                    "duration": "2-24 hours",
                    "actions": ["Damage assessment", "Medical care", "Shelter establishment"],
                    "teams": ["Medical", "Infrastructure", "Logistics"]
                },
                {
                    "phase": "recovery",
                    "duration": "24+ hours",
                    "actions": ["Infrastructure repair", "Community support", "Long-term planning"],
                    "teams": ["Infrastructure", "Logistics", "Communication"]
                }
            ]
        else:
            return [
                {
                    "phase": "immediate_response",
                    "duration": "0-4 hours",
                    "actions": ["Assessment", "Team deployment", "Emergency communications"],
                    "teams": ["All response teams"]
                },
                {
                    "phase": "stabilization",
                    "duration": "4-24 hours",
                    "actions": ["Situation control", "Resource coordination", "Public support"],
                    "teams": ["All response teams"]
                },
                {
                    "phase": "recovery",
                    "duration": "24+ hours",
                    "actions": ["Recovery planning", "Resource management", "Community support"],
                    "teams": ["Infrastructure", "Logistics", "Communication"]
                }
            ]

    def _generate_evacuation_plan(self, 
                                 emergency_type: str,
                                 location: str,
                                 severity: str) -> Dict:
        """Generate evacuation plan for the emergency"""
        
        evacuation_zones = {
            "tsunami": ["coastal_0_500m", "coastal_500m_1km", "coastal_1km_2km"],
            "cyclone": ["coastal_0_1km", "coastal_1km_3km", "flood_prone_areas"],
            "storm_surge": ["coastal_0_500m", "low_lying_areas", "river_mouths"],
            "habitat_degradation": ["affected_ecosystems", "pollution_impact_zones"]
        }
        
        zones = evacuation_zones.get(emergency_type, ["affected_areas"])
        
        return {
            "evacuation_zones": zones,
            "evacuation_routes": self._define_evacuation_routes(location, zones),
            "assembly_points": self._define_assembly_points(location, zones),
            "shelter_locations": self._define_shelter_locations(location, emergency_type),
            "transportation_coordination": self._coordinate_transportation(severity),
            "evacuation_timeline": self._generate_evacuation_timeline(emergency_type, severity)
        }

    def _define_evacuation_routes(self, location: str, zones: List[str]) -> Dict:
        """Define evacuation routes for each zone"""
        
        # This would integrate with actual geographic data
        # For now, providing template routes
        routes = {}
        for zone in zones:
            routes[zone] = {
                "primary_route": f"Primary evacuation route from {zone}",
                "secondary_route": f"Secondary evacuation route from {zone}",
                "emergency_route": f"Emergency evacuation route from {zone}",
                "route_conditions": "Monitor for obstacles and hazards"
            }
        
        return routes

    def _define_assembly_points(self, location: str, zones: List[str]) -> Dict:
        """Define assembly points for each zone"""
        
        # This would integrate with actual geographic data
        # For now, providing template assembly points
        assembly_points = {}
        for zone in zones:
            assembly_points[zone] = {
                "primary_point": f"Primary assembly point for {zone}",
                "secondary_point": f"Secondary assembly point for {zone}",
                "capacity": "1000+ people",
                "facilities": ["Medical aid", "Water", "Basic supplies", "Communication"]
            }
        
        return assembly_points

    def _define_shelter_locations(self, location: str, emergency_type: str) -> List[Dict]:
        """Define shelter locations for the emergency"""
        
        shelter_types = {
            "tsunami": ["High ground shelters", "Multi-story buildings", "Designated evacuation centers"],
            "cyclone": ["Cyclone shelters", "Schools", "Community centers", "Government buildings"],
            "storm_surge": ["High ground", "Multi-story buildings", "Designated shelters"],
            "habitat_degradation": ["Community centers", "Government buildings", "Educational institutions"]
        }
        
        shelter_list = shelter_types.get(emergency_type, ["General shelters"])
        
        shelters = []
        for shelter_type in shelter_list:
            shelters.append({
                "type": shelter_type,
                "capacity": "500-1000 people",
                "facilities": ["Basic amenities", "Medical support", "Communication", "Security"],
                "accessibility": "Wheelchair accessible",
                "coordination": "Local authorities"
            })
        
        return shelters

    def _coordinate_transportation(self, severity: str) -> Dict:
        """Coordinate transportation for evacuation"""
        
        transportation_requirements = {
            "low": {"vehicles": 10, "coordination": "Local transport"},
            "medium": {"vehicles": 25, "coordination": "Regional transport"},
            "high": {"vehicles": 50, "coordination": "Multi-regional transport"},
            "critical": {"vehicles": 100, "coordination": "National transport coordination"}
        }
        
        return transportation_requirements.get(severity, {"vehicles": 25, "coordination": "Regional transport"})

    def _generate_evacuation_timeline(self, emergency_type: str, severity: str) -> Dict:
        """Generate evacuation timeline"""
        
        if emergency_type == "tsunami":
            return {
                "immediate": "0-15 minutes",
                "urgent": "15-30 minutes",
                "standard": "30-60 minutes",
                "delayed": "60+ minutes"
            }
        else:
            return {
                "immediate": "0-30 minutes",
                "urgent": "30-60 minutes",
                "standard": "1-2 hours",
                "delayed": "2+ hours"
            }

    def _generate_communication_strategy(self, emergency_type: str, severity: str) -> Dict:
        """Generate communication strategy for the emergency"""
        
        communication_channels = {
            "emergency_broadcast": "Radio and TV emergency broadcasts",
            "mobile_sms": "Emergency SMS alerts",
            "social_media": "Social media updates",
            "public_address": "Public address systems",
            "door_to_door": "Door-to-door notifications",
            "digital_signage": "Digital signage displays"
        }
        
        priority_channels = {
            "critical": ["emergency_broadcast", "mobile_sms", "public_address"],
            "high": ["emergency_broadcast", "mobile_sms", "social_media"],
            "medium": ["mobile_sms", "social_media", "digital_signage"],
            "low": ["social_media", "digital_signage"]
        }
        
        return {
            "primary_channels": priority_channels.get(severity, ["mobile_sms", "social_media"]),
            "all_channels": communication_channels,
            "coordination_protocols": "Centralized communication coordination",
            "update_frequency": "Every 15 minutes for critical, hourly for others"
        }

    def _generate_resource_mobilization_plan(self, resource_assessment: Dict) -> Dict:
        """Generate resource mobilization plan"""
        
        return {
            "immediate_mobilization": {
                "personnel": "Deploy available personnel immediately",
                "vehicles": "Mobilize all available vehicles",
                "equipment": "Deploy essential equipment"
            },
            "short_term_mobilization": {
                "personnel": "Coordinate additional personnel within 2 hours",
                "vehicles": "Coordinate additional vehicles within 1 hour",
                "equipment": "Coordinate additional equipment within 2 hours"
            },
            "long_term_mobilization": {
                "personnel": "Coordinate long-term personnel support",
                "vehicles": "Coordinate long-term vehicle support",
                "equipment": "Coordinate long-term equipment support"
            }
        }

    def _coordinate_team_deployment(self, 
                                   emergency_type: str,
                                   severity: str,
                                   resource_assessment: Dict) -> Dict:
        """Coordinate deployment of response teams"""
        
        team_deployment = {}
        
        for team_type, team_config in self.response_teams.items():
            # Determine if team should be deployed
            should_deploy = self._should_deploy_team(team_type, emergency_type, severity)
            
            if should_deploy:
                team_deployment[team_type.value] = {
                    "deployment_status": "deploying",
                    "response_time": team_config["response_time"],
                    "personnel_required": team_config["personnel_required"],
                    "equipment": team_config["equipment"],
                    "capabilities": team_config["capabilities"],
                    "coordination_required": team_config["coordination_required"],
                    "deployment_location": "Emergency location",
                    "coordination_center": "Main coordination center"
                }
            else:
                team_deployment[team_type.value] = {
                    "deployment_status": "standby",
                    "response_time": "on_call",
                    "personnel_required": 0,
                    "equipment": "Standard equipment",
                    "capabilities": team_config["capabilities"],
                    "coordination_required": False,
                    "deployment_location": "Home base",
                    "coordination_center": "Local coordination center"
                }
        
        return team_deployment

    def _should_deploy_team(self, team_type: ResponseTeamType, emergency_type: str, severity: str) -> bool:
        """Determine if a team should be deployed"""
        
        # All teams deploy for critical emergencies
        if severity == "critical":
            return True
        
        # Team-specific deployment logic
        if team_type == ResponseTeamType.SEARCH_AND_RESCUE:
            return emergency_type in ["tsunami", "cyclone", "storm_surge"]
        elif team_type == ResponseTeamType.MEDICAL:
            return True  # Medical always deploys
        elif team_type == ResponseTeamType.FIRE_AND_SAFETY:
            return emergency_type in ["cyclone", "habitat_degradation"]
        elif team_type == ResponseTeamType.INFRASTRUCTURE:
            return emergency_type in ["tsunami", "cyclone", "storm_surge"]
        elif team_type == ResponseTeamType.COMMUNICATION:
            return True  # Communication always deploys
        elif team_type == ResponseTeamType.LOGISTICS:
            return True  # Logistics always deploys
        elif team_type == ResponseTeamType.SECURITY:
            return severity in ["high", "critical"]
        
        return False

    def _establish_communication_protocols(self, emergency_type: str) -> Dict:
        """Establish communication protocols for the emergency"""
        
        return {
            "primary_frequency": "Emergency frequency 1",
            "secondary_frequency": "Emergency frequency 2",
            "coordination_frequency": "Coordination frequency",
            "backup_communication": "Satellite phones, mobile networks",
            "communication_hierarchy": "Central command → Team leaders → Team members",
            "update_protocols": "Regular updates every 15-30 minutes",
            "emergency_protocols": "Immediate communication for critical situations"
        }

    def _generate_coordination_timeline(self, emergency_type: str, severity: str) -> Dict:
        """Generate coordination timeline for the emergency"""
        
        if severity == "critical":
            return {
                "immediate": "0-15 minutes",
                "short_term": "15 minutes - 1 hour",
                "medium_term": "1-4 hours",
                "long_term": "4+ hours"
            }
        else:
            return {
                "immediate": "0-30 minutes",
                "short_term": "30 minutes - 2 hours",
                "medium_term": "2-6 hours",
                "long_term": "6+ hours"
            }

    def _get_stakeholder_notifications(self, emergency_type: str, severity: str) -> List[Dict]:
        """Get stakeholder notifications for the emergency"""
        
        notifications = [
            {
                "stakeholder": "Government agencies",
                "priority": "immediate",
                "method": "Emergency protocols",
                "content": f"Emergency declaration for {emergency_type}"
            },
            {
                "stakeholder": "Emergency services",
                "priority": "immediate",
                "method": "Emergency protocols",
                "content": f"Activate emergency response for {emergency_type}"
            },
            {
                "stakeholder": "Public",
                "priority": "immediate" if severity in ["high", "critical"] else "urgent",
                "method": "Emergency broadcasts",
                "content": f"Emergency alert for {emergency_type}"
            }
        ]
        
        if emergency_type in ["tsunami", "cyclone", "storm_surge"]:
            notifications.append({
                "stakeholder": "Coastal communities",
                "priority": "immediate",
                "method": "Multiple channels",
                "content": f"Evacuation orders for {emergency_type}"
            })
        
        return notifications

    def get_coordination_summary(self, location: str) -> Dict:
        """Get summary of coordination capabilities and status"""
        
        return {
            "location": location,
            "coordination_status": "active",
            "response_teams": len(self.response_teams),
            "emergency_protocols": len(self.emergency_protocols),
            "coordination_capabilities": {
                "multi_agency_coordination": True,
                "resource_management": True,
                "communication_systems": True,
                "evacuation_planning": True,
                "emergency_response": True
            },
            "coordination_centers": "Main center and local centers",
            "response_capacity": "Full emergency response capacity",
            "coordination_tools": "Advanced coordination and communication systems"
        }
