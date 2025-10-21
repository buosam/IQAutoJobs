import React from 'react';

const jobs = [
  {
    title: 'Software Engineer',
    company: 'Google',
    location: 'Mountain View, CA',
    description: 'We are looking for a talented Software Engineer to join our team.',
  },
  {
    title: 'Product Manager',
    company: 'Facebook',
    location: 'Menlo Park, CA',
    description: 'We are looking for a talented Product Manager to join our team.',
  },
  {
    title: 'Data Scientist',
    company: 'Amazon',
    location: 'Seattle, WA',
    description: 'We are looking for a talented Data Scientist to join our team.',
  },
];

const FeaturedJobs = () => {
  return (
    <section className="bg-gray-100">
      <div className="container mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center text-gray-800">
          Featured Jobs
        </h2>
        <div className="mt-8 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {jobs.map((job, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md p-6">
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
