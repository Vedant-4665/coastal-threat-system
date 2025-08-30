import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service object with all methods
export const apiService = {
  // Generic GET method
  async get(url) {
    try {
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      console.error('Error in API call:', error);
      throw error;
    }
  },

  // Get comprehensive data for a specific location
  async getDataForLocation(location) {
    try {
      const response = await api.get(`/data/${location}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching data for location:', error);
      throw error;
    }
  },

  // Get available coastal locations
  async getAvailableLocations() {
    try {
      const response = await api.get('/locations');
      return response.data;
    } catch (error) {
      console.error('Error fetching available locations:', error);
      throw error;
    }
  },

  // Get active alerts
  async getAlerts() {
    try {
      const response = await api.get('/alerts');
      return response.data;
    } catch (error) {
      console.error('Error fetching alerts:', error);
      throw error;
    }
  },

  // Deactivate an alert
  async deactivateAlert(alertId) {
    try {
      const response = await api.delete(`/alerts/${alertId}`);
      return response.data;
    } catch (error) {
      console.error('Error deactivating alert:', error);
      throw error;
    }
  },

  // Get demo data for presentation
  async getDemoData(location) {
    try {
      const response = await api.get(`/demo/${location}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching demo data:', error);
      throw error;
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },

  // Get system information
  async getSystemInfo() {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      console.error('Error fetching system info:', error);
      throw error;
    }
  }
};

// Export individual functions for backward compatibility
export const getDataForLocation = apiService.getDataForLocation;
export const getAvailableLocations = apiService.getAvailableLocations;
export const getAlerts = apiService.getAlerts;
export const deactivateAlert = apiService.deactivateAlert;
export const getDemoData = apiService.getDemoData;
export const healthCheck = apiService.healthCheck;
export const getSystemInfo = apiService.getSystemInfo;

// Disaster Management APIs
export const getStakeholderAlert = async (stakeholderType, location = 'mumbai') => {
  try {
    const response = await apiService.get(`/disaster-management/stakeholder-alert/${stakeholderType}?location=${location}`);
    return response;
  } catch (error) {
    console.error('Error fetching stakeholder alert:', error);
    throw error;
  }
};

export const getEmergencyCoordination = async (emergencyType, location = 'mumbai', severity = 'medium', affectedPopulation = 10000) => {
  try {
    const response = await apiService.get(`/disaster-management/coordination/${emergencyType}?location=${location}&severity=${severity}&affected_population=${affectedPopulation}`);
    return response;
  } catch (error) {
    console.error('Error fetching emergency coordination:', error);
    throw error;
  }
};

// Habitat Protection APIs
export const getHabitatAssessment = async (habitatType, location = 'mumbai') => {
  try {
    const response = await apiService.get(`/habitat-protection/assessment/${habitatType}?location=${location}`);
    return response;
  } catch (error) {
    console.error('Error fetching habitat assessment:', error);
    throw error;
  }
};

export const getHabitatProtectionReport = async (habitatType, location = 'mumbai') => {
  try {
    const response = await apiService.get(`/habitat-protection/report/${habitatType}?location=${location}`);
    return response;
  } catch (error) {
    console.error('Error fetching habitat protection report:', error);
    throw error;
  }
};

// Fisherfolk Safety APIs
export const getFishingZoneSafety = async (location = 'mumbai') => {
  try {
    const response = await apiService.get(`/fisherfolk-safety/zone-assessment?location=${location}`);
    return response;
  } catch (error) {
    console.error('Error fetching fishing zone safety:', error);
    throw error;
  }
};

export const getFishingSafetyReport = async (location = 'mumbai') => {
  try {
    const response = await apiService.get(`/fisherfolk-safety/report?location=${location}`);
    return response;
  } catch (error) {
    console.error('Error fetching fishing safety report:', error);
    throw error;
  }
};

// Civil Defence APIs
export const getCivilDefenceCoordination = async (emergencyType, location = 'mumbai', severity = 'medium', affectedPopulation = 10000) => {
  try {
    const response = await apiService.get(`/civil-defence/coordination/${emergencyType}?location=${location}&severity=${severity}&affected_population=${affectedPopulation}`);
    return response;
  } catch (error) {
    console.error('Error fetching civil defence coordination:', error);
    throw error;
  }
};

export const getCivilDefenceSummary = async (location = 'mumbai') => {
  try {
    const response = await apiService.get(`/civil-defence/summary?location=${location}`);
    return response;
  } catch (error) {
    console.error('Error fetching civil defence summary:', error);
    throw error;
  }
};

// Coastal Government APIs
export const getPolicyRecommendations = async (location = 'mumbai', stakeholderPriorities = 'economic_development,sustainable_development') => {
  try {
    const response = await apiService.get(`/coastal-government/policy-recommendations?location=${location}&stakeholder_priorities=${stakeholderPriorities}`);
    return response;
  } catch (error) {
    console.error('Error fetching policy recommendations:', error);
    throw error;
  }
};

export const getEconomicImpactAnalysis = async (sector, location = 'mumbai', policyChanges = 'sustainable_development,infrastructure_improvement') => {
  try {
    const response = await apiService.get(`/coastal-government/economic-impact/${sector}?location=${location}&policy_changes=${policyChanges}`);
    return response;
  } catch (error) {
    console.error('Error fetching economic impact analysis:', error);
    throw error;
  }
};

export const getCoastalGovernmentSummary = async (location = 'mumbai') => {
  try {
    const response = await apiService.get(`/coastal-government/summary?location=${location}`);
    return response;
  } catch (error) {
    console.error('Error fetching coastal government summary:', error);
    throw error;
  }
};

// Stakeholder Dashboard API
export const getStakeholderDashboard = async (stakeholderType, location = 'mumbai') => {
  try {
    const response = await apiService.get(`/stakeholder-dashboard/${stakeholderType}?location=${location}`);
    return response;
  } catch (error) {
    console.error('Error fetching stakeholder dashboard:', error);
    throw error;
  }
};
