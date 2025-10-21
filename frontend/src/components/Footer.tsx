import React from 'react';
import Link from 'next/link';

const Footer = () => {
  return (
    <footer className="bg-white">
      <div className="container mx-auto px-6 py-8">
        <div className="flex flex-col items-center text-center">
          <Link href="/" className="text-xl font-bold text-gray-800 hover:text-blue-500">
            IQAutoJobs
          </Link>
          <div className="flex mt-4">
            <Link href="/about" className="px-4 text-gray-800 hover:text-blue-500">
              About Us
            </Link>
            <Link href="/contact" className="px-4 text-gray-800 hover:text-blue-500">
              Contact
            </Link>
            <Link href="/terms" className="px-4 text-gray-800 hover:text-blue-500">
              Terms of Service
            </Link>
          </div>
          <div className="flex mt-4">
            <a
              href="#"
              className="px-4 text-gray-800 hover:text-blue-500"
              aria-label="Facebook"
            >
              <i className="fab fa-facebook-f"></i>
            </a>
            <a
              href="#"
              className="px-4 text-gray-800 hover:text-blue-500"
              aria-label="Twitter"
            >
              <i className="fab fa-twitter"></i>
            </a>
            <a
              href="#"
              className="px-4 text-gray-800 hover:text-blue-500"
              aria-label="Instagram"
            >
              <i className="fab fa-instagram"></i>
            </a>
          </div>
          <p className="mt-4 text-gray-600">
            © {new Date().getFullYear()} IQAutoJobs. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
