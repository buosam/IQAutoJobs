"""
Job service for IQAutoJobs.
"""
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.models import (
    JobCreate, JobUpdate, JobResponse, JobSearchFilters, JobSearchResponse,
    JobStatus, EmploymentType
)
from app.repositories.job_repo import JobRepository
from app.repositories.company_repo import CompanyRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.core.errors import NotFoundError, ConflictError


class JobService:
    """Job service."""
    
    def __init__(
        self,
        db: Session,
        job_repo: JobRepository,
        company_repo: CompanyRepository,
        audit_repo: AuditLogRepository
    ):
        self.db = db
        self.job_repo = job_repo
        self.company_repo = company_repo
        self.audit_repo = audit_repo
    
    def get_job_by_id(self, job_id: UUID) -> Optional[JobResponse]:
        """Get job by ID."""
        job = self.job_repo.get_job_with_company(job_id)
        if not job:
            raise NotFoundError("Job not found")
        
        return JobResponse.from_orm(job)
    
    def get_job_by_slug(self, slug: str) -> Optional[JobResponse]:
        """Get job by slug."""
        job = self.job_repo.get_by_slug(slug)
        if not job:
            return None
        
        return JobResponse.from_orm(job)
    
    def get_jobs(self, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Get jobs with pagination."""
        jobs = self.job_repo.get_multi(skip=skip, limit=limit)
        return [JobResponse.from_orm(job) for job in jobs]
    
    def get_published_jobs(self, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Get published jobs."""
        jobs = self.job_repo.get_published_jobs(skip=skip, limit=limit)
        return [JobResponse.from_orm(job) for job in jobs]
    
    def get_jobs_by_company(self, company_id: UUID, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Get jobs by company."""
        jobs = self.job_repo.get_jobs_by_company(company_id, skip=skip, limit=limit)
        return [JobResponse.from_orm(job) for job in jobs]
    
    def create_job(self, job_data: JobCreate, company_id: UUID, user_id: UUID) -> JobResponse:
        """Create a new job."""
        # Check if company exists and user owns it
        company = self.company_repo.get(company_id)
        if not company:
            raise NotFoundError("Company not found")
        
        if company.owner_user_id != user_id:
            raise ConflictError("You don't have permission to create jobs for this company")
        
        # Generate slug from job title
        slug = self._generate_slug(job_data.title)
        
        # Check if slug is available for this company
        if not self.job_repo.is_slug_available(company_id, slug):
            raise ConflictError("Job title is already taken for this company")
        
        job_dict = job_data.dict()
        job_dict["company_id"] = company_id
        job_dict["slug"] = slug
        
        job = self.job_repo.create(job_dict)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="JOB_CREATE",
            user_id=user_id,
            subject_type="Job",
            subject_id=str(job.id),
            payload={"title": job.title, "company_id": str(company_id)}
        )
        
        return JobResponse.from_orm(job)
    
    def update_job(self, job_id: UUID, job_data: JobUpdate, user_id: UUID) -> JobResponse:
        """Update a job."""
        job = self.job_repo.get(job_id)
        if not job:
            raise NotFoundError("Job not found")
        
        # Check if user owns the company
        if job.company.owner_user_id != user_id:
            raise ConflictError("You don't have permission to update this job")
        
        # Convert to dict and remove None values
        update_data = job_data.dict(exclude_unset=True)
        
        # If title is being updated, generate new slug
        if "title" in update_data:
            new_slug = self._generate_slug(update_data["title"])
            if new_slug != job.slug:
                if not self.job_repo.is_slug_available(job.company_id, new_slug, job_id):
                    raise ConflictError("Job title is already taken for this company")
                update_data["slug"] = new_slug
        
        # If status is being changed to PUBLISHED, set published_at
        if "status" in update_data and update_data["status"] == JobStatus.PUBLISHED:
            if job.status != JobStatus.PUBLISHED:
                update_data["published_at"] = datetime.utcnow()
        
        job = self.job_repo.update(job, update_data)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="JOB_UPDATE",
            user_id=user_id,
            subject_type="Job",
            subject_id=str(job_id),
            payload=update_data
        )
        
        return JobResponse.from_orm(job)
    
    def publish_job(self, job_id: UUID, user_id: UUID) -> JobResponse:
        """Publish a job."""
        job = self.job_repo.get(job_id)
        if not job:
            raise NotFoundError("Job not found")
        
        # Check if user owns the company
        if job.company.owner_user_id != user_id:
            raise ConflictError("You don't have permission to publish this job")
        
        # Update job status
        job.status = JobStatus.PUBLISHED
        job.published_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(job)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="JOB_PUBLISH",
            user_id=user_id,
            subject_type="Job",
            subject_id=str(job_id)
        )
        
        return JobResponse.from_orm(job)
    
    def close_job(self, job_id: UUID, user_id: UUID) -> JobResponse:
        """Close a job."""
        job = self.job_repo.get(job_id)
        if not job:
            raise NotFoundError("Job not found")
        
        # Check if user owns the company
        if job.company.owner_user_id != user_id:
            raise ConflictError("You don't have permission to close this job")
        
        # Update job status
        job.status = JobStatus.CLOSED
        self.db.commit()
        self.db.refresh(job)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="JOB_CLOSE",
            user_id=user_id,
            subject_type="Job",
            subject_id=str(job_id)
        )
        
        return JobResponse.from_orm(job)
    
    def search_jobs(self, filters: JobSearchFilters, page: int = 1, size: int = 20) -> JobSearchResponse:
        """Search jobs with filters."""
        skip = (page - 1) * size
        
        jobs = self.job_repo.search_jobs(
            search_term=filters.search,
            location=filters.location,
            employment_type=filters.type,
            category=filters.category,
            experience_level=filters.experience_level,
            salary_min=filters.salary_min,
            salary_max=filters.salary_max,
            status=filters.status,
            skip=skip,
            limit=size
        )
        
        total = self.job_repo.count_search_jobs(
            search_term=filters.search,
            location=filters.location,
            employment_type=filters.type,
            category=filters.category,
            experience_level=filters.experience_level,
            salary_min=filters.salary_min,
            salary_max=filters.salary_max,
            status=filters.status
        )
        
        pages = (total + size - 1) // size
        
        return JobSearchResponse(
            jobs=[JobResponse.from_orm(job) for job in jobs],
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    
    def get_recent_jobs(self, limit: int = 10) -> List[JobResponse]:
        """Get recent published jobs."""
        jobs = self.job_repo.get_recent_jobs(limit)
        return [JobResponse.from_orm(job) for job in jobs]
    
    def get_jobs_by_type(self, employment_type: EmploymentType, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Get jobs by employment type."""
        jobs = self.job_repo.get_jobs_by_type(employment_type, skip, limit)
        return [JobResponse.from_orm(job) for job in jobs]
    
    def get_jobs_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Get jobs by category."""
        jobs = self.job_repo.get_jobs_by_category(category, skip, limit)
        return [JobResponse.from_orm(job) for job in jobs]
    
    def get_jobs_by_location(self, location: str, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Get jobs by location."""
        jobs = self.job_repo.get_jobs_by_location(location, skip, limit)
        return [JobResponse.from_orm(job) for job in jobs]
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from job title."""
        # Convert to lowercase
        slug = title.lower()
        
        # Replace special characters with hyphens
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        
        # Remove consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        return slug