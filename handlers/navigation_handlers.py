# handlers/navigation_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import NavigationMenu
from utils.localization import loc

router = Router()

@router.message(F.text == loc.get_message("buttons.navigation"))
async def show_navigation(message: Message):
    await message.answer(
        loc.get_message("messages.navigation_menu"),
        reply_markup=NavigationMenu.get_main_navigation()
    )

@router.message(F.text == loc.get_message("buttons.characters"))
async def show_heroes(message: Message):
    await message.answer(
        loc.get_message("messages.select_hero_class"),
        reply_markup=NavigationMenu.get_heroes_menu()
    )

@router.message(F.text == loc.get_message("buttons.back_to_navigation"))
async def back_to_navigation(message: Message):
    await message.answer(
        loc.get_message("messages.navigation_menu"),
        reply_markup=NavigationMenu.get_main_navigation()
    )

# handlers/profile_handlers.py
@router.message(F.text == loc.get_message("buttons.statistics"))
async def show_statistics(message: Message):
    # Тут можна додати логіку отримання реальної статистики
    stats = {
        "games": 0,
        "wins": 0,
        "winrate": 0
    }
    
    await message.answer(
        loc.get_message("messages.statistics_info").format(
            games=stats["games"],
            wins=stats["wins"],
            winrate=stats["winrate"]
        ),
        reply_markup=ProfileMenu.get_profile_menu()
    )
