"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { 
  Save, 
  Eye, 
  X,
  Plus,
  Trash2,
  Info
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
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface JobFormData {
  title: string
  description: string
  requirements: string
  benefits: string
  location: string
  type: string
  category: string
  experience_level: string
  salary_min: string
  salary_max: string
  currency: string
  application_deadline: string
  status: string
  skills: string[]
}

const jobTypes = [
  "Full-time",
  "Part-time",
  "Contract",
  "Internship",
  "Remote",
  "Hybrid"
]

const categories = [
  "Engineering",
  "Design",
  "Marketing",
  "Sales",
  "Customer Support",
  "Product",
  "Data Science",
  "DevOps",
  "HR",
  "Finance",
  "Operations",
  "Other"
]

const experienceLevels = [
  "Entry Level",
  "Junior",
  "Mid-Level",
  "Senior",
  "Lead",
  "Executive"
]

const currencies = [
  "USD",
  "EUR",
  "GBP",
  "CAD",
  "AUD",
  "JPY",
  "CNY",
  "INR"
]

interface JobPostFormProps {
  job?: any
  isEditing?: boolean
}

export function JobPostForm({ job, isEditing = false }: JobPostFormProps) {
  const router = useRouter()
  const [formData, setFormData] = useState<JobFormData>({
    title: "",
    description: "",
    requirements: "",
    benefits: "",
    location: "",
    type: "",
    category: "",
    experience_level: "",
    salary_min: "",
    salary_max: "",
    currency: "USD",
    application_deadline: "",
    status: "draft",
    skills: []
  })
  const [loading, setLoading] = useState(false)
  const [newSkill, setNewSkill] = useState("")
  const [showPreview, setShowPreview] = useState(false)
  const [showSaveDialog, setShowSaveDialog] = useState(false)

  useEffect(() => {
    if (job) {
      setFormData({
        title: job.title || "",
        description: job.description || "",
        requirements: job.requirements || "",
        benefits: job.benefits || "",
        location: job.location || "",
        type: job.type || "",
        category: job.category || "",
        experience_level: job.experience_level || "",
        salary_min: job.salary_min?.toString() || "",
        salary_max: job.salary_max?.toString() || "",
        currency: job.currency || "USD",
        application_deadline: job.application_deadline || "",
        status: job.status || "draft",
        skills: job.skills || []
      })
    }
  }, [job])

  const handleInputChange = (field: keyof JobFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const addSkill = () => {
    if (newSkill.trim() && !formData.skills.includes(newSkill.trim())) {
      setFormData(prev => ({
        ...prev,
        skills: [...prev.skills, newSkill.trim()]
      }))
      setNewSkill("")
    }
  }

  const removeSkill = (skillToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      skills: prev.skills.filter(skill => skill !== skillToRemove)
    }))
  }

  const handleSubmit = async (status: string = formData.status) => {
    setLoading(true)
    try {
      const payload = {
        ...formData,
        status,
        salary_min: formData.salary_min ? parseInt(formData.salary_min) : null,
        salary_max: formData.salary_max ? parseInt(formData.salary_max) : null
      }

      const url = isEditing ? `/api/employer/jobs/${job.id}` : "/api/employer/jobs"
      const method = isEditing ? "PUT" : "POST"

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        const savedJob = await response.json()
        router.push(`/employer/jobs/${savedJob.id}`)
      }
    } catch (error) {
      console.error("Failed to save job:", error)
    } finally {
      setLoading(false)
      setShowSaveDialog(false)
    }
  }

  const handleSaveDraft = () => {
    handleSubmit("draft")
  }

  const handlePublish = () => {
    setShowSaveDialog(true)
  }

  const confirmPublish = () => {
    handleSubmit("active")
  }

  if (showPreview) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Preview</h1>
          <div className="flex space-x-2">
            <Button variant="outline" onClick={() => setShowPreview(false)}>
              <X className="h-4 w-4 mr-2" />
              Back to Edit
            </Button>
            <Button onClick={handlePublish}>
              <Save className="h-4 w-4 mr-2" />
              Publish Job
            </Button>
          </div>
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              {formData.title}
              <Badge variant="outline">{formData.type}</Badge>
            </CardTitle>
            <CardDescription>
              {formData.location} • {formData.category} • {formData.experience_level}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="font-semibold mb-2">Job Description</h3>
              <p className="text-muted-foreground whitespace-pre-wrap">{formData.description}</p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Requirements</h3>
              <p className="text-muted-foreground whitespace-pre-wrap">{formData.requirements}</p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Benefits</h3>
              <p className="text-muted-foreground whitespace-pre-wrap">{formData.benefits}</p>
            </div>
            
            {formData.skills.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Required Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {formData.skills.map((skill, index) => (
                    <Badge key={index} variant="secondary">{skill}</Badge>
                  ))}
                </div>
              </div>
            )}
            
            {formData.salary_min && formData.salary_max && (
              <div>
                <h3 className="font-semibold mb-2">Salary</h3>
                <p className="text-muted-foreground">
                  {formData.currency} {formData.salary_min} - {formData.salary_max}
                </p>
              </div>
            )}
            
            {formData.application_deadline && (
              <div>
                <h3 className="font-semibold mb-2">Application Deadline</h3>
                <p className="text-muted-foreground">
                  {new Date(formData.application_deadline).toLocaleDateString()}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">
          {isEditing ? "Edit Job" : "Post New Job"}
        </h1>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={handleSaveDraft} disabled={loading}>
            <Save className="h-4 w-4 mr-2" />
            Save Draft
          </Button>
          <Button onClick={() => setShowPreview(true)}>
            <Eye className="h-4 w-4 mr-2" />
            Preview
          </Button>
        </div>
      </div>

      <Tabs defaultValue="basic" className="space-y-6">
        <TabsList>
          <TabsTrigger value="basic">Basic Info</TabsTrigger>
          <TabsTrigger value="details">Job Details</TabsTrigger>
          <TabsTrigger value="requirements">Requirements</TabsTrigger>
          <TabsTrigger value="compensation">Compensation</TabsTrigger>
        </TabsList>

        <TabsContent value="basic" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
              <CardDescription>
                Enter the basic details about the job position
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="title">Job Title *</Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => handleInputChange("title", e.target.value)}
                  placeholder="e.g. Senior Frontend Developer"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="location">Location *</Label>
                  <Input
                    id="location"
                    value={formData.location}
                    onChange={(e) => handleInputChange("location", e.target.value)}
                    placeholder="e.g. San Francisco, CA"
                  />
                </div>
                
                <div>
                  <Label htmlFor="type">Job Type *</Label>
                  <Select value={formData.type} onValueChange={(value) => handleInputChange("type", value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select job type" />
                    </SelectTrigger>
                    <SelectContent>
                      {jobTypes.map((type) => (
                        <SelectItem key={type} value={type}>{type}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="category">Category *</Label>
                  <Select value={formData.category} onValueChange={(value) => handleInputChange("category", value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((category) => (
                        <SelectItem key={category} value={category}>{category}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label htmlFor="experience_level">Experience Level *</Label>
                  <Select value={formData.experience_level} onValueChange={(value) => handleInputChange("experience_level", value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select experience level" />
                    </SelectTrigger>
                    <SelectContent>
                      {experienceLevels.map((level) => (
                        <SelectItem key={level} value={level}>{level}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="details" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Job Description</CardTitle>
              <CardDescription>
                Provide a detailed description of the job role and responsibilities
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="description">Job Description *</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => handleInputChange("description", e.target.value)}
                  placeholder="Describe the role, responsibilities, and what the candidate will be doing..."
                  rows={6}
                />
              </div>
              
              <div>
                <Label htmlFor="benefits">Benefits & Perks</Label>
                <Textarea
                  id="benefits"
                  value={formData.benefits}
                  onChange={(e) => handleInputChange("benefits", e.target.value)}
                  placeholder="List the benefits, perks, and additional compensation..."
                  rows={4}
                />
              </div>
              
              <div>
                <Label htmlFor="skills">Required Skills</Label>
                <div className="space-y-2">
                  <div className="flex space-x-2">
                    <Input
                      value={newSkill}
                      onChange={(e) => setNewSkill(e.target.value)}
                      placeholder="Add a skill..."
                      onKeyPress={(e) => e.key === "Enter" && (e.preventDefault(), addSkill())}
                    />
                    <Button type="button" onClick={addSkill}>
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {formData.skills.map((skill, index) => (
                      <Badge key={index} variant="secondary" className="flex items-center space-x-1">
                        <span>{skill}</span>
                        <button
                          type="button"
                          onClick={() => removeSkill(skill)}
                          className="ml-1 hover:text-destructive"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="requirements" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Requirements & Qualifications</CardTitle>
              <CardDescription>
                Specify the requirements, qualifications, and application process
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="requirements">Requirements *</Label>
                <Textarea
                  id="requirements"
                  value={formData.requirements}
                  onChange={(e) => handleInputChange("requirements", e.target.value)}
                  placeholder="List the required qualifications, skills, experience, and education..."
                  rows={6}
                />
              </div>
              
              <div>
                <Label htmlFor="application_deadline">Application Deadline</Label>
                <Input
                  id="application_deadline"
                  type="date"
                  value={formData.application_deadline}
                  onChange={(e) => handleInputChange("application_deadline", e.target.value)}
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="compensation" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Compensation & Benefits</CardTitle>
              <CardDescription>
                Set the salary range and compensation details
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Alert>
                <Info className="h-4 w-4" />
                <AlertDescription>
                  Providing salary information helps attract qualified candidates and promotes pay transparency.
                </AlertDescription>
              </Alert>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="currency">Currency</Label>
                  <Select value={formData.currency} onValueChange={(value) => handleInputChange("currency", value)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {currencies.map((currency) => (
                        <SelectItem key={currency} value={currency}>{currency}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label htmlFor="salary_min">Minimum Salary</Label>
                  <Input
                    id="salary_min"
                    type="number"
                    value={formData.salary_min}
                    onChange={(e) => handleInputChange("salary_min", e.target.value)}
                    placeholder="e.g. 50000"
                  />
                </div>
                
                <div>
                  <Label htmlFor="salary_max">Maximum Salary</Label>
                  <Input
                    id="salary_max"
                    type="number"
                    value={formData.salary_max}
                    onChange={(e) => handleInputChange("salary_max", e.target.value)}
                    placeholder="e.g. 80000"
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Publish Confirmation Dialog */}
      <Dialog open={showSaveDialog} onOpenChange={setShowSaveDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Publish Job Posting</DialogTitle>
            <DialogDescription>
              Are you sure you want to publish this job? It will be visible to all candidates and you'll start receiving applications.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowSaveDialog(false)}>
              Cancel
            </Button>
            <Button onClick={confirmPublish} disabled={loading}>
              {loading ? "Publishing..." : "Publish Job"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}