"use client"

import { useState, useEffect } from "react"
import { 
  User, 
  Briefcase, 
  MapPin, 
  Mail, 
  Phone, 
  Calendar,
  Edit,
  Save,
  X,
  Plus,
  Trash2,
  Upload,
  Download,
  FileText,
  Eye
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface ProfileData {
  first_name: string
  last_name: string
  email: string
  phone?: string
  location?: string
  headline?: string
  summary?: string
  website?: string
  linkedin?: string
  github?: string
  experience: Experience[]
  education: Education[]
  skills: string[]
  resume_url?: string
}

interface Experience {
  id: string
  title: string
  company: string
  location?: string
  start_date: string
  end_date?: string
  current: boolean
  description: string
}

interface Education {
  id: string
  institution: string
  degree: string
  field: string
  start_date: string
  end_date?: string
  current: boolean
  gpa?: string
}

const experienceLevels = [
  "Entry Level",
  "Junior",
  "Mid-Level",
  "Senior",
  "Lead",
  "Executive"
]

const jobTypes = [
  "Full-time",
  "Part-time",
  "Contract",
  "Internship",
  "Remote",
  "Hybrid"
]

export function CandidateProfile() {
  const [profile, setProfile] = useState<ProfileData>({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    location: "",
    headline: "",
    summary: "",
    website: "",
    linkedin: "",
    github: "",
    experience: [],
    education: [],
    skills: []
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [newSkill, setNewSkill] = useState("")
  const [showResumeDialog, setShowResumeDialog] = useState(false)
  const [resumeFile, setResumeFile] = useState<File | null>(null)

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const response = await fetch("/api/candidate/profile")
      if (response.ok) {
        const profileData = await response.json()
        setProfile(profileData)
      }
    } catch (error) {
      console.error("Failed to fetch profile:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const response = await fetch("/api/candidate/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(profile),
      })
      
      if (response.ok) {
        setIsEditing(false)
      }
    } catch (error) {
      console.error("Failed to save profile:", error)
    } finally {
      setSaving(false)
    }
  }

  const addSkill = () => {
    if (newSkill.trim() && !profile.skills.includes(newSkill.trim())) {
      setProfile(prev => ({
        ...prev,
        skills: [...prev.skills, newSkill.trim()]
      }))
      setNewSkill("")
    }
  }

  const removeSkill = (skillToRemove: string) => {
    setProfile(prev => ({
      ...prev,
      skills: prev.skills.filter(skill => skill !== skillToRemove)
    }))
  }

  const handleResumeUpload = async () => {
    if (!resumeFile) return

    const formData = new FormData()
    formData.append("resume", resumeFile)

    try {
      const response = await fetch("/api/candidate/profile/resume", {
        method: "POST",
        body: formData,
      })
      
      if (response.ok) {
        const data = await response.json()
        setProfile(prev => ({
          ...prev,
          resume_url: data.resume_url
        }))
        setShowResumeDialog(false)
        setResumeFile(null)
      }
    } catch (error) {
      console.error("Failed to upload resume:", error)
    }
  }

  const getProfileCompletion = () => {
    const fields = [
      profile.first_name,
      profile.last_name,
      profile.headline,
      profile.summary,
      profile.location,
      profile.skills.length > 0,
      profile.experience.length > 0,
      profile.education.length > 0,
      profile.resume_url
    ]
    
    const completedFields = fields.filter(field => field).length
    return Math.round((completedFields / fields.length) * 100)
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-1/3 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[...Array(3)].map((_, i) => (
              <Card key={i}>
                <CardContent className="p-6">
                  <div className="h-4 bg-muted rounded w-3/4 mb-2"></div>
                  <div className="h-3 bg-muted rounded w-full mb-2"></div>
                  <div className="h-3 bg-muted rounded w-2/3"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Profile</h1>
          <p className="text-muted-foreground">
            Manage your profile information and preferences
          </p>
        </div>
        <div className="flex space-x-2">
          {isEditing ? (
            <>
              <Button variant="outline" onClick={() => setIsEditing(false)}>
                <X className="h-4 w-4 mr-2" />
                Cancel
              </Button>
              <Button onClick={handleSave} disabled={saving}>
                <Save className="h-4 w-4 mr-2" />
                {saving ? "Saving..." : "Save Changes"}
              </Button>
            </>
          ) : (
            <Button onClick={() => setIsEditing(true)}>
              <Edit className="h-4 w-4 mr-2" />
              Edit Profile
            </Button>
          )}
        </div>
      </div>

      {/* Profile Completion */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold">Profile Completion</h3>
              <p className="text-sm text-muted-foreground">
                Complete your profile to increase visibility to employers
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold">{getProfileCompletion()}%</div>
            </div>
          </div>
          <div className="mt-4">
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div 
                className="h-full bg-primary transition-all duration-300"
                style={{ width: `${getProfileCompletion()}%` }}
              ></div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="basic" className="space-y-6">
        <TabsList>
          <TabsTrigger value="basic">Basic Info</TabsTrigger>
          <TabsTrigger value="experience">Experience</TabsTrigger>
          <TabsTrigger value="education">Education</TabsTrigger>
          <TabsTrigger value="skills">Skills</TabsTrigger>
          <TabsTrigger value="resume">Resume</TabsTrigger>
        </TabsList>

        <TabsContent value="basic" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
              <CardDescription>
                Update your personal and contact information
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="first_name">First Name</Label>
                  <Input
                    id="first_name"
                    value={profile.first_name}
                    onChange={(e) => setProfile(prev => ({ ...prev, first_name: e.target.value }))}
                    disabled={!isEditing}
                  />
                </div>
                <div>
                  <Label htmlFor="last_name">Last Name</Label>
                  <Input
                    id="last_name"
                    value={profile.last_name}
                    onChange={(e) => setProfile(prev => ({ ...prev, last_name: e.target.value }))}
                    disabled={!isEditing}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={profile.email}
                    onChange={(e) => setProfile(prev => ({ ...prev, email: e.target.value }))}
                    disabled={!isEditing}
                  />
                </div>
                <div>
                  <Label htmlFor="phone">Phone</Label>
                  <Input
                    id="phone"
                    value={profile.phone || ""}
                    onChange={(e) => setProfile(prev => ({ ...prev, phone: e.target.value }))}
                    disabled={!isEditing}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    value={profile.location || ""}
                    onChange={(e) => setProfile(prev => ({ ...prev, location: e.target.value }))}
                    disabled={!isEditing}
                  />
                </div>
                <div>
                  <Label htmlFor="headline">Professional Headline</Label>
                  <Input
                    id="headline"
                    value={profile.headline || ""}
                    onChange={(e) => setProfile(prev => ({ ...prev, headline: e.target.value }))}
                    placeholder="e.g. Senior Frontend Developer"
                    disabled={!isEditing}
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="summary">Professional Summary</Label>
                <Textarea
                  id="summary"
                  value={profile.summary || ""}
                  onChange={(e) => setProfile(prev => ({ ...prev, summary: e.target.value }))}
                  placeholder="Write a brief summary about yourself, your experience, and your career goals..."
                  rows={4}
                  disabled={!isEditing}
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="website">Website</Label>
                  <Input
                    id="website"
                    value={profile.website || ""}
                    onChange={(e) => setProfile(prev => ({ ...prev, website: e.target.value }))}
                    placeholder="https://yourwebsite.com"
                    disabled={!isEditing}
                  />
                </div>
                <div>
                  <Label htmlFor="linkedin">LinkedIn</Label>
                  <Input
                    id="linkedin"
                    value={profile.linkedin || ""}
                    onChange={(e) => setProfile(prev => ({ ...prev, linkedin: e.target.value }))}
                    placeholder="https://linkedin.com/in/yourprofile"
                    disabled={!isEditing}
                  />
                </div>
                <div>
                  <Label htmlFor="github">GitHub</Label>
                  <Input
                    id="github"
                    value={profile.github || ""}
                    onChange={(e) => setProfile(prev => ({ ...prev, github: e.target.value }))}
                    placeholder="https://github.com/yourusername"
                    disabled={!isEditing}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="experience" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Work Experience</CardTitle>
              <CardDescription>
                Add your work experience to showcase your career journey
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Alert className="mb-4">
                <Briefcase className="h-4 w-4" />
                <AlertDescription>
                  Add your most recent work experience first. Include relevant achievements and responsibilities.
                </AlertDescription>
              </Alert>
              
              <div className="space-y-4">
                {profile.experience.map((exp) => (
                  <div key={exp.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-semibold">{exp.title}</h3>
                        <p className="text-muted-foreground">{exp.company}</p>
                        {exp.location && (
                          <p className="text-sm text-muted-foreground">
                            <MapPin className="inline h-3 w-3 mr-1" />
                            {exp.location}
                          </p>
                        )}
                        <p className="text-sm text-muted-foreground">
                          <Calendar className="inline h-3 w-3 mr-1" />
                          {new Date(exp.start_date).toLocaleDateString()} - {exp.current ? "Present" : new Date(exp.end_date!).toLocaleDateString()}
                        </p>
                      </div>
                      {isEditing && (
                        <Button variant="ghost" size="icon">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                    {exp.description && (
                      <p className="mt-2 text-sm">{exp.description}</p>
                    )}
                  </div>
                ))}
                
                {isEditing && (
                  <Button variant="outline" className="w-full">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Experience
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="education" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Education</CardTitle>
              <CardDescription>
                Add your educational background and qualifications
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {profile.education.map((edu) => (
                  <div key={edu.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-semibold">{edu.degree} in {edu.field}</h3>
                        <p className="text-muted-foreground">{edu.institution}</p>
                        <p className="text-sm text-muted-foreground">
                          <Calendar className="inline h-3 w-3 mr-1" />
                          {new Date(edu.start_date).toLocaleDateString()} - {edu.current ? "Present" : new Date(edu.end_date!).toLocaleDateString()}
                        </p>
                        {edu.gpa && (
                          <p className="text-sm text-muted-foreground">GPA: {edu.gpa}</p>
                        )}
                      </div>
                      {isEditing && (
                        <Button variant="ghost" size="icon">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
                
                {isEditing && (
                  <Button variant="outline" className="w-full">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Education
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="skills" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Skills</CardTitle>
              <CardDescription>
                Add your skills to help employers find you
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex space-x-2">
                  <Input
                    value={newSkill}
                    onChange={(e) => setNewSkill(e.target.value)}
                    placeholder="Add a skill..."
                    onKeyPress={(e) => e.key === "Enter" && (e.preventDefault(), addSkill())}
                    disabled={!isEditing}
                  />
                  <Button type="button" onClick={addSkill} disabled={!isEditing}>
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                
                <div className="flex flex-wrap gap-2">
                  {profile.skills.map((skill, index) => (
                    <Badge key={index} variant="secondary" className="flex items-center space-x-1">
                      <span>{skill}</span>
                      {isEditing && (
                        <button
                          type="button"
                          onClick={() => removeSkill(skill)}
                          className="ml-1 hover:text-destructive"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      )}
                    </Badge>
                  ))}
                </div>
                
                {profile.skills.length === 0 && (
                  <p className="text-muted-foreground">No skills added yet. Add your technical and soft skills here.</p>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="resume" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Resume</CardTitle>
              <CardDescription>
                Upload and manage your resume
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {profile.resume_url ? (
                  <div className="border rounded-lg p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-8 w-8 text-primary" />
                        <div>
                          <h3 className="font-medium">Resume Uploaded</h3>
                          <p className="text-sm text-muted-foreground">
                            Last updated: {new Date().toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <Button variant="outline" asChild>
                          <a href={profile.resume_url} target="_blank" rel="noopener noreferrer">
                            <Eye className="h-4 w-4 mr-2" />
                            View
                          </a>
                        </Button>
                        <Button variant="outline" asChild>
                          <a href={profile.resume_url} download>
                            <Download className="h-4 w-4 mr-2" />
                            Download
                          </a>
                        </Button>
                        <Button onClick={() => setShowResumeDialog(true)}>
                          <Upload className="h-4 w-4 mr-2" />
                          Update
                        </Button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center">
                    <Upload className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">No Resume Uploaded</h3>
                    <p className="text-muted-foreground mb-4">
                      Upload your resume to apply for jobs faster
                    </p>
                    <Button onClick={() => setShowResumeDialog(true)}>
                      <Upload className="h-4 w-4 mr-2" />
                      Upload Resume
                    </Button>
                  </div>
                )}
                
                <Alert>
                  <AlertDescription>
                    Supported formats: PDF, DOC, DOCX (Max size: 5MB). Make sure your resume is up-to-date and highlights your most relevant experience and skills.
                  </AlertDescription>
                </Alert>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Resume Upload Dialog */}
      <Dialog open={showResumeDialog} onOpenChange={setShowResumeDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Upload Resume</DialogTitle>
            <DialogDescription>
              Choose a PDF or Word document to upload as your resume
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            <div>
              <Label htmlFor="resume-file">Select Resume File</Label>
              <Input
                id="resume-file"
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
              />
            </div>
            
            {resumeFile && (
              <div className="p-4 bg-muted rounded-lg">
                <p className="text-sm">
                  <strong>File:</strong> {resumeFile.name}
                </p>
                <p className="text-sm">
                  <strong>Size:</strong> {(resumeFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            )}
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowResumeDialog(false)}>
              Cancel
            </Button>
            <Button onClick={handleResumeUpload} disabled={!resumeFile}>
              Upload Resume
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}