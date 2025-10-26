"use client"

import { useState, useEffect } from "react"
import { 
  Briefcase, 
  FileText, 
  Heart, 
  TrendingUp, 
  Clock,
  MapPin,
  DollarSign,
  Eye,
  User,
  Building2,
  Calendar,
  CheckCircle,
  XCircle
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Progress } from "@/components/ui/progress"
import Link from "next/link"

interface Job {
  id: string
  title: string
  company: {
    name: string
    logo_url?: string
  }
  location: string
  type: string
  category: string
  salary_min?: number
  salary_max?: number
  currency: string
  created_at: string
  is_saved: boolean
}

interface Application {
  id: string
  job_title: string
  company_name: string
  company_logo?: string
  status: string
  applied_at: string
  last_updated: string
}

interface DashboardStats {
  total_applications: number
  pending_applications: number
  interviewed_applications: number
  saved_jobs: number
  profile_completion: number
}

export function CandidateDashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    total_applications: 0,
    pending_applications: 0,
    interviewed_applications: 0,
    saved_jobs: 0,
    profile_completion: 0
  })
  const [recommendedJobs, setRecommendedJobs] = useState<Job[]>([])
  const [recentApplications, setRecentApplications] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch stats
      const statsResponse = await fetch("/api/candidate/stats")
      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setStats(statsData)
      }

      // Fetch recommended jobs
      const jobsResponse = await fetch("/api/candidate/jobs/recommended?limit=4")
      if (jobsResponse.ok) {
        const jobsData = await jobsResponse.json()
        setRecommendedJobs(jobsData)
      }

      // Fetch recent applications
      const applicationsResponse = await fetch("/api/candidate/applications?limit=5")
      if (applicationsResponse.ok) {
        const applicationsData = await applicationsResponse.json()
        setRecentApplications(applicationsData)
      }
    } catch (error) {
      console.error("Failed to fetch dashboard data:", error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
      pending: "default",
      reviewed: "secondary",
      interviewed: "outline",
      rejected: "destructive",
      hired: "default"
    }
    const labels: Record<string, string> = {
      pending: "Pending",
      reviewed: "Reviewed",
      interviewed: "Interviewed",
      rejected: "Rejected",
      hired: "Hired"
    }
    return <Badge variant={variants[status] || "outline"}>{labels[status] || status}</Badge>
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "hired":
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case "rejected":
        return <XCircle className="h-4 w-4 text-red-600" />
      case "interviewed":
        return <Calendar className="h-4 w-4 text-blue-600" />
      default:
        return <Clock className="h-4 w-4 text-gray-600" />
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          {[...Array(5)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-muted rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-muted rounded w-1/2"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary/10 to-primary/5 rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Welcome back! 👋</h1>
            <p className="text-muted-foreground mt-2">
              Here's what's happening with your job search today.
            </p>
          </div>
          <Button asChild>
            <Link href="/jobs">
              <Briefcase className="h-4 w-4 mr-2" />
              Browse Jobs
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Applications</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_applications}</div>
            <p className="text-xs text-muted-foreground">
              {stats.pending_applications} pending review
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Interviews</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.interviewed_applications}</div>
            <p className="text-xs text-muted-foreground">
              Scheduled interviews
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Saved Jobs</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.saved_jobs}</div>
            <p className="text-xs text-muted-foreground">
              Jobs you're interested in
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Profile Completion</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.profile_completion}%</div>
            <Progress value={stats.profile_completion} className="mt-2" />
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24%</div>
            <p className="text-xs text-muted-foreground">
              Interview rate
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recommended Jobs */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Recommended for You</CardTitle>
                <CardDescription>Jobs that match your profile and preferences</CardDescription>
              </div>
              <Button variant="ghost" size="sm" asChild>
                <Link href="/candidate/saved-jobs">View All</Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {recommendedJobs.length > 0 ? (
              <div className="space-y-4">
                {recommendedJobs.map((job) => (
                  <div key={job.id} className="flex items-start space-x-4 p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={job.company.logo_url} />
                      <AvatarFallback>
                        {job.company.name.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-medium text-sm">{job.title}</h3>
                          <p className="text-sm text-muted-foreground">{job.company.name}</p>
                        </div>
                        <Heart className={`h-4 w-4 ${job.is_saved ? 'fill-red-500 text-red-500' : 'text-gray-400'}`} />
                      </div>
                      <div className="flex items-center space-x-4 mt-2 text-xs text-muted-foreground">
                        <div className="flex items-center">
                          <MapPin className="h-3 w-3 mr-1" />
                          {job.location}
                        </div>
                        <Badge variant="outline" className="text-xs">{job.type}</Badge>
                        {job.salary_min && job.salary_max && (
                          <div className="flex items-center">
                            <DollarSign className="h-3 w-3 mr-1" />
                            {job.currency} {job.salary_min.toLocaleString()} - {job.salary_max.toLocaleString()}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Briefcase className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No recommendations yet</h3>
                <p className="text-muted-foreground mb-4">Complete your profile to get personalized job recommendations</p>
                <Button asChild size="sm">
                  <Link href="/candidate/profile">Complete Profile</Link>
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Applications */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Recent Applications</CardTitle>
                <CardDescription>Track your job application progress</CardDescription>
              </div>
              <Button variant="ghost" size="sm" asChild>
                <Link href="/candidate/applications">View All</Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {recentApplications.length > 0 ? (
              <div className="space-y-4">
                {recentApplications.map((application) => (
                  <div key={application.id} className="flex items-start space-x-4 p-4 border rounded-lg">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={application.company_logo} />
                      <AvatarFallback>
                        {application.company_name.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-medium text-sm">{application.job_title}</h3>
                          <p className="text-sm text-muted-foreground">{application.company_name}</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(application.status)}
                          {getStatusBadge(application.status)}
                        </div>
                      </div>
                      <div className="flex items-center space-x-4 mt-2 text-xs text-muted-foreground">
                        <div className="flex items-center">
                          <Calendar className="h-3 w-3 mr-1" />
                          Applied {new Date(application.applied_at).toLocaleDateString()}
                        </div>
                        <div className="flex items-center">
                          <Clock className="h-3 w-3 mr-1" />
                          Updated {new Date(application.last_updated).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No applications yet</h3>
                <p className="text-muted-foreground mb-4">Start applying to jobs to track your progress here</p>
                <Button asChild size="sm">
                  <Link href="/jobs">Browse Jobs</Link>
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common tasks to help you with your job search</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button variant="outline" className="h-auto p-6 flex flex-col items-center space-y-3" asChild>
              <Link href="/candidate/profile">
                <User className="h-8 w-8" />
                <span>Update Profile</span>
              </Link>
            </Button>
            <Button variant="outline" className="h-auto p-6 flex flex-col items-center space-y-3" asChild>
              <Link href="/jobs">
                <Briefcase className="h-8 w-8" />
                <span>Browse Jobs</span>
              </Link>
            </Button>
            <Button variant="outline" className="h-auto p-6 flex flex-col items-center space-y-3" asChild>
              <Link href="/candidate/applications">
                <FileText className="h-8 w-8" />
                <span>View Applications</span>
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}