"""
Authentication router for IQAutoJobs.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from app.db.base import get_db
from app.domain.models import (
    UserCreate, UserLogin, Token, PasswordResetRequest, PasswordReset,
    PasswordChange, UserResponse
)
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import RefreshTokenRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.core.errors import AuthenticationError, ConflictError, NotFoundError
from app.api.dependencies import get_auth_service

logger = get_logger()
router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get current user from JWT token."""
    user = await auth_service.get_current_user(credentials.credentials)
    if not user:
        raise AuthenticationError("Invalid authentication credentials")
    
    return user


@router.post("/register", response_model=dict)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user."""
    try:
        result = await auth_service.register_user(user_data)
        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": result["token_type"],
            "user": UserResponse.model_validate(result["user"])
        }
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error("Registration failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")


@router.post("/login", response_model=dict)
async def login(
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login a user."""
    try:
        result = await auth_service.login_user(login_data)
        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": result["token_type"],
            "user": UserResponse.model_validate(result["user"])
        }
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")


@router.post("/refresh", response_model=dict)
async def refresh_token(
    refresh_token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh access token."""
    try:
        result = await auth_service.refresh_access_token(refresh_token)
        return result
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token refresh failed")


@router.post("/logout")
async def logout(
    refresh_token: str,
    current_user = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Logout a user."""
    try:
        await auth_service.logout_user(refresh_token, current_user.id)
        return {"message": "Successfully logged out"}
    except Exception as e:
        logger.error("Logout failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Logout failed")


@router.post("/request-reset")
async def request_password_reset(
    request_data: PasswordResetRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Request password reset."""
    try:
        await auth_service.request_password_reset(request_data.email)
        return {"message": "If the email exists, a password reset link has been sent"}
    except Exception as e:
        logger.error("Password reset request failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password reset request failed")


@router.post("/reset")
async def reset_password(
    reset_data: PasswordReset,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Reset password."""
    try:
        await auth_service.reset_password(reset_data)
        return {"message": "Password reset successfully"}
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Password reset failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password reset failed")


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Change user password."""
    try:
        await auth_service.change_password(
            current_user.id,
            password_data.current_password,
            password_data.new_password
        )
        return {"message": "Password changed successfully"}
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        logger.error("Password change failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password change failed")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse.model_validate(current_user)
