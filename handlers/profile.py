from aiogram import Router, types
from aiogram.dispatcher.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from states.profile_states import ProfileStates

profile_router = Router()

@profile_router.message(Command("profile"))
async def show_profile(message: types.Message, db: AsyncSession):
    stmt = select(User).where(User.telegram_id == message.from_user.id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        await message.answer("Ви ще не зареєстровані. Використовуйте /start для початку роботи.")
        return

    profile_text = format_user_profile(user)
    inline_keyboard = get_profile_inline_keyboard()
    await message.answer(profile_text, reply_markup=inline_keyboard, parse_mode="Markdown")

def format_user_profile(user):
    verification_status = "✅ Верифікований" if user.is_verified else "❌ Неверифікований"
    profile_text = (
        f"👤 *Ваш профіль*\n"
        f"======================\n"
        f"📛 Ім'я користувача: `{user.username or 'Не вказано'}`\n"
        f"🎮 ID гравця: `{user.player_id or 'Не вказано'}`\n"
        f"🎮 Ігровий ID: `{user.game_id or 'Не вказано'}` ({verification_status})\n"
        f"🌟 Рівень: *{user.level}*\n"
        f"----------------------\n"
        f"📸 *Статистика:*\n"
        f"  • Скріншотів: `{user.screenshot_count}`\n"
        f"  • Місій виконано: `{user.mission_count}`\n"
        f"  • Вікторин пройдено: `{user.quiz_count}`\n"
        f"  • Турнірів: `{user.tournaments_participated}`\n"
        f"======================\n"
    )
    return profile_text

def get_profile_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📈 Статистика", callback_data="view_stats")],
            [InlineKeyboardButton(text="🎖️ Нагороди", callback_data="view_badges")],
            [InlineKeyboardButton(text="✏️ Змінити Ігровий ID", callback_data="change_game_id")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
        ]
    )
