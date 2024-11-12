# services/__init__.py
from .base_service import BaseService
from .s3_service import S3Service
from .hero_service import HeroService
from .user_service import UserService
from .achievement_service import AchievementService

__all__ = [
    'BaseService',
    'S3Service',
    'HeroService',
    'UserService',
    'AchievementService'
]

# Версія пакету сервісів
__version__ = '1.0.0'

# Налаштування логування для всіх сервісів
import logging

# Створюємо форматтер для логів
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Створюємо обробник для виводу в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Встановлюємо рівень логування
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Функція для ініціалізації всіх необхідних сервісів
async def init_services(session, s3_client=None):
    """
    Ініціалізація всіх сервісів додатку
    
    Args:
        session: AsyncSession для роботи з базою даних
        s3_client: Опціональний клієнт S3 для роботи з файлами
    
    Returns:
        Dict[str, Any]: Словник з ініціалізованими сервісами
    """
    try:
        # Ініціалізуємо S3 сервіс
        s3_service = S3Service() if not s3_client else s3_client
        
        # Ініціалізуємо інші сервіси
        hero_service = HeroService(session, s3_service)
        user_service = UserService(session)
        achievement_service = AchievementService(session)
        
        return {
            's3_service': s3_service,
            'hero_service': hero_service,
            'user_service': user_service,
            'achievement_service': achievement_service
        }
    except Exception as e:
        logger.error(f"Error initializing services: {e}")
        raise

# Функція для перевірки здоров'я сервісів
async def check_services_health(services):
    """
    Перевірка стану всіх сервісів
    
    Args:
        services: Dict[str, Any] словник сервісів
    
    Returns:
        Dict[str, bool]: Статус кожного сервісу
    """
    health_status = {}
    
    try:
        # Перевіряємо S3
        try:
            # Тестовий виклик до S3
            await services['s3_service'].check_file_exists('test_health_check')
            health_status['s3_service'] = True
        except Exception as e:
            logger.error(f"S3 service health check failed: {e}")
            health_status['s3_service'] = False
        
        # Перевіряємо інші сервіси через прості запити
        for service_name in ['hero_service', 'user_service', 'achievement_service']:
            try:
                service = services[service_name]
                # Перевіряємо з'єднання з базою даних
                await service._session.execute("SELECT 1")
                health_status[service_name] = True
            except Exception as e:
                logger.error(f"{service_name} health check failed: {e}")
                health_status[service_name] = False
        
        return health_status
    except Exception as e:
        logger.error(f"Error checking services health: {e}")
        return {service: False for service in services}

# Константи для конфігурації сервісів
class ServiceConfig:
    """Конфігураційні константи для сервісів"""
    
    # Загальні налаштування
    MAX_RETRIES = 3
    TIMEOUT = 30  # секунд
    
    # Налаштування для роботи з файлами
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_CONTENT_TYPES = [
        'image/jpeg',
        'image/png',
        'image/gif'
    ]
    
    # Налаштування кешування
    CACHE_TTL = 3600  # 1 година
    
    # Налаштування досягнень
    ACHIEVEMENT_POINTS = {
        'First Hero': 10,
        'Hero Collector': 50,
        'Hero Master': 100,
        'Hero Legend': 200,
        'Popular Contributor': 20,
        'Community Favorite': 100,
        'Content Star': 200,
        'Legend Creator': 500,
        'Active Contributor': 30,
        'Dedicated Contributor': 150,
        'Elite Contributor': 300,
        'Legendary Contributor': 1000
    }
