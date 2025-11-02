"""
Saved job repository for IQAutoJobs.
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, select, func

from app.db.models import SavedJob
from app.repositories.base import BaseRepository


class SavedJobRepository(BaseRepository[SavedJob]):
    """Saved job repository with saved job-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(SavedJob, db)
    
    async def get_by_user_and_job(self, user_id: UUID, job_id: UUID) -> Optional[SavedJob]:
        """Get saved job by user and job."""
        result = await self.db.execute(
            select(SavedJob).filter(
                and_(
                    SavedJob.user_id == user_id,
                    SavedJob.job_id == job_id
                )
            )
        )
        return result.scalars().first()
    
    async def get_saved_jobs_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[SavedJob]:
        """Get saved jobs by user."""
        result = await self.db.execute(
            select(SavedJob).filter(SavedJob.user_id == user_id).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_saved_jobs_by_job(self, job_id: UUID, skip: int = 0, limit: int = 100) -> List[SavedJob]:
        """Get saved jobs by job."""
        result = await self.db.execute(
            select(SavedJob).filter(SavedJob.job_id == job_id).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def is_job_saved_by_user(self, user_id: UUID, job_id: UUID) -> bool:
        """Check if job is saved by user."""
        result = await self.db.execute(
            select(SavedJob).filter(
                and_(
                    SavedJob.user_id == user_id,
                    SavedJob.job_id == job_id
                )
            )
        )
        return result.scalars().first() is not None
    
    async def save_job(self, user_id: UUID, job_id: UUID) -> SavedJob:
        """Save a job for a user."""
        saved_job_data = {
            "user_id": user_id,
            "job_id": job_id
        }
        return await self.create(saved_job_data)
    
    async def unsave_job(self, user_id: UUID, job_id: UUID) -> bool:
        """Unsave a job for a user."""
        saved_job = await self.get_by_user_and_job(user_id, job_id)
        if saved_job:
            await self.db.delete(saved_job)
            await self.db.commit()
            return True
        return False
    
    async def get_recent_saved_jobs(self, user_id: UUID, limit: int = 10) -> List[SavedJob]:
        """Get recent saved jobs for a user."""
        result = await self.db.execute(
            select(SavedJob).filter(SavedJob.user_id == user_id).order_by(SavedJob.created_at.desc()).limit(limit)
        )
        return result.scalars().all()
    
    async def count_saved_jobs_by_user(self, user_id: UUID) -> int:
        """Count saved jobs by user."""
        result = await self.db.execute(select(func.count(SavedJob.id)).filter(SavedJob.user_id == user_id))
        return result.scalar_one()
    
    async def count_saved_jobs_by_job(self, job_id: UUID) -> int:
        """Count saved jobs by job."""
        result = await self.db.execute(select(func.count(SavedJob.id)).filter(SavedJob.job_id == job_id))
        return result.scalar_one()
