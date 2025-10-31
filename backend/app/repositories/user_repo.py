"""
User repository for IQAutoJobs.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.orm

from app.db.models import User, UserRole
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository with user-specific operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_oauth(self, provider: str, oauth_id: str) -> Optional[User]:
        """Get user by OAuth provider and ID."""
        result = await self.db.execute(
            select(User).filter(
                User.oauth_provider == provider, User.oauth_id == oauth_id
            )
        )
        return result.scalar_one_or_none()

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users."""
        result = await self.db.execute(
            select(User).filter(User.is_active == True).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_by_role(
        self, role: UserRole, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Get users by role."""
        result = await self.db.execute(
            select(User).filter(User.role == role).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user."""
        return await self.create(user_data)

    async def update_user(self, user: User, user_data: Dict[str, Any]) -> User:
        """Update a user."""
        return await self.update(user, user_data)

    async def deactivate_user(self, user_id: UUID) -> Optional[User]:
        """Deactivate a user."""
        user = await self.get(user_id)
        if user:
            user.is_active = False
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def activate_user(self, user_id: UUID) -> Optional[User]:
        """Activate a user."""
        user = await self.get(user_id)
        if user:
            user.is_active = True
            await self.db.commit()
            await self.db.refresh(user)
        return user
    
    async def get_employers(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get employer users."""
        return await self.get_by_role(UserRole.EMPLOYER, skip, limit)
    
    async def get_candidates(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get candidate users."""
        return await self.get_by_role(UserRole.CANDIDATE, skip, limit)
    
    async def get_admins(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get admin users."""
        return await self.get_by_role(UserRole.ADMIN, skip, limit)
    
    async def search_users(
        self,
        search_term: str,
        role: Optional[UserRole] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Search users by name or email."""
        query = select(User)
        
        if search_term:
            search_conditions = [
                User.email.ilike(f"%{search_term}%"),
                User.first_name.ilike(f"%{search_term}%"),
                User.last_name.ilike(f"%{search_term}%")
            ]
            query = query.filter(or_(*search_conditions))
        
        if role:
            query = query.filter(User.role == role)
        
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def count_by_role(self, role: UserRole) -> int:
        """Count users by role."""
        result = await self.db.execute(select(func.count(User.id)).filter(User.role == role))
        return result.scalar_one()
    
    async def get_user_with_company(self, user_id: UUID) -> Optional[User]:
        """Get user with company relationship loaded."""
        result = await self.db.execute(
            select(User).options(
                sqlalchemy.orm.joinedload(User.company)
            ).filter(User.id == user_id)
        )
        return result.scalar_one_or_none()
