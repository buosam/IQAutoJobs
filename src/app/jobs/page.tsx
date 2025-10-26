"use client"

import { Suspense } from "react"
import JobsContent from "./jobs-content"

export default function JobsPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
        <p className="text-muted-foreground">Loading jobs...</p>
      </div>
    </div>}>
      <JobsContent />
    </Suspense>
  )
}
