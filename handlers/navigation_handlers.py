# handlers/navigation_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import NavigationMenu
from keyboards.main_menu import MainMenu
from keyboards.profile_menu import ProfileMenu
from utils.localization import loc

router = Router()

@router.message(F.text == loc.get_message("buttons.navigation"))
async def show_navigation(message: Message):
    await message.answer(
        loc.get_message("messages.navigation_menu"),
        reply_markup=NavigationMenu().get_main_navigation()
    )

@router.message(F.text == loc.get_message("buttons.characters"))
async def show_heroes(message: Message):
    await message.answer(
        loc.get_message("messages.select_hero_class"),
        reply_markup=NavigationMenu().get_heroes_menu()
    )

@router.message(F.text == loc.get_message("buttons.back"))
async def handle_back(message: Message):
    await message.answer(
        loc.get_message("messages.menu_welcome"),
        reply_markup=MainMenu().get_main_menu()
    )

@router.message(F.text == loc.get_message("buttons.back_to_navigation"))
async def back_to_navigation(message: Message):
    await message.answer(
        loc.get_message("messages.navigation_menu"),
        reply_markup=NavigationMenu().get_main_navigation()
    )

@router.message(F.text == loc.get_message("buttons.guides"))
async def show_guides(message: Message):
    await message.answer(
        loc.get_message("messages.guides_menu"),
        reply_markup=NavigationMenu().get_guides_menu()
    )

@router.message(F.text == loc.get_message("buttons.counter_picks"))
async def show_counter_picks(message: Message):
    await message.answer(
        loc.get_message("messages.counter_picks_menu"),
        reply_markup=NavigationMenu().get_counter_picks_menu()
    )

@router.message(F.text == loc.get_message("buttons.builds"))
async def show_builds(message: Message):
    await message.answer(
        loc.get_message("messages.builds_menu"),
        reply_markup=NavigationMenu().get_builds_menu()
    )

@router.message(F.text == loc.get_message("buttons.voting"))
async def show_voting(message: Message):
    await message.answer(
        loc.get_message("messages.voting_menu"),
        reply_markup=NavigationMenu().get_voting_menu()
    )

@router.message(F.text == loc.get_message("buttons.statistics"))
async def show_statistics(message: Message):
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
        reply_markup=ProfileMenu().get_profile_menu()
    )

# Обробник помилок
@router.errors()
async def handle_errors(update: Message, exception: Exception):
    await update.answer(
        loc.get_message("errors.general"),
        reply_markup=MainMenu().get_main_menu()
    )
