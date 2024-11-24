import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import register_handlers

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

async def main():
    # Ініціалізація бота та диспетчера
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Реєстрація хендлерів
    register_handlers(dp)

    # Запуск бота
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception("Виникла помилка при запуску бота")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
