from aiogram import Router, F
from aiogram.types import Message
from keyboards.characters_menu import get_characters_keyboard
from keyboards.navigation_menu import get_navigation_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

# Обробник для типів героїв
@router.message(F.text.in_({"🗡️ Бійці", "🏹 Стрільці", "🔮 Маги", "🛡️ Танки", "🏥 Саппорти", "🗲 Гібриди"}))
async def show_heroes_by_type(message: Message):
    try:
        hero_type = message.text
        logger.info(f"User {message.from_user.id} selected hero type: {hero_type}")
        
        hero_descriptions = {
            "🗡️ Бійці": "Спеціалізуються на близькому бою та завданні високої шкоди.",
            "🏹 Стрільці": "Завдають високої шкоди з дальньої дистанції.",
            "🔮 Маги": "Використовують магічні здібності для контролю та знищення.",
            "🛡️ Танки": "Витривалі герої, що захищають команду.",
            "🏥 Саппорти": "Допомагають команді хілом та баффами.",
            "🗲 Гібриди": "Поєднують характеристики різних класів."
        }
        
        await message.answer(
            f"{hero_type}\n\n{hero_descriptions[hero_type]}\n\nРозділ у розробці. Скоро тут з'явиться список героїв.",
            reply_markup=get_characters_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in hero type handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🔙 Назад до Навігації")
async def return_to_navigation(message: Message):
    try:
        logger.info(f"User {message.from_user.id} returned to navigation menu")
        await message.answer(
            "Меню навігації:",
            reply_markup=get_navigation_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in return to navigation handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
