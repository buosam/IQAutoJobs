"""
FastAPI application for IQAutoJobs job board.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from structlog import get_logger
from contextlib import asynccontextmanager
from concurrent.futures import ProcessPoolExecutor

from app.core.config import settings
from app.core.security import get_executor, shutdown_executor
from app.core.errors import (
    BaseHTTPException,
    base_exception_handler,
    validation_exception_handler,
    http_exception_handler,
)
from app.api.routers import auth, jobs, applications, companies, admin, files, public, users, oauth

# Configure structured logging
logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the application's lifespan."""
    logger.info("Application startup")
    get_executor()
    try:
        yield
    finally:
        logger.info("Application shutdown")
        shutdown_executor()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    description="IQAutoJobs - A modern job board platform",
    version="1.0.0",
    docs_url="/api/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response

# Add request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or "unknown"
    logger.bind(request_id=request_id).info("Request started", method=request.method, url=str(request.url))
    response = await call_next(request)
    logger.bind(request_id=request_id).info("Request completed", status_code=response.status_code)
    return response

# Add exception handlers
app.add_exception_handler(BaseHTTPException, base_exception_handler)
app.add_exception_handler(Exception, http_exception_handler)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(oauth.router, prefix="/api/oauth", tags=["oauth"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(public.router, prefix="/api/public", tags=["public"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

# Health check endpoints
@app.get("/healthz")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "IQAutoJobs API"}

@app.get("/readiness")
async def readiness_check():
    """Readiness check endpoint."""
    # Add database check here
    return {"status": "ready", "service": "IQAutoJobs API"}

@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint."""
    return {
        "service": "IQAutoJobs API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)