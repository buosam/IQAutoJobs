"use client"

import { useState, useEffect } from "react"
import { 
  Users, 
  Building2, 
  Briefcase, 
  FileText, 
  TrendingUp, 
  TrendingDown,
  Activity,
  AlertTriangle,
  CheckCircle,
  Clock,
  UserPlus,
  Building,
  File,
  DollarSign,
  Eye,
  BarChart3,
  Calendar,
  MapPin
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import Link from "next/link"

interface SystemStats {
  total_users: number
  total_companies: number
  total_jobs: number
  total_applications: number
  active_users_today: number
  new_users_this_month: number
  new_companies_this_month: number
  new_jobs_this_month: number
  revenue_this_month: number
}

interface RecentActivity {
  id: string
  type: string
  action: string
  user_name: string
  target_name: string
  timestamp: string
  ip_address: string
}

interface TopCompany {
  id: string
  name: string
  logo_url?: string
  jobs_count: number
  applications_count: number
  created_at: string
}

interface TopJob {
  id: string
  title: string
  company_name: string
  company_logo?: string
  applications_count: number
  views_count: number
  created_at: string
}

export function AdminDashboard() {
  const [stats, setStats] = useState<SystemStats>({
    total_users: 0,
    total_companies: 0,
    total_jobs: 0,
    total_applications: 0,
    active_users_today: 0,
    new_users_this_month: 0,
    new_companies_this_month: 0,
    new_jobs_this_month: 0,
    revenue_this_month: 0
  })
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([])
  const [topCompanies, setTopCompanies] = useState<TopCompany[]>([])
  const [topJobs, setTopJobs] = useState<TopJob[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch system stats
      const statsResponse = await fetch("/api/admin/stats")
      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setStats(statsData)
      }

      // Fetch recent activity
      const activityResponse = await fetch("/api/admin/activity?limit=10")
      if (activityResponse.ok) {
        const activityData = await activityResponse.json()
        setRecentActivity(activityData)
      }

      // Fetch top companies
      const companiesResponse = await fetch("/api/admin/companies/top?limit=5")
      if (companiesResponse.ok) {
        const companiesData = await companiesResponse.json()
        setTopCompanies(companiesData)
      }

      // Fetch top jobs
      const jobsResponse = await fetch("/api/admin/jobs/top?limit=5")
      if (jobsResponse.ok) {
        const jobsData = await jobsResponse.json()
        setTopJobs(jobsData)
      }
    } catch (error) {
      console.error("Failed to fetch dashboard data:", error)
    } finally {
      setLoading(false)
    }
  }

  const getActivityIcon = (type: string) => {
    switch (type) {
      case "user":
        return <Users className="h-4 w-4" />
      case "company":
        return <Building2 className="h-4 w-4" />
      case "job":
        return <Briefcase className="h-4 w-4" />
      case "application":
        return <FileText className="h-4 w-4" />
      default:
        return <Activity className="h-4 w-4" />
    }
  }

  const getActivityBadge = (action: string) => {
    const variants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
      create: "default",
      update: "secondary",
      delete: "destructive",
      login: "outline",
      logout: "outline"
    }
    return <Badge variant={variants[action] || "outline"}>{action}</Badge>
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
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
          <p className="text-muted-foreground">
            Monitor and manage your platform
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline">
            <BarChart3 className="h-4 w-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>

      {/* System Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Users</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_users.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              +{stats.new_users_this_month} this month
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Companies</CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_companies.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              +{stats.new_companies_this_month} this month
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Jobs</CardTitle>
            <Briefcase className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_jobs.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              +{stats.new_jobs_this_month} this month
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Applications</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_applications.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Total applications
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Latest system activities and user actions</CardDescription>
              </div>
              <Button variant="ghost" size="sm" asChild>
                <Link href="/admin/audit">View All</Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {recentActivity.length > 0 ? (
              <div className="space-y-4">
                {recentActivity.slice(0, 5).map((activity) => (
                  <div key={activity.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                    <div className="flex-shrink-0">
                      {getActivityIcon(activity.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium">
                          {activity.user_name} {activity.action} {activity.target_name}
                        </p>
                        {getActivityBadge(activity.action)}
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {new Date(activity.timestamp).toLocaleString()} • {activity.ip_address}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Activity className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No recent activity</h3>
                <p className="text-muted-foreground">System activity will appear here</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Top Companies */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Top Companies</CardTitle>
                <CardDescription>Most active companies on the platform</CardDescription>
              </div>
              <Button variant="ghost" size="sm" asChild>
                <Link href="/admin/companies">View All</Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {topCompanies.length > 0 ? (
              <div className="space-y-4">
                {topCompanies.map((company) => (
                  <div key={company.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={company.logo_url} />
                      <AvatarFallback>
                        {company.name.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-sm">{company.name}</h3>
                      <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                        <span>{company.jobs_count} jobs</span>
                        <span>{company.applications_count} applications</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Building2 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No companies yet</h3>
                <p className="text-muted-foreground">Companies will appear here once they register</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Jobs */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Popular Jobs</CardTitle>
                <CardDescription>Jobs with the most applications and views</CardDescription>
              </div>
              <Button variant="ghost" size="sm" asChild>
                <Link href="/admin/jobs">View All</Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {topJobs.length > 0 ? (
              <div className="space-y-4">
                {topJobs.map((job) => (
                  <div key={job.id} className="flex items-start space-x-3 p-3 border rounded-lg">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={job.company_logo} />
                      <AvatarFallback>
                        {job.company_name.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-sm">{job.title}</h3>
                      <p className="text-xs text-muted-foreground">{job.company_name}</p>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-muted-foreground">
                        <span className="flex items-center">
                          <FileText className="h-3 w-3 mr-1" />
                          {job.applications_count} applications
                        </span>
                        <span className="flex items-center">
                          <Eye className="h-3 w-3 mr-1" />
                          {job.views_count} views
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Briefcase className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No jobs posted yet</h3>
                <p className="text-muted-foreground">Jobs will appear here once companies start posting</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <Card>
          <CardHeader>
            <CardTitle>Platform Health</CardTitle>
            <CardDescription>Key performance indicators</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Active Users Today</span>
                <span className="text-sm text-muted-foreground">{stats.active_users_today}</span>
              </div>
              <Progress value={75} className="h-2" />
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Monthly Revenue</span>
                <span className="text-sm text-muted-foreground">${stats.revenue_this_month.toLocaleString()}</span>
              </div>
              <Progress value={60} className="h-2" />
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Job Application Rate</span>
                <span className="text-sm text-muted-foreground">3.2 per job</span>
              </div>
              <Progress value={45} className="h-2" />
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">User Retention</span>
                <span className="text-sm text-muted-foreground">78%</span>
              </div>
              <Progress value={78} className="h-2" />
            </div>
            
            <div className="grid grid-cols-2 gap-4 pt-4">
              <div className="text-center p-4 border rounded-lg">
                <CheckCircle className="h-8 w-8 text-green-600 mx-auto mb-2" />
                <div className="text-2xl font-bold">98.5%</div>
                <div className="text-xs text-muted-foreground">Uptime</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <TrendingUp className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                <div className="text-2xl font-bold">+24%</div>
                <div className="text-xs text-muted-foreground">Growth</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common administrative tasks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Button variant="outline" className="h-auto p-6 flex flex-col items-center space-y-3" asChild>
              <Link href="/admin/users">
                <Users className="h-8 w-8" />
                <span>Manage Users</span>
              </Link>
            </Button>
            <Button variant="outline" className="h-auto p-6 flex flex-col items-center space-y-3" asChild>
              <Link href="/admin/companies">
                <Building2 className="h-8 w-8" />
                <span>Manage Companies</span>
              </Link>
            </Button>
            <Button variant="outline" className="h-auto p-6 flex flex-col items-center space-y-3" asChild>
              <Link href="/admin/jobs">
                <Briefcase className="h-8 w-8" />
                <span>Manage Jobs</span>
              </Link>
            </Button>
            <Button variant="outline" className="h-auto p-6 flex flex-col items-center space-y-3" asChild>
              <Link href="/admin/applications">
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