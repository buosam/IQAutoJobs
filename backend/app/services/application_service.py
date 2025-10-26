"""
Application service for IQAutoJobs.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.models import (
    ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationStatus
)
from app.repositories.application_repo import ApplicationRepository
from app.repositories.job_repo import JobRepository
from app.repositories.user_repo import UserRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.core.errors import NotFoundError, ConflictError


class ApplicationService:
    """Application service."""
    
    def __init__(
        self,
        db: Session,
        app_repo: ApplicationRepository,
        job_repo: JobRepository,
        user_repo: UserRepository,
        audit_repo: AuditLogRepository
    ):
        self.db = db
        self.app_repo = app_repo
        self.job_repo = job_repo
        self.user_repo = user_repo
        self.audit_repo = audit_repo
    
    def get_application_by_id(self, application_id: UUID) -> Optional[ApplicationResponse]:
        """Get application by ID."""
        application = self.app_repo.get_application_with_job_and_candidate(application_id)
        if not application:
            raise NotFoundError("Application not found")
        
        return ApplicationResponse.from_orm(application)
    
    def get_applications_by_job(self, job_id: UUID, skip: int = 0, limit: int = 100) -> List[ApplicationResponse]:
        """Get applications by job."""
        applications = self.app_repo.get_applications_by_job(job_id, skip=skip, limit=limit)
        return [ApplicationResponse.from_orm(app) for app in applications]
    
    def get_applications_by_candidate(self, candidate_user_id: UUID, skip: int = 0, limit: int = 100) -> List[ApplicationResponse]:
        """Get applications by candidate."""
        applications = self.app_repo.get_applications_by_candidate(candidate_user_id, skip=skip, limit=limit)
        return [ApplicationResponse.from_orm(app) for app in applications]
    
    def get_applications_by_company(self, company_id: UUID, skip: int = 0, limit: int = 100) -> List[ApplicationResponse]:
        """Get applications by company."""
        applications = self.app_repo.get_applications_by_company_with_details(company_id, skip=skip, limit=limit)
        return [ApplicationResponse.from_orm(app) for app in applications]
    
    def create_application(self, application_data: ApplicationCreate, candidate_user_id: UUID, cv_key: str) -> ApplicationResponse:
        """Create a new application."""
        # Check if job exists and is published
        job = self.job_repo.get_job_with_company(application_data.job_id)
        if not job:
            raise NotFoundError("Job not found")
        
        if job.status.value != "PUBLISHED":
            raise ConflictError("Job is not accepting applications")
        
        # Check if user has already applied
        if self.app_repo.has_candidate_applied(application_data.job_id, candidate_user_id):
            raise ConflictError("You have already applied to this job")
        
        # Create application
        app_dict = application_data.dict()
        app_dict["candidate_user_id"] = candidate_user_id
        app_dict["cv_key"] = cv_key
        
        application = self.app_repo.create(app_dict)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="APPLICATION_CREATE",
            user_id=candidate_user_id,
            subject_type="Application",
            subject_id=str(application.id),
            payload={"job_id": str(application_data.job_id), "cv_key": cv_key}
        )
        
        return ApplicationResponse.from_orm(application)
    
    def update_application_status(self, application_id: UUID, status: ApplicationStatus, user_id: UUID) -> ApplicationResponse:
        """Update application status."""
        application = self.app_repo.get_application_with_job_and_candidate(application_id)
        if not application:
            raise NotFoundError("Application not found")
        
        # Check if user owns the company
        if application.job.company.owner_user_id != user_id:
            raise ConflictError("You don't have permission to update this application")
        
        # Update status
        application = self.app_repo.update_application_status(application_id, status)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="APPLICATION_STATUS_UPDATE",
            user_id=user_id,
            subject_type="Application",
            subject_id=str(application_id),
            payload={"status": status.value}
        )
        
        return ApplicationResponse.from_orm(application)
    
    def search_applications(
        self,
        company_id: Optional[UUID] = None,
        candidate_user_id: Optional[UUID] = None,
        job_id: Optional[UUID] = None,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ApplicationResponse]:
        """Search applications with filters."""
        applications = self.app_repo.search_applications(
            company_id=company_id,
            candidate_user_id=candidate_user_id,
            job_id=job_id,
            status=status,
            skip=skip,
            limit=limit
        )
        return [ApplicationResponse.from_orm(app) for app in applications]
    
    def count_applications(
        self,
        company_id: Optional[UUID] = None,
        candidate_user_id: Optional[UUID] = None,
        job_id: Optional[UUID] = None,
        status: Optional[ApplicationStatus] = None
    ) -> int:
        """Count applications with filters."""
        return self.app_repo.count_applications(
            company_id=company_id,
            candidate_user_id=candidate_user_id,
            job_id=job_id,
            status=status
        )
    
    def get_recent_applications(self, limit: int = 10) -> List[ApplicationResponse]:
        """Get recent applications."""
        applications = self.app_repo.get_recent_applications(limit)
        return [ApplicationResponse.from_orm(app) for app in applications]
    
    def get_applications_by_status(self, status: ApplicationStatus, skip: int = 0, limit: int = 100) -> List[ApplicationResponse]:
        """Get applications by status."""
        applications = self.app_repo.get_applications_by_status(status, skip, limit)
        return [ApplicationResponse.from_orm(app) for app in applications]
    
    def has_candidate_applied(self, job_id: UUID, candidate_user_id: UUID) -> bool:
        """Check if candidate has applied to a job."""
        return self.app_repo.has_candidate_applied(job_id, candidate_user_id)