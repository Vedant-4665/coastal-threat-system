from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import logging
import math
from enum import Enum

class HabitatType(Enum):
    MANGROVE_FOREST = "mangrove_forest"
    SEAGRASS_BED = "seagrass_bed"
    SALT_MARSH = "salt_marsh"
    CORAL_REEF = "coral_reef"
    COASTAL_WETLAND = "coastal_wetland"
    ESTUARY = "estuary"

class HabitatHealth(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

class HabitatProtectionService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Blue carbon habitat characteristics
        self.habitat_characteristics = {
            HabitatType.MANGROVE_FOREST: {
                "carbon_storage": "1000-3000 tons CO2/ha",
                "biodiversity": "High - fish, birds, crustaceans",
                "protection_value": "Storm surge, erosion control",
                "threats": ["deforestation", "pollution", "climate_change", "urbanization"],
                "restoration_time": "10-20 years",
                "monitoring_indicators": ["tree_density", "canopy_cover", "soil_carbon", "fauna_diversity"]
            },
            HabitatType.SEAGRASS_BED: {
                "carbon_storage": "500-1500 tons CO2/ha",
                "biodiversity": "High - fish, sea turtles, dugongs",
                "protection_value": "Wave attenuation, sediment stabilization",
                "threats": ["eutrophication", "dredging", "anchor_damage", "climate_change"],
                "restoration_time": "5-15 years",
                "monitoring_indicators": ["shoot_density", "cover_percentage", "species_richness", "water_quality"]
            },
            HabitatType.SALT_MARSH: {
                "carbon_storage": "800-2000 tons CO2/ha",
                "biodiversity": "Medium - migratory birds, fish",
                "protection_value": "Flood control, water filtration",
                "threats": ["sea_level_rise", "drainage", "pollution", "invasive_species"],
                "restoration_time": "8-15 years",
                "monitoring_indicators": ["vegetation_cover", "elevation", "salinity", "bird_populations"]
            },
            HabitatType.CORAL_REEF: {
                "carbon_storage": "200-800 tons CO2/ha",
                "biodiversity": "Very High - 25% of marine species",
                "protection_value": "Coastal protection, tourism, fisheries",
                "threats": ["ocean_acidification", "bleaching", "overfishing", "pollution"],
                "restoration_time": "20-50 years",
                "monitoring_indicators": ["coral_cover", "bleaching_events", "fish_abundance", "water_temperature"]
            },
            HabitatType.COASTAL_WETLAND: {
                "carbon_storage": "600-1800 tons CO2/ha",
                "biodiversity": "Medium - waterfowl, amphibians",
                "protection_value": "Water purification, flood control",
                "threats": ["drainage", "pollution", "invasive_species", "climate_change"],
                "restoration_time": "10-25 years",
                "monitoring_indicators": ["water_level", "vegetation_health", "water_quality", "fauna_presence"]
            },
            HabitatType.ESTUARY: {
                "carbon_storage": "400-1200 tons CO2/ha",
                "biodiversity": "High - fish, birds, marine mammals",
                "protection_value": "Nursery grounds, water filtration",
                "threats": ["pollution", "overfishing", "habitat_loss", "climate_change"],
                "restoration_time": "15-30 years",
                "monitoring_indicators": ["water_quality", "fish_populations", "sediment_quality", "flow_patterns"]
            }
        }
        
        # Habitat monitoring protocols
        self.monitoring_protocols = {
            "weekly": ["water_quality", "visual_inspection", "basic_measurements"],
            "monthly": ["detailed_surveys", "species_counts", "habitat_extent"],
            "quarterly": ["comprehensive_assessment", "carbon_storage_estimation", "threat_analysis"],
            "annually": ["full_ecosystem_audit", "restoration_planning", "stakeholder_reporting"]
        }

    def assess_habitat_health(self, 
                             habitat_type: HabitatType,
                             monitoring_data: Dict,
                             location: str) -> Dict:
        """Assess the health of a specific habitat based on monitoring data"""
        
        try:
            characteristics = self.habitat_characteristics[habitat_type]
            indicators = characteristics["monitoring_indicators"]
            
            # Calculate health score based on indicators
            health_score = self._calculate_health_score(habitat_type, monitoring_data, indicators)
            health_status = self._determine_health_status(health_score)
            
            # Assess threats and risks
            threats = self._assess_threats(habitat_type, monitoring_data, location)
            risk_level = self._calculate_risk_level(threats)
            
            # Generate conservation recommendations
            recommendations = self._generate_conservation_recommendations(
                habitat_type, health_status, threats, risk_level
            )
            
            return {
                "habitat_type": habitat_type.value,
                "location": location,
                "assessment_date": datetime.utcnow().isoformat(),
                "health_score": health_score,
                "health_status": health_status.value,
                "threats": threats,
                "risk_level": risk_level,
                "carbon_storage_potential": characteristics["carbon_storage"],
                "biodiversity_value": characteristics["biodiversity"],
                "protection_value": characteristics["protection_value"],
                "restoration_time": characteristics["restoration_time"],
                "monitoring_indicators": indicators,
                "conservation_recommendations": recommendations,
                "monitoring_frequency": self._recommend_monitoring_frequency(health_status, risk_level)
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing habitat health: {str(e)}")
            return None

    def _calculate_health_score(self, 
                               habitat_type: HabitatType,
                               monitoring_data: Dict,
                               indicators: List[str]) -> float:
        """Calculate a health score from 0-100 based on monitoring data"""
        
        total_score = 0
        max_score = len(indicators) * 20  # Each indicator worth 20 points
        
        for indicator in indicators:
            if indicator in monitoring_data:
                value = monitoring_data[indicator]
                score = self._score_indicator(indicator, value, habitat_type)
                total_score += score
        
        # Normalize to 0-100 scale
        return min(100, max(0, (total_score / max_score) * 100))

    def _score_indicator(self, indicator: str, value: any, habitat_type: HabitatType) -> float:
        """Score an individual monitoring indicator"""
        
        if indicator == "tree_density" and habitat_type == HabitatType.MANGROVE_FOREST:
            # Mangrove tree density scoring (trees/ha)
            if isinstance(value, (int, float)):
                if value >= 1000: return 20
                elif value >= 500: return 15
                elif value >= 200: return 10
                elif value >= 100: return 5
                else: return 0
        
        elif indicator == "coral_cover" and habitat_type == HabitatType.CORAL_REEF:
            # Coral cover percentage scoring
            if isinstance(value, (int, float)):
                if value >= 50: return 20
                elif value >= 30: return 15
                elif value >= 15: return 10
                elif value >= 5: return 5
                else: return 0
        
        elif indicator == "water_quality":
            # Water quality scoring (assuming 0-100 scale)
            if isinstance(value, (int, float)):
                if value >= 80: return 20
                elif value >= 60: return 15
                elif value >= 40: return 10
                elif value >= 20: return 5
                else: return 0
        
        # Default scoring for other indicators
        return 10 if value else 0

    def _determine_health_status(self, health_score: float) -> HabitatHealth:
        """Determine habitat health status based on score"""
        
        if health_score >= 80:
            return HabitatHealth.EXCELLENT
        elif health_score >= 60:
            return HabitatHealth.GOOD
        elif health_score >= 40:
            return HabitatHealth.FAIR
        elif health_score >= 20:
            return HabitatHealth.POOR
        else:
            return HabitatHealth.CRITICAL

    def _assess_threats(self, 
                        habitat_type: HabitatType,
                        monitoring_data: Dict,
                        location: str) -> List[Dict]:
        """Assess current threats to the habitat"""
        
        characteristics = self.habitat_characteristics[habitat_type]
        potential_threats = characteristics["threats"]
        detected_threats = []
        
        for threat in potential_threats:
            threat_level = self._assess_threat_level(threat, monitoring_data, location)
            if threat_level["level"] in ["medium", "high", "critical"]:
                detected_threats.append(threat_level)
        
        return detected_threats

    def _assess_threat_level(self, 
                            threat: str,
                            monitoring_data: Dict,
                            location: str) -> Dict:
        """Assess the level of a specific threat"""
        
        # This would integrate with real monitoring data
        # For now, using realistic threat assessments
        threat_assessments = {
            "deforestation": {
                "level": "medium" if "deforestation_rate" in monitoring_data else "low",
                "description": "Habitat clearing for development or agriculture",
                "impact": "Loss of carbon storage and biodiversity",
                "mitigation": "Protected area designation, sustainable land use"
            },
            "pollution": {
                "level": "high" if "water_quality" in monitoring_data and monitoring_data.get("water_quality", 100) < 50 else "medium",
                "description": "Water and soil contamination from various sources",
                "impact": "Reduced habitat quality and species survival",
                "mitigation": "Pollution control, wastewater treatment"
            },
            "climate_change": {
                "level": "high",
                "description": "Rising temperatures, sea levels, and extreme weather",
                "impact": "Habitat degradation and species range shifts",
                "mitigation": "Climate action, habitat restoration, adaptation"
            },
            "overfishing": {
                "level": "medium" if "fish_population" in monitoring_data else "low",
                "description": "Excessive fishing pressure on key species",
                "impact": "Disruption of food webs and ecosystem balance",
                "mitigation": "Sustainable fishing practices, marine protected areas"
            }
        }
        
        return threat_assessments.get(threat, {
            "level": "low",
            "description": f"Unknown threat: {threat}",
            "impact": "Unknown impact",
            "mitigation": "Further assessment required"
        })

    def _calculate_risk_level(self, threats: List[Dict]) -> str:
        """Calculate overall risk level based on threats"""
        
        if not threats:
            return "low"
        
        # Count high and critical threats
        high_critical_count = sum(1 for t in threats if t["level"] in ["high", "critical"])
        
        if high_critical_count >= 3:
            return "critical"
        elif high_critical_count >= 2:
            return "high"
        elif high_critical_count >= 1:
            return "medium"
        else:
            return "low"

    def _generate_conservation_recommendations(self,
                                            habitat_type: HabitatType,
                                            health_status: HabitatHealth,
                                            threats: List[Dict],
                                            risk_level: str) -> List[str]:
        """Generate conservation recommendations based on assessment"""
        
        recommendations = []
        
        # Health-based recommendations
        if health_status == HabitatHealth.CRITICAL:
            recommendations.extend([
                "Immediate intervention required",
                "Establish emergency protection measures",
                "Implement habitat restoration program",
                "Increase monitoring frequency to weekly"
            ])
        elif health_status == HabitatHealth.POOR:
            recommendations.extend([
                "Urgent conservation action needed",
                "Develop restoration plan within 3 months",
                "Implement threat mitigation measures",
                "Increase monitoring frequency to monthly"
            ])
        elif health_status == HabitatHealth.FAIR:
            recommendations.extend([
                "Implement conservation measures",
                "Monitor threats closely",
                "Plan habitat enhancement activities",
                "Maintain current monitoring frequency"
            ])
        
        # Threat-specific recommendations
        for threat in threats:
            if threat["level"] in ["high", "critical"]:
                recommendations.append(f"Priority: Address {threat['description']} - {threat['mitigation']}")
        
        # General recommendations
        recommendations.extend([
            "Establish long-term monitoring program",
            "Engage local communities in conservation",
            "Develop stakeholder partnerships",
            "Secure funding for conservation activities"
        ])
        
        return recommendations

    def _recommend_monitoring_frequency(self, 
                                      health_status: HabitatHealth,
                                      risk_level: str) -> str:
        """Recommend monitoring frequency based on health and risk"""
        
        if health_status in [HabitatHealth.CRITICAL, HabitatHealth.POOR] or risk_level == "critical":
            return "weekly"
        elif health_status == HabitatHealth.FAIR or risk_level == "high":
            return "monthly"
        elif health_status == HabitatHealth.GOOD or risk_level == "medium":
            return "quarterly"
        else:
            return "annually"

    def generate_habitat_report(self, 
                              habitat_type: HabitatType,
                              location: str,
                              monitoring_data: Dict) -> Dict:
        """Generate comprehensive habitat protection report"""
        
        health_assessment = self.assess_habitat_health(habitat_type, monitoring_data, location)
        
        if not health_assessment:
            return None
        
        return {
            "report_type": "habitat_protection_assessment",
            "location": location,
            "habitat_type": habitat_type.value,
            "generated_date": datetime.utcnow().isoformat(),
            "summary": {
                "health_status": health_assessment["health_status"],
                "risk_level": health_assessment["risk_level"],
                "carbon_storage_potential": health_assessment["carbon_storage_potential"],
                "biodiversity_value": health_assessment["biodiversity_value"]
            },
            "detailed_assessment": health_assessment,
            "conservation_priorities": self._prioritize_conservation_actions(health_assessment),
            "monitoring_plan": self._generate_monitoring_plan(habitat_type, health_assessment),
            "stakeholder_actions": self._get_stakeholder_actions(health_assessment),
            "funding_requirements": self._estimate_funding_requirements(health_assessment)
        }

    def _prioritize_conservation_actions(self, health_assessment: Dict) -> List[Dict]:
        """Prioritize conservation actions based on assessment"""
        
        priorities = []
        
        # Critical actions first
        if health_assessment["health_status"] == "critical":
            priorities.append({
                "priority": "immediate",
                "action": "Emergency habitat protection",
                "timeline": "Within 24 hours",
                "resources_needed": "Emergency response team, protection equipment"
            })
        
        # High priority threats
        for threat in health_assessment["threats"]:
            if threat["level"] in ["high", "critical"]:
                priorities.append({
                    "priority": "high",
                    "action": f"Mitigate {threat['description']}",
                    "timeline": "Within 1 week",
                    "resources_needed": threat["mitigation"]
                })
        
        # Medium priority actions
        if health_assessment["health_status"] in ["poor", "fair"]:
            priorities.append({
                "priority": "medium",
                "action": "Habitat restoration planning",
                "timeline": "Within 1 month",
                "resources_needed": "Restoration specialists, planning resources"
            })
        
        return priorities

    def _generate_monitoring_plan(self, 
                                 habitat_type: HabitatType,
                                 health_assessment: Dict) -> Dict:
        """Generate monitoring plan for the habitat"""
        
        frequency = health_assessment["monitoring_frequency"]
        indicators = health_assessment["monitoring_indicators"]
        
        return {
            "monitoring_frequency": frequency,
            "key_indicators": indicators,
            "monitoring_protocols": self.monitoring_protocols[frequency],
            "data_collection_methods": self._get_data_collection_methods(habitat_type, indicators),
            "quality_control": "Standardized protocols, trained personnel, regular calibration",
            "reporting_schedule": f"Reports due every {frequency}",
            "stakeholder_notifications": "Immediate for critical issues, weekly for high priority"
        }

    def _get_data_collection_methods(self, 
                                   habitat_type: HabitatType,
                                   indicators: List[str]) -> Dict:
        """Get data collection methods for monitoring indicators"""
        
        methods = {
            "tree_density": "Systematic sampling plots, drone surveys",
            "coral_cover": "Underwater transects, photo-quadrats",
            "water_quality": "Water sampling, sensors, laboratory analysis",
            "fish_population": "Underwater visual census, net sampling",
            "vegetation_cover": "Aerial photography, ground surveys",
            "species_richness": "Biodiversity surveys, species identification"
        }
        
        return {indicator: methods.get(indicator, "Standard field methods") for indicator in indicators}

    def _get_stakeholder_actions(self, health_assessment: Dict) -> Dict:
        """Get actions for different stakeholder groups"""
        
        return {
            "environmental_ngos": [
                "Conduct detailed habitat assessments",
                "Implement conservation programs",
                "Engage local communities",
                "Advocate for habitat protection"
            ],
            "government_agencies": [
                "Enforce protection regulations",
                "Provide funding for conservation",
                "Coordinate multi-stakeholder efforts",
                "Establish protected areas"
            ],
            "local_communities": [
                "Participate in monitoring programs",
                "Support conservation initiatives",
                "Report threats and violations",
                "Engage in habitat restoration"
            ],
            "scientific_institutions": [
                "Conduct research on habitat health",
                "Develop monitoring protocols",
                "Train monitoring personnel",
                "Provide technical expertise"
            ]
        }

    def _estimate_funding_requirements(self, health_assessment: Dict) -> Dict:
        """Estimate funding requirements for conservation activities"""
        
        base_funding = {
            "excellent": 5000,
            "good": 10000,
            "fair": 25000,
            "poor": 50000,
            "critical": 100000
        }
        
        health_status = health_assessment["health_status"]
        base_amount = base_funding.get(health_status, 25000)
        
        # Adjust for risk level
        risk_multiplier = {
            "low": 1.0,
            "medium": 1.5,
            "high": 2.0,
            "critical": 3.0
        }
        
        risk_level = health_assessment["risk_level"]
        adjusted_amount = base_amount * risk_multiplier.get(risk_level, 1.5)
        
        return {
            "annual_funding_required": adjusted_amount,
            "funding_breakdown": {
                "monitoring": adjusted_amount * 0.3,
                "conservation_actions": adjusted_amount * 0.4,
                "restoration": adjusted_amount * 0.2,
                "community_engagement": adjusted_amount * 0.1
            },
            "funding_sources": [
                "Government grants",
                "International conservation funds",
                "Private foundations",
                "Corporate social responsibility",
                "Community fundraising"
            ]
        }
