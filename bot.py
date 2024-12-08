# bot.py

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bot")

# Зчитування токена з змінних середовища
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не встановлений в змінних середовища!")
    exit(1)
logger.info(f"Loaded TELEGRAM_BOT_TOKEN: {TELEGRAM_BOT_TOKEN[:5]}***")  # Логування перших символів токена

# Власний фільтр для перевірки, що повідомлення не є командою
class NotCommand(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not message.text.startswith('/')

# Окрема функція для створення бота і диспетчера
def create_bot_and_dispatcher() -> tuple[Bot, Dispatcher]:
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),  # Використання DefaultBotProperties
        session=AiohttpSession()  # Явна сесія для HTTP-запитів
    )
    dp = Dispatcher(storage=MemoryStorage())  # FSM сховище
    return bot, dp

# Створення клавіатури
def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Команда 1"),
                KeyboardButton(text="Команда 2"),
            ],
            [
                KeyboardButton(text="Команда 3"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard

# Обробник команди /start
async def cmd_start(message: Message):
    keyboard = get_main_keyboard()
    await message.answer("Привіт! Я бот. Як я можу допомогти?", reply_markup=keyboard)

# Обробник команди /help
async def cmd_help(message: Message):
    help_text = (
        "Доступні команди:\n"
        "/start - Запустити бота\n"
        "/help - Отримати допомогу\n"
        "/echo &lt;текст&gt; - Ехо повідомлення"
    )
    await message.answer(help_text)

# Обробник команди /echo
async def cmd_echo(message: Message):
    args = message.text.partition(' ')[2]  # Отримання аргументів після команди
    if args:
        await message.answer(args)
    else:
        await message.answer("Будь ласка, введіть текст після команди /echo.")

# Обробник всіх текстових повідомлень, які не є командами
async def handle_all_text(message: Message):
    await message.answer(f"Ви написали: {message.text}")

# Реєстрація обробників
def setup_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_help, Command(commands=["help"]))
    dp.message.register(cmd_echo, Command(commands=["echo"]))
    dp.message.register(handle_all_text, NotCommand(), F.text)  # Реєстрація обробника для всіх текстових повідомлень, які не є командами

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
        await bot.session.close()

# Точка входу
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot has been stopped gracefully!")