import { 
  KPIData, 
  Insight, 
  RiskIndicator, 
  Recommendation, 
  ExecutiveSummary, 
  BusinessHealthScore,
  DashboardData,
  KPIDataResponse,
  InsightsResponse,
  RecommendationsResponse,
  ExecutiveSummaryResponse,
  APIResponse
} from '@/types/business';
import { calculateHealthStatus } from '@/lib/business-logic/thresholds';
import { generateInsights } from '@/lib/business-logic/insight-rules';

// Mock API Layer for Executive Business Health Dashboard
// Simulates real backend API with realistic business data

// Mock KPI Data with realistic business scenarios
// We calculate health status dynamically based on thresholds to ensure consistency
const rawKPIData: Omit<KPIData, 'healthStatus'>[] = [
  {
    id: 'revenue',
    currentValue: 850000,
    previousValue: 920000,
    targetValue: 1000000,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 880000 },
      { period: '2024-09', value: 910000 },
      { period: '2024-10', value: 920000 },
      { period: '2024-11', value: 890000 },
      { period: '2024-12', value: 850000 }
    ]
  },
  {
    id: 'revenue-growth',
    currentValue: 8.5,
    previousValue: 12.3,
    targetValue: 15.0,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 15.2 },
      { period: '2024-09', value: 14.8 },
      { period: '2024-10', value: 13.1 },
      { period: '2024-11', value: 11.5 },
      { period: '2024-12', value: 8.5 }
    ]
  },
  {
    id: 'profit-margin',
    currentValue: 12.8,
    previousValue: 14.2,
    targetValue: 18.0,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 15.1 },
      { period: '2024-09', value: 14.8 },
      { period: '2024-10', value: 14.2 },
      { period: '2024-11', value: 13.5 },
      { period: '2024-12', value: 12.8 }
    ]
  },
  {
    id: 'expense-ratio',
    currentValue: 87.2,
    previousValue: 85.8,
    targetValue: 75.0,
    trend: 'up',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 84.9 },
      { period: '2024-09', value: 85.2 },
      { period: '2024-10', value: 85.8 },
      { period: '2024-11', value: 86.5 },
      { period: '2024-12', value: 87.2 }
    ]
  },
  {
    id: 'customer-health',
    currentValue: 72.5,
    previousValue: 78.3,
    targetValue: 85.0,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 82.1 },
      { period: '2024-09', value: 80.5 },
      { period: '2024-10', value: 78.3 },
      { period: '2024-11', value: 75.8 },
      { period: '2024-12', value: 72.5 }
    ]
  },
  {
    id: 'churn-rate',
    currentValue: 6.2,
    previousValue: 5.8,
    targetValue: 5.0,
    trend: 'up',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 5.1 },
      { period: '2024-09', value: 5.4 },
      { period: '2024-10', value: 5.8 },
      { period: '2024-11', value: 6.0 },
      { period: '2024-12', value: 6.2 }
    ]
  },
  {
    id: 'clv',
    currentValue: 4200,
    previousValue: 4250,
    targetValue: 5000,
    trend: 'stable',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 4100 },
      { period: '2024-09', value: 4150 },
      { period: '2024-10', value: 4200 },
      { period: '2024-11', value: 4250 },
      { period: '2024-12', value: 4200 }
    ]
  },
  {
    id: 'cac',
    currentValue: 850,
    previousValue: 820,
    targetValue: 600,
    trend: 'up',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 780 },
      { period: '2024-09', value: 800 },
      { period: '2024-10', value: 820 },
      { period: '2024-11', value: 835 },
      { period: '2024-12', value: 850 }
    ]
  },
  {
    id: 'ltv-cac-ratio',
    currentValue: 4.94,
    previousValue: 5.18,
    targetValue: 3.0,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 5.26 },
      { period: '2024-09', value: 5.19 },
      { period: '2024-10', value: 5.18 },
      { period: '2024-11', value: 5.09 },
      { period: '2024-12', value: 4.94 }
    ]
  },
  {
    id: 'mrr',
    currentValue: 125000,
    previousValue: 132000,
    targetValue: 150000,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 128000 },
      { period: '2024-09', value: 130000 },
      { period: '2024-10', value: 132000 },
      { period: '2024-11', value: 128500 },
      { period: '2024-12', value: 125000 }
    ]
  },
  {
    id: 'arr',
    currentValue: 1500000,
    previousValue: 1584000,
    targetValue: 1800000,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 1536000 },
      { period: '2024-09', value: 1560000 },
      { period: '2024-10', value: 1584000 },
      { period: '2024-11', value: 1542000 },
      { period: '2024-12', value: 1500000 }
    ]
  },
  {
    id: 'nps',
    currentValue: 42,
    previousValue: 48,
    targetValue: 50,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 52 },
      { period: '2024-09', value: 50 },
      { period: '2024-10', value: 48 },
      { period: '2024-11', value: 45 },
      { period: '2024-12', value: 42 }
    ]
  },
  {
    id: 'csat',
    currentValue: 78,
    previousValue: 82,
    targetValue: 85,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 85 },
      { period: '2024-09', value: 83 },
      { period: '2024-10', value: 82 },
      { period: '2024-11', value: 80 },
      { period: '2024-12', value: 78 }
    ]
  },
  {
    id: 'operational-efficiency',
    currentValue: 68,
    previousValue: 72,
    targetValue: 80,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 75 },
      { period: '2024-09', value: 73 },
      { period: '2024-10', value: 72 },
      { period: '2024-11', value: 70 },
      { period: '2024-12', value: 68 }
    ]
  },
  {
    id: 'employee-satisfaction',
    currentValue: 71,
    previousValue: 74,
    targetValue: 80,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 76 },
      { period: '2024-09', value: 75 },
      { period: '2024-10', value: 74 },
      { period: '2024-11', value: 72 },
      { period: '2024-12', value: 71 }
    ]
  },
  {
    id: 'market-share',
    currentValue: 12.5,
    previousValue: 13.2,
    targetValue: 15.0,
    trend: 'down',
    lastUpdated: '2026-01-13T05:00:00Z',
    historicalValues: [
      { period: '2024-08', value: 13.8 },
      { period: '2024-09', value: 13.5 },
      { period: '2024-10', value: 13.2 },
      { period: '2024-11', value: 12.8 },
      { period: '2024-12', value: 12.5 }
    ]
  }
];

const mockKPIData: KPIData[] = rawKPIData.map(kpi => ({
  ...kpi,
  healthStatus: calculateHealthStatus(kpi.id, kpi.currentValue)
}));

// Generate insights from mock KPI data
const mockInsights: Insight[] = generateInsights(mockKPIData);

// Mock Risk Indicators
const mockRiskIndicators: RiskIndicator[] = [
  {
    id: 'risk-1',
    kpiId: 'revenue',
    status: 'warning',
    title: 'Revenue Decline Risk',
    explanation: 'Revenue has declined for 2 consecutive months, indicating potential market share loss or demand reduction.',
    thresholdLogic: 'Revenue below $900K for 2+ months triggers warning status',
    consecutivePeriods: 2,
    severity: 'medium'
  },
  {
    id: 'risk-2',
    kpiId: 'profit-margin',
    status: 'warning',
    title: 'Margin Erosion Risk',
    explanation: 'Profit margin below 15% for 2 consecutive months indicates pricing pressure or cost structure issues.',
    thresholdLogic: 'Profit margin below 15% for 2+ months triggers warning status',
    consecutivePeriods: 2,
    severity: 'medium'
  },
  {
    id: 'risk-3',
    kpiId: 'customer-health',
    status: 'warning',
    title: 'Customer Satisfaction Risk',
    explanation: 'Customer health score below 75% indicates potential churn risk and brand reputation impact.',
    thresholdLogic: 'Customer health below 75% triggers warning status',
    consecutivePeriods: 1,
    severity: 'high'
  },
  {
    id: 'risk-4',
    kpiId: 'churn-rate',
    status: 'warning',
    title: 'Elevated Churn Rate',
    explanation: 'Churn rate has exceeded the 5% threshold, indicating increasing customer attrition.',
    thresholdLogic: 'Churn rate > 5% triggers warning status',
    consecutivePeriods: 1,
    severity: 'high'
  }
];

// Mock Recommendations
const mockRecommendations: Recommendation[] = [
  {
    id: 'rec-1',
    insightId: mockInsights[0]?.id || 'insight-1',
    kpiId: 'revenue',
    title: 'Accelerate Sales Pipeline',
    description: 'Implement targeted sales initiatives to reverse revenue decline and achieve quarterly targets.',
    actionType: 'increase',
    expectedImpact: '5-10% revenue increase within 2 quarters',
    timeframe: 'short-term',
    effort: 'medium',
    confidence: 'high'
  },
  {
    id: 'rec-2',
    insightId: mockInsights[1]?.id || 'insight-2',
    kpiId: 'profit-margin',
    title: 'Optimize Cost Structure',
    description: 'Review and optimize major expense categories to improve profit margins to healthy levels.',
    actionType: 'reduce',
    expectedImpact: '2-3% margin improvement within 6 months',
    timeframe: 'short-term',
    effort: 'high',
    confidence: 'medium'
  },
  {
    id: 'rec-3',
    insightId: mockInsights[2]?.id || 'insight-3',
    kpiId: 'customer-health',
    title: 'Customer Success Initiative',
    description: 'Launch comprehensive customer success program to improve satisfaction and reduce churn.',
    actionType: 'prioritize',
    expectedImpact: '10-15 point improvement in customer health score',
    timeframe: 'short-term',
    effort: 'medium',
    confidence: 'high'
  }
];

// Mock Business Health Score
const mockBusinessHealthScore: BusinessHealthScore = {
  overall: 68,
  financial: 65,
  operational: 70,
  customer: 68,
  status: 'warning',
  factors: [
    { category: 'Revenue Growth', score: 55, weight: 0.2 },
    { category: 'Profitability', score: 65, weight: 0.2 },
    { category: 'Cost Efficiency', score: 70, weight: 0.2 },
    { category: 'Customer Satisfaction', score: 72, weight: 0.2 },
    { category: 'Churn Management', score: 58, weight: 0.1 },
    { category: 'Customer Lifetime Value', score: 75, weight: 0.1 }
  ]
};

// Mock Executive Summary
const mockExecutiveSummary: ExecutiveSummary = {
  id: 'exec-summary-1',
  period: 'Q4 2024',
  overallHealth: 'warning',
  keyHighlights: [
    'Revenue decline of 7.6% requires immediate attention',
    'Customer health score declining but still above critical threshold',
    'Cost structure needs optimization to protect margins'
  ],
  topRisks: [
    {
      title: 'Revenue Decline',
      description: 'Two consecutive months of revenue decline indicating market challenges',
      kpiId: 'revenue'
    },
    {
      title: 'Margin Pressure',
      description: 'Profit margins below healthy levels due to rising costs',
      kpiId: 'profit-margin'
    },
    {
      title: 'Customer Satisfaction',
      description: 'Declining customer health may lead to increased churn',
      kpiId: 'customer-health'
    }
  ],
  topOpportunities: [
    {
      title: 'Cost Optimization',
      description: 'Significant opportunity to improve margins through expense management',
      kpiId: 'expense-ratio'
    },
    {
      title: 'Customer Retention',
      description: 'Targeted customer success initiatives can significantly improve health scores',
      kpiId: 'customer-health'
    },
    {
      title: 'Sales Acceleration',
      description: 'Revitalized sales strategy could reverse revenue decline',
      kpiId: 'revenue'
    }
  ],
  narrative: 'Business health is in warning territory due to declining revenue and margins across multiple metrics. While customer satisfaction remains above critical levels, the downward trend requires immediate leadership attention. Key focus areas include sales pipeline acceleration, cost structure optimization, and customer success initiatives to stabilize performance and return to growth trajectory.',
  generatedAt: '2026-01-13T05:00:00Z'
};

// Complete Dashboard Data
const mockDashboardData: DashboardData = {
  kpis: mockKPIData,
  insights: mockInsights,
  risks: mockRiskIndicators,
  recommendations: mockRecommendations,
  executiveSummary: mockExecutiveSummary,
  businessHealthScore: mockBusinessHealthScore,
  lastUpdated: '2026-01-13T05:00:00Z'
};

// API Simulation Functions
export const mockAPI = {
  // Simulate network delay
  delay: (ms: number = 500) => new Promise(resolve => setTimeout(resolve, ms)),

  // Get all KPI data
  getKPIData: async (): Promise<KPIDataResponse> => {
    await mockAPI.delay(300);
    return {
      data: mockKPIData,
      success: true,
      timestamp: new Date().toISOString()
    };
  },

  // Get insights
  getInsights: async (): Promise<InsightsResponse> => {
    await mockAPI.delay(200);
    return {
      data: mockInsights,
      success: true,
      timestamp: new Date().toISOString()
    };
  },

  // Get recommendations
  getRecommendations: async (): Promise<RecommendationsResponse> => {
    await mockAPI.delay(250);
    return {
      data: mockRecommendations,
      success: true,
      timestamp: new Date().toISOString()
    };
  },

  // Get executive summary
  getExecutiveSummary: async (): Promise<ExecutiveSummaryResponse> => {
    await mockAPI.delay(400);
    return {
      data: mockExecutiveSummary,
      success: true,
      timestamp: new Date().toISOString()
    };
  },

  // Get complete dashboard data
  getDashboardData: async (): Promise<APIResponse<DashboardData>> => {
    await mockAPI.delay(600);
    return {
      data: mockDashboardData,
      success: true,
      timestamp: new Date().toISOString()
    };
  },

  // Update insight (for editing functionality)
  updateInsight: async (insightId: string, updates: Partial<Insight>): Promise<APIResponse<Insight>> => {
    await mockAPI.delay(300);
    const insightIndex = mockInsights.findIndex(i => i.id === insightId);
    if (insightIndex === -1) {
      return {
        data: {} as Insight,
        success: false,
        message: 'Insight not found',
        timestamp: new Date().toISOString()
      };
    }
    
    mockInsights[insightIndex] = { ...mockInsights[insightIndex], ...updates };
    return {
      data: mockInsights[insightIndex],
      success: true,
      timestamp: new Date().toISOString()
    };
  }
};

// Export mock data for testing and development
export {
  mockKPIData,
  mockInsights,
  mockRiskIndicators,
  mockRecommendations,
  mockExecutiveSummary,
  mockBusinessHealthScore,
  mockDashboardData
};
