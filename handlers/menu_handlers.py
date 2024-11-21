# handlers/menu_handlers.py

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import MainMenu
from keyboards.hero_menu import HeroMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

# Визначення станів FSM
class HeroStates(StatesGroup):
    SelectingClass = State()
    SelectingHero = State()

@router.message(Text(equals=loc.get_message("buttons.show_heroes")))
async def show_heroes(message: types.Message, state: FSMContext):
    try:
        hero_names = loc.get_all_hero_names()
        if hero_names:
            await message.answer(f"Доступні герої: {', '.join(hero_names)}")
        else:
            await message.answer(loc.get_message("messages.errors.hero_not_found"))
    except Exception as e:
        logger.exception(f"Помилка у show_heroes хендлері: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

# Інші хендлери...
