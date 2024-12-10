# handlers/ai_handler.py

import logging
import openai
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import settings
from keyboards.menus import get_generic_reply_keyboard  # Переконайтеся, що ця функція повертає ReplyKeyboardMarkup
from texts import (
    GENERIC_ERROR_MESSAGE_TEXT,
    AI_INTRO_TEXT,
    AI_RESPONSE_TEXT,
    UNKNOWN_COMMAND_TEXT,
)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізуємо OpenAI API
openai.api_key = settings.OPENAI_API_KEY

# Створюємо Router для AI
router = Router()

# Визначаємо стани для AI
class AIStates(StatesGroup):
    WAITING_FOR_QUERY = State()

@router.message(F.text == "🤖 AI")
async def ai_intro_handler(message: Message, state: FSMContext, bot: Bot):
    """
    Обробник для кнопки "🤖 AI" у головному меню.
    """
    logger.info(f"Користувач {message.from_user.id} обрав {message.text} у головному меню")
    
    # Надсилаємо вступне повідомлення та меню AI
    await message.answer(
        text=AI_INTRO_TEXT,
        reply_markup=get_ai_menu_keyboard()
    )
    
    # Встановлюємо стан очікування запиту від користувача
    await AIStates.WAITING_FOR_QUERY.set()

@router.message(AIStates.WAITING_FOR_QUERY)
async def ai_query_handler(message: Message, state: FSMContext, bot: Bot):
    """
    Обробляє запити користувача до AI та відповідає згенерованим текстом.
    """
    user_query = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} запитав AI: {user_query}")
    
    if not user_query:
        await message.answer(
            text="Будь ласка, введіть запит для AI.",
            reply_markup=get_ai_menu_keyboard()
        )
        return
    
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant for Mobile Legends players."},
                {"role": "user", "content": user_query}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        
        ai_reply = response.choices[0].message['content'].strip()
        
        await message.answer(
            text=AI_RESPONSE_TEXT.format(response=ai_reply),
            parse_mode="HTML",
            reply_markup=get_ai_menu_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Помилка при виклику OpenAI API: {e}")
        await message.answer(
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_ai_menu_keyboard()
        )
    
    # Повертаємо користувача до головного меню
    await state.clear()
    await message.answer(
        text="Повертаємось до головного меню.",
        reply_markup=get_main_menu()
    )

def get_ai_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Створює меню для розділу AI.
    """
    buttons = [
        KeyboardButton(text="🤖 Запитати AI"),
        KeyboardButton(text="📚 Інструкції"),
        KeyboardButton(text="🔙")  # Кнопка "Назад"
    ]
    return ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True
    )

def get_generic_reply_keyboard() -> ReplyKeyboardMarkup:
    """
    Створює загальну клавіатуру (якщо необхідно).
    """
    buttons = [
        KeyboardButton(text="🔙"),
        KeyboardButton(text="Інша кнопка")  # Додайте інші кнопки за потребою
    ]
    return ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True
    )
