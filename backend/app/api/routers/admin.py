"""
Admin router for IQAutoJobs.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from structlog import get_logger

from app.db.base import get_db
from app.domain.models import (
    UserResponse, UserRole, ApplicationResponse, JobResponse, CompanyResponse,
    AuditLogResponse
)
from app.services.user_service import UserService
from app.services.job_service import JobService
from app.services.company_service import CompanyService
from app.services.application_service import ApplicationService
from app.repositories.user_repo import UserRepository
from app.repositories.job_repo import JobRepository
from app.repositories.company_repo import CompanyRepository
from app.repositories.application_repo import ApplicationRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.api.routers.auth import get_current_user
from app.core.errors import NotFoundError

logger = get_logger()
router = APIRouter()


def require_admin(current_user):
    """Check if current user is admin."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.get("/users", response_model=list[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    role: Optional[UserRole] = Query(None, description="Filter by role"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)."""
    require_admin(current_user)
    
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    user_service = UserService(db, user_repo, audit_repo)
    
    if role:
        if role == UserRole.EMPLOYER:
            return user_service.get_employers(skip, limit)
        elif role == UserRole.CANDIDATE:
            return user_service.get_candidates(skip, limit)
        elif role == UserRole.ADMIN:
            return user_service.get_admins(skip, limit)
    
    return user_service.get_users(skip, limit)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)."""
    require_admin(current_user)
    
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    user_service = UserService(db, user_repo, audit_repo)
    
    try:
        return user_service.get_user_by_id(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/users/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activate a user (admin only)."""
    require_admin(current_user)
    
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    user_service = UserService(db, user_repo, audit_repo)
    
    try:
        return user_service.activate_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/users/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deactivate a user (admin only)."""
    require_admin(current_user)
    
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    user_service = UserService(db, user_repo, audit_repo)
    
    try:
        return user_service.deactivate_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/companies", response_model=list[CompanyResponse])
async def get_companies(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all companies (admin only)."""
    require_admin(current_user)
    
    company_repo = CompanyRepository(db)
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    company_service = CompanyService(db, company_repo, user_repo, audit_repo)
    
    return company_service.get_companies(skip, limit)


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get company by ID (admin only)."""
    require_admin(current_user)
    
    company_repo = CompanyRepository(db)
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    company_service = CompanyService(db, company_repo, user_repo, audit_repo)
    
    try:
        return company_service.get_company_by_id(company_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/jobs", response_model=list[JobResponse])
async def get_jobs(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all jobs (admin only)."""
    require_admin(current_user)
    
    job_repo = JobRepository(db)
    company_repo = CompanyRepository(db)
    audit_repo = AuditLogRepository(db)
    job_service = JobService(db, job_repo, company_repo, audit_repo)
    
    return job_service.get_jobs(skip, limit)


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get job by ID (admin only)."""
    require_admin(current_user)
    
    job_repo = JobRepository(db)
    company_repo = CompanyRepository(db)
    audit_repo = AuditLogRepository(db)
    job_service = JobService(db, job_repo, company_repo, audit_repo)
    
    try:
        return job_service.get_job_by_id(job_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/applications", response_model=list[ApplicationResponse])
async def get_applications(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all applications (admin only)."""
    require_admin(current_user)
    
    app_repo = ApplicationRepository(db)
    job_repo = JobRepository(db)
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    app_service = ApplicationService(db, app_repo, job_repo, user_repo, audit_repo)
    
    return app_service.search_applications(skip=skip, limit=limit)


@router.get("/applications/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get application by ID (admin only)."""
    require_admin(current_user)
    
    app_repo = ApplicationRepository(db)
    job_repo = JobRepository(db)
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    app_service = ApplicationService(db, app_repo, job_repo, user_repo, audit_repo)
    
    try:
        return app_service.get_application_by_id(application_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/audit-logs", response_model=list[AuditLogResponse])
async def get_audit_logs(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    action: Optional[str] = Query(None, description="Filter by action"),
    subject_type: Optional[str] = Query(None, description="Filter by subject type"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get audit logs (admin only)."""
    require_admin(current_user)
    
    audit_repo = AuditLogRepository(db)
    
    if action:
        logs = audit_repo.get_by_action(action, skip, limit)
    elif subject_type:
        logs = audit_repo.get_by_subject_type(subject_type, skip, limit)
    else:
        logs = audit_repo.get_audit_logs_with_actor(skip, limit)
    
    return [AuditLogResponse.from_orm(log) for log in logs]


@router.get("/stats")
async def get_admin_stats(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get admin statistics (admin only)."""
    require_admin(current_user)
    
    user_repo = UserRepository(db)
    job_repo = JobRepository(db)
    app_repo = ApplicationRepository(db)
    company_repo = CompanyRepository(db)
    
    stats = {
        "total_users": user_repo.count(),
        "total_companies": company_repo.count(),
        "total_jobs": job_repo.count(),
        "total_applications": app_repo.count(),
        "active_users": user_repo.count({"is_active": True}),
        "published_jobs": job_repo.count({"status": "PUBLISHED"}),
        "users_by_role": {
            "admins": user_repo.count_by_role("ADMIN"),
            "employers": user_repo.count_by_role("EMPLOYER"),
            "candidates": user_repo.count_by_role("CANDIDATE")
        }
    }
    
    return stats