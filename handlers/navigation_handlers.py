from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import NavigationMenu
from keyboards.characters_menu import CharactersMenu

router = Router()

@router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message):
    await message.reply(
        "Це розділ навігації. Оберіть опцію:",
        reply_markup=NavigationMenu.get_navigation_menu()
    )

@router.message(F.text == "🛡️ Персонажі")
async def handle_characters(message: Message):
    await message.reply(
        "Це меню 'Персонажі'. Оберіть категорію:",
        reply_markup=CharactersMenu.get_characters_menu()
    )

@router.message(F.text == "🔄 Назад")
async def handle_back_to_main_menu(message: Message):
    await message.reply(
        "Повернення до головного меню. Оберіть дію:",
        reply_markup=NavigationMenu.get_main_menu()
    )
