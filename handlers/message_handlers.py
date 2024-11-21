# handlers/message_handlers.py

from aiogram import Router, types, F  # Added F here
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.localization import loc
from keyboards.main_menu import MainMenu
from keyboards.hero_menu import HeroMenu
import logging

logger = logging.getLogger(__name__)
router = Router()

# Визначення станів FSM (якщо використовується)
class HeroStates(StatesGroup):
    SelectingClass = State()
    SelectingHero = State()

@router.message(F.text == loc.get_message("buttons.show_heroes"))
async def show_heroes(message: types.Message):
    try:
        await message.answer(
            "Оберіть клас героя:",
            reply_markup=HeroMenu().get_hero_classes_menu()
        )
        logger.info(f"Користувач {message.from_user.id} запитав показати героїв.")
    except Exception as e:
        logger.exception(f"Помилка в show_heroes хендлері: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

# Додайте інші хендлери за потреби
