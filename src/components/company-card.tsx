"use client"

import { MapPin, Building2, Users } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"

interface Company {
  id: string
  name: string
  logo_url?: string
  industry: string
  location: string
  description: string
}

interface CompanyCardProps {
  company: Company
}

export function CompanyCard({ company }: CompanyCardProps) {
  return (
    <Card className="h-full hover:shadow-lg transition-shadow duration-200">
      <CardHeader className="pb-3">
        <div className="flex items-center gap-3">
          {company.logo_url ? (
            <img 
              src={company.logo_url} 
              alt={company.name}
              className="w-12 h-12 rounded-lg object-cover flex-shrink-0"
            />
          ) : (
            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
              <Building2 className="h-6 w-6 text-primary" />
            </div>
          )}
          <div className="flex-1 min-w-0">
            <CardTitle className="text-base font-semibold line-clamp-1">
              <Link 
                href={`/companies/${company.id}`} 
                className="hover:text-primary transition-colors"
              >
                {company.name}
              </Link>
            </CardTitle>
            <p className="text-sm text-muted-foreground">{company.industry}</p>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <MapPin className="h-3 w-3" />
          <span>{company.location}</span>
        </div>
        
        <p className="text-sm text-muted-foreground line-clamp-3">
          {company.description}
        </p>
        
        <Button asChild variant="outline" className="w-full">
          <Link href={`/companies/${company.id}`}>
            View Company
          </Link>
        </Button>
      </CardContent>
    </Card>
  )
}