import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const returnTo = searchParams.get('returnTo') || '/dashboard'
    
    const backendUrl = new URL(`${BACKEND_URL}/api/oauth/google/login`)
    backendUrl.searchParams.set('returnTo', returnTo)
    
    return NextResponse.redirect(backendUrl.toString())
  } catch (error) {
    console.error('OAuth login redirect error:', error)
    return NextResponse.json(
      { error: { message: 'Failed to initiate Google OAuth' } },
      { status: 500 }
    )
  }
}
