"""
Refresh token repository for IQAutoJobs.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Refresh token repository with token-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(RefreshToken, db)
    
    def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Get refresh token by hash."""
        return self.db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash
        ).first()
    
    def get_by_user(self, user_id: UUID) -> List[RefreshToken]:
        """Get all refresh tokens for a user."""
        return self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id
        ).all()
    
    def get_active_tokens_by_user(self, user_id: UUID) -> List[RefreshToken]:
        """Get active refresh tokens for a user."""
        return self.db.query(RefreshToken).filter(
            and_(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False,
                RefreshToken.expires_at > datetime.utcnow()
            )
        ).all()
    
    def create_token(self, user_id: UUID, token_hash: str, expires_at: datetime) -> RefreshToken:
        """Create a new refresh token."""
        token_data = {
            "user_id": user_id,
            "token_hash": token_hash,
            "expires_at": expires_at,
            "revoked": False
        }
        return self.create(token_data)
    
    def revoke_token(self, token_id: UUID) -> Optional[RefreshToken]:
        """Revoke a refresh token."""
        token = self.get(token_id)
        if token:
            token.revoked = True
            self.db.commit()
            self.db.refresh(token)
        return token
    
    def revoke_all_user_tokens(self, user_id: UUID) -> int:
        """Revoke all refresh tokens for a user."""
        count = self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id
        ).update({"revoked": True})
        self.db.commit()
        return count
    
    def revoke_all_active_user_tokens(self, user_id: UUID) -> int:
        """Revoke all active refresh tokens for a user."""
        count = self.db.query(RefreshToken).filter(
            and_(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False,
                RefreshToken.expires_at > datetime.utcnow()
            )
        ).update({"revoked": True})
        self.db.commit()
        return count
    
    def is_token_valid(self, token_hash: str) -> bool:
        """Check if refresh token is valid."""
        token = self.get_by_token_hash(token_hash)
        if not token:
            return False
        
        return (
            not token.revoked and
            token.expires_at > datetime.utcnow()
        )
    
    def cleanup_expired_tokens(self) -> int:
        """Remove expired tokens."""
        count = self.db.query(RefreshToken).filter(
            RefreshToken.expires_at <= datetime.utcnow()
        ).delete()
        self.db.commit()
        return count
    
    def cleanup_revoked_tokens(self) -> int:
        """Remove revoked tokens that are also expired."""
        count = self.db.query(RefreshToken).filter(
            and_(
                RefreshToken.revoked == True,
                RefreshToken.expires_at <= datetime.utcnow()
            )
        ).delete()
        self.db.commit()
        return count