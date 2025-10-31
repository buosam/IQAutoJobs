"""
SQLAlchemy database models for IQAutoJobs.
"""
from datetime import datetime, timezone
from enum import Enum as PyEnum
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, ForeignKey, Integer, JSON, String, Text,
    UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class UserRole(PyEnum):
    """User roles."""
    ADMIN = "ADMIN"
    EMPLOYER = "EMPLOYER"
    CANDIDATE = "CANDIDATE"


class EmploymentType(PyEnum):
    """Employment types."""
    FT = "FT"  # Full-time
    PT = "PT"  # Part-time
    CONTRACT = "CONTRACT"
    INTERN = "INTERN"


class JobStatus(PyEnum):
    """Job statuses."""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"


class ApplicationStatus(PyEnum):
    """Application statuses."""
    RECEIVED = "RECEIVED"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEW = "INTERVIEW"
    REJECTED = "REJECTED"
    HIRED = "HIRED"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CANDIDATE)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    oauth_provider = Column(String(50), nullable=True)
    oauth_id = Column(String(255), nullable=True)
    
    # Profile fields
    bio = Column(Text, nullable=True)
    skills = Column(JSON, nullable=True)
    location = Column(String(255), nullable=True)
    headline = Column(String(255), nullable=True)
    resume_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="owner", uselist=False)
    applications = relationship("Application", back_populates="candidate")
    saved_jobs = relationship("SavedJob", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="actor")


class Company(Base):
    """Company model."""
    __tablename__ = "companies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    website = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    logo_key = Column(String(500), nullable=True)  # R2 key for logo
    industry = Column(String(100), nullable=True)
    size = Column(String(50), nullable=True)  # e.g., "1-10", "11-50", etc.
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="company")
    jobs = relationship("Job", back_populates="company")


class Job(Base):
    """Job model."""
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    type = Column(Enum(EmploymentType), nullable=False)
    category = Column(String(100), nullable=False)
    experience_level = Column(String(50), nullable=False)  # e.g., "Entry", "Mid", "Senior"
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    currency = Column(String(3), default="USD", nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.DRAFT, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    apply_email = Column(String(255), nullable=True)  # Optional email for applications
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
    
    # Unique constraint for slug per company
    __table_args__ = (
        UniqueConstraint('company_id', 'slug', name='uq_company_job_slug'),
    )


class Application(Base):
    """Application model."""
    __tablename__ = "applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    candidate_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    cv_key = Column(String(500), nullable=False)  # R2 key for CV
    cover_letter = Column(Text, nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.RECEIVED, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    candidate = relationship("User", back_populates="applications")


class SavedJob(Base):
    """Saved job model."""
    __tablename__ = "saved_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="saved_jobs")
    
    # Unique constraint for user-job combination
    __table_args__ = (
        UniqueConstraint('user_id', 'job_id', name='uq_user_saved_job'),
    )


class RefreshToken(Base):
    """Refresh token model."""
    __tablename__ = "refresh_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")


class AuditLog(Base):
    """Audit log model."""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    actor_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    subject_type = Column(String(100), nullable=False)
    subject_id = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    actor = relationship("User", back_populates="audit_logs")