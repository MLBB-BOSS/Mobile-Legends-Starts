# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command

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
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,  # Використання токена
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=AiohttpSession()  # Явна сесія для HTTP-запитів
    )
    dp = Dispatcher(storage=MemoryStorage())  # FSM сховище
    return bot, dp

# Приклад обробників

# Команда /start
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Я бот. Як я можу допомогти?")

# Команда /help
async def cmd_help(message: types.Message):
    help_text = (
        "Доступні команди:\n"
        "/start - Запустити бота\n"
        "/help - Отримати допомогу\n"
        "/echo <текст> - Ехо повідомлення"
    )
    await message.answer(help_text)

# Команда /echo
async def cmd_echo(message: types.Message):
    args = message.get_args()
    if args:
        await message.answer(args)
    else:
        await message.answer("Будь ласка, введіть текст після команди /echo.")

# Реєстрація обробників
def setup_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_echo, Command("echo"))

# Основна функція запуску бота
async def main():
    logger.info("Starting bot...")
    bot, dp = create_bot_and_dispatcher()

    # Підключення обробників
    setup_handlers(dp)

    # Використання асинхронного контекстного менеджера
    try:
        async with bot:
            logger.info("Bot is polling...")
            await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped manually.")
    except Exception as e:
        logger.error("Critical error occurred: %s", e, exc_info=True)
    finally:
        logger.info("Closing bot session...")
        if bot.session:
            await bot.session.close()

# Точка входу
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot has been stopped gracefully!")