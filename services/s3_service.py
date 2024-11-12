# services/s3_service.py
import os
import boto3
import logging
from typing import Optional, Dict, Any, BinaryIO
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        """
        Ініціалізація сервісу S3 з змінних середовища Heroku
        Необхідні змінні:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION
        - AWS_S3_BUCKET_NAME
        """
        self.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region = os.environ.get('AWS_REGION', 'eu-central-1')
        self.bucket_name = os.environ.get('AWS_S3_BUCKET_NAME')

        if not all([self.aws_access_key_id, self.aws_secret_access_key, self.bucket_name]):
            raise ValueError("Missing required AWS credentials in environment variables")

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region
        )

    async def upload_file(self, 
                         file_data: bytes,
                         file_key: str,
                         metadata: Dict[str, str] = None,
                         content_type: str = 'image/jpeg') -> Optional[str]:
        """
        Завантаження файлу в S3
        
        Args:
            file_data: Байти файлу
            file_key: Ключ файлу в S3 (шлях/назва)
            metadata: Метадані файлу
            content_type: Тип контенту файлу
            
        Returns:
            URL завантаженого файлу або None у випадку помилки
        """
        try:
            # Додаємо базові метадані
            full_metadata = {
                'uploaded_at': datetime.utcnow().isoformat(),
                'uploaded_by': 'mlbb-bot'
            }
            if metadata:
                full_metadata.update(metadata)

            # Завантаження файлу
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_data,
                ContentType=content_type,
                Metadata=full_metadata
            )

            # Формуємо URL файлу
            url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_key}"
            logger.info(f"File uploaded successfully to {url}")
            return url

        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            return None

    async def delete_file(self, file_key: str) -> bool:
        """
        Видалення файлу з S3
        
        Args:
            file_key: Ключ файлу в S3
            
        Returns:
            True якщо файл успішно видалено, False у випадку помилки
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            logger.info(f"File {file_key} deleted successfully")
            return True
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False

    async def get_file_url(self, file_key: str, expires_in: int = 3600) -> Optional[str]:
        """
        Отримання тимчасового URL для файлу
        
        Args:
            file_key: Ключ файлу в S3
            expires_in: Час дії URL в секундах (за замовчуванням 1 година)
            
        Returns:
            Тимчасовий URL або None у випадку помилки
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_key
                },
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None

    async def check_file_exists(self, file_key: str) -> bool:
        """
        Перевірка існування файлу в S3
        
        Args:
            file_key: Ключ файлу в S3
            
        Returns:
            True якщо файл існує, False якщо ні або виникла помилка
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            return True
        except ClientError:
            return False
