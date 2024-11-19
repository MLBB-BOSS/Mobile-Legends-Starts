# handlers/menu_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.profile_menu import ProfileMenu
from utils.localization import loc

router = Router()

# Обробник для кнопки "Навігація"
@router.message(F.text == loc.get_message("buttons.navigation"))
async def show_navigation(message: Message):
    await message.answer(
        loc.get_message("messages.navigation_menu"),
        reply_markup=NavigationMenu.get_navigation_menu()
    )

# Обробник для кнопки "Мій Кабінет"
@router.message(F.text == loc.get_message("buttons.profile"))
async def show_profile(message: Message):
    await message.answer(
        loc.get_message("messages.profile_menu"),
        reply_markup=ProfileMenu.get_profile_menu()
    )

# Обробник для кнопки "Назад"
@router.message(F.text == loc.get_message("buttons.back"))
async def back_to_main(message: Message):
    await message.answer(
        loc.get_message("messages.menu_welcome"),
        reply_markup=MainMenu.get_main_menu()
    )

# Додайте цей обробник для команди /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        loc.get_message("messages.start_command"),
        reply_markup=MainMenu.get_main_menu()
    )
