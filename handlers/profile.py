# handlers/profile.py

import logging

# Якщо використовуєте aiogram 3.x, F імпортується з aiogram:
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession  # Якщо потрібно для db
# Або: from typing import Annotated  # За бажання, якщо використовуєте інші фішки

from utils.message_utils import safe_delete_message
from utils.db import get_user_profile
from utils.text_formatter import format_profile_text
from texts import PROFILE_INTERACTIVE_TEXT, GENERIC_ERROR_MESSAGE_TEXT

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🤪 Мій Профіль")
async def handle_my_profile_handler(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробник повідомлення з текстом "🤪 Мій Профіль".
    """
    await safe_delete_message(bot, message.chat.id, message.message_id)
    await process_my_profile(message, state, db, bot)

async def process_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Функція обробки профілю користувача:
    - Дістає дані профілю з бази
    - Форматує профіль
    - Надсилає користувачу
    """
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)

    if profile_data:
        profile_info = {
            "username": profile_data.get('username', 'N/A'),
            "level": profile_data.get('level', 'N/A'),
            "rating": profile_data.get('rating', 'N/A'),
            "achievements_count": profile_data.get('achievements_count', 'N/A'),
            "screenshots_count": profile_data.get('screenshots_count', 'N/A'),
            "missions_count": profile_data.get('missions_count', 'N/A'),
            "quizzes_count": profile_data.get('quizzes_count', 'N/A'),
            "total_matches": profile_data.get('total_matches', 'N/A'),
            "total_wins": profile_data.get('total_wins', 'N/A'),
            "total_losses": profile_data.get('total_losses', 'N/A'),
            "tournament_participations": profile_data.get('tournament_participations', 'N/A'),
            "badges_count": profile_data.get('badges_count', 'N/A'),
            "last_update": (
                profile_data['last_update'].strftime('%d.%m.%Y %H:%M') 
                if profile_data.get('last_update') else 'N/A'
            )
        }
        try:
            formatted_profile_text = format_profile_text(PROFILE_INTERACTIVE_TEXT, profile_info)
        except ValueError as e:
            logger.error(f"Error formatting profile text: {e}")
            await bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT
            )
            return
        
        # Відправляємо повідомлення з готовим профілем
        await bot.send_message(chat_id=message.chat.id, text=formatted_profile_text)
    else:
        # Якщо профіль не знайдено в БД
        await bot.send_message(chat_id=message.chat.id, text="Користувач не знайдений.")