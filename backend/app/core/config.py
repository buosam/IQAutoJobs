"""
Configuration management for IQAutoJobs.
"""
from typing import List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    PROJECT_NAME: str = "IQAutoJobs"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # R2/S3 Storage
    R2_ACCOUNT_ID: str = Field(..., env="R2_ACCOUNT_ID")
    R2_ACCESS_KEY_ID: str = Field(..., env="R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY: str = Field(..., env="R2_SECRET_ACCESS_KEY")
    R2_BUCKET: str = Field(..., env="R2_BUCKET")
    R2_PUBLIC_BASE: str = Field(..., env="R2_PUBLIC_BASE")
    
    # CORS
    ALLOWED_HOSTS: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")
    
    # File upload settings
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
        env="ALLOWED_FILE_TYPES"
    )
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # seconds

    # Email
    EMAIL_PROVIDER: str
    EMAIL_API_KEY: str
    EMAIL_FROM_ADDRESS: str
    EMAIL_FROM_NAME: str
    RESEND_API_BASE_URL: str = Field(default="https://api.resend.com/emails", env="RESEND_API_BASE_URL")

    # URLs
    BACKEND_URL: str
    NEXT_PUBLIC_API_URL: str
    
    # Google OAuth
    GOOGLE_OAUTH_CLIENT_ID: str = Field(default="", env="GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET: str = Field(default="", env="GOOGLE_OAUTH_CLIENT_SECRET")
    GOOGLE_OAUTH_REDIRECT_URI: str = Field(default="", env="GOOGLE_OAUTH_REDIRECT_URI")
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("ALLOWED_FILE_TYPES", pre=True)
    def parse_allowed_file_types(cls, v):
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
