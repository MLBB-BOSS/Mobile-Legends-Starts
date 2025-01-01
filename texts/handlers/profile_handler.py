# handlers/profile_handler.py

from aiogram import types
from texts import PROFILE_MENU_TEXT, PROFILE_INTERACTIVE_TEXT
from keyboards.menus import get_profile_menu

async def handle_profile(message: types.Message):
    user = get_user_from_db(message.from_user.id)  # Припустимо, ви маєте функцію для отримання користувача
    await message.reply(
        PROFILE_INTERACTIVE_TEXT.format(
            username=user.username,
            level=user.level,
            rating=user.rating,
            achievements_count=user.achievements_count,
            missions_count=user.missions_count,
            quizzes_count=user.quizzes_count,
            screenshots_count=user.screenshots_count,
            total_matches=user.total_matches,
            total_wins=user.total_wins,
            total_losses=user.total_losses,
            tournament_participations=user.tournament_participations,
            badges_count=user.badges_count,
            last_update=user.last_update
        ),
        reply_markup=get_profile_menu()
    )
