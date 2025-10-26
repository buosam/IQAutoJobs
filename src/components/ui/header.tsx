"use client"

import Link from "next/link"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { User } from "@/lib/types"
import { API_ROUTES, PAGE_ROUTES } from "@/lib/constants"

export default function Header() {
  const [user, setUser] = useState<User | null>(null)
  const router = useRouter()

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error('Failed to parse user data from localStorage:', error);
        localStorage.removeItem('user'); // Clear corrupted data
      }
    }
  }, [])

  const handleLogout = async () => {
    try {
      const response = await fetch(API_ROUTES.LOGOUT, { method: 'POST' });
      if (response.ok) {
        localStorage.removeItem('user');
        setUser(null);
        router.push('/');
      } else {
        console.error('Server-side logout failed.');
      }
    } catch (error) {
      console.error('Logout request failed:', error);
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
              <Link href={PAGE_ROUTES.DASHBOARD} className="text-gray-600 hover:text-blue-600">Dashboard</Link>
              <button onClick={handleLogout} className="px-4 py-2 bg-red-600 text-white font-semibold rounded-md hover:bg-red-700">
                Logout
              </button>
            </>
          ) : (
            <Link href={PAGE_ROUTES.LOGIN} className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700">
              Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  )
}
