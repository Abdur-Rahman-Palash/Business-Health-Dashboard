import { NextResponse } from 'next/server';

export const dynamic = 'force-static';

// Mock AI insights data
const mockInsights = [
  {
    id: '1',
    title: 'Revenue Growth Acceleration',
    description: 'Q4 revenue shows 23% growth compared to Q3, driven by new product launches',
    priority: 'high',
    category: 'financial',
    impact: 'high',
    confidence: 0.92,
    generated_at: new Date().toISOString()
  },
  {
    id: '2',
    title: 'Customer Retention Improvement',
    description: 'Customer churn rate decreased by 15% after implementing loyalty program',
    priority: 'medium',
    category: 'customer',
    impact: 'medium',
    confidence: 0.87,
    generated_at: new Date().toISOString()
  }
];

export async function GET() {
  try {
    const response = {
      data: mockInsights,
      success: true,
      timestamp: new Date().toISOString(),
      model: 'mock-ai-model'
    };
    
    return NextResponse.json(response);
  } catch (error: unknown) {
    console.error('AI Insights API Error:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to fetch AI insights',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
