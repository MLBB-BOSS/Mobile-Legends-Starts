import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import settings
from handlers import register_handlers
from database import create_db_and_tables, DatabaseMiddleware

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

async def main():
    # Спрощена ініціалізація бота
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        parse_mode=ParseMode.HTML  # Тільки базові налаштування
    )
    
    # Створення диспетчера
    dp = Dispatcher()

    # Додаємо middleware для роботи з базою даних
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())

    # Реєстрація хендлерів
    register_handlers(dp)

    # Створення таблиць у базі даних
    await create_db_and_tables()

    # Запуск бота
    try:
        # Видалення webhook на випадок, якщо він був встановлений
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Запуск polling з новим синтаксисом
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            polling_timeout=30
        )
    except Exception as e:
        logging.exception("Виникла помилка при запуску бота")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
