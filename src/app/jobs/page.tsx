"use client"

import { useState, useEffect, Suspense } from "react"
import { useSearchParams } from "next/navigation"
import { Search, MapPin, Briefcase, Filter, Grid, List } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { JobCard } from "@/components/job-card"
import { JobFilters } from "@/components/job-filters"
import { Pagination } from "@/components/pagination"

interface Job {
  id: string
  title: string
  company: {
    name: string
    logo_url?: string
    id: string
  }
  location: string
  type: string
  category: string
  description: string
  salary_min?: number
  salary_max?: number
  currency: string
  created_at: string
  slug: string
  status: string
}

interface JobSearchResponse {
  jobs: Job[]
  total: number
  page: number
  size: number
  pages: number
}

export default function JobsPage() {
  const searchParams = useSearchParams()
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    size: 20,
    pages: 0
  })

  // Get filter values from URL
  const search = searchParams.get("search") || ""
  const location = searchParams.get("location") || ""
  const type = searchParams.get("type") || ""
  const category = searchParams.get("category") || ""
  const page = parseInt(searchParams.get("page") || "1")

  useEffect(() => {
    fetchJobs()
  }, [search, location, type, category, page])

  const fetchJobs = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (search) params.append("search", search)
      if (location) params.append("location", location)
      if (type) params.append("type", type)
      if (category) params.append("category", category)
      params.append("page", page.toString())
      params.append("size", "20")

      const response = await fetch(`/api/jobs?${params}`)
      if (response.ok) {
        const data: JobSearchResponse = await response.json()
        setJobs(data.jobs)
        setPagination({
          total: data.total,
          page: data.page,
          size: data.size,
          pages: data.pages
        })
      }
    } catch (error) {
      console.error("Failed to fetch jobs:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    const searchQuery = formData.get("search") as string
    const locationQuery = formData.get("location") as string
    
    const params = new URLSearchParams(searchParams)
    if (searchQuery) {
      params.set("search", searchQuery)
    } else {
      params.delete("search")
    }
    if (locationQuery) {
      params.set("location", locationQuery)
    } else {
      params.delete("location")
    }
    params.set("page", "1")
    
    window.location.href = `/jobs?${params.toString()}`
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <section className="bg-muted/50 py-8 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-6">
            <h1 className="text-3xl font-bold mb-2">Find Your Perfect Job</h1>
            <p className="text-muted-foreground">
              Browse through thousands of opportunities from top companies
            </p>
          </div>
          
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="flex flex-col sm:flex-row gap-2 p-2 bg-background rounded-lg shadow-sm">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                <Input
                  type="text"
                  name="search"
                  placeholder="Search jobs, companies, or keywords..."
                  defaultValue={search}
                  className="pl-10 border-0"
                />
              </div>
              <div className="flex-1 relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                <Input
                  type="text"
                  name="location"
                  placeholder="Location..."
                  defaultValue={location}
                  className="pl-10 border-0"
                />
              </div>
              <Button type="submit">Search</Button>
            </div>
          </form>
        </div>
      </section>

      <div className="container mx-auto max-w-6xl py-8 px-4">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filters Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            <JobFilters />
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Header with view toggle */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-semibold">
                  {search || location ? "Search Results" : "All Jobs"}
                </h2>
                <p className="text-sm text-muted-foreground">
                  {pagination.total} jobs found
                </p>
              </div>
              
              <div className="flex items-center gap-2">
                <Button
                  variant={viewMode === "grid" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setViewMode("grid")}
                >
                  <Grid className="h-4 w-4" />
                </Button>
                <Button
                  variant={viewMode === "list" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setViewMode("list")}
                >
                  <List className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Jobs Grid/List */}
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <Card key={i} className="animate-pulse">
                    <CardContent className="p-6">
                      <div className="h-4 bg-muted rounded w-3/4 mb-2"></div>
                      <div className="h-3 bg-muted rounded w-1/2 mb-4"></div>
                      <div className="h-3 bg-muted rounded w-full mb-2"></div>
                      <div className="h-3 bg-muted rounded w-full"></div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : jobs.length > 0 ? (
              <div className={
                viewMode === "grid" 
                  ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                  : "space-y-4"
              }>
                {jobs.map((job) => (
                  <JobCard key={job.id} job={job} />
                ))}
              </div>
            ) : (
              <Card className="text-center py-12">
                <CardContent>
                  <Briefcase className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No jobs found</h3>
                  <p className="text-muted-foreground mb-4">
                    Try adjusting your search criteria or check back later for new opportunities.
                  </p>
                  <Button onClick={() => window.location.href = "/jobs"}>
                    Clear Filters
                  </Button>
                </CardContent>
              </Card>
            )}

            {/* Pagination */}
            {pagination.pages > 1 && (
              <div className="mt-8">
                <Pagination
                  currentPage={pagination.page}
                  totalPages={pagination.pages}
                  onPageChange={(newPage) => {
                    const params = new URLSearchParams(searchParams)
                    params.set("page", newPage.toString())
                    window.location.href = `/jobs?${params.toString()}`
                  }}
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}