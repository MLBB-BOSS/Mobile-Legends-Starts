# handlers/ai_handler.py

import logging
import openai
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types

from config import OPENAI_API_KEY, API_URL
from keyboards.inline_menus import get_generic_inline_keyboard
from utils.messages import (
    GENERIC_ERROR_MESSAGE_TEXT,
    AI_INTRO_TEXT,
    AI_RESPONSE_TEXT,
)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізуємо OpenAI API
openai.api_key = OPENAI_API_KEY

# Створюємо Router для AI
router = Router()

# Визначаємо стани для AI
class AIStates(StatesGroup):
    WAITING_FOR_QUERY = State()

# Команда для початку взаємодії з AI
@router.message(F.text.lower() == "допомога з персонажем")
async def ai_start(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} розпочав взаємодію з AI")
    
    await message.delete()
    
    await state.set_state(AIStates.WAITING_FOR_QUERY)
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=AI_INTRO_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )

# Обробник для отримання запиту від користувача
@router.message(AIStates.WAITING_FOR_QUERY)
async def ai_handle_query(message: Message, state: FSMContext, bot: Bot):
    user_query = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} запитує AI: {user_query}")
    
    await message.delete()
    
    if not user_query:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Будь ласка, введіть запит для AI.",
            reply_markup=get_generic_inline_keyboard()
        )
        return
    
    try:
        # Формуємо промпт
        prompt = f"Provide detailed information about the Mobile Legends character: {user_query}."
        
        # Викликаємо OpenAI API асинхронно
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Mobile Legends."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        
        ai_reply = response.choices[0].message['content'].strip()
        
        # Відправляємо відповідь користувачу
        await bot.send_message(
            chat_id=message.chat.id,
            text=AI_RESPONSE_TEXT.format(response=ai_reply),
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
        
        # Повертаємо користувача до попереднього стану або завершуємо
        await state.clear()
        
    except Exception as e:
        logger.error(f"Помилка при виклику OpenAI API: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.clear()

# Обробник для скасування взаємодії з AI
@router.message(F.text.lower() == "скасувати")
async def ai_cancel(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} скасував взаємодію з AI")
    
    await message.delete()
    await state.clear()
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Взаємодія з AI скасована.",
        reply_markup=get_generic_inline_keyboard()
    )
