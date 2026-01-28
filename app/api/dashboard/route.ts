import { NextResponse } from 'next/server';

export const dynamic = 'force-static';

export async function GET() {
  try {
    return NextResponse.json({
      message: 'Dashboard API is working',
      timestamp: new Date().toISOString(),
      success: true,
      features: {
        languageDetection: true,
        bilingualSupport: true,
        kpiAnalysis: true,
        recommendations: true
      }
    });
  } catch (error: unknown) {
    console.error('Dashboard API Error:', error);
    return NextResponse.json(
      { 
        error: 'Dashboard API failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const data = await request.json();
    
    // Simple language detection for static export
    const companyName = data.company?.name || '';
    const isBangladeshi = companyName.toLowerCase().includes('bangladesh') || 
                         companyName.toLowerCase().includes('dhaka') ||
                         companyName.toLowerCase().includes('garments') ||
                         companyName.includes('লিমিটেড');
    
    const language = isBangladeshi ? 'bn' : 'en';
    
    return NextResponse.json({
      language: language,
      confidence: 0.8,
      is_bangladeshi: isBangladeshi,
      company_info: data.company,
      timestamp: new Date().toISOString()
    });
  } catch (error: unknown) {
    console.error('Dashboard POST Error:', error);
    return NextResponse.json(
      { 
        error: 'Dashboard POST failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
