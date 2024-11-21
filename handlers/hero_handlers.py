from aiogram import Router, types
from aiogram.filters import Text
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

# Отримуємо всі імена героїв з усіх класів
ALL_HEROES = []
classes = loc.get_message("heroes.classes")
for class_info in classes.values():
    ALL_HEROES.extend(class_info["heroes"])

@router.message(Text(equals=ALL_HEROES))
async def handle_hero_selection(message: types.Message):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} вибрав героя: {hero_name}")

    try:
        hero_info = loc.get_message(f"heroes.info.{hero_name}")

        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[[
                types.KeyboardButton(text=loc.get_message("buttons.back_to_hero_list"))
            ]],
            resize_keyboard=True
        )

        await message.answer(
            text=hero_info,
            reply_markup=keyboard
        )
    except Exception as e:
        logger.exception(f"Помилка при обробці вибору героя: {e}")
        await message.answer(loc.get_message("messages.errors.hero_not_found"))
