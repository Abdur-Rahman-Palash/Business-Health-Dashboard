// API Configuration for different environments
export const API_CONFIG = {
  // Development environment - disabled for Streamlit
  development: {
    baseURL: 'http://localhost:3002/api', // Use local Next.js API
    timeout: 10000,
  },
  
  // Production Vercel (Serverless Functions)
  vercel: {
    baseURL: 'https://executive-dashboard.vercel.app/api',
    timeout: 10000,
  },
  
  // Production with separate backend (Render) - disabled
  production: {
    baseURL: 'http://localhost:3002/api', // Use local Next.js API
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
    if (hostname.includes('onrender.com')) return 'production';
    if (hostname.includes('executive-dashboard.com')) return 'production';
    return 'production'; // Default to production for other domains
  }
  
  // For server-side rendering, check if we're in development
  if (typeof process !== 'undefined' && process.env.NODE_ENV === 'development') {
    return 'development';
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
