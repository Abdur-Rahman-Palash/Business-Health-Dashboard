import { NextResponse } from 'next/server';

export const dynamic = 'force-static';

// Mock executive summary data
const mockExecutiveSummary = {
  overall_health: 'good',
  health_score: 82,
  key_highlights: [
    'Revenue increased by 23% in Q4',
    'Customer satisfaction improved by 15%',
    'Operational efficiency up by 8%'
  ],
  key_concerns: [
    'Profit margin decreased by 2.1%',
    'Supply chain costs increased by 12%'
  ],
  recommendations: [
    'Focus on high-margin products',
    'Optimize supply chain operations',
    'Invest in customer retention programs'
  ],
  generated_at: new Date().toISOString()
};

export async function GET() {
  try {
    const response = {
      data: mockExecutiveSummary,
      success: true,
      timestamp: new Date().toISOString(),
      model: 'mock-ai-model'
    };
    
    return NextResponse.json(response);
  } catch (error: unknown) {
    console.error('Executive Summary API Error:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: 'Failed to fetch executive summary',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
