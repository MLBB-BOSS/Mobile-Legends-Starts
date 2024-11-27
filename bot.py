# bot.py
import os
import logging
import asyncio
from aiogram import Bot, Dispatcher

# Ініціалізація бота та диспетчера
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено!")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Імпорт ваших обробників
from handlers.start import router as start_router
from handlers.heroes import router as heroes_router
from handlers.tank import router as tank_router
from handlers.fighter import router as fighter_router
from handlers.guides import router as guides_router
from handlers.back import router as back_router
# Додайте інші обробники за потребою

# Реєстрація обробників у диспетчері
dp.include_router(start_router)
dp.include_router(heroes_router)
dp.include_router(tank_router)
dp.include_router(fighter_router)
dp.include_router(guides_router)
dp.include_router(back_router)
# Додайте інші маршрутизатори

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот зупинено.")
