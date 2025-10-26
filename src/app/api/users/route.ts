import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    
    const response = await fetch(`${BACKEND_URL}/api/public/users?${searchParams.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    const data = await response.json()
    
    // Wrap in users object if the backend returns an array directly
    const users = Array.isArray(data) ? data : data.users || data
    return NextResponse.json({ users }, { status: response.status })
  } catch (error) {
    console.error('Users fetch error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch users' },
      { status: 500 }
    )
  }
}
