import asyncio
import logging
from core.bot import setup_bot
from config.settings import settings

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Головна функція запуску бота"""
    try:
        # Ініціалізуємо і запускаємо бота
        bot = await setup_bot()
        logger.info("Bot started successfully!")
        
        # Тримаємо бота запущеним
        await bot.idle()
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)

if __name__ == '__main__':
    asyncio.run(main())
