#!/usr/bin/env bash
set -m

echo "=== Starting IQAutoJobs Full Stack ==="

# Start backend
echo "Starting backend server on localhost:8000..."
cd backend && python3.11 -m gunicorn wsgi:app --bind localhost:8000 --reload --log-level info &
cd ..

sleep 3

# Start frontend (using npx to find nodemon)
echo "Starting frontend server on 0.0.0.0:5000..."
PORT=5000 npx nodemon --exec "npx tsx server.ts" --watch server.ts --watch src --ext ts,tsx,js,jsx

