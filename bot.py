# bot.py

import os
import asyncio
from aiogram import Bot, Dispatcher
from handlers.menu_handlers import router as menu_router

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Реєстрація маршрутизаторів
dp.include_router(menu_router)
# Додайте інші маршрутизатори за потребою

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот зупинено.")
