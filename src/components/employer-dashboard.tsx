"use client"

import { useState, useEffect } from "react"
import { 
  Briefcase, 
  Users, 
  FileText, 
  TrendingUp, 
  Clock,
  MapPin,
  DollarSign,
  Eye,
  Edit,
  Trash2
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
  location: string
  type: string
  status: string
  applications_count: number
  views_count: number
  created_at: string
  salary_min?: number
  salary_max?: number
  currency: string
}

interface RecentApplication {
  id: string
  job_title: string
  candidate_name: string
  candidate_email: string
  status: string
  applied_at: string
  avatar_url?: string
}

interface DashboardStats {
  active_jobs: number
  total_applications: number
  pending_applications: number
  total_views: number
}

export function EmployerDashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    active_jobs: 0,
    total_applications: 0,
    pending_applications: 0,
    total_views: 0
  })
  const [recentJobs, setRecentJobs] = useState<Job[]>([])
  const [recentApplications, setRecentApplications] = useState<RecentApplication[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch stats
      const statsResponse = await fetch("/api/employer/stats")
      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setStats(statsData)
      }

      // Fetch recent jobs
      const jobsResponse = await fetch("/api/employer/jobs?limit=5")
      if (jobsResponse.ok) {
        const jobsData = await jobsResponse.json()
        setRecentJobs(jobsData)
      }

      // Fetch recent applications
      const applicationsResponse = await fetch("/api/employer/applications?limit=5")
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
      active: "default",
      inactive: "secondary",
      draft: "outline",
      closed: "destructive"
    }
    return <Badge variant={variants[status] || "outline"}>{status}</Badge>
  }

  const getApplicationStatusBadge = (status: string) => {
    const variants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
      pending: "default",
      reviewed: "secondary",
      rejected: "destructive",
      hired: "outline"
    }
    return <Badge variant={variants[status] || "outline"}>{status}</Badge>
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
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
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Jobs</CardTitle>
            <Briefcase className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.active_jobs}</div>
            <p className="text-xs text-muted-foreground">
              +2 from last month
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Applications</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_applications}</div>
            <p className="text-xs text-muted-foreground">
              +12% from last month
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Review</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pending_applications}</div>
            <p className="text-xs text-muted-foreground">
              Requires attention
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Views</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_views.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              +18% from last month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Jobs */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Recent Job Postings</CardTitle>
              <CardDescription>Your latest job listings and their performance</CardDescription>
            </div>
            <Button asChild>
              <Link href="/employer/jobs">View All Jobs</Link>
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {recentJobs.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Job Title</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Applications</TableHead>
                  <TableHead>Views</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentJobs.map((job) => (
                  <TableRow key={job.id}>
                    <TableCell>
                      <div className="font-medium">{job.title}</div>
                      {job.salary_min && job.salary_max && (
                        <div className="text-sm text-muted-foreground">
                          {job.currency} {job.salary_min.toLocaleString()} - {job.salary_max.toLocaleString()}
                        </div>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-1 text-muted-foreground" />
                        {job.location}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{job.type}</Badge>
                    </TableCell>
                    <TableCell>{getStatusBadge(job.status)}</TableCell>
                    <TableCell>{job.applications_count}</TableCell>
                    <TableCell>{job.views_count}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button variant="ghost" size="icon" asChild>
                          <Link href={`/employer/jobs/${job.id}`}>
                            <Eye className="h-4 w-4" />
                          </Link>
                        </Button>
                        <Button variant="ghost" size="icon" asChild>
                          <Link href={`/employer/jobs/${job.id}/edit`}>
                            <Edit className="h-4 w-4" />
                          </Link>
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="text-center py-8">
              <Briefcase className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">No jobs posted yet</h3>
              <p className="text-muted-foreground mb-4">Start by creating your first job posting</p>
              <Button asChild>
                <Link href="/employer/jobs/new">Post a Job</Link>
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
              <CardDescription>Latest candidates who applied to your jobs</CardDescription>
            </div>
            <Button asChild>
              <Link href="/employer/applications">View All Applications</Link>
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {recentApplications.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Candidate</TableHead>
                  <TableHead>Job</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Applied</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentApplications.map((application) => (
                  <TableRow key={application.id}>
                    <TableCell>
                      <div className="flex items-center space-x-3">
                        <Avatar>
                          <AvatarImage src={application.avatar_url} />
                          <AvatarFallback>
                            {application.candidate_name.charAt(0).toUpperCase()}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <div className="font-medium">{application.candidate_name}</div>
                          <div className="text-sm text-muted-foreground">
                            {application.candidate_email}
                          </div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>{application.job_title}</TableCell>
                    <TableCell>{getApplicationStatusBadge(application.status)}</TableCell>
                    <TableCell>
                      {new Date(application.applied_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <Button variant="ghost" size="sm" asChild>
                        <Link href={`/employer/applications/${application.id}`}>
                          View
                        </Link>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="text-center py-8">
              <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">No applications yet</h3>
              <p className="text-muted-foreground mb-4">Applications will appear here once candidates start applying</p>
              <Button asChild>
                <Link href="/employer/jobs">Post a Job</Link>
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}