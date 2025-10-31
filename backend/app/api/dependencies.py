# In a new file, e.g., app/api/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.auth_service import AuthService
from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import RefreshTokenRepository
from app.repositories.audit_log_repo import AuditLogRepository

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Dependency to get an instance of AuthService."""
    user_repo = UserRepository(db)
    token_repo = RefreshTokenRepository(db)
    audit_repo = AuditLogRepository(db)
    return AuthService(db, user_repo, token_repo, audit_repo)
