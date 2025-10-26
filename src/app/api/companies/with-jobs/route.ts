import { NextRequest, NextResponse } from 'next/server'

// Mock data for featured companies
const mockFeaturedCompanies = [
  {
    id: "1",
    name: "TechCorp",
    logo_url: "https://via.placeholder.com/80x80?text=TC",
    industry: "Technology",
    location: "San Francisco, CA",
    description: "Leading technology company focused on building innovative solutions for the future."
  },
  {
    id: "2",
    name: "InnovateCo",
    logo_url: "https://via.placeholder.com/80x80?text=IC",
    industry: "Software",
    location: "New York, NY",
    description: "Fast-growing software company that's changing the way businesses operate."
  },
  {
    id: "3",
    name: "DesignStudio",
    logo_url: "https://via.placeholder.com/80x80?text=DS",
    industry: "Design",
    location: "Remote",
    description: "Creative design studio specializing in user experience and interface design."
  },
  {
    id: "4",
    name: "ServerTech",
    logo_url: "https://via.placeholder.com/80x80?text=ST",
    industry: "Cloud Infrastructure",
    location: "Austin, TX",
    description: "Enterprise-grade cloud infrastructure and server solutions provider."
  }
]

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get('limit') || '4')
    
    // Return limited number of featured companies
    const featuredCompanies = mockFeaturedCompanies.slice(0, limit)
    
    return NextResponse.json(featuredCompanies)
  } catch (error) {
    console.error('Error fetching featured companies:', error)
    return NextResponse.json(
      { error: 'Failed to fetch featured companies' },
      { status: 500 }
    )
  }
}