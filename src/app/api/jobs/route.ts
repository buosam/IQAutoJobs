import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    
    const response = await fetch(`${BACKEND_URL}/api/jobs/?${searchParams.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    const data = await response.json()
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Jobs fetch error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch jobs' },
      { status: 500 }
    )
  }
}
