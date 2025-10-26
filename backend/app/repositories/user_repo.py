"""
User repository for IQAutoJobs.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
import sqlalchemy.orm

from app.db.models import User, UserRole
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository with user-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_oauth(self, provider: str, oauth_id: str) -> Optional[User]:
        """Get user by OAuth provider and ID."""
        return self.db.query(User).filter(
            User.oauth_provider == provider,
            User.oauth_id == oauth_id
        ).first()
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users."""
        return self.db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def get_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role."""
        return self.db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user."""
        return self.create(user_data)
    
    def update_user(self, user: User, user_data: Dict[str, Any]) -> User:
        """Update a user."""
        return self.update(user, user_data)
    
    def deactivate_user(self, user_id: UUID) -> Optional[User]:
        """Deactivate a user."""
        user = self.get(user_id)
        if user:
            user.is_active = False
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def activate_user(self, user_id: UUID) -> Optional[User]:
        """Activate a user."""
        user = self.get(user_id)
        if user:
            user.is_active = True
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def get_employers(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get employer users."""
        return self.get_by_role(UserRole.EMPLOYER, skip, limit)
    
    def get_candidates(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get candidate users."""
        return self.get_by_role(UserRole.CANDIDATE, skip, limit)
    
    def get_admins(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get admin users."""
        return self.get_by_role(UserRole.ADMIN, skip, limit)
    
    def search_users(
        self,
        search_term: str,
        role: Optional[UserRole] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Search users by name or email."""
        query = self.db.query(User)
        
        if search_term:
            search_conditions = [
                User.email.ilike(f"%{search_term}%"),
                User.first_name.ilike(f"%{search_term}%"),
                User.last_name.ilike(f"%{search_term}%")
            ]
            query = query.filter(or_(*search_conditions))
        
        if role:
            query = query.filter(User.role == role)
        
        return query.offset(skip).limit(limit).all()
    
    def count_by_role(self, role: UserRole) -> int:
        """Count users by role."""
        return self.db.query(User).filter(User.role == role).count()
    
    def get_user_with_company(self, user_id: UUID) -> Optional[User]:
        """Get user with company relationship loaded."""
        return self.db.query(User).options(
            sqlalchemy.orm.joinedload(User.company)
        ).filter(User.id == user_id).first()