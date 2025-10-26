"use client"

import { useState } from "react"

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("")
  const [locationQuery, setLocationQuery] = useState("")

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    alert(`Searching for: ${searchQuery} in ${locationQuery}`)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-50 to-blue-100 py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-6">
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-gray-900">
              Find Your Dream Job at
              <span className="text-blue-600"> IQAutoJobs</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Connect with top companies and discover opportunities that match your skills and aspirations.
            </p>
            
            {/* Search Bar */}
            <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
              <div className="flex flex-col sm:flex-row gap-2 p-2 bg-white rounded-lg shadow-lg">
                <div className="flex-1 relative">
                  <input
                    type="text"
                    placeholder="Search jobs, companies, or keywords..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="flex-1 relative">
                  <input
                    type="text"
                    placeholder="Location..."
                    value={locationQuery}
                    onChange={(e) => setLocationQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <button 
                  type="submit" 
                  className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  Search Jobs
                </button>
              </div>
            </form>
            
            {/* Quick Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl mx-auto mt-8">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">10K+</div>
                <div className="text-sm text-gray-600">Active Jobs</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">500+</div>
                <div className="text-sm text-gray-600">Companies</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">50K+</div>
                <div className="text-sm text-gray-600">Candidates</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">98%</div>
                <div className="text-sm text-gray-600">Success Rate</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 bg-blue-600 text-white">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Find Your Dream Job?</h2>
          <p className="text-lg mb-8 opacity-90">
            Join thousands of professionals who have found their perfect match through IQAutoJobs
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-white">
              Browse Jobs
            </button>
            <button className="px-6 py-3 border border-white text-white font-semibold rounded-md hover:bg-white hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-white">
              Create Account
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}