"""
Rate limiting utilities for IQAutoJobs.
"""
import time
from collections import defaultdict
from typing import Dict, List, Optional
from fastapi import Request, HTTPException, status
from structlog import get_logger

from app.core.config import settings
from app.core.errors import RateLimitError

logger = get_logger()


class RateLimiter:
    """Simple in-memory rate limiter using token bucket algorithm."""
    
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        self.buckets: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        
        # Remove old timestamps
        bucket = self.buckets[key]
        bucket[:] = [timestamp for timestamp in bucket if timestamp > now - self.window]
        
        # Check if bucket has capacity
        if len(bucket) < self.requests:
            bucket.append(now)
            return True
        
        return False
    
    def get_remaining(self, key: str) -> int:
        """Get remaining requests for key."""
        now = time.time()
        bucket = self.buckets[key]
        bucket[:] = [timestamp for timestamp in bucket if timestamp > now - self.window]
        return max(0, self.requests - len(bucket))


# Global rate limiter instance
rate_limiter = RateLimiter(
    requests=settings.RATE_LIMIT_REQUESTS,
    window=settings.RATE_LIMIT_WINDOW
)


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware."""
    # Get client identifier
    client_ip = request.client.host if request.client else "unknown"
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    
    # Check rate limit
    if not rate_limiter.is_allowed(client_ip):
        remaining = rate_limiter.get_remaining(client_ip)
        logger.warning(
            "Rate limit exceeded",
            client_ip=client_ip,
            remaining=remaining,
            url=str(request.url),
            method=request.method,
        )
        
        raise RateLimitError(
            f"Rate limit exceeded. {remaining} requests remaining."
        )
    
    # Add rate limit headers
    response = await call_next(request)
    remaining = rate_limiter.get_remaining(client_ip)
    response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(int(time.time()) + settings.RATE_LIMIT_WINDOW)
    
    return response


def create_rate_limiter(requests: int, window: int):
    """Create a rate limiter with custom settings."""
    return RateLimiter(requests=requests, window=window)