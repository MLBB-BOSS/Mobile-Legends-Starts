# handlers/characters_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.characters_menu import CharactersMenu
from keyboards.navigation_menu import NavigationMenu

router = Router()

@router.message(F.text == "🛡️ Танк")
async def handle_tank(message: Message):
    await message.reply("Герої класу 'Танк':\n- Герой 1\n- Герой 2", reply_markup=CharactersMenu.get_characters_menu())

@router.message(F.text == "🔮 Маг")
async def handle_mage(message: Message):
    await message.reply("Герої класу 'Маг':\n- Герой 3\n- Герой 4", reply_markup=CharactersMenu.get_characters_menu())

@router.message(F.text == "🔄 Назад")
async def handle_back_to_navigation(message: Message):
    await message.reply(
        "Повернення до меню навігації. Оберіть опцію:",
        reply_markup=NavigationMenu.get_navigation_menu()
    )
