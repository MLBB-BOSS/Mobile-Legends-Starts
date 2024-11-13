import asyncio
import logging
from aiogram import Dispatcher
from core.bot import dp, bot, on_startup, on_shutdown  # Імпортуємо диспетчер, бота і функції з core/bot.py

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Головна функція для запуску бота"""
    try:
        # Запускаємо callback для налаштування служб при старті
        await on_startup(dp)
        
        # Запуск бота
        await dp.start_polling(bot)  # `start_polling` запускає цикл обробки повідомлень
        
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}", exc_info=True)
    finally:
        # Викликаємо on_shutdown для завершальних дій, таких як закриття сесій
        await on_shutdown(dp)

if __name__ == '__main__':
    # Використовуємо asyncio для запуску основної функції
    asyncio.run(main())
