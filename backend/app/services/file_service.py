"""
File service for IQAutoJobs - handles R2/S3 operations.
"""
import os
import uuid
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from structlog import get_logger

from app.core.config import settings
from app.core.errors import FileUploadError

logger = get_logger()


class FileService:
    """File service for R2/S3 operations."""
    
    def __init__(self):
        self.bucket_name = settings.R2_BUCKET
        self.account_id = settings.R2_ACCOUNT_ID
        self.access_key_id = settings.R2_ACCESS_KEY_ID
        self.secret_access_key = settings.R2_SECRET_ACCESS_KEY
        self.public_base = settings.R2_PUBLIC_BASE
        self.max_file_size = settings.MAX_FILE_SIZE
        self.allowed_file_types = settings.ALLOWED_FILE_TYPES
        
        # Initialize S3 client
        self.s3_client = self._create_s3_client()
    
    def _create_s3_client(self):
        """Create S3 client for R2."""
        try:
            return boto3.client(
                's3',
                endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name='auto'
            )
        except Exception as e:
            logger.error("Failed to create S3 client", error=str(e))
            raise FileUploadError("Failed to initialize file storage service")
    
    def generate_file_key(self, user_id: str, file_type: str = "cv") -> str:
        """Generate unique file key for storage."""
        unique_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        return f"{file_type}/{user_id}/{timestamp}/{unique_id}"
    
    def validate_file(self, file_data: Dict[str, Any]) -> bool:
        """Validate file before upload."""
        # Check file size
        if file_data["size"] > self.max_file_size:
            raise FileUploadError(f"File size exceeds maximum limit of {self.max_file_size} bytes")
        
        # Check file type
        if file_data["content_type"] not in self.allowed_file_types:
            raise FileUploadError(f"File type {file_data['content_type']} is not allowed")
        
        return True
    
    def upload_file(self, file_data: Dict[str, Any], user_id: str) -> str:
        """Upload file to R2/S3."""
        try:
            # Validate file
            self.validate_file(file_data)
            
            # Generate file key
            file_key = self.generate_file_key(user_id, "cv")
            
            # Upload file
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_data["content"],
                ContentType=file_data["content_type"]
            )
            
            logger.info("File uploaded successfully", file_key=file_key, size=file_data["size"])
            
            return file_key
        
        except ClientError as e:
            logger.error("Failed to upload file", error=str(e))
            raise FileUploadError("Failed to upload file")
        except Exception as e:
            logger.error("Unexpected error during file upload", error=str(e))
            raise FileUploadError("Failed to upload file")
    
    def upload_cv(self, file_data: Dict[str, Any], user_id: str) -> str:
        """Upload CV file to R2/S3."""
        return self.upload_file(file_data, user_id)
    
    def upload_company_logo(self, file_data: Dict[str, Any], company_id: str) -> str:
        """Upload company logo to R2/S3."""
        try:
            # Validate file (logo files have different requirements)
            if file_data["size"] > 2 * 1024 * 1024:  # 2MB limit for logos
                raise FileUploadError("Logo file size exceeds maximum limit of 2MB")
            
            # Generate file key
            file_key = f"logo/{company_id}/{uuid.uuid4()}"
            
            # Upload file
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_data["content"],
                ContentType=file_data["content_type"]
            )
            
            logger.info("Company logo uploaded successfully", file_key=file_key)
            
            return file_key
        
        except ClientError as e:
            logger.error("Failed to upload company logo", error=str(e))
            raise FileUploadError("Failed to upload company logo")
        except Exception as e:
            logger.error("Unexpected error during logo upload", error=str(e))
            raise FileUploadError("Failed to upload company logo")
    
    def get_file_url(self, file_key: str, expires_in: int = 3600) -> str:
        """Generate signed URL for file download."""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            logger.error("Failed to generate file URL", error=str(e))
            raise FileUploadError("Failed to generate file URL")
    
    def get_public_url(self, file_key: str) -> str:
        """Get public URL for file."""
        return f"{self.public_base}/{file_key}"
    
    def delete_file(self, file_key: str) -> bool:
        """Delete file from R2/S3."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)
            logger.info("File deleted successfully", file_key=file_key)
            return True
        except ClientError as e:
            logger.error("Failed to delete file", error=str(e))
            raise FileUploadError("Failed to delete file")
    
    def file_exists(self, file_key: str) -> bool:
        """Check if file exists in R2/S3."""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            logger.error("Failed to check file existence", error=str(e))
            raise FileUploadError("Failed to check file existence")
    
    def get_file_info(self, file_key: str) -> Optional[Dict[str, Any]]:
        """Get file information from R2/S3."""
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            return {
                "size": response["ContentLength"],
                "content_type": response["ContentType"],
                "last_modified": response["LastModified"]
            }
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None
            logger.error("Failed to get file info", error=str(e))
            raise FileUploadError("Failed to get file information")
    
    def list_files(self, prefix: str = "", max_keys: int = 1000) -> List[Dict[str, Any]]:
        """List files in R2/S3 bucket with prefix."""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            files = []
            for obj in response.get("Contents", []):
                files.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"]
                })
            
            return files
        except ClientError as e:
            logger.error("Failed to list files", error=str(e))
            raise FileUploadError("Failed to list files")
    
    def cleanup_old_files(self, prefix: str, days_old: int = 30) -> int:
        """Clean up files older than specified days."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            files = self.list_files(prefix)
            
            deleted_count = 0
            for file_info in files:
                if file_info["last_modified"] < cutoff_date:
                    self.delete_file(file_info["key"])
                    deleted_count += 1
            
            logger.info("Cleaned up old files", prefix=prefix, deleted_count=deleted_count)
            return deleted_count
        
        except Exception as e:
            logger.error("Failed to cleanup old files", error=str(e))
            raise FileUploadError("Failed to cleanup old files")