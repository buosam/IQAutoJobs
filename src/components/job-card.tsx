"use client"

import { MapPin, Briefcase, Clock, DollarSign, Building2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Link } from "next/link"

interface Job {
  id: string
  title: string
  company: {
    name: string
    logo_url?: string
  }
  location: string
  type: string
  category: string
  description: string
  salary_min?: number
  salary_max?: number
  currency: string
  created_at: string
}

interface JobCardProps {
  job: Job
}

export function JobCard({ job }: JobCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", { 
      month: "short", 
      day: "numeric",
      year: date.getFullYear() !== new Date().getFullYear() ? "numeric" : undefined
    })
  }

  const getJobTypeColor = (type: string) => {
    switch (type) {
      case "FT": return "bg-green-100 text-green-800"
      case "PT": return "bg-blue-100 text-blue-800"
      case "CONTRACT": return "bg-purple-100 text-purple-800"
      case "INTERN": return "bg-orange-100 text-orange-800"
      default: return "bg-gray-100 text-gray-800"
    }
  }

  const getJobTypeLabel = (type: string) => {
    switch (type) {
      case "FT": return "Full-time"
      case "PT": return "Part-time"
      case "CONTRACT": return "Contract"
      case "INTERN": return "Internship"
      default: return type
    }
  }

  const formatSalary = () => {
    if (!job.salary_min && !job.salary_max) return null
    
    const currency = job.currency || "USD"
    const min = job.salary_min
    const max = job.salary_max
    
    if (min && max) {
      return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}`
    } else if (min) {
      return `${currency} ${min.toLocaleString()}+`
    } else if (max) {
      return `Up to ${currency} ${max.toLocaleString()}`
    }
    
    return null
  }

  return (
    <Card className="h-full hover:shadow-lg transition-shadow duration-200">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg font-semibold mb-1 line-clamp-2">
              <Link 
                href={`/jobs/${job.id}`} 
                className="hover:text-primary transition-colors"
              >
                {job.title}
              </Link>
            </CardTitle>
            <CardDescription className="flex items-center gap-1 text-sm">
              <Building2 className="h-3 w-3" />
              <Link 
                href={`/companies/${job.company.id}`}
                className="hover:text-primary transition-colors"
              >
                {job.company.name}
              </Link>
            </CardDescription>
          </div>
          {job.company.logo_url && (
            <img 
              src={job.company.logo_url} 
              alt={job.company.name}
              className="w-10 h-10 rounded-lg object-cover flex-shrink-0 ml-2"
            />
          )}
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <Badge variant="secondary" className={getJobTypeColor(job.type)}>
            {getJobTypeLabel(job.type)}
          </Badge>
          <Badge variant="outline">
            {job.category}
          </Badge>
        </div>
        
        <div className="space-y-2 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <MapPin className="h-3 w-3" />
            <span>{job.location}</span>
          </div>
          
          {formatSalary() && (
            <div className="flex items-center gap-2">
              <DollarSign className="h-3 w-3" />
              <span>{formatSalary()}</span>
            </div>
          )}
          
          <div className="flex items-center gap-2">
            <Clock className="h-3 w-3" />
            <span>Posted {formatDate(job.created_at)}</span>
          </div>
        </div>
        
        <p className="text-sm text-muted-foreground line-clamp-2">
          {job.description}
        </p>
        
        <Button asChild className="w-full mt-4">
          <Link href={`/jobs/${job.id}`}>
            View Details
          </Link>
        </Button>
      </CardContent>
    </Card>
  )
}