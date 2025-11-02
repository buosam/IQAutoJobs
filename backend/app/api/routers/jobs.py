"""
Jobs router for IQAutoJobs.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from structlog import get_logger

from app.db.base import get_db
from app.domain.models import (
    JobCreate, JobUpdate, JobResponse, JobSearchFilters, JobSearchResponse,
    JobStatus, EmploymentType
)
from app.services.job_service import JobService
from app.services.company_service import CompanyService
from app.services.auth_service import AuthService
from app.repositories.job_repo import JobRepository
from app.repositories.company_repo import CompanyRepository
from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import RefreshTokenRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.api.routers.auth import get_current_user
from app.core.errors import NotFoundError, ConflictError

logger = get_logger()
router = APIRouter()


async def get_job_service(db: Session = Depends(get_db)) -> JobService:
    """Get job service instance."""
    job_repo = JobRepository(db)
    company_repo = CompanyRepository(db)
    audit_repo = AuditLogRepository(db)
    return JobService(db, job_repo, company_repo, audit_repo)


@router.get("/", response_model=JobSearchResponse)
async def get_jobs(
    search: Optional[str] = Query(None, description="Search term"),
    location: Optional[str] = Query(None, description="Location filter"),
    type: Optional[EmploymentType] = Query(None, description="Employment type"),
    category: Optional[str] = Query(None, description="Category filter"),
    experience_level: Optional[str] = Query(None, description="Experience level"),
    salary_min: Optional[int] = Query(None, description="Minimum salary"),
    salary_max: Optional[int] = Query(None, description="Maximum salary"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    job_service: JobService = Depends(get_job_service)
):
    """Get jobs with search and filters."""
    filters = JobSearchFilters(
        search=search,
        location=location,
        type=type,
        category=category,
        experience_level=experience_level,
        salary_min=salary_min,
        salary_max=salary_max
    )
    
    return await job_service.search_jobs(filters, page, size)


@router.get("/recent", response_model=list[JobResponse])
async def get_recent_jobs(
    limit: int = Query(10, ge=1, le=50, description="Number of recent jobs"),
    job_service: JobService = Depends(get_job_service)
):
    """Get recent published jobs."""
    return await job_service.get_recent_jobs(limit)


@router.get("/by-type/{employment_type}", response_model=list[JobResponse])
async def get_jobs_by_type(
    employment_type: EmploymentType,
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    job_service: JobService = Depends(get_job_service)
):
    """Get jobs by employment type."""
    return await job_service.get_jobs_by_type(employment_type, skip, limit)


@router.get("/by-category/{category}", response_model=list[JobResponse])
async def get_jobs_by_category(
    category: str,
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    job_service: JobService = Depends(get_job_service)
):
    """Get jobs by category."""
    return await job_service.get_jobs_by_category(category, skip, limit)


@router.get("/by-location/{location}", response_model=list[JobResponse])
async def get_jobs_by_location(
    location: str,
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    job_service: JobService = Depends(get_job_service)
):
    """Get jobs by location."""
    return await job_service.get_jobs_by_location(location, skip, limit)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, job_service: JobService = Depends(get_job_service)):
    """Get job by ID."""
    try:
        return await job_service.get_job_by_id(job_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/slug/{slug}", response_model=JobResponse)
async def get_job_by_slug(slug: str, job_service: JobService = Depends(get_job_service)):
    """Get job by slug."""
    job = await job_service.get_job_by_slug(slug)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.post("/", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    current_user = Depends(get_current_user),
    job_service: JobService = Depends(get_job_service)
):
    """Create a new job."""
    try:
        return await job_service.create_job(job_data, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Job creation failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Job creation failed")


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    current_user = Depends(get_current_user),
    job_service: JobService = Depends(get_job_service)
):
    """Update a job."""
    try:
        return await job_service.update_job(job_id, job_data, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Job update failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Job update failed")


@router.patch("/{job_id}/publish", response_model=JobResponse)
async def publish_job(
    job_id: str,
    current_user = Depends(get_current_user),
    job_service: JobService = Depends(get_job_service)
):
    """Publish a job."""
    try:
        return await job_service.publish_job(job_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Job publish failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Job publish failed")


@router.patch("/{job_id}/close", response_model=JobResponse)
async def close_job(
    job_id: str,
    current_user = Depends(get_current_user),
    job_service: JobService = Depends(get_job_service)
):
    """Close a job."""
    try:
        return await job_service.close_job(job_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Job close failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Job close failed")


@router.delete("/{job_id}")
async def delete_job(
    job_id: str,
    current_user = Depends(get_current_user),
    job_service: JobService = Depends(get_job_service)
):
    """Delete a job."""
    try:
        # Get job to check ownership
        job = await job_service.job_repo.get_job_with_company(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        
        # Check if user owns the company
        if job.company.owner_user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this job")
        
        # Delete job
        await job_service.job_repo.delete(job_id)
        
        return {"message": "Job deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Job deletion failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Job deletion failed")
