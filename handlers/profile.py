# handlers/profile.py
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db import get_all_badges, get_user_by_telegram_id
from sqlalchemy.ext.asyncio import AsyncSession

profile_router = Router()

@profile_router.message(Command("profile"))
async def show_profile(message: types.Message, db: AsyncSession):
    user_id = message.from_user.id
    user = await get_user_by_telegram_id(db, user_id)

    if not user:
        await message.answer("Ви ще не зареєстровані. Використовуйте команду /start для реєстрації.")
        return

    all_badges = await get_all_badges(db)
    user_badge_ids = {b.id for b in user.badges}

    obtained_badges = user.badges
    not_obtained_badges = [b for b in all_badges if b.id not in user_badge_ids]

    # Замінюємо Markdown на HTML
    profile_text = (
        f"👤 <b>Ваш Профіль:</b>\n\n"
        f"• Ім'я користувача: @{user.username if user.username else 'Не вказано'}\n"
        f"• Рівень: {user.level}\n"
        f"• Скриншотів: {user.screenshot_count}\n"
        f"• Місій: {user.mission_count}\n"
        f"• Вікторин: {user.quiz_count}\n\n"
    )

    if obtained_badges:
        profile_text += "🎖 <b>Отримані Бейджі:</b>\n"
        for b in obtained_badges:
            desc = (b.description or "").replace('<', '&lt;').replace('>', '&gt;')
            profile_text += f"• {b.name} - {desc}\n"
    else:
        profile_text += "🎖 Отримані Бейджі: Немає\n"

    if not_obtained_badges:
        profile_text += "\n🔒 <b>Недоступні Бейджі:</b>\n"
        for b in not_obtained_badges:
            desc = (b.description or "").replace('<', '&lt;').replace('>', '&gt;')
            profile_text += f"• {b.name} - {desc}\n"
    else:
        profile_text += "\n🔓 Всі бейджі отримано! 🎉\n"

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

    # Використовуємо parse_mode="HTML"
    await message.answer(profile_text, parse_mode="HTML", reply_markup=inline_keyboard)
