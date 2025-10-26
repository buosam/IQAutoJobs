"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { 
  MapPin, Briefcase, Clock, DollarSign, Building2, Mail, 
  Calendar, Share2, Heart, ExternalLink 
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ApplyDialog } from "@/components/apply-dialog"
import { Link } from "next/link"

interface Job {
  id: string
  title: string
  description: string
  location: string
  type: string
  category: string
  experience_level: string
  salary_min?: number
  salary_max?: number
  currency: string
  status: string
  published_at?: string
  created_at: string
  company: {
    id: string
    name: string
    description?: string
    website?: string
    logo_url?: string
    industry?: string
    location?: string
    size?: string
  }
}

export default function JobDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [job, setJob] = useState<Job | null>(null)
  const [loading, setLoading] = useState(true)
  const [showApplyDialog, setShowApplyDialog] = useState(false)

  useEffect(() => {
    fetchJob()
  }, [params.id])

  const fetchJob = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/jobs/${params.id}`)
      if (response.ok) {
        const jobData = await response.json()
        setJob(jobData)
      } else if (response.status === 404) {
        router.push("/jobs")
      }
    } catch (error) {
      console.error("Failed to fetch job:", error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString?: string) => {
    if (!dateString) return ""
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", { 
      year: "numeric", 
      month: "long", 
      day: "numeric" 
    })
  }

  const getJobTypeColor = (type: string) => {
    switch (type) {
      case "FT": return "bg-green-100 text-green-800"
      case "PT": return "bg-blue-100 text-blue-800"
      case "CONTRACT": return "bg-purple-100 text-purple-800"
      case "INTERN": return "bg-orange-100 text-orange-800"
      default: return "bg-gray-100 text-gray-800"
    }
  }

  const getJobTypeLabel = (type: string) => {
    switch (type) {
      case "FT": return "Full-time"
      case "PT": return "Part-time"
      case "CONTRACT": return "Contract"
      case "INTERN": return "Internship"
      default: return type
    }
  }

  const formatSalary = () => {
    if (!job?.salary_min && !job?.salary_max) return null
    
    const currency = job?.currency || "USD"
    const min = job?.salary_min
    const max = job?.salary_max
    
    if (min && max) {
      return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}`
    } else if (min) {
      return `${currency} ${min.toLocaleString()}+`
    } else if (max) {
      return `Up to ${currency} ${max.toLocaleString()}`
    }
    
    return null
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: job?.title,
          text: `Check out this job at ${job?.company.name}`,
          url: window.location.href
        })
      } catch (error) {
        console.log("Error sharing:", error)
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href)
      alert("Link copied to clipboard!")
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!job) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Job Not Found</h1>
          <p className="text-muted-foreground mb-4">The job you're looking for doesn't exist.</p>
          <Button onClick={() => router.push("/jobs")}>
            Browse Jobs
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <section className="bg-muted/50 py-8 px-4">
        <div className="container mx-auto max-w-4xl">
          <div className="flex flex-col sm:flex-row gap-4 items-start">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <Badge className={getJobTypeColor(job.type)}>
                  {getJobTypeLabel(job.type)}
                </Badge>
                <Badge variant="outline">{job.category}</Badge>
                {job.status === "PUBLISHED" && (
                  <Badge variant="secondary">Active</Badge>
                )}
              </div>
              
              <h1 className="text-3xl font-bold mb-2">{job.title}</h1>
              
              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mb-4">
                <div className="flex items-center gap-1">
                  <Building2 className="h-4 w-4" />
                  <Link 
                    href={`/companies/${job.company.id}`}
                    className="hover:text-primary transition-colors"
                  >
                    {job.company.name}
                  </Link>
                </div>
                <div className="flex items-center gap-1">
                  <MapPin className="h-4 w-4" />
                  <span>{job.location}</span>
                </div>
                {job.published_at && (
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    <span>Posted {formatDate(job.published_at)}</span>
                  </div>
                )}
              </div>
            </div>
            
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={handleShare}>
                <Share2 className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="sm">
                <Heart className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </section>

      <div className="container mx-auto max-w-4xl py-8 px-4">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Job Description */}
            <Card>
              <CardHeader>
                <CardTitle>Job Description</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="prose prose-sm max-w-none">
                  <div dangerouslySetInnerHTML={{ __html: job.description.replace(/\n/g, '<br />') }} />
                </div>
              </CardContent>
            </Card>

            {/* Company Info */}
            <Card>
              <CardHeader>
                <CardTitle>About {job.company.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {job.company.description && (
                    <p className="text-sm text-muted-foreground">
                      {job.company.description}
                    </p>
                  )}
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    {job.company.industry && (
                      <div>
                        <span className="font-medium">Industry:</span>
                        <p className="text-muted-foreground">{job.company.industry}</p>
                      </div>
                    )}
                    {job.company.size && (
                      <div>
                        <span className="font-medium">Size:</span>
                        <p className="text-muted-foreground">{job.company.size}</p>
                      </div>
                    )}
                    {job.company.location && (
                      <div>
                        <span className="font-medium">Location:</span>
                        <p className="text-muted-foreground">{job.company.location}</p>
                      </div>
                    )}
                  </div>
                  
                  {job.company.website && (
                    <Button variant="outline" size="sm" asChild>
                      <a href={job.company.website} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="h-4 w-4 mr-2" />
                        Visit Website
                      </a>
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Job Summary */}
            <Card>
              <CardHeader>
                <CardTitle>Job Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{getJobTypeLabel(job.type)}</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{job.location}</span>
                </div>
                
                {formatSalary() && (
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">{formatSalary()}</span>
                  </div>
                )}
                
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{job.experience_level}</span>
                </div>
                
                <Separator />
                
                <Button 
                  className="w-full" 
                  size="lg"
                  onClick={() => setShowApplyDialog(true)}
                  disabled={job.status !== "PUBLISHED"}
                >
                  {job.status === "PUBLISHED" ? "Apply Now" : "Not Accepting Applications"}
                </Button>
                
                {job.status !== "PUBLISHED" && (
                  <p className="text-xs text-muted-foreground text-center">
                    This job is currently not accepting applications
                  </p>
                )}
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button variant="outline" className="w-full" asChild>
                  <Link href={`/companies/${job.company.id}`}>
                    View Company Profile
                  </Link>
                </Button>
                <Button variant="outline" className="w-full" asChild>
                  <Link href="/jobs">
                    Browse Similar Jobs
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Apply Dialog */}
      <ApplyDialog 
        open={showApplyDialog} 
        onOpenChange={setShowApplyDialog}
        job={job}
      />
    </div>
  )
}