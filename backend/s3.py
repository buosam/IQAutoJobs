import os
import boto3
from botocore.client import Config

s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get('R2_ENDPOINT'),
    aws_access_key_id=os.environ.get('R2_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('R2_SECRET_ACCESS_KEY'),
    config=Config(signature_version='s3v4')
)

def upload_to_s3(file, bucket_name, object_name):
    try:
        s3.upload_fileobj(file, bucket_name, object_name)
        return f"{os.environ.get('R2_ENDPOINT')}/{bucket_name}/{object_name}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None
