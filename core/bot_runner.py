# core/bot_runner.py

from handlers.hero_handler import router as hero_router  # Імпорт вашого роутера з hero_handler
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.utils.executor import start_polling

API_TOKEN = "YOUR_BOT_API_TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Реєструємо роутер
dp.include_router(hero_router)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/hero", description="Get hero response"),
    ]
    await bot.set_my_commands(commands)

async def on_startup(dispatcher: Dispatcher):
    await set_commands(dispatcher.bot)

if __name__ == "__main__":
    start_polling(dp, skip_updates=True, on_startup=on_startup)
