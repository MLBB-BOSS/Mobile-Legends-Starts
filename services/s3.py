# services/s3.py

import boto3
import logging
from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_S3_BUCKET_NAME
)

logger = logging.getLogger(__name__)

# Створення клієнта S3
s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_file_to_s3(file_path, object_name):
    try:
        # Завантаження файлу до S3 bucket
        response = s3_client.put_object(
            Bucket=AWS_S3_BUCKET_NAME,
            Key=object_name,
            Body=open(file_path, 'rb')
        )
        logger.info(f"Uploaded {file_path} to S3 Bucket {AWS_S3_BUCKET_NAME} as {object_name}")
        # Генерація URL для доступу до файлу
        s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
        return s3_url
    except Exception as e:
        logger.error(f"Failed to upload {file_path} to S3: {e}")
        return None