"use client"

import Link from "next/link"

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto max-w-6xl px-4 py-4 flex justify-between items-center">
        <Link href="/">
          <h1 className="text-2xl font-bold text-blue-600">IQAutoJobs</h1>
        </Link>
        <nav>
          <Link href="/auth/login">
            <button className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700">
              Login
            </button>
          </Link>
        </nav>
      </div>
    </header>
  )
}
