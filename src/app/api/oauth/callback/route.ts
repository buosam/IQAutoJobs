import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const access_token = searchParams.get('access_token')
    const refresh_token = searchParams.get('refresh_token')
    const returnTo = searchParams.get('returnTo') || '/dashboard'
    
    if (!access_token || !refresh_token) {
      return NextResponse.redirect(new URL('/auth/login?error=oauth_failed', request.url))
    }
    
    const response = NextResponse.redirect(new URL(returnTo, request.url))
    
    response.cookies.set('access_token', access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 15,
      path: '/',
    })
    
    response.cookies.set('refresh_token', refresh_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7,
      path: '/',
    })
    
    return response
  } catch (error) {
    console.error('OAuth callback error:', error)
    return NextResponse.redirect(new URL('/auth/login?error=oauth_failed', request.url))
  }
}
