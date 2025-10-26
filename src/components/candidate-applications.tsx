"use client"

import { useState, useEffect } from "react"
import { 
  Briefcase, 
  Calendar, 
  Clock, 
  Eye,
  FileText,
  User,
  Building2,
  MapPin,
  CheckCircle,
  XCircle,
  AlertCircle,
  Filter,
  Search
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
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
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Label } from "@/components/ui/label"
import Link from "next/link"

interface Application {
  id: string
  job_id: string
  job_title: string
  company_name: string
  company_logo?: string
  company_location?: string
  status: string
  applied_at: string
  last_updated: string
  cover_letter?: string
  resume_url?: string
  notes?: string
}

interface ApplicationStats {
  total: number
  pending: number
  reviewed: number
  interviewed: number
  rejected: number
  hired: number
}

export function CandidateApplications() {
  const [applications, setApplications] = useState<Application[]>([])
  const [filteredApplications, setFilteredApplications] = useState<Application[]>([])
  const [stats, setStats] = useState<ApplicationStats>({
    total: 0,
    pending: 0,
    reviewed: 0,
    interviewed: 0,
    rejected: 0,
    hired: 0
  })
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null)
  const [showDetailDialog, setShowDetailDialog] = useState(false)

  useEffect(() => {
    fetchApplications()
  }, [])

  useEffect(() => {
    filterApplications()
  }, [applications, searchTerm, statusFilter])

  const fetchApplications = async () => {
    try {
      const response = await fetch("/api/candidate/applications")
      if (response.ok) {
        const data = await response.json()
        setApplications(data.applications || [])
        setStats(data.stats || stats)
      }
    } catch (error) {
      console.error("Failed to fetch applications:", error)
    } finally {
      setLoading(false)
    }
  }

  const filterApplications = () => {
    let filtered = applications

    if (searchTerm) {
      filtered = filtered.filter(app =>
        app.job_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        app.company_name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (statusFilter !== "all") {
      filtered = filtered.filter(app => app.status === statusFilter)
    }

    setFilteredApplications(filtered)
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
      case "pending":
        return <Clock className="h-4 w-4 text-yellow-600" />
      default:
        return <AlertCircle className="h-4 w-4 text-gray-600" />
    }
  }

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      pending: "bg-yellow-100 text-yellow-800",
      reviewed: "bg-blue-100 text-blue-800",
      interviewed: "bg-purple-100 text-purple-800",
      rejected: "bg-red-100 text-red-800",
      hired: "bg-green-100 text-green-800"
    }
    return colors[status] || "bg-gray-100 text-gray-800"
  }

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
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
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Applications</h1>
          <p className="text-muted-foreground">
            Track the status of your job applications
          </p>
        </div>
        <Button asChild>
          <Link href="/jobs">
            <Briefcase className="h-4 w-4 mr-2" />
            Browse More Jobs
          </Link>
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pending}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Reviewed</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.reviewed}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Interviewed</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.interviewed}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Rejected</CardTitle>
            <XCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.rejected}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Hired</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.hired}</div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input
                placeholder="Search by job title or company..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline">
                  <Filter className="h-4 w-4 mr-2" />
                  Status: {statusFilter === "all" ? "All" : statusFilter}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem onClick={() => setStatusFilter("all")}>
                  All Status
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter("pending")}>
                  Pending
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter("reviewed")}>
                  Reviewed
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter("interviewed")}>
                  Interviewed
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter("rejected")}>
                  Rejected
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setStatusFilter("hired")}>
                  Hired
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </CardContent>
      </Card>

      {/* Applications Table */}
      <Card>
        <CardHeader>
          <CardTitle>Applications</CardTitle>
          <CardDescription>
            {filteredApplications.length} application{filteredApplications.length !== 1 ? "s" : ""} found
          </CardDescription>
        </CardHeader>
        <CardContent>
          {filteredApplications.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Job</TableHead>
                  <TableHead>Company</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Applied</TableHead>
                  <TableHead>Last Updated</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredApplications.map((application) => (
                  <TableRow key={application.id}>
                    <TableCell>
                      <div className="font-medium">{application.job_title}</div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Avatar className="h-6 w-6">
                          <AvatarImage src={application.company_logo} />
                          <AvatarFallback>
                            {application.company_name.charAt(0).toUpperCase()}
                          </AvatarFallback>
                        </Avatar>
                        <span>{application.company_name}</span>
                      </div>
                    </TableCell>
                    <TableCell>{getStatusBadge(application.status)}</TableCell>
                    <TableCell>
                      <div className="flex items-center text-sm text-muted-foreground">
                        <Calendar className="h-4 w-4 mr-1" />
                        {new Date(application.applied_at).toLocaleDateString()}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center text-sm text-muted-foreground">
                        <Clock className="h-4 w-4 mr-1" />
                        {new Date(application.last_updated).toLocaleDateString()}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={() => {
                          setSelectedApplication(application)
                          setShowDetailDialog(true)
                        }}
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="text-center py-8">
              <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">No applications found</h3>
              <p className="text-muted-foreground mb-4">
                {applications.length === 0 
                  ? "You haven't applied to any jobs yet" 
                  : "Try adjusting your search or filter criteria"
                }
              </p>
              {applications.length === 0 && (
                <Button asChild>
                  <Link href="/jobs">Browse Jobs</Link>
                </Button>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Application Detail Dialog */}
      <Dialog open={showDetailDialog} onOpenChange={setShowDetailDialog}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Application Details</DialogTitle>
            <DialogDescription>
              Review your application and track its progress
            </DialogDescription>
          </DialogHeader>
          
          {selectedApplication && (
            <div className="space-y-6">
              {/* Job Info */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src={selectedApplication.company_logo} />
                      <AvatarFallback>
                        {selectedApplication.company_name.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <div>{selectedApplication.job_title}</div>
                      <div className="text-sm text-muted-foreground">
                        {selectedApplication.company_name}
                      </div>
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label className="text-sm font-medium">Status</Label>
                      <div className="mt-1">{getStatusBadge(selectedApplication.status)}</div>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">Applied Date</Label>
                      <div className="mt-1">{new Date(selectedApplication.applied_at).toLocaleDateString()}</div>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">Last Updated</Label>
                      <div className="mt-1">{new Date(selectedApplication.last_updated).toLocaleDateString()}</div>
                    </div>
                    {selectedApplication.company_location && (
                      <div>
                        <Label className="text-sm font-medium">Location</Label>
                        <div className="mt-1 flex items-center">
                          <MapPin className="h-4 w-4 mr-1" />
                          {selectedApplication.company_location}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Application Content */}
              <Card>
                <CardHeader>
                  <CardTitle>Application Content</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {selectedApplication.cover_letter && (
                    <div>
                      <Label className="text-sm font-medium">Cover Letter</Label>
                      <div className="mt-2 p-4 bg-muted rounded-md">
                        <p className="whitespace-pre-wrap">{selectedApplication.cover_letter}</p>
                      </div>
                    </div>
                  )}
                  
                  {selectedApplication.resume_url && (
                    <div>
                      <Label className="text-sm font-medium">Resume</Label>
                      <div className="mt-2">
                        <Button variant="outline" asChild>
                          <a href={selectedApplication.resume_url} target="_blank" rel="noopener noreferrer">
                            <FileText className="h-4 w-4 mr-2" />
                            View Resume
                          </a>
                        </Button>
                      </div>
                    </div>
                  )}
                  
                  {selectedApplication.notes && (
                    <div>
                      <Label className="text-sm font-medium">Notes</Label>
                      <div className="mt-2 p-4 bg-muted rounded-md">
                        <p className="whitespace-pre-wrap">{selectedApplication.notes}</p>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Status Timeline */}
              <Card>
                <CardHeader>
                  <CardTitle>Application Timeline</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                      </div>
                      <div>
                        <div className="font-medium">Application Submitted</div>
                        <div className="text-sm text-muted-foreground">
                          {new Date(selectedApplication.applied_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    
                    {selectedApplication.status !== "pending" && (
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                          <Eye className="h-4 w-4 text-blue-600" />
                        </div>
                        <div>
                          <div className="font-medium">Application Reviewed</div>
                          <div className="text-sm text-muted-foreground">
                            Employer has reviewed your application
                          </div>
                        </div>
                      </div>
                    )}
                    
                    {selectedApplication.status === "interviewed" && (
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                          <Calendar className="h-4 w-4 text-purple-600" />
                        </div>
                        <div>
                          <div className="font-medium">Interview Scheduled</div>
                          <div className="text-sm text-muted-foreground">
                            You have been selected for an interview
                          </div>
                        </div>
                      </div>
                    )}
                    
                    {selectedApplication.status === "hired" && (
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                          <CheckCircle className="h-4 w-4 text-green-600" />
                        </div>
                        <div>
                          <div className="font-medium">Congratulations! You're Hired</div>
                          <div className="text-sm text-muted-foreground">
                            The employer has offered you the position
                          </div>
                        </div>
                      </div>
                    )}
                    
                    {selectedApplication.status === "rejected" && (
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                          <XCircle className="h-4 w-4 text-red-600" />
                        </div>
                        <div>
                          <div className="font-medium">Application Not Selected</div>
                          <div className="text-sm text-muted-foreground">
                            The employer has decided to move forward with other candidates
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDetailDialog(false)}>
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}