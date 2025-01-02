# bot.py

import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start_intro_router  # Імпортуйте інші роутери тут

from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота, диспетчера та сховища FSM
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Налаштування обробників
dp.include_router(start_intro_router)
# Додайте інші роутери тут, наприклад:
# dp.include_router(main_menu_router)

async def main():
    try:
        # Запуск бота
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
