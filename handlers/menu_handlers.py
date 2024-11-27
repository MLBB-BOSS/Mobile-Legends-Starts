# handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.menus import (
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    MenuButton
)

router = Router()

# Обробник для команди /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привіт! Ласкаво просимо до бота. Оберіть опцію:",
        reply_markup=get_main_menu()
    )

# Обробник для головного меню
@router.message(F.text == MenuButton.NAVIGATION.value)
async def main_menu_navigation(message: Message):
    await message.answer(
        "🧭 Навігація: Оберіть потрібний розділ:",
        reply_markup=get_navigation_menu()
    )

@router.message(F.text == MenuButton.PROFILE.value)
async def main_menu_profile(message: Message):
    await message.answer(
        "🪪 Ваш профіль. Тут буде більше функцій пізніше.",
        reply_markup=get_main_menu()
    )

# Обробник для навігаційного меню
@router.message(F.text == MenuButton.HEROES.value)
async def navigation_menu_heroes(message: Message):
    await message.answer(
        "🛡️ Персонажі: Оберіть клас персонажів:",
        reply_markup=get_heroes_menu()
    )

@router.message(F.text == MenuButton.BACK.value)
async def navigation_menu_back(message: Message):
    await message.answer(
        "Ви повернулися до головного меню.",
        reply_markup=get_main_menu()
    )

# Обробники для меню героїв та інших меню
# ...

# Додайте інші обробники
