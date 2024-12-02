# handlers/ai_handler.py

import logging
import openai
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import settings
from keyboards.inline_menus import get_generic_inline_keyboard
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
    Обробляє натискання кнопки AI, надсилає вступне повідомлення та переводить користувача в стан очікування запиту.
    """
    logger.info(f"Користувач {message.from_user.id} обрав AI")
    
    await message.delete()
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=AI_INTRO_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )
    
    await state.set_state(AIStates.WAITING_FOR_QUERY)

@router.message(AIStates.WAITING_FOR_QUERY)
async def ai_query_handler(message: Message, state: FSMContext, bot: Bot):
    """
    Обробляє запити користувача до AI та відповідає згенерованим текстом.
    """
    user_query = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} запитав AI: {user_query}")
    
    await message.delete()
    
    if not user_query:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Будь ласка, введіть запит для AI.",
            reply_markup=get_generic_inline_keyboard()
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
        
        await bot.send_message(
            chat_id=message.chat.id,
            text=AI_RESPONSE_TEXT.format(response=ai_reply),
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Помилка при виклику OpenAI API: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
    
    # Повертаємо користувача до головного меню
    await state.set_state(MenuStates.MAIN_MENU)
