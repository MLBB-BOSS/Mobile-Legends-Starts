# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import settings

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bot")

# Змінна для токена (логування)
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
logger.info(f"Loaded TELEGRAM_BOT_TOKEN: {TELEGRAM_BOT_TOKEN[:5]}***")  # Логування перших символів токена

# Окрема функція для створення бота і диспетчера
def create_bot_and_dispatcher() -> tuple[Bot, Dispatcher]:
    bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    return bot, dp

# Приклад обробників

# Обробник команди /start
async def cmd_start(message: Message):
    await message.answer("Привіт! Я бот. Як я можу допомогти?")

# Обробник команди /help
async def cmd_help(message: Message):
    help_text = (
        "Доступні команди:\n"
        "/start - Запустити бота\n"
        "/help - Отримати допомогу\n"
        "/echo <текст> - Ехо повідомлення"
    )
    await message.answer(help_text)

# Обробник команди /echo
async def cmd_echo(message: Message):
    args = message.text.partition(' ')[2]  # Отримання аргументів після команди
    if args:
        await message.answer(args)
    else:
        await message.answer("Будь ласка, введіть текст після команди /echo.")

# Реєстрація обробників
def setup_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_help, Command(commands=["help"]))
    dp.message.register(cmd_echo, Command(commands=["echo"]))

# Основна функція запуску бота
async def main():
    logger.info("Starting bot...")
    bot, dp = create_bot_and_dispatcher()

    # Підключення обробників
    setup_handlers(dp)

    # Використання асинхронного контекстного менеджера
    try:
        logger.info("Bot is polling...")
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped manually.")
    except Exception as e:
        logger.error("Critical error occurred: %s", e, exc_info=True)
    finally:
        logger.info("Closing bot session...")
        await bot.session.close()

# Точка входу
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot has been stopped gracefully!")