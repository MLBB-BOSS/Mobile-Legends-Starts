import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Імпорти роутерів
from handlers.error_handler import error_handler
from handlers.start_command import router as start_router
from handlers.hero_commands import router as hero_commands_router
from handlers.message_handlers import router as message_router
from handlers.menu_handlers import router as menu_router
from handlers.hero_class_handlers import router as hero_class_router
from handlers.statistics_handler import router as statistics_router

async def setup_dispatcher() -> Dispatcher:
    """Налаштування диспетчера"""
    try:
        dp = Dispatcher()
        
        # Налаштування обробки помилок
        dp.errors.register(error_handler)
        
        return dp
    except Exception as e:
        logger.error(f"Помилка при налаштуванні диспетчера: {e}")
        raise

async def setup_bot() -> Bot:
    """Створення та налаштування об'єкта бота"""
    try:
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN.get_secret_value())
        logger.info("Бот успішно створений")
        return bot
    except Exception as e:
        logger.error(f"Помилка при створенні бота: {e}")
        raise

def setup_routers(dp: Dispatcher) -> None:
    """Налаштування роутерів"""
    try:
        logger.info("Починаємо реєстрацію роутерів...")
        
        # Реєструємо всі роутери
        routers = [
            hero_class_router,
            statistics_router,
            menu_router,
            start_router,
            hero_commands_router,
            message_router
        ]
        
        for router in routers:
            dp.include_router(router)
        
        logger.info("Всі роутери зареєстровано успішно")
    except Exception as e:
        logger.error(f"Помилка при реєстрації роутерів: {e}")
        raise

async def main() -> None:
    """Головна функція запуску бота"""
    try:
        # Створюємо та налаштовуємо диспетчер
        dp = await setup_dispatcher()
        
        # Налаштовуємо бота
        bot = await setup_bot()
        
        # Налаштовуємо роутери
        setup_routers(dp)
        
        logger.info("Запускаємо бота...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
        raise
    finally:
        if 'bot' in locals():
            await bot.session.close()
            logger.info("З'єднання з Telegram закрито")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинений користувачем")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
        exit(1)
