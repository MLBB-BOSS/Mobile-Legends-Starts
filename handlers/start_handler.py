from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

bot = Bot(token='TELEGRAM_BOT_TOKEN')
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(commands=['start'])
async def send_welcome(message: Message):
    await message.answer("Привіт! Я бот.")

if __name__ == '__main__':
    dp.run_polling(bot)
