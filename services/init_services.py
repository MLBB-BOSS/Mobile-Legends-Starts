# services/init_services.py

from services.s3_service import S3Service

async def init_services(notify_callback: Optional[Callable[[str], None]] = None) -> dict:
    """
    Ініціалізація сервісів.

    Args:
        notify_callback (Optional[Callable[[str], None]]): Callback-функція для повідомлень.

    Returns:
        dict: Словник сервісів.
    """
    s3_service = S3Service(notify_callback=notify_callback)
    # Ініціалізуйте інші сервіси тут
    return {
        's3_service': s3_service,
        # Інші сервіси
    }
