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
