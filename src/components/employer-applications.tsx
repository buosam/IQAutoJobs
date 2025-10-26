"use client"

import { useState, useEffect } from "react"
import { 
  Search, 
  Filter, 
  Download,
  Eye,
  MessageSquare,
  Check,
  X,
  Clock,
  User,
  Mail,
  Phone,
  MapPin,
  Calendar,
  FileText
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
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import Link from "next/link"

interface Application {
  id: string
  job_id: string
  job_title: string
  candidate_id: string
  candidate_name: string
  candidate_email: string
  candidate_phone?: string
  candidate_location?: string
  candidate_resume_url?: string
  cover_letter?: string
  status: string
  applied_at: string
  last_updated: string
  avatar_url?: string
  skills: string[]
  experience_years?: number
  education?: string
}

interface ApplicationStats {
  total: number
  pending: number
  reviewed: number
  rejected: number
  hired: number
}

export function EmployerApplications() {
  const [applications, setApplications] = useState<Application[]>([])
  const [filteredApplications, setFilteredApplications] = useState<Application[]>([])
  const [stats, setStats] = useState<ApplicationStats>({
    total: 0,
    pending: 0,
    reviewed: 0,
    rejected: 0,
    hired: 0
  })
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null)
  const [rejectionReason, setRejectionReason] = useState("")
  const [showRejectionDialog, setShowRejectionDialog] = useState(false)
  const [showDetailDialog, setShowDetailDialog] = useState(false)

  useEffect(() => {
    fetchApplications()
  }, [])

  useEffect(() => {
    filterApplications()
  }, [applications, searchTerm, statusFilter])

  const fetchApplications = async () => {
    try {
      const response = await fetch("/api/employer/applications")
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
        app.candidate_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        app.candidate_email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        app.job_title.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (statusFilter !== "all") {
      filtered = filtered.filter(app => app.status === statusFilter)
    }

    setFilteredApplications(filtered)
  }

  const updateApplicationStatus = async (applicationId: string, status: string, reason?: string) => {
    try {
      const response = await fetch(`/api/employer/applications/${applicationId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status, reason }),
      })
      
      if (response.ok) {
        setApplications(applications.map(app => 
          app.id === applicationId 
            ? { ...app, status, last_updated: new Date().toISOString() }
            : app
        ))
        setShowRejectionDialog(false)
        setRejectionReason("")
      }
    } catch (error) {
      console.error("Failed to update application status:", error)
    }
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
      pending: "default",
      reviewed: "secondary",
      rejected: "destructive",
      hired: "outline"
    }
    return <Badge variant={variants[status] || "outline"}>{status}</Badge>
  }

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      pending: "bg-blue-100 text-blue-800",
      reviewed: "bg-yellow-100 text-yellow-800",
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
          <h1 className="text-3xl font-bold tracking-tight">Applications</h1>
          <p className="text-muted-foreground">
            Manage and review candidate applications
          </p>
        </div>
        <Button variant="outline">
          <Download className="h-4 w-4 mr-2" />
          Export CSV
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
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
            <CardTitle className="text-sm font-medium">Rejected</CardTitle>
            <X className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.rejected}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Hired</CardTitle>
            <Check className="h-4 w-4 text-muted-foreground" />
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
                placeholder="Search by candidate name, email, or job title..."
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
                  <TableHead>Candidate</TableHead>
                  <TableHead>Job</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Applied</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredApplications.map((application) => (
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
                    <TableCell>{getStatusBadge(application.status)}</TableCell>
                    <TableCell>
                      <div className="flex items-center text-sm text-muted-foreground">
                        <Calendar className="h-4 w-4 mr-1" />
                        {new Date(application.applied_at).toLocaleDateString()}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
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
                        
                        {application.status === "pending" && (
                          <>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => updateApplicationStatus(application.id, "reviewed")}
                            >
                              <Eye className="h-4 w-4" />
                              Review
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => {
                                setSelectedApplication(application)
                                setShowRejectionDialog(true)
                              }}
                            >
                              <X className="h-4 w-4" />
                            </Button>
                          </>
                        )}
                        
                        {application.status === "reviewed" && (
                          <>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => updateApplicationStatus(application.id, "hired")}
                            >
                              <Check className="h-4 w-4" />
                              Hire
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => {
                                setSelectedApplication(application)
                                setShowRejectionDialog(true)
                              }}
                            >
                              <X className="h-4 w-4" />
                            </Button>
                          </>
                        )}
                      </div>
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
                  ? "Applications will appear here once candidates start applying" 
                  : "Try adjusting your search or filter criteria"
                }
              </p>
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
              Review candidate application and information
            </DialogDescription>
          </DialogHeader>
          
          {selectedApplication && (
            <div className="space-y-6">
              {/* Candidate Info */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src={selectedApplication.avatar_url} />
                      <AvatarFallback>
                        {selectedApplication.candidate_name.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <div>{selectedApplication.candidate_name}</div>
                      <div className="text-sm text-muted-foreground">
                        {selectedApplication.candidate_email}
                      </div>
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {selectedApplication.candidate_phone && (
                      <div className="flex items-center space-x-2">
                        <Phone className="h-4 w-4 text-muted-foreground" />
                        <span>{selectedApplication.candidate_phone}</span>
                      </div>
                    )}
                    {selectedApplication.candidate_location && (
                      <div className="flex items-center space-x-2">
                        <MapPin className="h-4 w-4 text-muted-foreground" />
                        <span>{selectedApplication.candidate_location}</span>
                      </div>
                    )}
                    {selectedApplication.experience_years && (
                      <div className="flex items-center space-x-2">
                        <User className="h-4 w-4 text-muted-foreground" />
                        <span>{selectedApplication.experience_years} years experience</span>
                      </div>
                    )}
                    {selectedApplication.education && (
                      <div className="flex items-center space-x-2">
                        <FileText className="h-4 w-4 text-muted-foreground" />
                        <span>{selectedApplication.education}</span>
                      </div>
                    )}
                  </div>
                  
                  {selectedApplication.skills.length > 0 && (
                    <div className="mt-4">
                      <Label className="text-sm font-medium">Skills</Label>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {selectedApplication.skills.map((skill, index) => (
                          <Badge key={index} variant="secondary">{skill}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Application Info */}
              <Card>
                <CardHeader>
                  <CardTitle>Application Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label className="text-sm font-medium">Job Title</Label>
                      <div>{selectedApplication.job_title}</div>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">Applied Date</Label>
                      <div>{new Date(selectedApplication.applied_at).toLocaleDateString()}</div>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">Status</Label>
                      <div>{getStatusBadge(selectedApplication.status)}</div>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">Last Updated</Label>
                      <div>{new Date(selectedApplication.last_updated).toLocaleDateString()}</div>
                    </div>
                  </div>
                  
                  {selectedApplication.cover_letter && (
                    <div>
                      <Label className="text-sm font-medium">Cover Letter</Label>
                      <div className="mt-2 p-4 bg-muted rounded-md">
                        <p className="whitespace-pre-wrap">{selectedApplication.cover_letter}</p>
                      </div>
                    </div>
                  )}
                  
                  {selectedApplication.candidate_resume_url && (
                    <div>
                      <Label className="text-sm font-medium">Resume</Label>
                      <div className="mt-2">
                        <Button variant="outline" asChild>
                          <a href={selectedApplication.candidate_resume_url} target="_blank" rel="noopener noreferrer">
                            <FileText className="h-4 w-4 mr-2" />
                            View Resume
                          </a>
                        </Button>
                      </div>
                    </div>
                  )}
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

      {/* Rejection Dialog */}
      <Dialog open={showRejectionDialog} onOpenChange={setShowRejectionDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Reject Application</DialogTitle>
            <DialogDescription>
              Please provide a reason for rejecting this application. This will be communicated to the candidate.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            <div>
              <Label htmlFor="rejection-reason">Rejection Reason</Label>
              <Textarea
                id="rejection-reason"
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                placeholder="Please explain why this application is being rejected..."
                rows={4}
              />
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowRejectionDialog(false)}>
              Cancel
            </Button>
            <Button 
              variant="destructive" 
              onClick={() => selectedApplication && updateApplicationStatus(selectedApplication.id, "rejected", rejectionReason)}
              disabled={!rejectionReason.trim()}
            >
              Reject Application
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}