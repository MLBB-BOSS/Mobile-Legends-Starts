from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.profile_menu import ProfileMenu
from keyboards.hero_menu import HeroMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == loc.get_message("buttons.navigation"))
async def show_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню навігації")
    try:
        await message.answer(
            loc.get_message("messages.navigation_menu"),
            reply_markup=NavigationMenu().get_main_navigation()
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні меню навігації: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.profile"))
async def show_profile(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив особистий кабінет")
    try:
        await message.answer(
            loc.get_message("messages.profile_menu"),
            reply_markup=ProfileMenu().get_profile_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні особистого кабінету: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.back"))
async def handle_back(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до головного меню")
    try:
        await message.answer(
            loc.get_message("messages.menu_welcome"),
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при поверненні до головного меню: {e}")
        await message.answer(loc.get_message("errors.general"))

@router.message(F.text == loc.get_message("buttons.back_to_navigation"))
async def back_to_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню навігації")
    try:
        await message.answer(
            loc.get_message("messages.navigation_menu"),
            reply_markup=NavigationMenu().get_main_navigation()
        )
    except Exception as e:
        logger.error(f"Помилка при поверненні до меню навігації: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.statistics"))
async def show_statistics(message: Message):
    logger.info(f"Користувач {message.from_user.id} переглядає статистику")
    try:
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
    except Exception as e:
        logger.error(f"Помилка при відображенні статистики: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.achievements"))
async def show_achievements(message: Message):
    logger.info(f"Користувач {message.from_user.id} переглядає досягнення")
    try:
        await message.answer(
            loc.get_message("messages.achievements_menu"),
            reply_markup=ProfileMenu().get_profile_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні досягнень: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

# Реалізація для кнопки "Персонажі" з вибором класу та героя
@router.message(F.text == loc.get_message("buttons.characters"))
async def show_hero_classes(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню класів героїв")
    try:
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні меню класів героїв: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.callback_query(lambda c: c.data.startswith('hero_class_'))
async def process_hero_class_selection(callback: CallbackQuery):
    class_key = callback.data.replace('hero_class_', '')
    logger.info(f"Користувач {callback.from_user.id} вибрав клас героя: {class_key}")
    try:
        class_name = loc.get_message(f"heroes.classes.{class_key}.name")
        await callback.message.edit_text(
            loc.get_message("messages.select_hero").format(class_name=class_name),
            reply_markup=HeroMenu().get_heroes_by_class(class_key)
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні героїв класу {class_key}: {e}")
        await callback.message.edit_text(
            loc.get_message("errors.general"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )

@router.callback_query(lambda c: c.data.startswith('hero_select_'))
async def process_hero_selection(callback: CallbackQuery):
    hero_id = callback.data.replace('hero_select_', '')
    logger.info(f"Користувач {callback.from_user.id} вибрав героя: {hero_id}")
    try:
        hero_info = loc.get_message(f"heroes.info.{hero_id}")
        await callback.message.edit_text(
            hero_info,
            reply_markup=HeroMenu().get_hero_details_menu(hero_id)
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні інформації про героя {hero_id}: {e}")
        await callback.message.edit_text(
            loc.get_message("errors.hero_not_found"),
            reply_markup=HeroMenu().get_heroes_by_class(HeroMenu().get_class_from_hero(hero_id))
        )

@router.callback_query(lambda c: c.data == 'back_to_hero_classes')
async def back_to_hero_classes(callback: CallbackQuery):
    logger.info(f"Користувач {callback.from_user.id} повертається до вибору класів героїв")
    try:
        await callback.message.edit_text(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при поверненні до меню класів героїв: {e}")
        await callback.message.edit_text(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.callback_query(lambda c: c.data == 'back_to_hero_list')
async def back_to_hero_list(callback: CallbackQuery):
    logger.info(f"Користувач {callback.from_user.id} повертається до списку героїв")
    try:
        class_key = HeroMenu().get_class_from_hero(callback.message)
        class_name = loc.get_message(f"heroes.classes.{class_key}.name")
        await callback.message.edit_text(
            loc.get_message("messages.select_hero").format(class_name=class_name),
            reply_markup=HeroMenu().get_heroes_by_class(class_key)
        )
    except Exception as e:
        logger.error(f"Помилка при поверненні до списку героїв: {e}")
        await callback.message.edit_text(
            loc.get_message("errors.general"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )
