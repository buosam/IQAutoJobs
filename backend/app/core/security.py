"""
Security utilities for IQAutoJobs.
"""
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from uuid import uuid4

from app.core.config import settings
from app.core import executors

# Password context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def _verify_password_sync(plain_password: str, hashed_password: str) -> bool:
    """Synchronous password verification for process pool."""
    return pwd_context.verify(plain_password, hashed_password)

def _get_password_hash_sync(password: str) -> str:
    """Synchronous password hashing for process pool."""
    return pwd_context.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash in a separate process."""
    if not executors.executor:
        raise RuntimeError("ProcessPoolExecutor is not initialized.")
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        executors.executor, _verify_password_sync, plain_password, hashed_password
    )

async def get_password_hash(password: str) -> str:
    """Generate password hash in a separate process."""
    if not executors.executor:
        raise RuntimeError("ProcessPoolExecutor is not initialized.")
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        executors.executor, _get_password_hash_sync, password
    )


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    user_id: Union[str, int]
) -> tuple[str, datetime]:
    """Create JWT refresh token and its expiration."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid4())  # JWT ID for token revocation
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt, expire


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        if payload.get("type") != token_type:
            return None
            
        return payload
    except JWTError:
        return None


def create_password_reset_token(email: str) -> str:
    """Create password reset token."""
    expire = datetime.now(timezone.utc) + timedelta(hours=1)  # 1 hour expiry
    
    to_encode = {
        "sub": email,
        "exp": expire,
        "type": "reset"
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify password reset token and return email."""
    payload = verify_token(token, "reset")
    if payload:
        return payload.get("sub")
    return None