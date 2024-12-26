import logging
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

logger = logging.getLogger(__name__)
router = Router()

# Кнопки ReplyKeyboardMarkup
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧭 Меню"), KeyboardButton(text="🦸 Персонажі")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "🧭 Меню")
async def handle_main_menu(message: Message):
    """
    Обробка кнопки "Меню".
    Повертає користувача до головного меню.
    """
    logger.info(f"Користувач {message.from_user.id} натиснув кнопку 'Меню'")
    await message.answer(
        text="Головне меню: оберіть дію.",
        reply_markup=main_menu_keyboard
    )

@router.message(F.text == "🦸 Персонажі")
async def handle_heroes_menu(message: Message):
    """
    Обробка кнопки "Персонажі".
    Відкриває розділ із персонажами.
    """
    logger.info(f"Користувач {message.from_user.id} натиснув кнопку 'Персонажі'")
    # Можна додати логіку завантаження списку героїв з бази чи іншого джерела
    await message.answer(
        text="Тут відображаються персонажі. (Функціонал у розробці)",
        reply_markup=main_menu_keyboard
    )
