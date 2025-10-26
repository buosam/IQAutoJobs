import { NextRequest, NextResponse } from 'next/server'

// Mock data for recent jobs
const mockRecentJobs = [
  {
    id: "1",
    title: "Senior Frontend Developer",
    company: {
      name: "TechCorp",
      logo_url: "https://via.placeholder.com/40x40?text=TC"
    },
    location: "San Francisco, CA",
    type: "FT",
    category: "Engineering",
    description: "We are looking for a Senior Frontend Developer to join our team and help build amazing user experiences.",
    salary_min: 120000,
    salary_max: 180000,
    currency: "USD",
    created_at: new Date().toISOString()
  },
  {
    id: "2", 
    title: "Product Manager",
    company: {
      name: "InnovateCo",
      logo_url: "https://via.placeholder.com/40x40?text=IC"
    },
    location: "New York, NY",
    type: "FT",
    category: "Product",
    description: "Join our product team and help shape the future of our platform.",
    salary_min: 130000,
    salary_max: 170000,
    currency: "USD",
    created_at: new Date(Date.now() - 86400000).toISOString()
  },
  {
    id: "3",
    title: "UX Designer",
    company: {
      name: "DesignStudio",
      logo_url: "https://via.placeholder.com/40x40?text=DS"
    },
    location: "Remote",
    type: "FT",
    category: "Design",
    description: "Looking for a talented UX Designer to create beautiful and intuitive user interfaces.",
    salary_min: 90000,
    salary_max: 140000,
    currency: "USD",
    created_at: new Date(Date.now() - 172800000).toISOString()
  },
  {
    id: "4",
    title: "Backend Engineer",
    company: {
      name: "ServerTech",
      logo_url: "https://via.placeholder.com/40x40?text=ST"
    },
    location: "Austin, TX",
    type: "FT",
    category: "Engineering",
    description: "Help us build scalable backend systems that power our platform.",
    salary_min: 110000,
    salary_max: 160000,
    currency: "USD",
    created_at: new Date(Date.now() - 259200000).toISOString()
  },
  {
    id: "5",
    title: "Marketing Specialist",
    company: {
      name: "GrowthCo",
      logo_url: "https://via.placeholder.com/40x40?text=GC"
    },
    location: "Chicago, IL",
    type: "FT",
    category: "Marketing",
    description: "Join our marketing team and help drive user acquisition and engagement.",
    salary_min: 70000,
    salary_max: 100000,
    currency: "USD",
    created_at: new Date(Date.now() - 345600000).toISOString()
  },
  {
    id: "6",
    title: "Data Scientist",
    company: {
      name: "DataCorp",
      logo_url: "https://via.placeholder.com/40x40?text=DC"
    },
    location: "Seattle, WA",
    type: "FT",
    category: "Data Science",
    description: "Looking for a Data Scientist to help us derive insights from our data and build ML models.",
    salary_min: 125000,
    salary_max: 175000,
    currency: "USD",
    created_at: new Date(Date.now() - 432000000).toISOString()
  }
]

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get('limit') || '6')
    
    // Return limited number of recent jobs
    const recentJobs = mockRecentJobs.slice(0, limit)
    
    return NextResponse.json(recentJobs)
  } catch (error) {
    console.error('Error fetching recent jobs:', error)
    return NextResponse.json(
      { error: 'Failed to fetch recent jobs' },
      { status: 500 }
    )
  }
}