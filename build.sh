#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

# Install frontend dependencies and build
echo "Installing frontend dependencies and building..."
cd frontend
npm install
npm run build
cd ..

echo "Build complete."
