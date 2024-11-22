import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.navigation_handlers import router as navigation_router
from handlers.profile_handlers import router as profile_router  # Інші обробники, якщо потрібні

# Увімкнення логів
logging.basicConfig(level=logging.INFO)

# Зчитуємо токен бота з змінної середовища
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Увага: змінна середовища TELEGRAM_BOT_TOKEN

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Змінна TELEGRAM_BOT_TOKEN не задана! Переконайтесь, що змінна середовища присутня на Heroku.")

# Ініціалізуємо бота і диспетчер
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

# Реєстрація роутерів
dp.include_router(navigation_router)
dp.include_router(profile_router)

# Запуск бота
async def main():
    logging.info("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
