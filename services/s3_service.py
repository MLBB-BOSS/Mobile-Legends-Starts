# services/s3_service.py

import logging
import os
from typing import Optional, Callable
import aioboto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(
        self, 
        notify_callback: Optional[Callable[[str], None]] = None, 
        aws_access_key_id: Optional[str] = None, 
        aws_secret_access_key: Optional[str] = None, 
        aws_region: Optional[str] = None
    ):
        """
        Ініціалізація S3 сервісу з використанням aioboto3 клієнта.

        Args:
            notify_callback (Optional[Callable[[str], None]]): Callback-функція для повідомлень.
            aws_access_key_id (Optional[str]): AWS Access Key ID.
            aws_secret_access_key (Optional[str]): AWS Secret Access Key.
            aws_region (Optional[str]): AWS Region.
        """
        self.logger = logger
        self.notify_callback = notify_callback
        self.aws_access_key_id = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = aws_region or os.getenv('AWS_REGION', 'us-east-1')  # Default region
        
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            self.logger.error("AWS credentials are not set.")
            raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set.")
        
        self.session = aioboto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )
        self.logger.info("Initialized S3Service with provided AWS credentials.")

    async def upload_file(self, file_path: str, bucket_name: str, object_name: Optional[str] = None) -> bool:
        """
        Завантаження файлу до S3.

        Args:
            file_path (str): Шлях до локального файлу.
            bucket_name (str): Назва S3 бакету.
            object_name (Optional[str]): Назва об'єкта в S3. Якщо не вказано, використовується ім'я файлу.

        Returns:
            bool: True якщо завантаження успішне, інакше False.
        """
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        try:
            async with self.session.client('s3') as s3_client:
                await s3_client.upload_file(file_path, bucket_name, object_name)
            self.logger.info(f"Successfully uploaded {file_path} to bucket {bucket_name} as {object_name}.")
            
            if self.notify_callback:
                await self.notify_callback(f"File {object_name} uploaded to {bucket_name}.")
            
            return True
        except (ClientError, BotoCoreError) as e:
            self.logger.error(f"Failed to upload {file_path} to bucket {bucket_name}: {e}")
            return False

    async def download_file(self, bucket_name: str, object_name: str, download_path: str) -> bool:
        """
        Завантаження файлу з S3.

        Args:
            bucket_name (str): Назва S3 бакету.
            object_name (str): Назва об'єкта в S3.
            download_path (str): Шлях для збереження завантаженого файлу.

        Returns:
            bool: True якщо завантаження успішне, інакше False.
        """
        try:
            async with self.session.client('s3') as s3_client:
                await s3_client.download_file(bucket_name, object_name, download_path)
            self.logger.info(f"Successfully downloaded {object_name} from bucket {bucket_name} to {download_path}.")
            return True
        except (ClientError, BotoCoreError) as e:
            self.logger.error(f"Failed to download {object_name} from bucket {bucket_name}: {e}")
            return False

    async def list_buckets(self) -> Optional[list]:
        """
        Отримання списку бакетів.

        Returns:
            Optional[list]: Список бакетів або None у випадку помилки.
        """
        try:
            async with self.session.client('s3') as s3_client:
                response = await s3_client.list_buckets()
            buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]
            self.logger.info(f"Retrieved bucket list: {buckets}")
            return buckets
        except (ClientError, BotoCoreError) as e:
            self.logger.error(f"Failed to list buckets: {e}")
            return None

    async def list_objects(self, bucket_name: str) -> Optional[list]:
        """
        Отримання списку об'єктів у бакеті.

        Args:
            bucket_name (str): Назва S3 бакету.

        Returns:
            Optional[list]: Список об'єктів або None у випадку помилки.
        """
        try:
            async with self.session.client('s3') as s3_client:
                response = await s3_client.list_objects_v2(Bucket=bucket_name)
            objects = [obj['Key'] for obj in response.get('Contents', [])]
            self.logger.info(f"Retrieved objects from bucket {bucket_name}: {objects}")
            return objects
        except (ClientError, BotoCoreError) as e:
            self.logger.error(f"Failed to list objects in bucket {bucket_name}: {e}")
            return None
