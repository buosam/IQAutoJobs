import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const cookieStore = await cookies()
    const accessToken = cookieStore.get('access_token')

    if (!accessToken) {
      return NextResponse.json(
        { error: { message: 'Authentication required' } },
        { status: 401 }
      )
    }

    // Forward the multipart form data directly
    const formData = await request.formData()

    const response = await fetch(`${BACKEND_URL}/api/files/cv`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken.value}`,
      },
      body: formData
    })

    const data = await response.json()

    if (!response.ok) {
      return NextResponse.json(data, { status: response.status })
    }

    return NextResponse.json(data)
  } catch (error) {
    console.error('CV upload error:', error)
    return NextResponse.json(
      { error: { message: 'Failed to upload CV' } },
      { status: 500 }
    )
  }
}
