"""
Files router for IQAutoJobs.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from structlog import get_logger

from app.db.base import get_db
from app.services.file_service import FileService
from app.api.routers.auth import get_current_user
from app.core.errors import FileUploadError

logger = get_logger()
router = APIRouter()


@router.post("/cv")
async def upload_cv(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload CV file."""
    file_service = FileService()
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")
        
        # Read file content
        file_content = await file.read()
        
        # Prepare file data
        file_data = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
            "content": file_content
        }
        
        # Upload file to R2
        cv_key = file_service.upload_cv(file_data, str(current_user.id))
        
        # Get public URL
        cv_url = file_service.get_public_url(cv_key)
        
        return {
            "cv_key": cv_key,
            "cv_url": cv_url,
            "filename": file.filename,
            "size": len(file_content),
            "content_type": file.content_type
        }
    
    except FileUploadError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("CV upload failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="CV upload failed")


@router.get("/cv/{file_key}")
async def get_cv_url(
    file_key: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get CV download URL."""
    file_service = FileService()
    
    try:
        # Generate signed URL
        cv_url = file_service.get_file_url(file_key, expires_in=3600)  # 1 hour
        
        return {"url": cv_url, "file_key": file_key}
    
    except FileUploadError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("CV URL generation failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate CV URL")


@router.delete("/cv/{file_key}")
async def delete_cv(
    file_key: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete CV file."""
    file_service = FileService()
    
    try:
        # Check if file exists and belongs to user
        if not file_service.file_exists(file_key):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        
        # Check if file belongs to user (basic check by key pattern)
        if str(current_user.id) not in file_key:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this file")
        
        # Delete file
        file_service.delete_file(file_key)
        
        return {"message": "CV deleted successfully"}
    
    except FileUploadError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("CV deletion failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="CV deletion failed")


@router.get("/cv/{file_key}/info")
async def get_cv_info(
    file_key: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get CV file information."""
    file_service = FileService()
    
    try:
        # Get file info
        file_info = file_service.get_file_info(file_key)
        
        if not file_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        
        # Check if file belongs to user (basic check by key pattern)
        if str(current_user.id) not in file_key:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this file")
        
        return {
            "file_key": file_key,
            "size": file_info["size"],
            "content_type": file_info["content_type"],
            "last_modified": file_info["last_modified"]
        }
    
    except FileUploadError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("CV info retrieval failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get CV info")