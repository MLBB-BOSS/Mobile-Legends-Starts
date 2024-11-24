import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from handlers import register_handlers
from database import create_db_and_tables

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

async def main():
    # Ініціалізація бота
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        parse_mode="HTML"
    )
    
    # Створення диспетчера
    dp = Dispatcher()

    # Реєстрація хендлерів
    register_handlers(dp)

    # Створення таблиць у базі даних
    await create_db_and_tables()

    # Запуск бота
    try:
        # Видалення webhook на випадок, якщо він був встановлений
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Запуск polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logging.exception("Виникла помилка при запуску бота")
    finally:
        # Закриття сесії бота
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
