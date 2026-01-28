import { NextResponse } from 'next/server';

export const dynamic = 'force-static';

export async function GET() {
  try {
    console.log('Test API route called');
    
    return NextResponse.json({
      message: 'API is working',
      timestamp: new Date().toISOString(),
      success: true
    });
  } catch (error: unknown) {
    console.error('Test API Error:', error);
    return NextResponse.json(
      { 
        error: 'Test API failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
