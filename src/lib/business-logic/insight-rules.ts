import { InsightRule, KPIData, Insight, KPIId } from '@/types/business';
import { calculateHealthStatus } from './thresholds';

// Business Insight Generation Rules
// Uses What → So What → Now What framework for executive decision making

export const insightRules: InsightRule[] = [
  {
    id: 'revenue-decline',
    name: 'Revenue Decline Detection',
    kpiId: 'revenue',
    priority: 'high',
    condition: (data: KPIData) => {
      return data.trend === 'down' && data.healthStatus === 'warning';
    },
    generateInsight: (data: KPIData) => ({
      kpiId: data.id,
      title: 'Revenue Decline Detected',
      observation: `Revenue has decreased by ${((data.previousValue - data.currentValue) / data.previousValue * 100).toFixed(1)}% from the previous period.`,
      businessImpact: 'Declining revenue reduces cash flow, limits growth investments, and may indicate market share loss or competitive pressure.',
      action: 'Investigate sales pipeline, market conditions, and competitive positioning. Consider pricing strategy review and sales team performance analysis.',
      priority: 'high'
    })
  },
  
  {
    id: 'profit-margin-erosion',
    name: 'Profit Margin Erosion',
    kpiId: 'profit-margin',
    priority: 'high',
    condition: (data: KPIData) => {
      return data.trend === 'down' && data.currentValue < 15;
    },
    generateInsight: (data: KPIData) => ({
      kpiId: data.id,
      title: 'Profit Margin Under Pressure',
      observation: `Profit margin has declined to ${data.currentValue}%, below the healthy 15% threshold.`,
      businessImpact: 'Reduced profitability limits reinvestment capacity, increases business risk, and may indicate cost structure problems or pricing pressure.',
      action: 'Conduct comprehensive cost analysis, review pricing strategy, and identify efficiency opportunities. Consider product mix optimization.',
      priority: 'high'
    })
  },
  
  {
    id: 'expense-ratio-increase',
    name: 'Rising Expense Ratio',
    kpiId: 'expense-ratio',
    priority: 'medium',
    condition: (data: KPIData) => {
      return data.trend === 'up' && data.currentValue > 85;
    },
    generateInsight: (data: KPIData) => ({
      kpiId: data.id,
      title: 'Expense Ratio Rising',
      observation: `Expense ratio has increased to ${data.currentValue}%, consuming too much of revenue.`,
      businessImpact: 'High expense ratios squeeze profitability, reduce financial flexibility, and may indicate operational inefficiencies or overspending.',
      action: 'Review all major expense categories, implement cost control measures, and establish spending approval processes. Focus on high-ROI expenses.',
      priority: 'medium'
    })
  },
  
  {
    id: 'customer-health-decline',
    name: 'Customer Health Deterioration',
    kpiId: 'customer-health',
    priority: 'high',
    condition: (data: KPIData) => {
      return data.trend === 'down' && data.currentValue < 70;
    },
    generateInsight: (data: KPIData) => ({
      kpiId: data.id,
      title: 'Customer Satisfaction Declining',
      observation: `Customer health score has fallen to ${data.currentValue}, indicating satisfaction issues.`,
      businessImpact: 'Poor customer health leads to higher churn, increased acquisition costs, negative word-of-mouth, and reduced lifetime value.',
      action: 'Conduct customer satisfaction surveys, analyze support tickets, and review product/service quality. Implement customer success initiatives.',
      priority: 'high'
    })
  },
  
  {
    id: 'revenue-growth-slowdown',
    name: 'Revenue Growth Slowdown',
    kpiId: 'revenue-growth',
    priority: 'medium',
    condition: (data: KPIData) => {
      return data.trend === 'down' && data.currentValue < 10;
    },
    generateInsight: (data: KPIData) => ({
      kpiId: data.id,
      title: 'Growth Momentum Slowing',
      observation: `Revenue growth has slowed to ${data.currentValue}%, below healthy growth levels.`,
      businessImpact: 'Slowing growth may indicate market saturation, increased competition, or product-market fit issues. Limits future valuation and talent attraction.',
      action: 'Explore new market segments, innovate product offerings, and review go-to-market strategy. Consider strategic partnerships or acquisitions.',
      priority: 'medium'
    })
  },
  
  {
    id: 'critical-profit-margin',
    name: 'Critical Profit Margin',
    kpiId: 'profit-margin',
    priority: 'high',
    condition: (data: KPIData) => {
      return data.healthStatus === 'critical';
    },
    generateInsight: (data: KPIData) => ({
      kpiId: data.id,
      title: 'Critical Profit Margin Alert',
      observation: `Profit margin has reached critical levels at ${data.currentValue}%.`,
      businessImpact: 'Critical profit levels threaten business sustainability and may require immediate cost restructuring or pricing changes.',
      action: 'Immediate leadership intervention required. Conduct emergency cost review and consider strategic pricing changes. Evaluate business model viability.',
      priority: 'high'
    })
  },
  
  {
    id: 'excellent-revenue-growth',
    name: 'Excellent Revenue Growth',
    kpiId: 'revenue-growth',
    priority: 'medium',
    condition: (data: KPIData) => {
      return data.healthStatus === 'excellent' && data.trend === 'up';
    },
    generateInsight: (data: KPIData) => ({
      kpiId: data.id,
      title: 'Exceptional Growth Performance',
      observation: `Revenue growth is exceptional at ${data.currentValue}%, significantly outperforming targets.`,
      businessImpact: 'Strong growth momentum increases market share, attracts talent and investors, and provides resources for expansion.',
      action: 'Scale successful growth initiatives, invest in capacity expansion, and protect market position from competitors.',
      priority: 'medium'
    })
  }
];

// Generate insights for all KPI data
export const generateInsights = (kpiData: KPIData[]): Insight[] => {
  const insights: Insight[] = [];
  
  kpiData.forEach(data => {
    insightRules.forEach(rule => {
      if (rule.condition(data)) {
        const insightData = rule.generateInsight(data);
        insights.push({
          ...insightData,
          id: `${rule.id}-${data.id}-${Date.now()}`,
          generatedAt: new Date().toISOString(),
          isAutoGenerated: true
        });
      }
    });
  });
  
  // Sort by priority (high first) and then by KPI
  return insights.sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
};

// Get insights for specific KPI
export const getInsightsForKPI = (kpiId: KPIId, kpiData: KPIData[]): Insight[] => {
  const data = kpiData.find(kpi => kpi.id === kpiId);
  if (!data) return [];
  
  const insights: Insight[] = [];
  
  insightRules.forEach(rule => {
    if (rule.kpiId === kpiId && rule.condition(data)) {
      const insightData = rule.generateInsight(data);
      insights.push({
        ...insightData,
        id: `${rule.id}-${data.id}-${Date.now()}`,
        generatedAt: new Date().toISOString(),
        isAutoGenerated: true
      });
    }
  });
  
  return insights;
};
