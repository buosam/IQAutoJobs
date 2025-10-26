"""
Saved job repository for IQAutoJobs.
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.models import SavedJob
from app.repositories.base import BaseRepository


class SavedJobRepository(BaseRepository[SavedJob]):
    """Saved job repository with saved job-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(SavedJob, db)
    
    def get_by_user_and_job(self, user_id: UUID, job_id: UUID) -> Optional[SavedJob]:
        """Get saved job by user and job."""
        return self.db.query(SavedJob).filter(
            and_(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id
            )
        ).first()
    
    def get_saved_jobs_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[SavedJob]:
        """Get saved jobs by user."""
        return self.db.query(SavedJob).filter(
            SavedJob.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_saved_jobs_by_job(self, job_id: UUID, skip: int = 0, limit: int = 100) -> List[SavedJob]:
        """Get saved jobs by job."""
        return self.db.query(SavedJob).filter(
            SavedJob.job_id == job_id
        ).offset(skip).limit(limit).all()
    
    def is_job_saved_by_user(self, user_id: UUID, job_id: UUID) -> bool:
        """Check if job is saved by user."""
        return self.db.query(SavedJob).filter(
            and_(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id
            )
        ).first() is not None
    
    def save_job(self, user_id: UUID, job_id: UUID) -> SavedJob:
        """Save a job for a user."""
        saved_job_data = {
            "user_id": user_id,
            "job_id": job_id
        }
        return self.create(saved_job_data)
    
    def unsave_job(self, user_id: UUID, job_id: UUID) -> bool:
        """Unsave a job for a user."""
        saved_job = self.get_by_user_and_job(user_id, job_id)
        if saved_job:
            self.db.delete(saved_job)
            self.db.commit()
            return True
        return False
    
    def get_recent_saved_jobs(self, user_id: UUID, limit: int = 10) -> List[SavedJob]:
        """Get recent saved jobs for a user."""
        return self.db.query(SavedJob).filter(
            SavedJob.user_id == user_id
        ).order_by(SavedJob.created_at.desc()).limit(limit).all()
    
    def count_saved_jobs_by_user(self, user_id: UUID) -> int:
        """Count saved jobs by user."""
        return self.db.query(SavedJob).filter(
            SavedJob.user_id == user_id
        ).count()
    
    def count_saved_jobs_by_job(self, job_id: UUID) -> int:
        """Count saved jobs by job."""
        return self.db.query(SavedJob).filter(
            SavedJob.job_id == job_id
        ).count()