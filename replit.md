# Job Board Application

## Overview
This is a full-stack job board application built with Flask (backend) and Next.js (frontend). It allows job seekers to create profiles, browse jobs, and apply to positions, while employers can post jobs and manage applications.

## Architecture
- **Backend**: Flask REST API with SQLAlchemy ORM, running on Gunicorn (localhost:8000)
- **Frontend**: Next.js 14 with React, running on port 5000
- **Database**: PostgreSQL with Alembic migrations
- **Authentication**: JWT-based authentication with Flask-JWT-Extended
- **File Storage**: S3-compatible storage (R2) for resume uploads

## Project Structure
```
├── backend/
│   ├── migrations/        # Alembic database migrations
│   ├── app.py            # Flask application factory
│   ├── models.py         # SQLAlchemy database models
│   ├── routes.py         # API endpoints
│   ├── extensions.py     # Flask extensions (db, jwt, migrate)
│   └── s3.py            # S3 file upload handling
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js app router pages
│   │   └── components/   # React components
│   ├── package.json
│   └── next.config.js
├── wsgi.py              # WSGI entry point
└── replit.md            # This file
```

## Environment Variables
Required environment variables (stored in Replit Secrets):
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `R2_ENDPOINT`: R2/S3 endpoint URL (optional, for file uploads)
- `R2_ACCESS_KEY_ID`: R2/S3 access key (optional)
- `R2_SECRET_ACCESS_KEY`: R2/S3 secret key (optional)

## Development Setup
The Dev Server workflow runs both backend and frontend concurrently:
- Backend: Gunicorn serves the Flask API on localhost:8000
- Frontend: Next.js dev server on 0.0.0.0:5000 (user-facing)

## Database Models
- **User**: Authentication and user type (job_seeker or employer)
- **UserProfile**: Job seeker profile information
- **CompanyProfile**: Employer company information
- **Job**: Job postings
- **Application**: Job applications linking users to jobs

## API Endpoints
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET/POST/PUT /profile` - User/company profile management
- `GET /jobs` - List all jobs
- `POST /jobs` - Create new job (employers only)
- `GET /jobs/<id>` - Get job details
- `POST /jobs/<id>/apply` - Apply to job
- `POST /upload/resume` - Upload resume file

## Deployment
Configured for autoscale deployment:
- Build: `cd frontend && npm run build`
- Run: Backend and frontend both serve on port 5000

## Recent Changes (Oct 23, 2025)
- Set up GitHub import in Replit environment
- Installed Python 3.11 and Node.js 20
- Created Next.js configuration files
- Configured PostgreSQL database with Alembic migrations
- Set up development workflow running both backend and frontend
- Configured deployment settings for production

## Notes
- Using Tailwind CSS via CDN for styling (should migrate to PostCSS plugin for production)
- Database migrations managed with Alembic
- Frontend uses .env.local with NEXT_PUBLIC_API_URL pointing to backend
