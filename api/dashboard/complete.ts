import { NextResponse } from 'next/server';

// Mock data for dashboard
const mockDashboardData = {
  kpis: [
    {
      id: 'revenue',
      name: 'Total Revenue',
      value: 1250000,
      change: 12.5,
      trend: 'up',
      category: 'financial',
      unit: 'USD',
      target: 1500000,
      status: 'good'
    },
    {
      id: 'customers',
      name: 'Active Customers',
      value: 8420,
      change: 8.2,
      trend: 'up',
      category: 'customer',
      unit: 'count',
      target: 10000,
      status: 'good'
    },
    {
      id: 'profit-margin',
      name: 'Profit Margin',
      value: 18.5,
      change: -2.1,
      trend: 'down',
      category: 'financial',
      unit: '%',
      target: 20,
      status: 'warning'
    }
  ],
  insights: [
    {
      id: '1',
      title: 'Revenue Growth Opportunity',
      description: 'Customer acquisition costs are 15% lower than industry average',
      priority: 'high',
      category: 'growth',
      impact: 'high',
      effort: 'medium'
    }
  ],
  recommendations: [
    {
      id: '1',
      title: 'Optimize Marketing Spend',
      description: 'Reallocate 20% of marketing budget to high-performing channels',
      priority: 'high',
      category: 'marketing',
      expectedImpact: '15% increase in ROI'
    }
  ]
};

export async function GET() {
  try {
    return NextResponse.json({
      data: mockDashboardData,
      success: true,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to fetch dashboard data'
      },
      { status: 500 }
    );
  }
}
