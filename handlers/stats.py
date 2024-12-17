from aiogram import Router, types
from utils.text_templates import (
    get_general_activity_text,
    get_game_stats_text,
    get_achievements_text,
)
import logging
from keyboards.statistics_keyboard import statistics_inline

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(lambda c: c.data == "general_activity")
async def show_general_activity(callback: types.CallbackQuery):
    logger.info(f"User {callback.from_user.id} selected general_activity")
    try:
        text = get_general_activity_text()
        await callback.message.edit_text(text, reply_markup=statistics_inline(), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error updating general_activity for user {callback.from_user.id}: {e}")
        await callback.answer("❗ Помилка при оновленні статистики.")

@router.callback_query(lambda c: c.data == "game_stats")
async def show_game_stats(callback: types.CallbackQuery):
    logger.info(f"User {callback.from_user.id} selected game_stats")
    try:
        text = get_game_stats_text()
        await callback.message.edit_text(text, reply_markup=statistics_inline(), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error updating game_stats for user {callback.from_user.id}: {e}")
        await callback.answer("❗ Помилка при оновленні статистики.")

@router.callback_query(lambda c: c.data == "achievements")
async def show_achievements(callback: types.CallbackQuery):
    logger.info(f"User {callback.from_user.id} selected achievements")
    try:
        text = get_achievements_text()
        await callback.message.edit_text(text, reply_markup=statistics_inline(), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error updating achievements for user {callback.from_user.id}: {e}")
        await callback.answer("❗ Помилка при оновленні досягнень.")
