import React from 'react';
import Link from 'next/link';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-6 py-3 md:flex md:justify-between md:items-center">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-xl font-bold text-gray-800 md:text-2xl hover:text-blue-500">
            IQAutoJobs
          </Link>
          <div className="flex md:hidden">
            <button
              type="button"
              className="text-gray-500 hover:text-gray-600 focus:outline-none focus:text-gray-600"
              aria-label="toggle menu"
            >
              <svg viewBox="0 0 24 24" className="h-6 w-6 fill-current">
                <path
                  fillRule="evenodd"
                  d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"
                />
              </svg>
            </button>
          </div>
        </div>
        <div className="hidden md:flex items-center">
          <Link href="/jobs" className="py-2 px-4 text-gray-800 hover:text-blue-500">
            Find a Job
          </Link>
          <Link href="/employers" className="py-2 px-4 text-gray-800 hover:text-blue-500">
            For Employers
          </Link>
          <Link href="/login" className="py-2 px-4 text-gray-800 hover:text-blue-500">
            Login
          </Link>
          <Link href="/signup" className="py-2 px-4 text-white bg-blue-500 rounded-md hover:bg-blue-600">
            Sign Up
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
