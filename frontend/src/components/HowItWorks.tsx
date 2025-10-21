import React from 'react';

const HowItWorks = () => {
  return (
    <section className="bg-white">
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-gray-800">
          How It Works
        </h2>
        <div className="mt-8 grid gap-8 md:grid-cols-2">
          <div className="bg-gray-100 rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800">For Job Seekers</h3>
            <p className="mt-4 text-gray-600">
              Create a profile, upload your resume, and start applying for jobs.
            </p>
          </div>
          <div className="bg-gray-100 rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800">For Employers</h3>
            <p className="mt-4 text-gray-600">
              Post a job, manage applicants, and hire the best talent.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
