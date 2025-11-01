"""
Authentication service for IQAutoJobs.
"""
import time
import structlog
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

logger = structlog.get_logger(__name__)


class AuthService:
    """Authentication service."""
    
    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: RefreshTokenRepository,
        audit_repo: AuditLogRepository
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.audit_repo = audit_repo
    
    async def register_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user."""
        start_time = time.time()
        log = logger.bind(email=user_data.email)
        log.info("Registration process started")

        # Check if user already exists
        log.info("Checking for existing user")
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            log.warn("User already exists")
            raise ConflictError("User with this email already exists")
        
        # Create user
        log.info("Hashing password")
        hash_start = time.time()
        hashed_password = await get_password_hash(user_data.password)
        log.info("Password hashing complete", duration=time.time() - hash_start)

        user_dict = user_data.dict()
        user_dict["hashed_password"] = hashed_password
        del user_dict["password"]
        
        log.info("Creating user in repository")
        user = await self.user_repo.create_user(user_dict)
        log.info("User created", user_id=user.id)
        
        # Create access and refresh tokens
        log.info("Creating tokens")
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token, expires_at = create_refresh_token(user.id)
        
        # Store refresh token
        log.info("Storing refresh token")
        refresh_token_hash = await get_password_hash(refresh_token)
        await self.token_repo.create_token(user.id, refresh_token_hash, expires_at)
        log.info("Refresh token stored")
        
        # Log audit
        await self.audit_repo.log_user_action(
            action="USER_REGISTER",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id),
            payload={"email": user.email, "role": user.role.value}
        )
        
        log.info("Registration process finished", duration=time.time() - start_time)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }
    
    async def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Login a user."""
        start_time = time.time()
        log = logger.bind(email=login_data.email)
        log.info("Login process started")

        # Find user by email
        log.info("Finding user by email")
        user = await self.user_repo.get_by_email(login_data.email)

        if not user:
            log.warn("User not found")
            raise AuthenticationError("Invalid email or password")

        log.info("Verifying password")
        verify_start = time.time()
        password_valid = await verify_password(login_data.password, user.hashed_password)
        log.info("Password verification complete", duration=time.time() - verify_start)

        if not password_valid:
            log.warn("Invalid password")
            raise AuthenticationError("Invalid email or password")

        if not user.is_active:
            log.warn("User account is deactivated")
            raise AuthenticationError("User account is deactivated")

        # Create access and refresh tokens
        log.info("Creating tokens")
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token, expires_at = create_refresh_token(user.id)

        # Store refresh token
        log.info("Storing refresh token")
        refresh_token_hash = await get_password_hash(refresh_token)
        await self.token_repo.create_token(user.id, refresh_token_hash, expires_at)
        log.info("Refresh token stored")

        # Log audit
        await self.audit_repo.log_user_action(
            action="USER_LOGIN",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id),
            payload={"email": user.email},
        )
        
        log.info("Login process finished", duration=time.time() - start_time)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token."""
        # Verify refresh token
        payload = verify_token(refresh_token, "refresh")
        if not payload:
            raise AuthenticationError("Invalid refresh token")
        
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Invalid refresh token")
        
        # Check if refresh token exists and is valid
        refresh_token_hash = await get_password_hash(refresh_token)
        token = await self.token_repo.get_by_token_hash(refresh_token_hash)
        if not token or token.revoked:
            raise AuthenticationError("Invalid or expired refresh token")
        
        # Get user
        user = await self.user_repo.get(UUID(user_id))
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        # Create new access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    async def logout_user(self, refresh_token: str, user_id: UUID) -> bool:
        """Logout a user."""
        # Verify refresh token
        refresh_token_hash = await get_password_hash(refresh_token)
        token = await self.token_repo.get_by_token_hash(refresh_token_hash)
        
        if token:
            # Revoke the refresh token
            await self.token_repo.revoke_token(token.id)
            
            # Log audit
            await self.audit_repo.log_user_action(
                action="USER_LOGOUT",
                user_id=user_id,
                subject_type="User",
                subject_id=str(user_id)
            )
            
            return True
        
        return False
    
    async def request_password_reset(self, email: str) -> bool:
        """Request password reset."""
        user = await self.user_repo.get_by_email(email)
        if not user:
            # Don't reveal that user doesn't exist
            return True
        
        # Create password reset token
        reset_token = create_password_reset_token(email)
        
        # In a real app, send email with reset token
        # For now, we'll just log it
        print(f"Password reset token for {email}: {reset_token}")
        
        # Log audit
        await self.audit_repo.log_user_action(
            action="PASSWORD_RESET_REQUEST",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id),
            payload={"email": email}
        )
        
        return True
    
    async def reset_password(self, reset_data: PasswordReset) -> bool:
        """Reset password."""
        # Verify reset token
        email = verify_password_reset_token(reset_data.token)
        if not email:
            raise AuthenticationError("Invalid or expired reset token")
        
        # Get user
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise NotFoundError("User not found")
        
        # Update password
        hashed_password = await get_password_hash(reset_data.new_password)
        await self.user_repo.update_user(user, {"hashed_password": hashed_password})
        
        # Revoke all refresh tokens for security
        await self.token_repo.revoke_all_user_tokens(user.id)
        
        # Log audit
        await self.audit_repo.log_user_action(
            action="PASSWORD_RESET",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id)
        )
        
        return True
    
    async def change_password(self, user_id: UUID, current_password: str, new_password: str) -> bool:
        """Change user password."""
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Verify current password
        if not await verify_password(current_password, user.hashed_password):
            raise AuthenticationError("Current password is incorrect")
        
        # Update password
        hashed_password = await get_password_hash(new_password)
        await self.user_repo.update_user(user, {"hashed_password": hashed_password})
        
        # Revoke all refresh tokens for security
        await self.token_repo.revoke_all_user_tokens(user.id)
        
        # Log audit
        await self.audit_repo.log_user_action(
            action="PASSWORD_CHANGE",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id)
        )
        
        return True
    
    async def get_current_user(self, token: str) -> Optional[Any]:
        """Get current user from token."""
        payload = verify_token(token, "access")
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await self.user_repo.get(UUID(user_id))
        if not user or not user.is_active:
            return None
        
        return user
    
    def is_token_valid(self, token: str) -> bool:
        """Check if token is valid."""
        return verify_token(token, "access") is not None    
    async def oauth_login(self, provider: str, oauth_id: str, email: str, first_name: str = "", last_name: str = "") -> Dict[str, Any]:
        """Login or register user via OAuth."""
        # First, try to find user by OAuth provider and ID
        user = await self.user_repo.get_by_oauth(provider, oauth_id)
        
        # If not found, try to find by email (existing user linking OAuth)
        if not user:
            user = await self.user_repo.get_by_email(email)
            if user:
                # Link OAuth to existing account
                user = await self.user_repo.update_user(user, {"oauth_provider": provider, "oauth_id": oauth_id})

        # If still not found, create new user
        if not user:
            user_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "oauth_provider": provider,
                "oauth_id": oauth_id,
                "hashed_password": None,  # OAuth users don't have password
                "role": "CANDIDATE",  # Default role for OAuth users
                "is_active": True
            }
            user = await self.user_repo.create_user(user_data)
            
            # Log audit for new OAuth user
            await self.audit_repo.log_user_action(
                action="OAUTH_REGISTER",
                user_id=user.id,
                subject_type="User",
                subject_id=str(user.id),
                payload={"email": email, "provider": provider}
            )
        else:
            # Log audit for OAuth login
            await self.audit_repo.log_user_action(
                action="OAUTH_LOGIN",
                user_id=user.id,
                subject_type="User",
                subject_id=str(user.id),
                payload={"email": email, "provider": provider}
            )
        
        # Create access and refresh tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token, expires_at = create_refresh_token(user.id)
        
        # Store refresh token
        refresh_token_hash = await get_password_hash(refresh_token)
        await self.token_repo.create_token(user.id, refresh_token_hash, expires_at)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }
