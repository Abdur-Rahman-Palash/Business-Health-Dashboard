// Simple API client that uses local mock data
import { mockAPI } from './mock-api';

export const apiClient = {
  // Get dashboard data
  getDashboardData: async () => {
    try {
      const response = await mockAPI.getDashboardData();
      return response;
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        message: 'Failed to fetch dashboard data',
        data: null,
        timestamp: new Date().toISOString()
      };
    }
  },

  // Get KPI data
  getKPIData: async () => {
    try {
      const response = await mockAPI.getKPIData();
      return response;
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        message: 'Failed to fetch KPI data',
        data: [],
        timestamp: new Date().toISOString()
      };
    }
  },

  // Get insights
  getInsights: async () => {
    try {
      const response = await mockAPI.getInsights();
      return response;
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        message: 'Failed to fetch insights',
        data: [],
        timestamp: new Date().toISOString()
      };
    }
  },

  // Get recommendations
  getRecommendations: async () => {
    try {
      const response = await mockAPI.getRecommendations();
      return response;
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        message: 'Failed to fetch recommendations',
        data: [],
        timestamp: new Date().toISOString()
      };
    }
  },

  // Get executive summary
  getExecutiveSummary: async () => {
    try {
      const response = await mockAPI.getExecutiveSummary();
      return response;
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        message: 'Failed to fetch executive summary',
        data: null,
        timestamp: new Date().toISOString()
      };
    }
  }
};
