'use client';

import React, { useState, useEffect } from 'react';

interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  applicants: string[];
}

const FeaturedJobs = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/jobs`);
        if (!response.ok) {
          throw new Error('Failed to fetch jobs');
        }
        const data = await response.json();
        setJobs(data);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('An unexpected error occurred');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

  return (
    <section className="bg-gray-100">
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-gray-800">
          Featured Jobs
        </h2>
        <div className="mt-8 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {loading && <p>Loading...</p>}
          {error && <p className="text-red-500">{error}</p>}
          {jobs.map((job) => (
            <div key={job.id} className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-gray-800">{job.title}</h3>
              <p className="mt-2 text-gray-600">{job.company}</p>
              <p className="mt-2 text-gray-600">{job.location}</p>
              <p className="mt-4 text-gray-600">{job.description}</p>
              <button className="mt-4 px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600">
                Apply Now
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturedJobs;
