# core/bot_runner.py

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start_router, navigation_router
import asyncio

API_TOKEN = "YOUR_BOT_TOKEN"

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(navigation_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
