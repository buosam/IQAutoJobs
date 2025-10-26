"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Briefcase, Users, Building2, FileText, LogOut, User } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"

interface UserData {
  id: string
  email: string
  first_name: string
  last_name: string
  role: string
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<UserData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("access_token")
    const userData = localStorage.getItem("user")

    if (!token || !userData) {
      router.push("/auth/login")
      return
    }

    try {
      setUser(JSON.parse(userData))
    } catch (error) {
      console.error("Error parsing user data:", error)
      router.push("/auth/login")
    } finally {
      setLoading(false)
    }
  }, [router])

  const handleLogout = async () => {
    // Call logout endpoint to clear httpOnly cookies
    await fetch("/api/auth/logout", { method: "POST" })
    
    // Clear localStorage
    localStorage.removeItem("user")
    
    // Redirect to login
    router.push("/auth/login")
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Briefcase className="h-6 w-6 text-primary" />
              <h1 className="text-xl font-bold">IQAutoJobs</h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-sm">
                <p className="font-medium">{user.first_name} {user.last_name}</p>
                <p className="text-muted-foreground text-xs">{user.role}</p>
              </div>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">
            Welcome back, {user.first_name}!
          </h2>
          <p className="text-muted-foreground">
            Here's what's happening with your account today.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Profile</CardTitle>
              <User className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{user.role}</div>
              <p className="text-xs text-muted-foreground">
                Account Type
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Jobs</CardTitle>
              <Briefcase className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3</div>
              <p className="text-xs text-muted-foreground">
                Available Positions
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Companies</CardTitle>
              <Building2 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">2</div>
              <p className="text-xs text-muted-foreground">
                Hiring Now
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Users</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">5</div>
              <p className="text-xs text-muted-foreground">
                Registered Users
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <Link href="/jobs">
              <CardHeader>
                <Briefcase className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Browse Jobs</CardTitle>
                <CardDescription>
                  Explore available job opportunities from top companies
                </CardDescription>
              </CardHeader>
            </Link>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <Link href="/companies">
              <CardHeader>
                <Building2 className="h-8 w-8 text-primary mb-2" />
                <CardTitle>View Companies</CardTitle>
                <CardDescription>
                  Discover innovative companies and find your perfect workplace
                </CardDescription>
              </CardHeader>
            </Link>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <Link href="/users">
              <CardHeader>
                <Users className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Browse Users</CardTitle>
                <CardDescription>
                  View all registered users on the platform
                </CardDescription>
              </CardHeader>
            </Link>
          </Card>
        </div>

        {/* Role-specific Actions */}
        {user.role === "EMPLOYER" && (
          <div className="mt-8">
            <Card>
              <CardHeader>
                <CardTitle>Employer Actions</CardTitle>
                <CardDescription>Manage your job postings and applications</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4">
                  <Button>
                    <Briefcase className="h-4 w-4 mr-2" />
                    Post a Job
                  </Button>
                  <Button variant="outline">
                    <FileText className="h-4 w-4 mr-2" />
                    View Applications
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {user.role === "CANDIDATE" && (
          <div className="mt-8">
            <Card>
              <CardHeader>
                <CardTitle>Candidate Actions</CardTitle>
                <CardDescription>Manage your job applications and profile</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4">
                  <Button>
                    <FileText className="h-4 w-4 mr-2" />
                    My Applications
                  </Button>
                  <Button variant="outline">
                    <User className="h-4 w-4 mr-2" />
                    Update Profile
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {user.role === "ADMIN" && (
          <div className="mt-8">
            <Card>
              <CardHeader>
                <CardTitle>Admin Actions</CardTitle>
                <CardDescription>Manage platform settings and users</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4">
                  <Button>
                    <Users className="h-4 w-4 mr-2" />
                    Manage Users
                  </Button>
                  <Button variant="outline">
                    <Building2 className="h-4 w-4 mr-2" />
                    Manage Companies
                  </Button>
                  <Button variant="outline">
                    <Briefcase className="h-4 w-4 mr-2" />
                    Manage Jobs
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </main>
    </div>
  )
}
