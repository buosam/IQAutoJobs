"""
Refresh token repository for IQAutoJobs.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Refresh token repository with token-specific operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(RefreshToken, db)
    
    async def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Get refresh token by hash."""
        result = await self.db.execute(
            select(RefreshToken).filter(RefreshToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()
    
    async def get_by_user(self, user_id: UUID) -> List[RefreshToken]:
        """Get all refresh tokens for a user."""
        result = await self.db.execute(
            select(RefreshToken).filter(RefreshToken.user_id == user_id)
        )
        return result.scalars().all()
    
    async def get_active_tokens_by_user(self, user_id: UUID) -> List[RefreshToken]:
        """Get active refresh tokens for a user."""
        result = await self.db.execute(
            select(RefreshToken).filter(
                and_(
                    RefreshToken.user_id == user_id,
                    RefreshToken.revoked == False,
                    RefreshToken.expires_at > datetime.utcnow()
                )
            )
        )
        return result.scalars().all()
    
    async def create_token(self, user_id: UUID, token_hash: str, expires_at: datetime) -> RefreshToken:
        """Create a new refresh token."""
        token_data = {
            "user_id": user_id,
            "token_hash": token_hash,
            "expires_at": expires_at,
            "revoked": False
        }
        return await self.create(token_data)
    
    async def revoke_token(self, token_id: UUID) -> Optional[RefreshToken]:
        """Revoke a refresh token."""
        token = await self.get(token_id)
        if token:
            token.revoked = True
            await self.db.commit()
            await self.db.refresh(token)
        return token
    
    async def revoke_all_user_tokens(self, user_id: UUID) -> int:
        """Revoke all refresh tokens for a user."""
        result = await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .values(revoked=True)
        )
        await self.db.commit()
        return result.rowcount
    
    async def revoke_all_active_user_tokens(self, user_id: UUID) -> int:
        """Revoke all active refresh tokens for a user."""
        result = await self.db.execute(
            update(RefreshToken)
            .where(
                and_(
                    RefreshToken.user_id == user_id,
                    RefreshToken.revoked == False,
                    RefreshToken.expires_at > datetime.utcnow()
                )
            )
            .values(revoked=True)
        )
        await self.db.commit()
        return result.rowcount
    
    async def cleanup_expired_tokens(self) -> int:
        """Remove expired tokens."""
        result = await self.db.execute(
            delete(RefreshToken).where(RefreshToken.expires_at <= datetime.utcnow())
        )
        await self.db.commit()
        return result.rowcount
    
    async def cleanup_revoked_tokens(self) -> int:
        """Remove revoked tokens that are also expired."""
        result = await self.db.execute(
            delete(RefreshToken).where(
                and_(
                    RefreshToken.revoked == True,
                    RefreshToken.expires_at <= datetime.utcnow()
                )
            )
        )
        await self.db.commit()
        return result.rowcount
