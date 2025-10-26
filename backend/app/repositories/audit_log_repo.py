"""
Audit log repository for IQAutoJobs.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_
import sqlalchemy.orm

from app.db.models import AuditLog
from app.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    """Audit log repository with audit log-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(AuditLog, db)
    
    def get_by_actor(self, actor_user_id: UUID, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by actor."""
        return self.db.query(AuditLog).filter(
            AuditLog.actor_user_id == actor_user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_action(self, action: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by action."""
        return self.db.query(AuditLog).filter(
            AuditLog.action == action
        ).offset(skip).limit(limit).all()
    
    def get_by_subject_type(self, subject_type: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by subject type."""
        return self.db.query(AuditLog).filter(
            AuditLog.subject_type == subject_type
        ).offset(skip).limit(limit).all()
    
    def get_by_subject_id(self, subject_id: str, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by subject ID."""
        return self.db.query(AuditLog).filter(
            AuditLog.subject_id == subject_id
        ).offset(skip).limit(limit).all()
    
    def get_audit_logs_with_actor(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs with actor relationship loaded."""
        return self.db.query(AuditLog).options(
            sqlalchemy.orm.joinedload(AuditLog.actor)
        ).offset(skip).limit(limit).all()
    
    def search_audit_logs(
        self,
        actor_user_id: Optional[UUID] = None,
        action: Optional[str] = None,
        subject_type: Optional[str] = None,
        subject_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Search audit logs with filters."""
        query = self.db.query(AuditLog)
        
        if actor_user_id:
            query = query.filter(AuditLog.actor_user_id == actor_user_id)
        
        if action:
            query = query.filter(AuditLog.action == action)
        
        if subject_type:
            query = query.filter(AuditLog.subject_type == subject_type)
        
        if subject_id:
            query = query.filter(AuditLog.subject_id == subject_id)
        
        return query.offset(skip).limit(limit).all()
    
    def create_audit_log(
        self,
        action: str,
        subject_type: str,
        subject_id: str,
        actor_user_id: Optional[UUID] = None,
        payload: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Create an audit log entry."""
        audit_log_data = {
            "action": action,
            "subject_type": subject_type,
            "subject_id": subject_id,
            "actor_user_id": actor_user_id,
            "payload": payload
        }
        return self.create(audit_log_data)
    
    def log_user_action(
        self,
        action: str,
        user_id: UUID,
        subject_type: str,
        subject_id: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Log a user action."""
        return self.create_audit_log(
            action=action,
            subject_type=subject_type,
            subject_id=subject_id,
            actor_user_id=user_id,
            payload=payload
        )
    
    def get_recent_audit_logs(self, limit: int = 50) -> List[AuditLog]:
        """Get recent audit logs."""
        return self.db.query(AuditLog).order_by(
            AuditLog.created_at.desc()
        ).limit(limit).all()
    
    def get_audit_logs_for_period(
        self,
        start_date: str,
        end_date: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get audit logs for a specific period."""
        return self.db.query(AuditLog).filter(
            and_(
                AuditLog.created_at >= start_date,
                AuditLog.created_at <= end_date
            )
        ).offset(skip).limit(limit).all()