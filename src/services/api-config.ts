// API Configuration for different environments
export const API_CONFIG = {
  // Development environment
  development: {
    baseURL: 'http://localhost:8001',
    timeout: 10000,
  },
  
  // Production Vercel (Serverless Functions)
  vercel: {
    baseURL: 'https://executive-dashboard.vercel.app/api',
    timeout: 10000,
  },
  
  // Production with separate backend
  production: {
    baseURL: 'https://your-backend-domain.com',
    timeout: 10000,
  },
  
  // Hostinger (same domain)
  hostinger: {
    baseURL: '/api',
    timeout: 10000,
  },
};

// Get current environment
const getEnvironment = (): keyof typeof API_CONFIG => {
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    
    if (hostname === 'localhost') return 'development';
    if (hostname.includes('vercel.app')) return 'vercel';
    if (hostname.includes('executive-dashboard.com')) return 'production';
    return 'hostinger'; // Default for other domains
  }
  
  return 'development';
};

// Export current API config
export const currentAPIConfig = API_CONFIG[getEnvironment()];

// API endpoints
export const API_ENDPOINTS = {
  health: '/health',
  dashboard: '/api/dashboard/complete',
  refresh: '/api/dashboard/refresh',
  aiInsights: '/api/ai/insights',
  aiSummary: '/api/ai/executive-summary',
  customerSegments: '/api/analytics/customer-segments',
  revenueTrends: '/api/analytics/revenue-trends',
  expenseBreakdown: '/api/analytics/expense-breakdown',
} as const;

// Helper function to get full URL
export const getAPIUrl = (endpoint: string): string => {
  return `${currentAPIConfig.baseURL}${endpoint}`;
};
