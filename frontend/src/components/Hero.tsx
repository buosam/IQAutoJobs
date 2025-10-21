import React from 'react';

const Hero = () => {
  return (
    <section className="bg-white">
      <div className="container mx-auto px-6 py-16 text-center">
        <h1 className="text-4xl font-bold text-gray-800 md:text-5xl">
          Find Your Dream Job Today
        </h1>
        <p className="mt-4 text-lg text-gray-600">
          Search thousands of job openings from top companies.
        </p>
        <div className="mt-8">
          <form className="flex flex-col items-center md:flex-row md:justify-center">
            <input
              type="text"
              className="w-full max-w-md px-4 py-3 text-gray-700 bg-white border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-300"
              placeholder="Job title, keywords, or company"
            />
            <button
              type="submit"
              className="w-full md:w-auto mt-4 md:mt-0 md:ml-4 px-6 py-3 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-300"
            >
              Search
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Hero;
