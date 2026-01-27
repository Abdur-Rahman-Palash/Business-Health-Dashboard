/**
 * Environment detection utilities
 */

export const isLocalDevelopment = (): boolean => {
  if (typeof window !== 'undefined') {
    return window.location.hostname === 'localhost';
  }
  
  if (typeof process !== 'undefined') {
    return process.env.NODE_ENV === 'development';
  }
  
  return false;
};

export const getStreamlitUrl = (): string => {
  return isLocalDevelopment() 
    ? 'http://localhost:8501'
    : 'https://business-health-dashboard-1.onrender.com';
};

export const getApiBaseUrl = (): string => {
  return isLocalDevelopment()
    ? 'http://localhost:8501'
    : 'https://business-health-dashboard-1.onrender.com';
};
