# handlers/base.py

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import asyncio

from states.menu_states import MenuStates
from utils.keyboards import get_main_keyboard

router = Router()

# Тексти привітальних повідомлень
WELCOME_MESSAGES = [
    "🎮 Ласкаво просимо до світу Mobile Legends!\n"
    "Я ваш особистий ігровий помічник.",
    
    "🌟 Разом ми:\n"
    "• Вивчимо всіх героїв\n"
    "• Розберемо тактики гри\n"
    "• Дізнаємось про мета-стратегії",
    
    "🎯 Готові почати?\n"
    "Використовуйте меню нижче для навігації!"
]

async def send_welcome_sequence(message: Message):
    """
    Відправляє серію привітальних повідомлень з анімацією
    """
    for text in WELCOME_MESSAGES:
        await message.answer(text)
        await asyncio.sleep(1)  # Затримка між повідомленнями

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Обробник команди /start
    Показує привітальні повідомлення та встановлює головне меню
    """
    # Відправляємо серію привітальних повідомлень
    await send_welcome_sequence(message)
    
    # Встановлюємо головне меню з кнопками
    await message.answer(
        "Оберіть опцію для початку роботи:",
        reply_markup=get_main_keyboard()
    )
    
    # Встановлюємо стан головного меню
    await state.set_state(MenuStates.MAIN_MENU)

@router.message(F.text == "🔄 Рестарт")
async def handle_restart(message: Message, state: FSMContext):
    """
    Обробник кнопки рестарту
    Повертає користувача до початкового стану
    """
    await message.answer("Перезапуск бота...")
    await cmd_start(message, state)
