"use client"

import { useState } from "react"
import { useSearchParams } from "next/navigation"
import { Filter, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"

const employmentTypes = [
  { value: "FT", label: "Full-time" },
  { value: "PT", label: "Part-time" },
  { value: "CONTRACT", label: "Contract" },
  { value: "INTERN", label: "Internship" }
]

const experienceLevels = [
  { value: "Entry", label: "Entry Level" },
  { value: "Mid", label: "Mid Level" },
  { value: "Senior", label: "Senior Level" },
  { value: "Executive", label: "Executive" }
]

const categories = [
  "Engineering",
  "Design",
  "Marketing",
  "Sales",
  "Customer Support",
  "Product",
  "Data Science",
  "Finance",
  "HR",
  "Operations",
  "Legal",
  "Other"
]

interface JobFiltersProps {
  className?: string
}

export function JobFilters({}: JobFiltersProps) {
  const searchParams = useSearchParams()
  const [isExpanded, setIsExpanded] = useState(false)

  // Get current filter values
  const currentType = searchParams.get("type") || ""
  const currentCategory = searchParams.get("category") || ""
  const currentExperience = searchParams.get("experience_level") || ""
  const currentSalaryMin = searchParams.get("salary_min") || ""
  const currentSalaryMax = searchParams.get("salary_max") || ""

  const updateFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams)
    if (value) {
      params.set(key, value)
    } else {
      params.delete(key)
    }
    params.set("page", "1")
    window.location.href = `/jobs?${params.toString()}`
  }

  const clearAllFilters = () => {
    const params = new URLSearchParams(searchParams)
    const keysToClear = ["type", "category", "experience_level", "salary_min", "salary_max"]
    keysToClear.forEach(key => params.delete(key))
    params.set("page", "1")
    window.location.href = `/jobs?${params.toString()}`
  }

  const hasActiveFilters = currentType || currentCategory || currentExperience || currentSalaryMin || currentSalaryMax

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg flex items-center gap-2">
            <Filter className="h-4 w-4" />
            Filters
          </CardTitle>
          {hasActiveFilters && (
            <Button
              variant="ghost"
              size="sm"
              onClick={clearAllFilters}
              className="text-xs"
            >
              Clear All
            </Button>
          )}
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Active Filters */}
        {hasActiveFilters && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Active Filters</h4>
            <div className="flex flex-wrap gap-1">
              {currentType && (
                <Badge variant="secondary" className="text-xs">
                  {employmentTypes.find(t => t.value === currentType)?.label}
                  <button
                    onClick={() => updateFilter("type", "")}
                    className="ml-1 hover:text-foreground"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              )}
              {currentCategory && (
                <Badge variant="secondary" className="text-xs">
                  {currentCategory}
                  <button
                    onClick={() => updateFilter("category", "")}
                    className="ml-1 hover:text-foreground"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              )}
              {currentExperience && (
                <Badge variant="secondary" className="text-xs">
                  {experienceLevels.find(e => e.value === currentExperience)?.label}
                  <button
                    onClick={() => updateFilter("experience_level", "")}
                    className="ml-1 hover:text-foreground"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              )}
            </div>
          </div>
        )}

        <Accordion type="single" collapsible className="w-full">
          {/* Employment Type */}
          <AccordionItem value="type">
            <AccordionTrigger className="text-sm">Employment Type</AccordionTrigger>
            <AccordionContent>
              <Select value={currentType} onValueChange={(value) => updateFilter("type", value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">All Types</SelectItem>
                  {employmentTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </AccordionContent>
          </AccordionItem>

          {/* Category */}
          <AccordionItem value="category">
            <AccordionTrigger className="text-sm">Category</AccordionTrigger>
            <AccordionContent>
              <Select value={currentCategory} onValueChange={(value) => updateFilter("category", value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">All Categories</SelectItem>
                  {categories.map((category) => (
                    <SelectItem key={category} value={category}>
                      {category}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </AccordionContent>
          </AccordionItem>

          {/* Experience Level */}
          <AccordionItem value="experience">
            <AccordionTrigger className="text-sm">Experience Level</AccordionTrigger>
            <AccordionContent>
              <Select value={currentExperience} onValueChange={(value) => updateFilter("experience_level", value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select experience level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">All Levels</SelectItem>
                  {experienceLevels.map((level) => (
                    <SelectItem key={level.value} value={level.value}>
                      {level.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </AccordionContent>
          </AccordionItem>

          {/* Salary Range */}
          <AccordionItem value="salary">
            <AccordionTrigger className="text-sm">Salary Range</AccordionTrigger>
            <AccordionContent>
              <div className="space-y-2">
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-xs text-muted-foreground">Min Salary</label>
                    <Input
                      type="number"
                      placeholder="0"
                      value={currentSalaryMin}
                      onChange={(e) => updateFilter("salary_min", e.target.value)}
                      className="h-8"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground">Max Salary</label>
                    <Input
                      type="number"
                      placeholder="100000"
                      value={currentSalaryMax}
                      onChange={(e) => updateFilter("salary_max", e.target.value)}
                      className="h-8"
                    />
                  </div>
                </div>
                <p className="text-xs text-muted-foreground">Annual salary in USD</p>
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </CardContent>
    </Card>
  )
}