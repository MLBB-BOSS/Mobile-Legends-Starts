import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.bot import bot, dp
from handlers.hero_commands import router as hero_router
from handlers.start_command import router as start_router
from handlers.message_handlers import router as message_router
from handlers.menu_handlers import router as menu_router  # Додаємо імпорт меню

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

async def main():
    try:
        # Реєструємо роутери в правильному порядку
        logger.info("Починаємо реєстрацію роутерів...")
        
        # Реєструємо кожен роутер окремо з перевіркою
        routers = [
            (menu_router, "menu_router"),
            (start_router, "start_router"),
            (hero_router, "hero_router"),
            (message_router, "message_router")
        ]
        
        for router, name in routers:
            try:
                if not router.parent_router:  # Перевіряємо, чи роутер ще не приєднаний
                    dp.include_router(router)
                    logger.info(f"Успішно зареєстровано роутер: {name}")
            except Exception as e:
                logger.warning(f"Роутер {name} вже зареєстрований або виникла помилка: {e}")
                continue
        
        logger.info("Всі роутери зареєстровано")
        
        # Запускаємо бота
        logger.info("Запускаємо бота...")
        await dp.start_polling(bot, skip_updates=True)
        
    except Exception as e:
        logger.error(f"Критична помилка при запуску бота: {e}")
        raise
    finally:
        logger.info("Завершення роботи бота...")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинений користувачем")
    except Exception as e:
        logger.critical(f"Необроблена помилка: {e}")
        raise
