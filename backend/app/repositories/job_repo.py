"""
Job repository for IQAutoJobs.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
import sqlalchemy.orm
from sqlalchemy import and_, or_, func, select

from app.db.models import Job, JobStatus, EmploymentType, Company
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    """Job repository with job-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(Job, db)
    
    async def get_by_slug(self, slug: str) -> Optional[Job]:
        """Get job by slug."""
        result = await self.db.execute(select(Job).filter(Job.slug == slug))
        return result.scalars().first()
    
    async def get_by_company_and_slug(self, company_id: UUID, slug: str) -> Optional[Job]:
        """Get job by company and slug."""
        result = await self.db.execute(
            select(Job).filter(and_(Job.company_id == company_id, Job.slug == slug))
        )
        return result.scalars().first()
    
    async def get_published_jobs(self, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get published jobs."""
        result = await self.db.execute(
            select(Job).filter(Job.status == JobStatus.PUBLISHED).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_jobs_by_company(self, company_id: UUID, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get jobs by company."""
        result = await self.db.execute(
            select(Job).filter(Job.company_id == company_id).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_jobs_by_status(self, status: JobStatus, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get jobs by status."""
        result = await self.db.execute(
            select(Job).filter(Job.status == status).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_jobs_by_type(self, employment_type: EmploymentType, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get jobs by employment type."""
        result = await self.db.execute(
            select(Job).filter(Job.type == employment_type).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_jobs_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get jobs by category."""
        result = await self.db.execute(
            select(Job).filter(Job.category.ilike(f"%{category}%")).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_jobs_by_location(self, location: str, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get jobs by location."""
        result = await self.db.execute(
            select(Job).filter(Job.location.ilike(f"%{location}%")).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_job_with_company(self, job_id: UUID) -> Optional[Job]:
        """Get job with company relationship loaded."""
        result = await self.db.execute(
            select(Job).options(sqlalchemy.orm.joinedload(Job.company)).filter(Job.id == job_id)
        )
        return result.scalars().first()
    
    async def get_job_with_applications(self, job_id: UUID) -> Optional[Job]:
        """Get job with applications relationship loaded."""
        result = await self.db.execute(
            select(Job).options(sqlalchemy.orm.joinedload(Job.applications)).filter(Job.id == job_id)
        )
        return result.scalars().first()
    
    async def search_jobs(
        self,
        search_term: Optional[str] = None,
        location: Optional[str] = None,
        employment_type: Optional[EmploymentType] = None,
        category: Optional[str] = None,
        experience_level: Optional[str] = None,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        company_id: Optional[UUID] = None,
        status: JobStatus = JobStatus.PUBLISHED,
        skip: int = 0,
        limit: int = 100
    ) -> List[Job]:
        """Search jobs with multiple filters."""
        query = select(Job).filter(Job.status == status).options(sqlalchemy.orm.selectinload(Job.company).selectinload(Company.owner))
        
        if search_term:
            search_conditions = [
                Job.title.ilike(f"%{search_term}%"),
                Job.description.ilike(f"%{search_term}%"),
                Job.category.ilike(f"%{search_term}%")
            ]
            query = query.filter(or_(*search_conditions))
        
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))
        
        if employment_type:
            query = query.filter(Job.type == employment_type)
        
        if category:
            query = query.filter(Job.category.ilike(f"%{category}%"))
        
        if experience_level:
            query = query.filter(Job.experience_level == experience_level)
        
        if salary_min is not None:
            query = query.filter(Job.salary_min >= salary_min)
        
        if salary_max is not None:
            query = query.filter(Job.salary_max <= salary_max)
        
        if company_id:
            query = query.filter(Job.company_id == company_id)
        
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def count_search_jobs(
        self,
        search_term: Optional[str] = None,
        location: Optional[str] = None,
        employment_type: Optional[EmploymentType] = None,
        category: Optional[str] = None,
        experience_level: Optional[str] = None,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        company_id: Optional[UUID] = None,
        status: JobStatus = JobStatus.PUBLISHED
    ) -> int:
        """Count jobs with search filters."""
        query = select(func.count(Job.id)).filter(Job.status == status)
        
        if search_term:
            search_conditions = [
                Job.title.ilike(f"%{search_term}%"),
                Job.description.ilike(f"%{search_term}%"),
                Job.category.ilike(f"%{search_term}%")
            ]
            query = query.filter(or_(*search_conditions))
        
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))
        
        if employment_type:
            query = query.filter(Job.type == employment_type)
        
        if category:
            query = query.filter(Job.category.ilike(f"%{category}%"))
        
        if experience_level:
            query = query.filter(Job.experience_level == experience_level)
        
        if salary_min is not None:
            query = query.filter(Job.salary_min >= salary_min)
        
        if salary_max is not None:
            query = query.filter(Job.salary_max <= salary_max)
        
        if company_id:
            query = query.filter(Job.company_id == company_id)
        
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def get_recent_jobs(self, limit: int = 10) -> List[Job]:
        """Get recent published jobs."""
        result = await self.db.execute(
            select(Job).filter(Job.status == JobStatus.PUBLISHED).order_by(Job.published_at.desc()).limit(limit)
        )
        return result.scalars().all()
    
    async def is_slug_available(self, company_id: UUID, slug: str, exclude_id: Optional[UUID] = None) -> bool:
        """Check if slug is available for a company."""
        query = select(Job).filter(and_(Job.company_id == company_id, Job.slug == slug))
        if exclude_id:
            query = query.filter(Job.id != exclude_id)

        result = await self.db.execute(query)
        return result.scalars().first() is None
