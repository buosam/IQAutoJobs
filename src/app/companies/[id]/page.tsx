"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { 
  Building2, MapPin, Globe, Users, Mail, Phone, 
  Calendar, ExternalLink, Briefcase 
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { JobCard } from "@/components/job-card"
import Link from "next/link"

interface Company {
  id: string
  name: string
  description?: string
  website?: string
  industry?: string
  size?: string
  location?: string
  logo_url?: string
  created_at: string
}

interface Job {
  id: string
  title: string
  location: string
  type: string
  category: string
  description: string
  salary_min?: number
  salary_max?: number
  currency: string
  created_at: string
  status: string
}

export default function CompanyDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [company, setCompany] = useState<Company | null>(null)
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCompany()
    fetchCompanyJobs()
  }, [params.id])

  const fetchCompany = async () => {
    try {
      const response = await fetch(`/api/companies/${params.id}`)
      if (response.ok) {
        const companyData = await response.json()
        setCompany(companyData)
      } else if (response.status === 404) {
        router.push("/companies")
      }
    } catch (error) {
      console.error("Failed to fetch company:", error)
    }
  }

  const fetchCompanyJobs = async () => {
    try {
      const response = await fetch(`/api/companies/${params.id}/jobs`)
      if (response.ok) {
        const jobsData = await response.json()
        setJobs(jobsData)
      }
    } catch (error) {
      console.error("Failed to fetch company jobs:", error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", { 
      year: "numeric", 
      month: "long", 
      day: "numeric" 
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!company) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Company Not Found</h1>
          <p className="text-muted-foreground mb-4">The company you're looking for doesn't exist.</p>
          <Button onClick={() => router.push("/companies")}>
            Browse Companies
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <section className="bg-muted/50 py-12 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row gap-8 items-start">
            {/* Company Logo */}
            <div className="flex-shrink-0">
              {company.logo_url ? (
                <img 
                  src={company.logo_url} 
                  alt={company.name}
                  className="w-24 h-24 md:w-32 md:h-32 rounded-lg object-cover shadow-lg"
                />
              ) : (
                <div className="w-24 h-24 md:w-32 md:h-32 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Building2 className="h-12 w-12 md:h-16 md:w-16 text-primary" />
                </div>
              )}
            </div>

            {/* Company Info */}
            <div className="flex-1">
              <h1 className="text-3xl md:text-4xl font-bold mb-2">{company.name}</h1>
              
              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mb-4">
                {company.industry && (
                  <div className="flex items-center gap-1">
                    <Briefcase className="h-4 w-4" />
                    <span>{company.industry}</span>
                  </div>
                )}
                {company.location && (
                  <div className="flex items-center gap-1">
                    <MapPin className="h-4 w-4" />
                    <span>{company.location}</span>
                  </div>
                )}
                {company.size && (
                  <div className="flex items-center gap-1">
                    <Users className="h-4 w-4" />
                    <span>{company.size}</span>
                  </div>
                )}
                <div className="flex items-center gap-1">
                  <Calendar className="h-4 w-4" />
                  <span>Joined {formatDate(company.created_at)}</span>
                </div>
              </div>

              {company.description && (
                <p className="text-base text-muted-foreground mb-6 max-w-3xl">
                  {company.description}
                </p>
              )}

              <div className="flex flex-wrap gap-3">
                {company.website && (
                  <Button variant="outline" asChild>
                    <a href={company.website} target="_blank" rel="noopener noreferrer">
                      <Globe className="h-4 w-4 mr-2" />
                      Visit Website
                    </a>
                  </Button>
                )}
                <Button>
                  Follow Company
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div className="container mx-auto max-w-6xl py-8 px-4">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* About Section */}
            {company.description && (
              <Card>
                <CardHeader>
                  <CardTitle>About {company.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground leading-relaxed">
                    {company.description}
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Company Details */}
            <Card>
              <CardHeader>
                <CardTitle>Company Details</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {company.industry && (
                    <div>
                      <span className="font-medium text-sm">Industry</span>
                      <p className="text-muted-foreground">{company.industry}</p>
                    </div>
                  )}
                  {company.size && (
                    <div>
                      <span className="font-medium text-sm">Company Size</span>
                      <p className="text-muted-foreground">{company.size}</p>
                    </div>
                  )}
                  {company.location && (
                    <div>
                      <span className="font-medium text-sm">Headquarters</span>
                      <p className="text-muted-foreground">{company.location}</p>
                    </div>
                  )}
                  <div>
                    <span className="font-medium text-sm">Founded</span>
                    <p className="text-muted-foreground">{formatDate(company.created_at)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Open Positions */}
            <Card>
              <CardHeader>
                <CardTitle>Open Positions ({jobs.length})</CardTitle>
                <CardDescription>
                  Current job opportunities at {company.name}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {jobs.length > 0 ? (
                  <div className="space-y-4">
                    {jobs.map((job) => (
                      <div key={job.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-semibold text-lg">
                            <Link 
                              href={`/jobs/${job.id}`}
                              className="hover:text-primary transition-colors"
                            >
                              {job.title}
                            </Link>
                          </h3>
                          <Badge variant="outline">{job.type}</Badge>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground mb-2">
                          <span>{job.location}</span>
                          {job.salary_min && job.salary_max && (
                            <span>${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}</span>
                          )}
                        </div>
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {job.description}
                        </p>
                        <Button 
                          variant="outline" 
                          size="sm" 
                          className="mt-3"
                          asChild
                        >
                          <Link href={`/jobs/${job.id}`}>
                            View Details
                          </Link>
                        </Button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Briefcase className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">No Open Positions</h3>
                    <p className="text-muted-foreground mb-4">
                      {company.name} doesn't have any open positions at the moment.
                    </p>
                    <Button variant="outline" asChild>
                      <Link href="/jobs">Browse Other Jobs</Link>
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button variant="outline" className="w-full" asChild>
                  <Link href="/jobs">
                    Browse All Jobs
                  </Link>
                </Button>
                <Button variant="outline" className="w-full" asChild>
                  <Link href="/companies">
                    Browse Companies
                  </Link>
                </Button>
              </CardContent>
            </Card>

            {/* Company Stats */}
            <Card>
              <CardHeader>
                <CardTitle>Company Stats</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Open Jobs</span>
                  <span className="font-medium">{jobs.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Industry</span>
                  <span className="font-medium">{company.industry || "N/A"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Size</span>
                  <span className="font-medium">{company.size || "N/A"}</span>
                </div>
              </CardContent>
            </Card>

            {/* Similar Companies */}
            <Card>
              <CardHeader>
                <CardTitle>Similar Companies</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  Companies in the same industry
                </p>
                <div className="space-y-2">
                  {/* This would be populated with actual similar companies */}
                  <div className="text-sm text-muted-foreground">
                    Similar companies will be shown here
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}