'use client';

import Link from 'next/link';
import FeaturedJobs from '@/components/FeaturedJobs';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-md">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">Job Board</h1>
          <div className="space-x-4">
            <Link href="/login" className="text-gray-700 hover:text-blue-600">
              Login
            </Link>
            <Link href="/signup" className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
              Sign Up
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold text-gray-800 mb-4">Find Your Dream Job</h2>
          <p className="text-xl text-gray-600">Connect with top employers and discover exciting opportunities</p>
        </div>

        <FeaturedJobs />
      </div>
    </div>
  );
}
