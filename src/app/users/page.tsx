"use client"

import { useState, useEffect } from "react"
import { Users as UsersIcon, Mail, Briefcase, Shield, User as UserIcon } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

interface User {
  id: string
  email: string
  role: string
  first_name?: string
  last_name?: string
  is_active: boolean
  created_at: string
}

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    setLoading(true)
    try {
      const response = await fetch("/api/users")
      
      if (response.ok) {
        const data = await response.json()
        setUsers(data.users || data || [])
      } else {
        setError("Failed to load users")
      }
    } catch (error) {
      console.error("Error fetching users:", error)
      setError("An error occurred while loading users")
    } finally {
      setLoading(false)
    }
  }

  const getRoleIcon = (role: string) => {
    switch (role) {
      case "ADMIN":
        return <Shield className="h-4 w-4" />
      case "EMPLOYER":
        return <Briefcase className="h-4 w-4" />
      case "CANDIDATE":
        return <UserIcon className="h-4 w-4" />
      default:
        return <UserIcon className="h-4 w-4" />
    }
  }

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case "ADMIN":
        return "bg-red-100 text-red-800"
      case "EMPLOYER":
        return "bg-blue-100 text-blue-800"
      case "CANDIDATE":
        return "bg-green-100 text-green-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getInitials = (user: User) => {
    if (user.first_name && user.last_name) {
      return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
    }
    return user.email[0].toUpperCase()
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", { 
      month: "short", 
      day: "numeric",
      year: "numeric"
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <UsersIcon className="h-12 w-12 text-primary mx-auto mb-4 animate-pulse" />
          <p className="text-muted-foreground">Loading users...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <UsersIcon className="h-8 w-8 text-primary" />
            <h1 className="text-3xl font-bold">Registered Users</h1>
          </div>
          <p className="text-muted-foreground">
            Browse all registered users on the platform
          </p>
        </div>

        {error && (
          <Card className="mb-6 border-destructive">
            <CardContent className="pt-6">
              <p className="text-destructive">{error}</p>
            </CardContent>
          </Card>
        )}

        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle>All Users ({users.length})</CardTitle>
              <CardDescription>
                Total registered users across all roles
              </CardDescription>
            </CardHeader>
            <CardContent>
              {users.length === 0 ? (
                <div className="text-center py-12">
                  <UsersIcon className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">No users found</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {users.map((user) => (
                    <div
                      key={user.id}
                      className="flex items-center gap-4 p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
                    >
                      <Avatar className="h-12 w-12">
                        <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                          {getInitials(user)}
                        </AvatarFallback>
                      </Avatar>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="font-semibold truncate">
                            {user.first_name && user.last_name
                              ? `${user.first_name} ${user.last_name}`
                              : user.email}
                          </h3>
                          <Badge className={getRoleBadgeColor(user.role)}>
                            <span className="flex items-center gap-1">
                              {getRoleIcon(user.role)}
                              {user.role}
                            </span>
                          </Badge>
                          {user.is_active && (
                            <Badge variant="outline" className="text-green-600 border-green-600">
                              Active
                            </Badge>
                          )}
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Mail className="h-3 w-3" />
                            {user.email}
                          </span>
                          <span>
                            Joined {formatDate(user.created_at)}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Total Users</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{users.length}</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Employers</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {users.filter(u => u.role === "EMPLOYER").length}
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium">Candidates</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {users.filter(u => u.role === "CANDIDATE").length}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
