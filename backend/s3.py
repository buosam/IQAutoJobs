import os
import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError
import logging

s3_client = None

def get_s3_client():
    """
    Lazy initializes and returns the S3 client.
    This ensures that the client is created only when it's first needed,
    allowing the application to load environment variables from a .env file
    before the client is instantiated.
    """
    global s3_client
    if s3_client is None:
        try:
            s3_client = boto3.client(
                's3',
                endpoint_url=os.environ.get('R2_ENDPOINT'),
                aws_access_key_id=os.environ.get('R2_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('R2_SECRET_ACCESS_KEY'),
                config=Config(signature_version='s3v4')
            )
        except (BotoCoreError, ClientError) as e:
            logging.error(f"Error creating S3 client: {e}")
            return None
    return s3_client

def upload_to_s3(file, bucket_name, object_name):
    try:
        s3 = get_s3_client()
        if s3 is None:
            return None
        s3.upload_fileobj(file, bucket_name, object_name)
        return f"{os.environ.get('R2_ENDPOINT')}/{bucket_name}/{object_name}"
    except Exception as e:
        logging.error(f"Error uploading to S3: {e}")
        return None
