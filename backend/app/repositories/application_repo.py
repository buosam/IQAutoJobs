"""
Application repository for IQAutoJobs.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
import sqlalchemy.orm
from sqlalchemy import and_

from app.db.models import Application, ApplicationStatus
from app.repositories.base import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    """Application repository with application-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(Application, db)
    
    def get_by_job_and_candidate(self, job_id: UUID, candidate_user_id: UUID) -> Optional[Application]:
        """Get application by job and candidate."""
        return self.db.query(Application).filter(
            and_(
                Application.job_id == job_id,
                Application.candidate_user_id == candidate_user_id
            )
        ).first()
    
    def get_applications_by_job(self, job_id: UUID, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get applications by job."""
        return self.db.query(Application).filter(
            Application.job_id == job_id
        ).offset(skip).limit(limit).all()
    
    def get_applications_by_candidate(self, candidate_user_id: UUID, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get applications by candidate."""
        return self.db.query(Application).filter(
            Application.candidate_user_id == candidate_user_id
        ).offset(skip).limit(limit).all()
    
    def get_applications_by_status(self, status: ApplicationStatus, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get applications by status."""
        return self.db.query(Application).filter(
            Application.status == status
        ).offset(skip).limit(limit).all()
    
    def get_application_with_job_and_candidate(self, application_id: UUID) -> Optional[Application]:
        """Get application with job and candidate relationships loaded."""
        return self.db.query(Application).options(
            sqlalchemy.orm.joinedload(Application.job),
            sqlalchemy.orm.joinedload(Application.candidate)
        ).filter(Application.id == application_id).first()
    
    def get_applications_by_company(self, company_id: UUID, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get applications for a company."""
        return self.db.query(Application).join(Application.job).filter(
            Job.company_id == company_id
        ).offset(skip).limit(limit).all()
    
    def get_applications_by_company_with_details(self, company_id: UUID, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get applications for a company with all details loaded."""
        return self.db.query(Application).options(
            sqlalchemy.orm.joinedload(Application.job),
            sqlalchemy.orm.joinedload(Application.candidate)
        ).join(Application.job).filter(
            Job.company_id == company_id
        ).offset(skip).limit(limit).all()
    
    def search_applications(
        self,
        company_id: Optional[UUID] = None,
        candidate_user_id: Optional[UUID] = None,
        job_id: Optional[UUID] = None,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Application]:
        """Search applications with filters."""
        query = self.db.query(Application)
        
        if company_id:
            query = query.join(Application.job).filter(Job.company_id == company_id)
        
        if candidate_user_id:
            query = query.filter(Application.candidate_user_id == candidate_user_id)
        
        if job_id:
            query = query.filter(Application.job_id == job_id)
        
        if status:
            query = query.filter(Application.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def count_applications(
        self,
        company_id: Optional[UUID] = None,
        candidate_user_id: Optional[UUID] = None,
        job_id: Optional[UUID] = None,
        status: Optional[ApplicationStatus] = None
    ) -> int:
        """Count applications with filters."""
        query = self.db.query(Application)
        
        if company_id:
            query = query.join(Application.job).filter(Job.company_id == company_id)
        
        if candidate_user_id:
            query = query.filter(Application.candidate_user_id == candidate_user_id)
        
        if job_id:
            query = query.filter(Application.job_id == job_id)
        
        if status:
            query = query.filter(Application.status == status)
        
        return query.count()
    
    def update_application_status(self, application_id: UUID, status: ApplicationStatus) -> Optional[Application]:
        """Update application status."""
        application = self.get(application_id)
        if application:
            application.status = status
            self.db.commit()
            self.db.refresh(application)
        return application
    
    def get_recent_applications(self, limit: int = 10) -> List[Application]:
        """Get recent applications."""
        return self.db.query(Application).order_by(
            Application.created_at.desc()
        ).limit(limit).all()
    
    def has_candidate_applied(self, job_id: UUID, candidate_user_id: UUID) -> bool:
        """Check if candidate has applied to a job."""
        return self.db.query(Application).filter(
            and_(
                Application.job_id == job_id,
                Application.candidate_user_id == candidate_user_id
            )
        ).first() is not None