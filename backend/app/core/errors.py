"""
Error handling utilities for IQAutoJobs.
"""
from typing import Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from structlog import get_logger

logger = get_logger()


class BaseHTTPException(HTTPException):
    """Base HTTP exception with custom error codes."""
    
    def __init__(
        self,
        status_code: int,
        error_code: str,
        detail: str,
        headers: Optional[dict] = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.headers = headers


class AuthenticationError(BaseHTTPException):
    """Authentication failed."""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTH_ERROR",
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(BaseHTTPException):
    """Authorization failed."""
    
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHZ_ERROR",
            detail=detail,
        )


class ValidationError(BaseHTTPException):
    """Validation error."""
    
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            detail=detail,
        )


class NotFoundError(BaseHTTPException):
    """Resource not found."""
    
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            detail=detail,
        )


class ConflictError(BaseHTTPException):
    """Resource conflict."""
    
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            detail=detail,
        )


class RateLimitError(BaseHTTPException):
    """Rate limit exceeded."""
    
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT",
            detail=detail,
        )


class FileUploadError(BaseHTTPException):
    """File upload error."""
    
    def __init__(self, detail: str = "File upload failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="FILE_UPLOAD_ERROR",
            detail=detail,
        )


async def base_exception_handler(request: Request, exc: BaseHTTPException):
    """Handle custom HTTP exceptions."""
    logger.error(
        "HTTP exception",
        error_code=exc.error_code,
        detail=exc.detail,
        status_code=exc.status_code,
        url=str(request.url),
        method=request.method,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
            }
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle FastAPI validation exceptions."""
    logger.error(
        "Validation error",
        errors=exc.errors(),
        url=str(request.url),
        method=request.method,
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": exc.errors(),
            }
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions."""
    logger.error(
        "HTTP exception",
        detail=exc.detail,
        status_code=exc.status_code,
        url=str(request.url),
        method=request.method,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
            }
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        error_type=type(exc).__name__,
        url=str(request.url),
        method=request.method,
        exc_info=True,
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error",
            }
        },
    )