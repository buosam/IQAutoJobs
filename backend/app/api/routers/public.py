"""
Public router for IQAutoJobs - endpoints that don't require authentication.
"""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from structlog import get_logger

from app.db.base import get_db
from app.domain.models import UserResponse
from app.services.user_service import UserService
from app.repositories.user_repo import UserRepository
from app.repositories.audit_log_repo import AuditLogRepository

logger = get_logger()
router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
async def get_public_users(
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(100, ge=1, le=100, description="Limit count"),
    db: Session = Depends(get_db)
):
    """Get all users (public endpoint for demo purposes)."""
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    user_service = UserService(db, user_repo, audit_repo)
    
    return user_service.get_users(skip, limit)
