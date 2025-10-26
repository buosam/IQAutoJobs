"""
User service for IQAutoJobs.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.models import UserCreate, UserUpdate, UserResponse
from app.repositories.user_repo import UserRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.core.errors import NotFoundError, ConflictError


class UserService:
    """User service."""
    
    def __init__(
        self,
        db: Session,
        user_repo: UserRepository,
        audit_repo: AuditLogRepository
    ):
        self.db = db
        self.user_repo = user_repo
        self.audit_repo = audit_repo
    
    def get_user_by_id(self, user_id: UUID) -> Optional[UserResponse]:
        """Get user by ID."""
        user = self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        return UserResponse.from_orm(user)
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email."""
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        
        return UserResponse.from_orm(user)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get users with pagination."""
        users = self.user_repo.get_multi(skip=skip, limit=limit)
        return [UserResponse.from_orm(user) for user in users]
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get active users."""
        users = self.user_repo.get_active_users(skip=skip, limit=limit)
        return [UserResponse.from_orm(user) for user in users]
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user."""
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ConflictError("User with this email already exists")
        
        user_dict = user_data.dict()
        user = self.user_repo.create_user(user_dict)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="USER_CREATE",
            user_id=user.id,
            subject_type="User",
            subject_id=str(user.id),
            payload={"email": user.email, "role": user.role.value}
        )
        
        return UserResponse.from_orm(user)
    
    def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserResponse:
        """Update a user."""
        user = self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Convert to dict and remove None values
        update_data = user_data.dict(exclude_unset=True)
        
        user = self.user_repo.update_user(user, update_data)
        
        # Log audit
        self.audit_repo.log_user_action(
            action="USER_UPDATE",
            user_id=user_id,
            subject_type="User",
            subject_id=str(user_id),
            payload=update_data
        )
        
        return UserResponse.from_orm(user)
    
    def deactivate_user(self, user_id: UUID) -> UserResponse:
        """Deactivate a user."""
        user = self.user_repo.deactivate_user(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Log audit
        self.audit_repo.log_user_action(
            action="USER_DEACTIVATE",
            user_id=user_id,
            subject_type="User",
            subject_id=str(user_id)
        )
        
        return UserResponse.from_orm(user)
    
    def activate_user(self, user_id: UUID) -> UserResponse:
        """Activate a user."""
        user = self.user_repo.activate_user(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Log audit
        self.audit_repo.log_user_action(
            action="USER_ACTIVATE",
            user_id=user_id,
            subject_type="User",
            subject_id=str(user_id)
        )
        
        return UserResponse.from_orm(user)
    
    def get_employers(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get employer users."""
        users = self.user_repo.get_employers(skip=skip, limit=limit)
        return [UserResponse.from_orm(user) for user in users]
    
    def get_candidates(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get candidate users."""
        users = self.user_repo.get_candidates(skip=skip, limit=limit)
        return [UserResponse.from_orm(user) for user in users]
    
    def get_admins(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get admin users."""
        users = self.user_repo.get_admins(skip=skip, limit=limit)
        return [UserResponse.from_orm(user) for user in users]
    
    def search_users(self, search_term: str, role: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Search users."""
        users = self.user_repo.search_users(search_term, role, skip, limit)
        return [UserResponse.from_orm(user) for user in users]
    
    def count_users_by_role(self, role: str) -> int:
        """Count users by role."""
        return self.user_repo.count_by_role(role)