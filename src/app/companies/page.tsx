"use client"

import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { Search, Building2, MapPin, Grid, List } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { CompanyCard } from "@/components/company-card"
import { Pagination } from "@/components/pagination"

interface Company {
  id: string
  name: string
  logo_url?: string
  industry: string
  location: string
  description: string
}

export default function CompaniesPage() {
  const searchParams = useSearchParams()
  const [companies, setCompanies] = useState<Company[]>([])
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
  const industry = searchParams.get("industry") || ""
  const location = searchParams.get("location") || ""
  const page = parseInt(searchParams.get("page") || "1")

  useEffect(() => {
    fetchCompanies()
  }, [search, industry, location, page])

  const fetchCompanies = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (search) params.append("search", search)
      if (industry) params.append("industry", industry)
      if (location) params.append("location", location)
      params.append("page", page.toString())
      params.append("size", "20")

      const response = await fetch(`/api/companies?${params}`)
      if (response.ok) {
        const data = await response.json()
        setCompanies(data)
        // For now, simulate pagination
        setPagination({
          total: data.length,
          page: page,
          size: 20,
          pages: Math.ceil(data.length / 20)
        })
      }
    } catch (error) {
      console.error("Failed to fetch companies:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    const searchQuery = formData.get("search") as string
    
    const params = new URLSearchParams(searchParams)
    if (searchQuery) {
      params.set("search", searchQuery)
    } else {
      params.delete("search")
    }
    params.set("page", "1")
    
    window.location.href = `/companies?${params.toString()}`
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <section className="bg-muted/50 py-8 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-6">
            <h1 className="text-3xl font-bold mb-2">Discover Great Companies</h1>
            <p className="text-muted-foreground">
              Explore innovative companies and find your perfect workplace
            </p>
          </div>
          
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="flex gap-2 p-2 bg-background rounded-lg shadow-sm">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                <Input
                  type="text"
                  name="search"
                  placeholder="Search companies by name, industry, or location..."
                  defaultValue={search}
                  className="pl-10 border-0"
                />
              </div>
              <Button type="submit">Search</Button>
            </div>
          </form>
        </div>
      </section>

      <div className="container mx-auto max-w-6xl py-8 px-4">
        {/* Header with view toggle */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-semibold">
              {search ? "Search Results" : "All Companies"}
            </h2>
            <p className="text-sm text-muted-foreground">
              {pagination.total} companies found
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

        {/* Companies Grid/List */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
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
        ) : companies.length > 0 ? (
          <div className={
            viewMode === "grid" 
              ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
              : "space-y-4"
          }>
            {companies.map((company) => (
              <CompanyCard key={company.id} company={company} />
            ))}
          </div>
        ) : (
          <Card className="text-center py-12">
            <CardContent>
              <Building2 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">No companies found</h3>
              <p className="text-muted-foreground mb-4">
                Try adjusting your search criteria or check back later for new companies.
              </p>
              <Button onClick={() => window.location.href = "/companies"}>
                Clear Search
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
                window.location.href = `/companies?${params.toString()}`
              }}
            />
          </div>
        )}
      </div>
    </div>
  )
}