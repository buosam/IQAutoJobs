"""
Companies router for IQAutoJobs.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from structlog import get_logger

from app.db.base import get_db
from app.domain.models import CompanyCreate, CompanyUpdate, CompanyResponse
from app.services.company_service import CompanyService
from app.services.file_service import FileService
from app.repositories.company_repo import CompanyRepository
from app.repositories.user_repo import UserRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.api.routers.auth import get_current_user
from app.core.errors import NotFoundError, ConflictError, FileUploadError

logger = get_logger()
router = APIRouter()


def get_company_service(db: Session) -> CompanyService:
    """Get company service instance."""
    company_repo = CompanyRepository(db)
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    return CompanyService(db, company_repo, user_repo, audit_repo)


@router.get("/", response_model=list[CompanyResponse])
async def get_companies(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    db: Session = Depends(get_db)
):
    """Get companies with pagination."""
    company_service = get_company_service(db)
    return company_service.get_companies(skip, limit)


@router.get("/with-jobs", response_model=list[CompanyResponse])
async def get_companies_with_jobs(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    db: Session = Depends(get_db)
):
    """Get companies with their jobs."""
    company_service = get_company_service(db)
    return company_service.get_companies_with_jobs(skip, limit)


@router.get("/search", response_model=list[CompanyResponse])
async def search_companies(
    search: str = Query(..., description="Search term"),
    industry: Optional[str] = Query(None, description="Industry filter"),
    location: Optional[str] = Query(None, description="Location filter"),
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    db: Session = Depends(get_db)
):
    """Search companies."""
    company_service = get_company_service(db)
    return company_service.search_companies(search, industry, location, skip, limit)


@router.get("/by-industry/{industry}", response_model=list[CompanyResponse])
async def get_companies_by_industry(
    industry: str,
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    db: Session = Depends(get_db)
):
    """Get companies by industry."""
    company_service = get_company_service(db)
    return company_service.get_companies_by_industry(industry, skip, limit)


@router.get("/by-location/{location}", response_model=list[CompanyResponse])
async def get_companies_by_location(
    location: str,
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    db: Session = Depends(get_db)
):
    """Get companies by location."""
    company_service = get_company_service(db)
    return company_service.get_companies_by_location(location, skip, limit)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: str, db: Session = Depends(get_db)):
    """Get company by ID."""
    company_service = get_company_service(db)
    
    try:
        return company_service.get_company_by_id(company_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/slug/{slug}", response_model=CompanyResponse)
async def get_company_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get company by slug."""
    company_service = get_company_service(db)
    company = company_service.get_company_by_slug(slug)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


@router.get("/my-company", response_model=CompanyResponse)
async def get_my_company(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's company."""
    company_service = get_company_service(db)
    company = company_service.get_company_by_owner(current_user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


@router.post("/", response_model=CompanyResponse)
async def create_company(
    company_data: CompanyCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company."""
    company_service = get_company_service(db)
    
    try:
        return company_service.create_company(company_data, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Company creation failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Company creation failed")


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a company."""
    company_service = get_company_service(db)
    
    try:
        return company_service.update_company(company_id, company_data, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Company update failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Company update failed")


@router.post("/{company_id}/logo")
async def upload_company_logo(
    company_id: str,
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload company logo."""
    company_service = get_company_service(db)
    file_service = FileService()
    
    try:
        # Check if user owns the company
        company = company_service.get_company_by_id(company_id)
        if company.owner_user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to upload logo for this company")
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")
        
        # Read file content
        file_content = await file.read()
        
        # Prepare file data
        file_data = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
            "content": file_content
        }
        
        # Upload logo to R2
        logo_key = file_service.upload_company_logo(file_data, company_id)
        
        # Update company with logo key
        from app.domain.models import CompanyUpdate
        company_update = CompanyUpdate()
        # This would need to be implemented in the company service
        # For now, we'll just return the logo URL
        
        logo_url = file_service.get_public_url(logo_key)
        
        return {"logo_url": logo_url, "logo_key": logo_key}
    
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except FileUploadError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Logo upload failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Logo upload failed")


@router.get("/{company_id}/jobs")
async def get_company_jobs(
    company_id: str,
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    db: Session = Depends(get_db)
):
    """Get jobs for a company."""
    from app.api.routers.jobs import get_job_service
    
    job_service = get_job_service(db)
    return job_service.get_jobs_by_company(company_id, skip, limit)