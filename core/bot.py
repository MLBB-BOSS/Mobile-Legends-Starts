from aiogram import Bot, Dispatcher
from core.config import settings
import logging

# Налаштовуємо логування
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Створюємо екземпляри бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Додаємо middleware для rate limiting якщо потрібно
if settings.RATE_LIMIT > 0:
    from aiogram.utils.chat_action import ChatActionMiddleware
    dp.message.middleware(ChatActionMiddleware())

# Додаємо базові перевірки при старті
async def check_bot_token():
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не налаштовано")
    try:
        bot_info = await bot.get_me()
        logger.info(f"Бот {bot_info.full_name} (@{bot_info.username}) успішно запущено")
    except Exception as e:
        logger.error(f"Помилка при перевірці токена бота: {e}")
        raise
