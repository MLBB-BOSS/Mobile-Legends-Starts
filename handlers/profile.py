# handlers/profile.py
import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from utils.db import get_all_badges, get_user_by_telegram_id
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import get_user_profile_text, get_user_rating_history
from utils.charts import generate_rating_chart

logger = logging.getLogger(__name__)
profile_router = Router()

@profile_router.message(Command("profile"))
async def show_profile(message: types.Message, db: AsyncSession):
    user_id = message.from_user.id
    user = await get_user_by_telegram_id(db, user_id)

    if not user:
        await message.answer("Ви ще не зареєстровані. Використовуйте команду /start для реєстрації.")
        return

    try:
        logger.info(f"Обробка профілю для користувача {user_id}")

        # Отримання текстової інформації про профіль, включаючи бейджі
        profile_text = await get_user_profile_text(db, user_id, user.username or "")
        logger.debug(f"Текст профілю: {profile_text}")

        # Отримання історії рейтингу користувача
        rating_history = await get_user_rating_history(db, user_id)
        logger.debug(f"Історія рейтингу: {rating_history}")

        if not rating_history:
            # Якщо історія відсутня, використаємо базові дані
            rating_history = [100, 120, 140, 180, 210, 230]
            logger.debug("Використано фіктивні дані рейтингу")

        # Генерація графіка рейтингу
        chart_bytes = generate_rating_chart(rating_history)
        logger.debug("Графік рейтингу згенеровано")

        chart_bytes.seek(0)
        input_file = BufferedInputFile(chart_bytes.read(), filename='rating_chart.png')
        logger.debug("Графік рейтингу готовий до відправки")

        # Створення inline клавіатури
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Оновити Бейджі", callback_data="update_badges"),
                InlineKeyboardButton(text="🎖 Дошка Нагород", callback_data="show_award_board")
            ],
            [
                InlineKeyboardButton(text="🔄 Оновити ID", callback_data="update_player_id"),
                InlineKeyboardButton(text="📜 Історія", callback_data="show_activity_history")
            ],
            [
                InlineKeyboardButton(text="💌 Запросити Друзів", callback_data="invite_friends"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
            ]
        ])

        # Відправка фото з графіком та текстом профілю
        await message.answer_photo(
            photo=input_file,
            caption=profile_text,
            parse_mode="HTML",
            reply_markup=inline_keyboard
        )
        logger.info(f"Профіль відправлено для користувача {user_id}")

    except Exception as e:
        logger.error(f"Сталася помилка при обробці профілю для користувача {user_id}: {e}")
        await message.reply("Сталася помилка при отриманні профілю. Спробуйте пізніше.")