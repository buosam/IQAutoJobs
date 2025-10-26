"""
Domain models for IQAutoJobs.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, HttpUrl


class UserRole(str, Enum):
    """User roles."""
    ADMIN = "ADMIN"
    EMPLOYER = "EMPLOYER"
    CANDIDATE = "CANDIDATE"


class EmploymentType(str, Enum):
    """Employment types."""
    FT = "FT"  # Full-time
    PT = "PT"  # Part-time
    CONTRACT = "CONTRACT"
    INTERN = "INTERN"


class JobStatus(str, Enum):
    """Job statuses."""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"


class ApplicationStatus(str, Enum):
    """Application statuses."""
    RECEIVED = "RECEIVED"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEW = "INTERVIEW"
    REJECTED = "REJECTED"
    HIRED = "HIRED"


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole = UserRole.CANDIDATE
    is_active: bool = True


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update model."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    """User response model."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data model."""
    sub: Optional[str] = None
    type: Optional[str] = None


class CompanyBase(BaseModel):
    """Base company model."""
    name: str = Field(..., min_length=2, max_length=255)
    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None


class CompanyCreate(CompanyBase):
    """Company creation model."""
    pass


class CompanyUpdate(BaseModel):
    """Company update model."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None


class CompanyResponse(CompanyBase):
    """Company response model."""
    id: UUID
    slug: str
    logo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner: UserResponse
    
    class Config:
        from_attributes = True


class JobBase(BaseModel):
    """Base job model."""
    title: str = Field(..., min_length=2, max_length=255)
    description: str = Field(..., min_length=10)
    location: str = Field(..., min_length=2, max_length=255)
    type: EmploymentType
    category: str = Field(..., min_length=2, max_length=100)
    experience_level: str = Field(..., min_length=2, max_length=50)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    currency: str = "USD"
    apply_email: Optional[EmailStr] = None


class JobCreate(JobBase):
    """Job creation model."""
    pass


class JobUpdate(BaseModel):
    """Job update model."""
    title: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    location: Optional[str] = Field(None, min_length=2, max_length=255)
    type: Optional[EmploymentType] = None
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    experience_level: Optional[str] = Field(None, min_length=2, max_length=50)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    currency: Optional[str] = None
    apply_email: Optional[EmailStr] = None
    status: Optional[JobStatus] = None


class JobResponse(JobBase):
    """Job response model."""
    id: UUID
    slug: str
    status: JobStatus
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    company: CompanyResponse
    
    class Config:
        from_attributes = True


class ApplicationBase(BaseModel):
    """Base application model."""
    cover_letter: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    """Application creation model."""
    job_id: UUID


class ApplicationUpdate(BaseModel):
    """Application update model."""
    status: ApplicationStatus


class ApplicationResponse(ApplicationBase):
    """Application response model."""
    id: UUID
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
    job: JobResponse
    candidate: UserResponse
    cv_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class SavedJobBase(BaseModel):
    """Base saved job model."""
    pass


class SavedJobCreate(SavedJobBase):
    """Saved job creation model."""
    job_id: UUID


class SavedJobResponse(SavedJobBase):
    """Saved job response model."""
    id: UUID
    created_at: datetime
    job: JobResponse
    
    class Config:
        from_attributes = True


class FileUpload(BaseModel):
    """File upload model."""
    filename: str
    content_type: str
    size: int


class FileResponse(BaseModel):
    """File response model."""
    id: str
    filename: str
    url: str
    size: int
    content_type: str
    created_at: datetime


class JobSearchFilters(BaseModel):
    """Job search filters."""
    search: Optional[str] = None
    location: Optional[str] = None
    type: Optional[EmploymentType] = None
    category: Optional[str] = None
    experience_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    company_id: Optional[UUID] = None
    status: JobStatus = JobStatus.PUBLISHED


class JobSearchResponse(BaseModel):
    """Job search response."""
    jobs: List[JobResponse]
    total: int
    page: int
    size: int
    pages: int


class PasswordResetRequest(BaseModel):
    """Password reset request model."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Password reset model."""
    token: str
    new_password: str = Field(..., min_length=8)


class PasswordChange(BaseModel):
    """Password change model."""
    current_password: str
    new_password: str = Field(..., min_length=8)


class AuditLogResponse(BaseModel):
    """Audit log response model."""
    id: UUID
    action: str
    subject_type: str
    subject_id: str
    payload: Optional[dict] = None
    created_at: datetime
    actor: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True