"use client"

import { Suspense } from "react"
import CompaniesContent from "./companies-content"

export default function CompaniesPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
        <p className="text-muted-foreground">Loading companies...</p>
      </div>
    </div>}>
      <CompaniesContent />
    </Suspense>
  )
}
