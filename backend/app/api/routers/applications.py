"""
Applications router for IQAutoJobs.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from structlog import get_logger

from app.db.base import get_db
from app.domain.models import (
    ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationStatus
)
from app.services.application_service import ApplicationService
from app.services.job_service import JobService
from app.services.file_service import FileService
from app.repositories.application_repo import ApplicationRepository
from app.repositories.job_repo import JobRepository
from app.repositories.user_repo import UserRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.api.routers.auth import get_current_user
from app.core.errors import NotFoundError, ConflictError, FileUploadError

logger = get_logger()
router = APIRouter()


async def get_application_service(db: Session = Depends(get_db)) -> ApplicationService:
    """Get application service instance."""
    app_repo = ApplicationRepository(db)
    job_repo = JobRepository(db)
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    return ApplicationService(db, app_repo, job_repo, user_repo, audit_repo)


@router.get("/", response_model=list[ApplicationResponse])
async def get_applications(
    job_id: Optional[str] = Query(None, description="Filter by job ID"),
    status: Optional[ApplicationStatus] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    current_user = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """Get applications for current user's company."""
    if job_id:
        return await app_service.get_applications_by_job(job_id, skip, limit)
    elif status:
        return await app_service.get_applications_by_status(status, skip, limit)
    else:
        return await app_service.get_applications_by_company(current_user.id, skip, limit)


@router.get("/my-applications", response_model=list[ApplicationResponse])
async def get_my_applications(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    current_user = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """Get applications for current user (candidate)."""
    return await app_service.get_applications_by_candidate(current_user.id, skip, limit)


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: str,
    current_user = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """Get application by ID."""
    try:
        application = await app_service.get_application_by_id(application_id)
        
        # Check if user has permission to view this application
        if (application.job.company.owner_user_id != current_user.id and 
            application.candidate_user_id != current_user.id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to view this application")
        
        return application
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ApplicationResponse)
async def create_application(
    job_id: str,
    cover_letter: Optional[str] = None,
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """Create a new application."""
    file_service = FileService()
    
    try:
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
        
        # Upload file to R2
        cv_key = file_service.upload_cv(file_data, str(current_user.id))
        
        # Create application
        application_data = ApplicationCreate(
            job_id=job_id,
            cover_letter=cover_letter
        )
        
        return await app_service.create_application(application_data, current_user.id, cv_key)
    
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except FileUploadError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Application creation failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Application creation failed")


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: str,
    status: ApplicationStatus,
    current_user = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """Update application status."""
    try:
        return await app_service.update_application_status(application_id, status, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Application status update failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Application status update failed")


@router.get("/{application_id}/cv")
async def get_application_cv(
    application_id: str,
    current_user = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """Get application CV download URL."""
    file_service = FileService()
    
    try:
        application = await app_service.get_application_by_id(application_id)
        
        # Check if user has permission to view this CV
        if (application.job.company.owner_user_id != current_user.id and 
            application.candidate_user_id != current_user.id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to view this CV")
        
        # Generate signed URL
        cv_url = file_service.get_file_url(application.cv_key, expires_in=3600)  # 1 hour
        
        return {"url": cv_url, "filename": f"cv_{application_id}.pdf"}
    
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("CV URL generation failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate CV URL")
