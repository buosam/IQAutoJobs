# IQAutoJobs - Modern Job Platform

## Overview

IQAutoJobs is a comprehensive job platform connecting talented professionals with top companies worldwide. The application features a multi-role system (Candidates, Employers, Administrators) with secure authentication, advanced job search capabilities, application tracking, and real-time communication via WebSocket. Built with a modern tech stack including Next.js 15 frontend and FastAPI backend, the platform emphasizes type safety, performance, and user experience.

**Current Status:** ✅ Fully functional in Replit environment
- Frontend: Running on port 5000 (Next.js 15 with custom server)
- Backend API: Running on port 8000 (FastAPI with PostgreSQL)
- All core features operational: Registration, Login, Job Browsing, Company Browsing

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework & Core Technologies:**
- Next.js 15 with App Router for server-side rendering and routing
- TypeScript 5 for type safety across the application
- React Server Components (RSC) enabled for optimal performance

**State Management & Data Fetching:**
- TanStack Query for server state management and data synchronization
- Zustand for client-side state management
- Custom hooks for reusable logic patterns

**UI & Styling:**
- Tailwind CSS 4 with utility-first approach and custom theme configuration
- shadcn/ui component library (New York style) for consistent, accessible components
- Lucide React for iconography
- CSS variables for theme customization with dark mode support

**Real-time Communication:**
- Socket.IO client for WebSocket connections
- Custom server integration in `server.ts` combining Next.js with Socket.IO on port 5000
- Echo-based message system for real-time updates

**API Integration:**
- Next.js API routes proxy requests to FastAPI backend (localhost:8000)
- Routes implemented: /api/auth/*, /api/jobs/*, /api/companies/*
- Environment variable BACKEND_URL configurable for deployment

**Development Setup:**
- Custom development server using nodemon and tsx for hot reloading
- TypeScript strict mode disabled (`ignoreBuildErrors: true`) for development flexibility
- ESLint configured but ignored during builds

### Backend Architecture

**Framework & Language:**
- FastAPI as the web framework for high performance async operations
- Python 3.11 with type hints throughout
- Structured logging with structlog for observability

**Database Layer:**
- SQLAlchemy 2.x as ORM with async support potential
- PostgreSQL as primary database
- Repository pattern for data access abstraction
- Base repository class with common CRUD operations inherited by specialized repositories

**Data Access Pattern:**
- Repository classes for each domain entity (User, Company, Job, Application, etc.)
- Service layer separating business logic from API routes
- Domain models using Pydantic for validation and serialization

**Authentication & Security:**
- JWT-based authentication with access and refresh tokens
- Argon2 password hashing via passlib
- Token refresh mechanism with database-stored refresh tokens
- Role-based access control (ADMIN, EMPLOYER, CANDIDATE)

**Error Handling:**
- Custom exception hierarchy extending FastAPI's HTTPException
- Centralized error handlers for validation, authentication, and business logic errors
- Structured error responses with error codes

**Middleware Stack:**
- CORS middleware for cross-origin requests
- Trusted host middleware for security
- Custom security headers middleware
- Rate limiting using in-memory token bucket algorithm

**API Structure:**
- Modular router organization (auth, jobs, applications, companies, admin, files)
- Consistent response formats
- API documentation via Swagger/ReDoc (development only)

### Data Models & Business Logic

**Core Entities:**
1. **User** - Multi-role system with profile data, skills, experience
2. **Company** - Employer profiles with branding and metadata
3. **Job** - Job postings with rich metadata (type, category, salary, requirements)
4. **Application** - Candidate applications with status tracking
5. **SavedJob** - Bookmarked opportunities for candidates
6. **RefreshToken** - Token management for authentication
7. **AuditLog** - Comprehensive activity logging

**Status Enumerations:**
- JobStatus: DRAFT, PUBLISHED, CLOSED
- ApplicationStatus: RECEIVED, SHORTLISTED, INTERVIEW, REJECTED, HIRED
- EmploymentType: FT (Full-time), PT (Part-time), CONTRACT, INTERN

**Search & Filtering:**
- Advanced job search with multiple filter criteria
- Company search by industry, location, and keywords
- Pagination support across all list endpoints

### External Dependencies

**File Storage:**
- Cloudflare R2 (S3-compatible) for resume and document storage
- boto3 client for S3 operations
- File upload service with size and type validation (10MB limit, PDF/DOC/DOCX)
- Public URL generation for stored files

**Database:**
- PostgreSQL connection via SQLAlchemy
- Connection pooling with StaticPool
- Database session management with dependency injection pattern

**Frontend Component Libraries:**
- Radix UI primitives for accessible components
- @dnd-kit for drag-and-drop functionality
- @mdxeditor for rich text editing
- react-day-picker for date selection
- Multiple Radix UI components (accordion, alert-dialog, avatar, checkbox, dialog, dropdown-menu, label, navigation-menu, popover, progress, radio-group, scroll-area, select, separator, slider, switch, tabs, toast, toggle, tooltip)

**Development Tools:**
- Prisma ORM (client installed but SQLAlchemy used in backend)
- nodemon for development server auto-restart
- tsx for TypeScript execution
- mypy, ruff, pytest for Python code quality

**SEO & Metadata:**
- Dynamic sitemap generation
- robots.txt configuration
- Structured data for job postings (JSON-LD schema)
- OpenGraph and Twitter card metadata

**Deployment Considerations:**
- Docker containerization support
- Railway cloud platform targeting
- Environment-based configuration (development/production)
- Separate logging for dev and production modes