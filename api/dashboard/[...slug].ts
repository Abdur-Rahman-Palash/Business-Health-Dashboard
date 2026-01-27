import { NextRequest, NextResponse } from 'next/server';

// Disable API proxy for Streamlit - use direct iframe instead
export async function GET(
  request: NextRequest,
  { params }: { params: { slug: string[] } }
) {
  return NextResponse.json(
    { 
      error: 'API proxy disabled for Streamlit. Please use direct iframe connection.',
      message: 'Streamlit dashboard is accessed via iframe, not API endpoints.'
    },
    { status: 404 }
  );
}

export async function POST(
  request: NextRequest,
  { params }: { params: { slug: string[] } }
) {
  return NextResponse.json(
    { 
      error: 'API proxy disabled for Streamlit. Please use direct iframe connection.',
      message: 'Streamlit dashboard is accessed via iframe, not API endpoints.'
    },
    { status: 404 }
  );
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
