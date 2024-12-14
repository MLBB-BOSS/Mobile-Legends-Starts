# handlers/profile.py
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.user_service import get_or_create_user
from sqlalchemy.ext.asyncio import AsyncSession
from utils.charts import generate_rating_chart
from models.user_stats import UserStats
import logging

profile_router = Router()
logger = logging.getLogger(__name__)

@profile_router.message(Command("profile"))
async def show_profile(message: types.Message, db: AsyncSession):
    user_id = message.from_user.id
    username = message.from_user.username or "Не вказано"

    try:
        # Отримуємо або створюємо користувача
        user = await get_or_create_user(db, telegram_id=user_id, username=username)
        
        # Отримуємо статистику користувача
        stats = user.stats
        if not stats:
            # Створюємо базову статистику, якщо її немає
            stats = UserStats(user_id=user.id, rating=100, achievements_count=0)
            db.add(stats)
            await db.commit()
            await db.refresh(stats)
        
        # Отримуємо історію рейтингу (замініть на реальні дані)
        rating_history = [stats.rating]  # Тут потрібно використовувати реальні історичні дані
        
        if not rating_history:
            rating_history = [stats.rating]  # Впевніться, що є хоча б одне значення
        
        # Генеруємо графік рейтингу
        chart = generate_rating_chart(rating_history)
        
        # Створюємо текст профілю
        profile_text = (
            f"👤 <b>Ваш Профіль:</b>\n\n"
            f"• Ім'я користувача: @{user.username}\n"
            f"• Рівень: {user.level}\n"
            f"• Скриншотів: {user.screenshot_count}\n"
            f"• Місій: {user.mission_count}\n"
            f"• Вікторин: {user.quiz_count}\n\n"
            f"📈 <b>Рейтинг:</b> {stats.rating}\n"
            f"🎯 <b>Досягнення:</b> {stats.achievements_count} досягнень\n"
        )
        
        # Додаємо бейджі
        if user.badges:
            profile_text += "\n🎖 <b>Отримані Бейджі:</b>\n"
            for badge in user.badges:
                desc = (badge.description or "").replace('<', '&lt;').replace('>', '&gt;')
                profile_text += f"• {badge.name} - {desc}\n"
        else:
            profile_text += "\n🎖 Отримані Бейджі: Немає\n"
        
        # Створюємо інлайн-клавіатуру
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
        
        # Надсилаємо зображення з графіком та текстом профілю як підписом
        await message.answer_photo(
            photo=chart,
            caption=profile_text,
            parse_mode="HTML",
            reply_markup=inline_keyboard
        )
        
    except Exception as e:
        logger.error(f"Error in show_profile handler: {e}")
        await message.answer("Виникла помилка при отриманні профілю. Спробуйте пізніше.")