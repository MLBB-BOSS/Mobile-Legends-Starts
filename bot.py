import os
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Отримання токену
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("Змінна оточення TELEGRAM_BOT_TOKEN не задана!")
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено!")

# Ініціалізація бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Клавіатура першого рівня
def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🧭 Навігація"), KeyboardButton("🪪 Профіль"))
    return keyboard

# Клавіатура другого рівня
def get_navigation_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton("🛡️ Персонажі"),
        KeyboardButton("📚 Гайди"),
        KeyboardButton("⚖️ Контр-піки")
    )
    keyboard.row(
        KeyboardButton("⚜️ Білди"),
        KeyboardButton("📊 Голосування"),
        KeyboardButton("🔄 Назад")
    )
    return keyboard

# Клавіатура для вибору персонажів
def get_heroes_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton("🔎 Пошук Персонажа"),
        KeyboardButton("🛡️ Танк"),
        KeyboardButton("🔮 Маг")
    )
    keyboard.row(
        KeyboardButton("🏹 Стрілець"),
        KeyboardButton("⚔️ Асасін"),
        KeyboardButton("🧬 Підтримка")
    )
    keyboard.add(KeyboardButton("🔄 Назад"))
    return keyboard

# Обробник команди /start
@router.message(Command("start"))
async def start_handler(message: Message):
    logger.info(f"Користувач {message.from_user.id} надіслав команду /start")
    await message.answer(
        "Привіт! Ласкаво просимо до бота.",
        reply_markup=get_main_menu()
    )

# Обробник для кнопок головного меню
@router.message(Text(["🧭 Навігація", "🪪 Профіль"]))
async def handle_main_menu(message: Message):
    if message.text == "🧭 Навігація":
        logger.info(f"Користувач {message.from_user.id} обрав '🧭 Навігація'")
        await message.answer(
            "🧭 Навігація: Оберіть потрібний розділ:",
            reply_markup=get_navigation_menu()
        )
    elif message.text == "🪪 Профіль":
        logger.info(f"Користувач {message.from_user.id} обрав '🪪 Профіль'")
        await message.answer(
            "🪪 Ваш профіль. Тут буде більше функцій пізніше.",
            reply_markup=get_main_menu()
        )

# Обробник для кнопок навігаційного меню
@router.message(Text(["🔄 Назад", "🛡️ Персонажі", "📚 Гайди", "⚖️ Контр-піки", "⚜️ Білди", "📊 Голосування"]))
async def handle_navigation_menu(message: Message):
    if message.text == "🔄 Назад":
        logger.info(f"Користувач {message.from_user.id} обрав '🔄 Назад'")
        await message.answer(
            "Ви повернулися до головного меню.",
            reply_markup=get_main_menu()
        )
    elif message.text == "🛡️ Персонажі":
        logger.info(f"Користувач {message.from_user.id} обрав '🛡️ Персонажі'")
        await message.answer(
            "🛡️ Персонажі: Оберіть клас персонажів:",
            reply_markup=get_heroes_menu()
        )
    else:
        logger.warning(f"Невідома команда в меню навігації: {message.text}")
        await message.answer("Невідома команда. Оберіть з меню.")

# Обробник для кнопок меню персонажів
@router.message(Text(["🔎 Пошук Персонажа", "🛡️ Танк", "🔮 Маг", "🏹 Стрілець", "⚔️ Асасін", "🧬 Підтримка", "🔄 Назад"]))
async def handle_heroes_menu(message: Message):
    if message.text == "🔄 Назад":
        logger.info(f"Користувач {message.from_user.id} обрав '🔄 Назад'")
        await message.answer(
            "Ви повернулися до навігаційного меню.",
            reply_markup=get_navigation_menu()
        )
    else:
        logger.info(f"Користувач {message.from_user.id} обрав {message.text}")
        await message.answer(
            f"Ви обрали {message.text}. Ця функція ще в розробці.",
            reply_markup=get_heroes_menu()
        )

# Реєстрація маршрутизатора
dp.include_router(router)

if __name__ == "__main__":
    import asyncio
    try:
        logger.info("Запуск бота...")
        asyncio.run(dp.start_polling(bot))
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено.")
