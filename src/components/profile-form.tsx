"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { User, Mail, Phone, MapPin, Briefcase, FileText, Upload, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { toast } from "sonner"

const profileSchema = z.object({
  first_name: z.string().min(1, "First name is required").max(50, "First name is too long"),
  last_name: z.string().min(1, "Last name is required").max(50, "Last name is too long"),
  phone: z.string().optional(),
  bio: z.string().max(500, "Bio must be less than 500 characters").optional(),
  skills: z.string().optional(),
  location: z.string().max(100, "Location is too long").optional(),
  headline: z.string().max(100, "Headline is too long").optional(),
})

type ProfileFormData = z.infer<typeof profileSchema>

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  phone?: string
  role: string
  bio?: string
  skills?: string[]
  location?: string
  headline?: string
  resume_url?: string
}

interface ProfileFormProps {
  user: User
  onSuccess: () => void
  onCancel: () => void
}

export function ProfileForm({ user, onSuccess, onCancel }: ProfileFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [uploadingResume, setUploadingResume] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [resumeUrl, setResumeUrl] = useState(user.resume_url || "")

  const {
    register,
    handleSubmit,
    formState: { errors, isDirty },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      first_name: user.first_name || "",
      last_name: user.last_name || "",
      phone: user.phone || "",
      bio: user.bio || "",
      skills: user.skills?.join(", ") || "",
      location: user.location || "",
      headline: user.headline || "",
    },
  })

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const allowedTypes = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ]
      
      if (!allowedTypes.includes(file.type)) {
        toast.error("Please upload a PDF, DOC, or DOCX file")
        return
      }
      
      if (file.size > 10 * 1024 * 1024) {
        toast.error("File size must be less than 10MB")
        return
      }
      
      setSelectedFile(file)
    }
  }

  const handleResumeUpload = async () => {
    if (!selectedFile) return

    setUploadingResume(true)

    try {
      const formData = new FormData()
      formData.append("file", selectedFile)

      const uploadResponse = await fetch(`/api/files/cv`, {
        method: "POST",
        body: formData,
      })

      if (!uploadResponse.ok) {
        const error = await uploadResponse.json()
        throw new Error(error.error?.message || "Failed to upload resume")
      }

      const uploadData = await uploadResponse.json()
      
      // Update user profile with new resume_url
      const updateResponse = await fetch(`/api/users/me`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_url: uploadData.cv_url,
        }),
      })

      if (updateResponse.ok) {
        setResumeUrl(uploadData.cv_url)
        setSelectedFile(null)
        toast.success("Resume uploaded successfully!")
      } else {
        const error = await updateResponse.json()
        throw new Error(error.error?.message || "Failed to update profile with resume")
      }
    } catch (error: any) {
      console.error("Resume upload error:", error)
      toast.error(error.message || "Failed to upload resume. Please try again.")
    } finally {
      setUploadingResume(false)
    }
  }

  const onSubmit = async (data: ProfileFormData) => {
    setIsSubmitting(true)

    try {
      // Convert comma-separated skills to array
      const skillsArray = data.skills
        ? data.skills.split(",").map(skill => skill.trim()).filter(Boolean)
        : []

      const response = await fetch(`/api/users/me`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          first_name: data.first_name,
          last_name: data.last_name,
          phone: data.phone || null,
          bio: data.bio || null,
          skills: skillsArray.length > 0 ? skillsArray : null,
          location: data.location || null,
          headline: data.headline || null,
        }),
      })

      if (response.ok) {
        toast.success("Profile updated successfully!")
        onSuccess()
      } else {
        const error = await response.json()
        throw new Error(error.error?.message || "Failed to update profile")
      }
    } catch (error: any) {
      console.error("Profile update error:", error)
      toast.error(error.message || "Failed to update profile. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Basic Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Basic Information
          </CardTitle>
          <CardDescription>Update your personal details</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="first_name">First Name *</Label>
              <Input
                id="first_name"
                {...register("first_name")}
                disabled={isSubmitting}
              />
              {errors.first_name && (
                <p className="text-sm text-destructive">{errors.first_name.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="last_name">Last Name *</Label>
              <Input
                id="last_name"
                {...register("last_name")}
                disabled={isSubmitting}
              />
              {errors.last_name && (
                <p className="text-sm text-destructive">{errors.last_name.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input
                id="email"
                type="email"
                value={user.email}
                disabled
                className="pl-10 bg-muted"
              />
            </div>
            <p className="text-xs text-muted-foreground">Email cannot be changed</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="phone">Phone</Label>
            <div className="relative">
              <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input
                id="phone"
                {...register("phone")}
                placeholder="+1 (555) 000-0000"
                className="pl-10"
                disabled={isSubmitting}
              />
            </div>
            {errors.phone && (
              <p className="text-sm text-destructive">{errors.phone.message}</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Professional Details */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Briefcase className="h-5 w-5" />
            Professional Details
          </CardTitle>
          <CardDescription>Tell us about your professional background</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="headline">Headline</Label>
            <Input
              id="headline"
              {...register("headline")}
              placeholder="e.g., Senior Software Engineer | Full Stack Developer"
              disabled={isSubmitting}
            />
            {errors.headline && (
              <p className="text-sm text-destructive">{errors.headline.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="location">Location</Label>
            <div className="relative">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input
                id="location"
                {...register("location")}
                placeholder="e.g., San Francisco, CA"
                className="pl-10"
                disabled={isSubmitting}
              />
            </div>
            {errors.location && (
              <p className="text-sm text-destructive">{errors.location.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="skills">Skills</Label>
            <Input
              id="skills"
              {...register("skills")}
              placeholder="e.g., JavaScript, React, Node.js, Python"
              disabled={isSubmitting}
            />
            <p className="text-xs text-muted-foreground">
              Separate skills with commas
            </p>
            {errors.skills && (
              <p className="text-sm text-destructive">{errors.skills.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="bio">Bio</Label>
            <Textarea
              id="bio"
              {...register("bio")}
              placeholder="Tell us about yourself, your experience, and what you're looking for..."
              rows={4}
              disabled={isSubmitting}
            />
            <p className="text-xs text-muted-foreground">
              Maximum 500 characters
            </p>
            {errors.bio && (
              <p className="text-sm text-destructive">{errors.bio.message}</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Resume Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Resume / CV
          </CardTitle>
          <CardDescription>Upload your latest resume</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {resumeUrl && !selectedFile && (
            <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
              <div className="flex items-center gap-3">
                <FileText className="h-8 w-8 text-blue-600" />
                <div>
                  <p className="text-sm font-medium">Current Resume</p>
                  <a
                    href={resumeUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-primary hover:underline"
                  >
                    View Resume
                  </a>
                </div>
              </div>
            </div>
          )}

          {!selectedFile ? (
            <div className="border-dashed border-2 border-muted-foreground/25 rounded-lg p-6">
              <div className="text-center space-y-3">
                <Upload className="h-10 w-10 text-muted-foreground mx-auto" />
                <div>
                  <Label htmlFor="resume-upload" className="cursor-pointer">
                    <span className="text-sm font-medium text-primary hover:underline">
                      Click to upload
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {" "}or drag and drop
                    </span>
                  </Label>
                  <Input
                    id="resume-upload"
                    type="file"
                    className="hidden"
                    accept=".pdf,.doc,.docx"
                    onChange={handleFileSelect}
                    disabled={uploadingResume}
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  PDF, DOC, or DOCX (max. 10MB)
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                <div className="flex items-center gap-3">
                  <FileText className="h-8 w-8 text-blue-600" />
                  <div>
                    <p className="text-sm font-medium">{selectedFile.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {formatFileSize(selectedFile.size)}
                    </p>
                  </div>
                </div>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedFile(null)}
                  disabled={uploadingResume}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
              <Button
                type="button"
                onClick={handleResumeUpload}
                disabled={uploadingResume}
                className="w-full"
              >
                {uploadingResume ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Uploading...
                  </>
                ) : (
                  <>
                    <Upload className="h-4 w-4 mr-2" />
                    Upload Resume
                  </>
                )}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3 sticky bottom-0 bg-background p-4 border-t">
        <Button
          type="submit"
          className="flex-1"
          disabled={isSubmitting || !isDirty}
        >
          {isSubmitting ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Saving...
            </>
          ) : (
            "Save Changes"
          )}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isSubmitting}
          className="flex-1"
        >
          Cancel
        </Button>
      </div>
    </form>
  )
}
