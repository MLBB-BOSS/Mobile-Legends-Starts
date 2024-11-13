import asyncio
import logging
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from config.settings import settings
from handlers.screenshot_handler import handle_screenshot, list_screenshots
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Створюємо engine для бази даних
engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionFactory = sessionmaker(engine, class_=AsyncSession)

async def setup_bot():
    """Налаштування та ініціалізація бота"""
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Створюємо middleware для передачі сесії бази даних
    async def db_session_middleware(update, context, callback):
        async with AsyncSessionFactory() as session:
            context.session = session
            try:
                await callback(update, context)
            finally:
                await session.close()

    # Реєструємо обробники з middleware
    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            lambda u, c: db_session_middleware(u, c, handle_screenshot)
        )
    )
    
    application.add_handler(
        CommandHandler(
            "screenshots",
            lambda u, c: db_session_middleware(u, c, list_screenshots)
        )
    )

    await application.initialize()
    await application.start()
    
    return application

async def main():
    """Головна функція запуску бота"""
    try:
        bot = await setup_bot()
        logger.info("Bot started successfully!")
        await bot.idle()
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)

if __name__ == '__main__':
    asyncio.run(main())
