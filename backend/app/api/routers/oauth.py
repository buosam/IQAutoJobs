"""
OAuth router for Google authentication.
"""
import secrets
from typing import Optional
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from structlog import get_logger
import httpx

from app.db.base import get_db
from app.core.config import settings
from app.services.auth_service import AuthService
from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import RefreshTokenRepository
from app.repositories.audit_log_repo import AuditLogRepository
from app.core.errors import AuthenticationError

logger = get_logger()
router = APIRouter()

# Google OAuth URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# In-memory state storage (in production, use Redis or similar)
_oauth_states = {}


@router.get("/google/login")
async def google_login(
    returnTo: Optional[str] = Query(None, description="URL to redirect to after successful login")
):
    """Initiate Google OAuth flow."""
    if not settings.GOOGLE_OAUTH_CLIENT_ID or not settings.GOOGLE_OAUTH_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not configured. Please set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET."
        )
    
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = {"returnTo": returnTo}
    
    # Build authorization URL
    params = {
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "consent"
    }
    
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    logger.info("Redirecting to Google OAuth", state=state)
    
    return RedirectResponse(url=auth_url)


@router.get("/google/callback")
async def google_callback(
    code: str = Query(..., description="Authorization code from Google"),
    state: str = Query(..., description="State parameter for CSRF protection"),
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback."""
    # Verify state
    if state not in _oauth_states:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state parameter"
        )
    
    state_data = _oauth_states.pop(state)
    returnTo = state_data.get("returnTo") or "/dashboard"
    
    try:
        # Exchange code for access token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI,
                    "grant_type": "authorization_code"
                }
            )
            
            if token_response.status_code != 200:
                logger.error("Failed to get access token", response=token_response.text)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get access token from Google"
                )
            
            token_data = token_response.json()
            access_token = token_data.get("access_token")
            
            # Get user info from Google
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if userinfo_response.status_code != 200:
                logger.error("Failed to get user info", response=userinfo_response.text)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info from Google"
                )
            
            userinfo = userinfo_response.json()
    
    except httpx.HTTPError as e:
        logger.error("HTTP error during OAuth", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to communicate with Google"
        )
    
    # Extract user information
    google_id = userinfo.get("id")
    email = userinfo.get("email")
    first_name = userinfo.get("given_name", "")
    last_name = userinfo.get("family_name", "")
    
    if not google_id or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get user information from Google"
        )
    
    # Authenticate or create user
    user_repo = UserRepository(db)
    token_repo = RefreshTokenRepository(db)
    audit_repo = AuditLogRepository(db)
    auth_service = AuthService(db, user_repo, token_repo, audit_repo)
    
    try:
        # Use the oauth_login method from auth_service
        result = auth_service.oauth_login(
            provider="google",
            oauth_id=google_id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Redirect to frontend with tokens as query parameters
        # Frontend will set httpOnly cookies via Next.js API route
        redirect_params = urlencode({
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "returnTo": returnTo
        })
        
        # Redirect to frontend callback handler
        frontend_callback_url = f"/api/oauth/callback?{redirect_params}"
        
        logger.info("OAuth login successful", email=email, provider="google")
        return RedirectResponse(url=frontend_callback_url)
        
    except Exception as e:
        logger.error("OAuth login failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to authenticate user"
        )
