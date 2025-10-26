"""
Company repository for IQAutoJobs.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
import sqlalchemy.orm

from app.db.models import Company
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    """Company repository with company-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(Company, db)
    
    def get_by_slug(self, slug: str) -> Optional[Company]:
        """Get company by slug."""
        return self.db.query(Company).filter(Company.slug == slug).first()
    
    def get_by_owner(self, owner_user_id: UUID) -> Optional[Company]:
        """Get company by owner."""
        return self.db.query(Company).filter(Company.owner_user_id == owner_user_id).first()
    
    def get_with_jobs(self, company_id: UUID) -> Optional[Company]:
        """Get company with jobs relationship loaded."""
        return self.db.query(Company).options(
            sqlalchemy.orm.joinedload(Company.jobs)
        ).filter(Company.id == company_id).first()
    
    def get_with_owner(self, company_id: UUID) -> Optional[Company]:
        """Get company with owner relationship loaded."""
        return self.db.query(Company).options(
            sqlalchemy.orm.joinedload(Company.owner)
        ).filter(Company.id == company_id).first()
    
    def get_companies_with_jobs(self, skip: int = 0, limit: int = 100) -> List[Company]:
        """Get companies with their jobs."""
        return self.db.query(Company).options(
            sqlalchemy.orm.joinedload(Company.jobs)
        ).offset(skip).limit(limit).all()
    
    def search_companies(
        self,
        search_term: str,
        industry: Optional[str] = None,
        location: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Company]:
        """Search companies by name, description, or other fields."""
        query = self.db.query(Company)
        
        if search_term:
            search_conditions = [
                Company.name.ilike(f"%{search_term}%"),
                Company.description.ilike(f"%{search_term}%"),
                Company.industry.ilike(f"%{search_term}%")
            ]
            query = query.filter(or_(*search_conditions))
        
        if industry:
            query = query.filter(Company.industry.ilike(f"%{industry}%"))
        
        if location:
            query = query.filter(Company.location.ilike(f"%{location}%"))
        
        return query.offset(skip).limit(limit).all()
    
    def get_companies_by_industry(self, industry: str, skip: int = 0, limit: int = 100) -> List[Company]:
        """Get companies by industry."""
        return self.db.query(Company).filter(
            Company.industry.ilike(f"%{industry}%")
        ).offset(skip).limit(limit).all()
    
    def get_companies_by_location(self, location: str, skip: int = 0, limit: int = 100) -> List[Company]:
        """Get companies by location."""
        return self.db.query(Company).filter(
            Company.location.ilike(f"%{location}%")
        ).offset(skip).limit(limit).all()
    
    def create_company(self, company_data: Dict[str, Any]) -> Company:
        """Create a new company."""
        return self.create(company_data)
    
    def update_company(self, company: Company, company_data: Dict[str, Any]) -> Company:
        """Update a company."""
        return self.update(company, company_data)
    
    def is_slug_available(self, slug: str, exclude_id: Optional[UUID] = None) -> bool:
        """Check if slug is available."""
        query = self.db.query(Company).filter(Company.slug == slug)
        if exclude_id:
            query = query.filter(Company.id != exclude_id)
        return query.first() is None