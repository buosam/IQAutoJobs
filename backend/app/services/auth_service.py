"""
Authentication service for IQAutoJobs.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    create_password_reset_token,
    verify_password_reset_token
)
from app.core.config import settings
from app.domain.models import UserCreate, UserLogin, Token, TokenData, PasswordResetRequest, PasswordReset
from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import RefreshTokenRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.core.errors import AuthenticationError, ConflictError, NotFoundError


class AuthService:
    """Authentication service."""
    
    def __init__(
        self,
        db: Session,
        user_repo: UserRepository,
        token_repo: RefreshTokenRepository,
        audit_repo: AuditLogRepository
    ):
        self.db = db
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.audit_repo = audit_repo
    
    def register_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user."""
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ConflictError("User with this email already exists")
        
        # Create user
        user_dict = user_data.dict()
        user_dict["password_hash"] = get_password_hash(user_data.password)
        del user_dict["password"]
        
        user = self.user_repo.create_user(user_dict)
        
        # Create access and refresh tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token, expires_at = create_refresh_token(user.id)
        
        # Store refresh token
        refresh_token_hash = get_password_hash(refresh_token)
        self.token_repo.create_token(user.id, refresh_token_hash, expires_at)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="USER_REGISTER",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id),
            payload={"email": user.email, "role": user.role.value}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }
    
    def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Login a user."""
        # Find user by email
        user = self.user_repo.get_by_email(login_data.email)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise AuthenticationError("Invalid email or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is deactivated")
        
        # Create access and refresh tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token, expires_at = create_refresh_token(user.id)
        
        # Store refresh token
        refresh_token_hash = get_password_hash(refresh_token)
        self.token_repo.create_token(user.id, refresh_token_hash, expires_at)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="USER_LOGIN",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id),
            payload={"email": user.email}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token."""
        # Verify refresh token
        payload = verify_token(refresh_token, "refresh")
        if not payload:
            raise AuthenticationError("Invalid refresh token")
        
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Invalid refresh token")
        
        # Check if refresh token exists and is valid
        refresh_token_hash = get_password_hash(refresh_token)
        token = self.token_repo.get_by_token_hash(refresh_token_hash)
        if not token or not self.token_repo.is_token_valid(refresh_token_hash):
            raise AuthenticationError("Invalid or expired refresh token")
        
        # Get user
        user = self.user_repo.get(UUID(user_id))
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        # Create new access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    def logout_user(self, refresh_token: str, user_id: UUID) -> bool:
        """Logout a user."""
        # Verify refresh token
        refresh_token_hash = get_password_hash(refresh_token)
        token = self.token_repo.get_by_token_hash(refresh_token_hash)
        
        if token:
            # Revoke the refresh token
            self.token_repo.revoke_token(token.id)
            
            # Log audit
            self.audit_repo.log_user_action(
                action="USER_LOGOUT",
                user_id=user_id,
                subject_type="User",
                subject_id=str(user_id)
            )
            
            return True
        
        return False
    
    def request_password_reset(self, email: str) -> bool:
        """Request password reset."""
        user = self.user_repo.get_by_email(email)
        if not user:
            # Don't reveal that user doesn't exist
            return True
        
        # Create password reset token
        reset_token = create_password_reset_token(email)
        
        # In a real app, send email with reset token
        # For now, we'll just log it
        print(f"Password reset token for {email}: {reset_token}")
        
        # Log audit
        self.audit_repo.log_user_action(
            action="PASSWORD_RESET_REQUEST",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id),
            payload={"email": email}
        )
        
        return True
    
    def reset_password(self, reset_data: PasswordReset) -> bool:
        """Reset password."""
        # Verify reset token
        email = verify_password_reset_token(reset_data.token)
        if not email:
            raise AuthenticationError("Invalid or expired reset token")
        
        # Get user
        user = self.user_repo.get_by_email(email)
        if not user:
            raise NotFoundError("User not found")
        
        # Update password
        user.password_hash = get_password_hash(reset_data.new_password)
        self.db.commit()
        
        # Revoke all refresh tokens for security
        self.token_repo.revoke_all_user_tokens(user.id)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="PASSWORD_RESET",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id)
        )
        
        return True
    
    def change_password(self, user_id: UUID, current_password: str, new_password: str) -> bool:
        """Change user password."""
        user = self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise AuthenticationError("Current password is incorrect")
        
        # Update password
        user.password_hash = get_password_hash(new_password)
        self.db.commit()
        
        # Revoke all refresh tokens for security
        self.token_repo.revoke_all_user_tokens(user.id)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="PASSWORD_CHANGE",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id)
        )
        
        return True
    
    def get_current_user(self, token: str) -> Optional[Any]:
        """Get current user from token."""
        payload = verify_token(token, "access")
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = self.user_repo.get(UUID(user_id))
        if not user or not user.is_active:
            return None
        
        return user
    
    def is_token_valid(self, token: str) -> bool:
        """Check if token is valid."""
        return verify_token(token, "access") is not None