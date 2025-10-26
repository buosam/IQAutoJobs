"""
Company service for IQAutoJobs.
"""
import re
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.models import CompanyCreate, CompanyUpdate, CompanyResponse
from app.repositories.company_repo import CompanyRepository
from app.repositories.user_repo import UserRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.core.errors import NotFoundError, ConflictError


class CompanyService:
    """Company service."""
    
    def __init__(
        self,
        db: Session,
        company_repo: CompanyRepository,
        user_repo: UserRepository,
        audit_repo: AuditLogRepository
    ):
        self.db = db
        self.company_repo = company_repo
        self.user_repo = user_repo
        self.audit_repo = audit_repo
    
    def get_company_by_id(self, company_id: UUID) -> Optional[CompanyResponse]:
        """Get company by ID."""
        company = self.company_repo.get(company_id)
        if not company:
            raise NotFoundError("Company not found")
        
        return CompanyResponse.from_orm(company)
    
    def get_company_by_slug(self, slug: str) -> Optional[CompanyResponse]:
        """Get company by slug."""
        company = self.company_repo.get_by_slug(slug)
        if not company:
            return None
        
        return CompanyResponse.from_orm(company)
    
    def get_company_by_owner(self, owner_user_id: UUID) -> Optional[CompanyResponse]:
        """Get company by owner."""
        company = self.company_repo.get_by_owner(owner_user_id)
        if not company:
            return None
        
        return CompanyResponse.from_orm(company)
    
    def get_companies(self, skip: int = 0, limit: int = 100) -> List[CompanyResponse]:
        """Get companies with pagination."""
        companies = self.company_repo.get_multi(skip=skip, limit=limit)
        return [CompanyResponse.from_orm(company) for company in companies]
    
    def get_companies_with_jobs(self, skip: int = 0, limit: int = 100) -> List[CompanyResponse]:
        """Get companies with their jobs."""
        companies = self.company_repo.get_companies_with_jobs(skip=skip, limit=limit)
        return [CompanyResponse.from_orm(company) for company in companies]
    
    def create_company(self, company_data: CompanyCreate, owner_user_id: UUID) -> CompanyResponse:
        """Create a new company."""
        # Check if user exists
        user = self.user_repo.get(owner_user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Check if user already has a company
        existing_company = self.company_repo.get_by_owner(owner_user_id)
        if existing_company:
            raise ConflictError("User already has a company")
        
        # Generate slug from company name
        slug = self._generate_slug(company_data.name)
        
        # Check if slug is available
        if not self.company_repo.is_slug_available(slug):
            raise ConflictError("Company name is already taken")
        
        company_dict = company_data.dict()
        company_dict["owner_user_id"] = owner_user_id
        company_dict["slug"] = slug
        
        company = self.company_repo.create_company(company_dict)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="COMPANY_CREATE",
            user_id=owner_user_id,
            subject_type="Company",
            subject_id=str(company.id),
            payload={"name": company.name, "slug": company.slug}
        )
        
        return CompanyResponse.from_orm(company)
    
    def update_company(self, company_id: UUID, company_data: CompanyUpdate, user_id: UUID) -> CompanyResponse:
        """Update a company."""
        company = self.company_repo.get(company_id)
        if not company:
            raise NotFoundError("Company not found")
        
        # Check if user owns the company
        if company.owner_user_id != user_id:
            raise ConflictError("You don't have permission to update this company")
        
        # Convert to dict and remove None values
        update_data = company_data.dict(exclude_unset=True)
        
        # If name is being updated, generate new slug
        if "name" in update_data:
            new_slug = self._generate_slug(update_data["name"])
            if new_slug != company.slug:
                if not self.company_repo.is_slug_available(new_slug, company_id):
                    raise ConflictError("Company name is already taken")
                update_data["slug"] = new_slug
        
        company = self.company_repo.update_company(company, update_data)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="COMPANY_UPDATE",
            user_id=user_id,
            subject_type="Company",
            subject_id=str(company_id),
            payload=update_data
        )
        
        return CompanyResponse.from_orm(company)
    
    def search_companies(
        self,
        search_term: str,
        industry: Optional[str] = None,
        location: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CompanyResponse]:
        """Search companies."""
        companies = self.company_repo.search_companies(
            search_term, industry, location, skip, limit
        )
        return [CompanyResponse.from_orm(company) for company in companies]
    
    def get_companies_by_industry(self, industry: str, skip: int = 0, limit: int = 100) -> List[CompanyResponse]:
        """Get companies by industry."""
        companies = self.company_repo.get_companies_by_industry(industry, skip, limit)
        return [CompanyResponse.from_orm(company) for company in companies]
    
    def get_companies_by_location(self, location: str, skip: int = 0, limit: int = 100) -> List[CompanyResponse]:
        """Get companies by location."""
        companies = self.company_repo.get_companies_by_location(location, skip, limit)
        return [CompanyResponse.from_orm(company) for company in companies]
    
    def _generate_slug(self, name: str) -> str:
        """Generate URL-friendly slug from company name."""
        # Convert to lowercase
        slug = name.lower()
        
        # Replace special characters with hyphens
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        
        # Remove consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        return slug