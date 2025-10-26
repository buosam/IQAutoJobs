"use client"

import Link from "next/link"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

export default function Header() {
  const [user, setUser] = useState<{ first_name: string; role: string } | null>(null)
  const router = useRouter()

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('user');
      setUser(null);
      router.push('/');
    }
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto max-w-6xl px-4 py-4 flex justify-between items-center">
        <Link href="/">
          <h1 className="text-2xl font-bold text-blue-600">IQAutoJobs</h1>
        </Link>
        <nav className="flex items-center space-x-4">
          {user ? (
            <>
              <span className="text-gray-700">Welcome, {user.first_name}</span>
              <Link href="/dashboard" className="text-gray-600 hover:text-blue-600">Dashboard</Link>
              <button onClick={handleLogout} className="px-4 py-2 bg-red-600 text-white font-semibold rounded-md hover:bg-red-700">
                Logout
              </button>
            </>
          ) : (
            <Link href="/auth/login" className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700">
              Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  )
}
