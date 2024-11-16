import asyncio
import logging
import sys
from typing import List
from aiogram import Bot, Dispatcher, Router
from contextlib import asynccontextmanager
from core.bot import bot, dp
from handlers.hero_commands import router as hero_router
from handlers.start_command import router as start_router
from handlers.message_handlers import router as message_router
from handlers.menu_handlers import router as menu_router  # Додаємо новий роутер меню
from handlers.menu_handlers import router as menu_router

# І додати його реєстрацію:
dp.include_router(menu_router)

# Покращене налаштування логування
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('bot.log', encoding='utf-8')
        ]
    )
    # Відключаємо зайві логи від aiogram
    logging.getLogger('aiogram').setLevel(logging.WARNING)
    return logging.getLogger(__name__)

logger = setup_logging()

class BotApp:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.routers: List[Router] = [
            start_router,
            menu_router,  # Додаємо новий роутер меню
            hero_router,
            message_router
        ]

    async def setup_routers(self):
        """Реєстрація всіх роутерів"""
        for router in self.routers:
            try:
                self.dp.include_router(router)
                logger.info(f"Зареєстровано роутер: {router.__module__}")
            except Exception as e:
                logger.error(f"Помилка при реєстрації роутера {router.__module__}: {e}")
                raise

    @asynccontextmanager
    async def bot_context(self):
        """Контекст менеджер для коректного запуску/зупинки бота"""
        try:
            await self.setup_routers()
            logger.info("Бот успішно налаштований і готовий до запуску")
            yield
        except Exception as e:
            logger.error(f"Критична помилка при налаштуванні бота: {e}")
            raise
        finally:
            logger.info("Зупинка бота...")
            await self.bot.session.close()

    async def start(self):
        """Запуск бота"""
        async with self.bot_context():
            try:
                logger.info("Запускаємо бота...")
                await self.dp.start_polling(
                    self.bot,
                    skip_updates=True,
                    allowed_updates=[
                        "message",
                        "callback_query",
                        "inline_query"
                    ]
                )
            except Exception as e:
                logger.critical(f"Критична помилка при роботі бота: {e}")
                raise

async def main():
    """Головна функція запуску бота"""
    try:
        app = BotApp(bot, dp)
        await app.start()
    except Exception as e:
        logger.critical(f"Неможливо запустити бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинений користувачем")
    except Exception as e:
        logger.critical(f"Необроблена помилка: {e}")
        sys.exit(1)
