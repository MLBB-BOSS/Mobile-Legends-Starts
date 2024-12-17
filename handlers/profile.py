from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from utils.charts import generate_rating_chart
from services.user_service import get_user_profile_text, update_mlbb_id
import logging

profile_router = Router()

# Налаштування логування
logger = logging.getLogger(__name__)

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: AsyncSession):
    """Показує профіль користувача з графіком рейтингу."""
    user_id = message.from_user.id
    logger.info(f"Fetching profile for user {user_id}")

    try:
        profile_text = await get_user_profile_text(db, user_id)
    except Exception as e:
        logger.error(f"Error fetching profile for user {user_id}: {e}")
        await message.answer("❗ Виникла помилка при отриманні профілю. Спробуйте пізніше.")
        return

    if not profile_text:
        profile_text = "🔎 <b>Профіль не знайдено або ще не заповнено.</b>"

    try:
        chart_bytes = generate_rating_chart([100, 120, 140, 180, 210, 230])
        input_file = BufferedInputFile(chart_bytes.getvalue(), filename='rating_chart.png')
        await message.answer_photo(photo=input_file, caption=profile_text)
        logger.info(f"Profile sent successfully to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to generate/send chart for user {user_id}: {e}")
        await message.answer("❗ Виникла помилка при генерації графіку.")

@profile_router.message(Command("add_mlbb"))
async def add_mlbb_id(message: Message, db: AsyncSession):
    """Додає або оновлює MLBB ID користувача."""
    user_id = message.from_user.id
    args = message.get_args()

    if not args.isdigit() or len(args) > 10:
        await message.answer("🚨 Некоректний MLBB ID. Переконайтеся, що це числовий ідентифікатор до 10 цифр.")
        return

    try:
        response = await update_mlbb_id(db, user_id, args)
        await message.answer(response)
        logger.info(f"MLBB ID updated for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to update MLBB ID for user {user_id}: {e}")
        await message.answer("❗ Виникла помилка при оновленні MLBB ID.")
