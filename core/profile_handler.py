# core/profile_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from models.contribution import Contribution

logger = logging.getLogger(__name__)

async def view_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробник команди для перегляду профілю користувача.

    Отримує внески та бейджі користувача, обчислює загальні бали та відправляє
    інформацію користувачу через Telegram.

    Args:
        update (Update): Оновлення від Telegram.
        context (ContextTypes.DEFAULT_TYPE): Контекст для обробки команди.
    """
    try:
        user = update.effective_user

        if not user:
            logger.warning("Не вдалося отримати інформацію про користувача.")
            await update.message.reply_text("Не вдалося отримати вашу інформацію.")
            return

        async with context.application.sessionmaker() as session:
            # Викликаємо асинхронні методи
            contributions = await Contribution.get_user_contributions(user.id, session)
            total_points = sum(c.points for c in contributions)
            badges = await Contribution.get_user_badges(user.id, session)

            profile_info = (
                f"📄 **Ваш профіль:**\n\n"
                f"👤 **Ім'я:** {user.first_name} {user.last_name or ''}\n"
                f"🔢 **ID:** {user.id}\n"
                f"⭐ **Бали:** {total_points}\n"
                f"🏅 **Бейджі:** {', '.join(badges) if badges else 'Немає'}"
            )

            await update.message.reply_text(profile_info, parse_mode='MarkdownV2')
            logger.info(f"Користувач {user.username or user.id} переглянув свій профіль.")
    except Exception as e:
        logger.error(f"Error in view_profile: {e}", exc_info=True)
        await update.message.reply_text("Виникла помилка при відображенні профілю.")
