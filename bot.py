from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
import os

# Ініціалізація бота
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено!")
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Обробник для команди /start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привіт! Ласкаво просимо до бота.")

# Додаємо маршрутизатор до Dispatcher
dp.include_router(router)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
