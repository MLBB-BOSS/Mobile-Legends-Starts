# handlers/start.py

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message, 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardRemove
)
import logging

router = Router()
logger = logging.getLogger(__name__)

# Function for creating the main keyboard
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🧭 Навігація"),
                KeyboardButton(text="🪪 Мій Профіль")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Виберіть опцію..."
    )
    return keyboard

@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обробник команди /start.
    Відправляє вітальне повідомлення та показує кнопки.
    """
    # Відправляємо інтро повідомлення
    intro_text = (
        "🎮 Ласкаво просимо до Mobile Legends Start!\n\n"
        "Я ваш особистий помічник у світі Mobile Legends. "
        "Тут ви зможете:\n"
        "• Дізнатися про ігрові механіки\n"
        "• Отримати корисні поради\n"
        "• Слідкувати за своїм прогресом\n"
        "• Знаходити нових союзників\n\n"
        "Оберіть опцію нижче, щоб розпочати:"
    )
    
    # Відправляємо повідомлення з клавіатурою
    await message.answer(
        intro_text,
        reply_markup=get_main_keyboard()
    )

# Обробник текстових повідомлень для кнопок
@router.message(F.text.in_(["🧭 Навігація", "🪪 Мій Профіль"]))
async def handle_button_press(message: Message):
    """
    Обробляє натискання кнопок головного меню.
    """
    if message.text == "🧭 Навігація":
        await message.answer(
            "Ви обрали навігацію. Ось доступні розділи:",
            reply_markup=get_main_keyboard()
        )
        # Тут можна додати додаткову логіку для навігації
        
    elif message.text == "🪪 Мій Профіль":
        await message.answer(
            "Ваш профіль:\n"
            "🎯 Рівень: 1\n"
            "🏆 Досягнення: 0\n"
            "📊 Статистика: Недоступна",
            reply_markup=get_main_keyboard()
        )
        # Тут можна додати додаткову логіку для профілю
