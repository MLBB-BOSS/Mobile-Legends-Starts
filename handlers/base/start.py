from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.hero_states import HeroStates
from keyboards.inline_menus import get_intro_page_1_keyboard
from keyboards.menus import get_main_menu_keyboard

router = Router()

@router.message(commands=["start"])
async def start_command(message: Message, state: FSMContext):
    """
    Обробник команди /start.
    """
    user_id = message.from_user.id
    # Перевіряємо стан користувача
    state_data = await state.get_data()

    if not state_data.get("intro_completed", False):
        await message.answer(
            f"👋 Вітаю, {message.from_user.first_name}! Почнемо знайомство!",
            reply_markup=get_intro_page_1_keyboard()
        )
        await state.set_state(HeroStates.main)
    else:
        await message.answer(
            "👋 Вітаю! Повертаю вас до головного меню.",
            reply_markup=get_main_menu_keyboard()
        )
