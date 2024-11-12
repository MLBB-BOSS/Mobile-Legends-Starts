# core/__init__.py
import logging
from typing import Dict, Any
from datetime import datetime

# Версія ядра
__version__ = '1.0.0'

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CoreConfig:
    """Базова конфігурація ядра додатку"""
    
    # Загальні налаштування
    APP_NAME = "MLBB-BOSS"
    VERSION = __version__
    DESCRIPTION = """
    MLBB-BOSS Telegram Bot – інструмент для організації та підтримки
    турнірів у грі Mobile Legends.
    """
    
    # Налаштування бази даних
    DATABASE_URL = "postgresql+asyncpg://user:password@localhost/mlbb_boss"
    
    # Налаштування Redis для кешування
    REDIS_URL = "redis://localhost"
    
    # Налаштування S3
    S3_BUCKET = "mlbb-boss-media"
    S3_REGION = "eu-central-1"
    
    # Налаштування додатку
    DEBUG = False
    MAINTENANCE_MODE = False
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Конвертує конфігурацію в словник"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('__') and not callable(value)
        }

class AppState:
    """Клас для зберігання стану додатку"""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.is_ready = False
        self.active_users = 0
        self.processed_commands = 0
        self._services = {}
        
    @property
    def uptime(self) -> str:
        """Повертає час роботи додатку"""
        delta = datetime.utcnow() - self.start_time
        return str(delta).split('.')[0]
    
    def register_service(self, name: str, service: Any) -> None:
        """Реєструє сервіс в додатку"""
        self._services[name] = service
        logger.info(f"Registered service: {name}")
    
    def get_service(self, name: str) -> Any:
        """Отримує сервіс за назвою"""
        return self._services.get(name)
    
    def increment_processed_commands(self) -> None:
        """Збільшує лічильник оброблених команд"""
        self.processed_commands += 1
    
    def update_active_users(self, count: int) -> None:
        """Оновлює кількість активних користувачів"""
        self.active_users = count
    
    def get_stats(self) -> Dict[str, Any]:
        """Повертає статистику додатку"""
        return {
            'uptime': self.uptime,
            'active_users': self.active_users,
            'processed_commands': self.processed_commands,
            'is_ready': self.is_ready,
            'registered_services': list(self._services.keys())
        }

# Глобальний стан додатку
app_state = AppState()

async def initialize_core(config: Dict[str, Any] = None) -> None:
    """
    Ініціалізація ядра додатку
    
    Args:
        config: Додаткові налаштування
    """
    try:
        logger.info("Initializing core...")
        
        # Оновлюємо конфігурацію якщо передано
        if config:
            for key, value in config.items():
                if hasattr(CoreConfig, key):
                    setattr(CoreConfig, key, value)
        
        # Тут можна додати додаткову ініціалізацію
        # Наприклад, підключення до бази даних, Redis тощо
        
        app_state.is_ready = True
        logger.info("Core initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize core: {e}")
        raise

async def shutdown_core() -> None:
    """Коректне завершення роботи ядра"""
    try:
        logger.info("Shutting down core...")
        
        # Закриваємо всі сервіси
        for service_name, service in app_state._services.items():
            try:
                if hasattr(service, 'close'):
                    await service.close()
                logger.info(f"Service {service_name} closed")
            except Exception as e:
                logger.error(f"Error closing service {service_name}: {e}")
        
        app_state.is_ready = False
        logger.info("Core shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during core shutdown: {e}")
        raise

def get_app_state() -> AppState:
    """Повертає глобальний стан додатку"""
    return app_state
