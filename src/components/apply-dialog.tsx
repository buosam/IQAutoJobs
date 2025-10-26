"use client"

import { useState } from "react"
import { Upload, FileText, Send, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface Job {
  id: string
  title: string
  company: {
    name: string
    id: string
  }
}

interface ApplyDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  job: Job
}

export function ApplyDialog({ open, onOpenChange, job }: ApplyDialogProps) {
  const [coverLetter, setCoverLetter] = useState("")
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      // Validate file type
      const allowedTypes = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ]
      
      if (!allowedTypes.includes(file.type)) {
        alert("Please upload a PDF, DOC, or DOCX file")
        return
      }
      
      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert("File size must be less than 10MB")
        return
      }
      
      setSelectedFile(file)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!selectedFile) {
      alert("Please upload your CV")
      return
    }

    setUploading(true)
    setUploadProgress(0)

    try {
      // Create form data
      const formData = new FormData()
      formData.append("file", selectedFile)
      formData.append("cover_letter", coverLetter)

      // Upload CV and apply
      const response = await fetch(`/api/applications`, {
        method: "POST",
        body: formData,
      })

      if (response.ok) {
        alert("Application submitted successfully!")
        onOpenChange(false)
        // Reset form
        setCoverLetter("")
        setSelectedFile(null)
      } else {
        const error = await response.json()
        alert(error.detail || "Failed to submit application")
      }
    } catch (error) {
      console.error("Application submission error:", error)
      alert("Failed to submit application. Please try again.")
    } finally {
      setUploading(false)
      setUploadProgress(0)
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
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Apply for {job.title}</DialogTitle>
          <DialogDescription>
            {job.company.name} • {job.company.location}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* CV Upload */}
          <div className="space-y-3">
            <Label htmlFor="cv">Upload Your CV *</Label>
            <Card className="border-dashed border-2 border-muted-foreground/25">
              <CardContent className="p-6">
                {!selectedFile ? (
                  <div className="text-center space-y-3">
                    <Upload className="h-10 w-10 text-muted-foreground mx-auto" />
                    <div>
                      <Label htmlFor="cv-upload" className="cursor-pointer">
                        <span className="text-sm font-medium text-primary hover:underline">
                          Click to upload
                        </span>
                        <span className="text-sm text-muted-foreground">
                          {" "}or drag and drop
                        </span>
                      </Label>
                      <Input
                        id="cv-upload"
                        type="file"
                        className="hidden"
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileSelect}
                      />
                    </div>
                    <p className="text-xs text-muted-foreground">
                      PDF, DOC, or DOCX (max. 10MB)
                    </p>
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
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Cover Letter */}
          <div className="space-y-3">
            <Label htmlFor="cover-letter">Cover Letter (Optional)</Label>
            <Textarea
              id="cover-letter"
              placeholder="Write a brief cover letter explaining why you're a great fit for this position..."
              value={coverLetter}
              onChange={(e) => setCoverLetter(e.target.value)}
              rows={4}
            />
            <p className="text-xs text-muted-foreground">
              Keep it concise and highlight your most relevant experience
            </p>
          </div>

          {/* Application Summary */}
          <Card>
            <CardContent className="p-4 space-y-2">
              <h4 className="font-medium text-sm">Application Summary</h4>
              <div className="flex items-center gap-2">
                <Badge variant="outline">
                  <FileText className="h-3 w-3 mr-1" />
                  CV: {selectedFile ? selectedFile.name : "Not uploaded"}
                </Badge>
                <Badge variant="outline">
                  Cover Letter: {coverLetter ? "Added" : "Not added"}
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex flex-col sm:flex-row gap-3">
            <Button 
              type="submit" 
              className="flex-1"
              disabled={uploading || !selectedFile}
            >
              {uploading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Submitting...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4 mr-2" />
                  Submit Application
                </>
              )}
            </Button>
            <Button 
              type="button" 
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={uploading}
            >
              Cancel
            </Button>
          </div>

          {uploading && uploadProgress > 0 && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Uploading...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
            </div>
          )}
        </form>
      </DialogContent>
    </Dialog>
  )
}