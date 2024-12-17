# handlers/menu.py

from aiogram import Router, types
from aiogram.types import InputMediaPhoto
from keyboards.menus import main_menu, statistics_inline
from utils.charts import generate_activity_chart
import logging

router = Router()

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Обробник для команди /start
@router.message(lambda message: message.text == "/start" or message.text == "🔙 Назад")
async def show_main_menu(message: types.Message):
    """Відображає головне меню користувачу."""
    user_id = message.from_user.id
    logger.info(f"User {user_id} opened the main menu")

    try:
        await message.delete()
        await message.answer("🗂 *Головне меню*", reply_markup=main_menu(), parse_mode="Markdown")
        await message.answer("📊 Виберіть категорію для перегляду статистики:", reply_markup=statistics_inline())
    except Exception as e:
        logger.error(f"Failed to display main menu for user {user_id}: {e}")

# Обробник для інлайн-кнопок статистики
@router.callback_query(lambda c: c.data in ["general_activity", "game_stats", "activity_chart"])
async def process_statistics_callback(callback: types.CallbackQuery):
    """Обробка кнопок статистики."""
    user_id = callback.from_user.id
    data = callback.data
    logger.info(f"User {user_id} pressed {data} in statistics menu")

    if data == "general_activity":
        text = "🎯 Загальна активність: 85% виконаних завдань"
    elif data == "game_stats":
        text = "🎮 Ігрова статистика:\n- Перемог: 120\n- Поразок: 30"
    elif data == "activity_chart":
        try:
            chart = generate_activity_chart()
            await callback.message.edit_media(
                media=InputMediaPhoto(media=chart, caption="📈 Ваш графік активності"),
                reply_markup=statistics_inline()
            )
            await callback.answer()
            return
        except Exception as e:
            logger.error(f"Failed to generate/send activity chart for user {user_id}: {e}")
            text = "Сталася помилка при генерації графіка. Спробуйте пізніше."

    try:
        await callback.message.edit_text(text, reply_markup=statistics_inline())
    except Exception as e:
        logger.error(f"Failed to update statistics menu for user {user_id}: {e}")
        await callback.message.answer("Сталася помилка при оновленні меню.")
    
    await callback.answer()

# Обробник для невідомих callback'ів
@router.callback_query()
async def handle_unknown_callback(callback: types.CallbackQuery):
    """Обробляє невідомі callback'и."""
    user_id = callback.from_user.id
    logger.warning(f"User {user_id} pressed unknown callback: {callback.data}")
    await callback.answer("Невідома команда. Використовуйте кнопки для навігації.")
