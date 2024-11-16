from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import NavigationMenu, ProfileMenu
import logging

router = Router()
logger = logging.getLogger(__name__)

# Обробники для кнопок першого рівня
@router.message(F.text == "🧭 Навігація")
async def show_navigation_menu(message: Message):
    try:
        keyboard = NavigationMenu.get_navigation_menu()
        await message.answer(
            "Оберіть розділ навігації:",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні меню навігації: {e}")
        await message.answer("Вибачте, сталася помилка.")

@router.message(F.text == "🪧 Мій Кабінет")
async def show_profile_menu(message: Message):
    try:
        keyboard = ProfileMenu.get_profile_menu()
        await message.answer(
            "Ваш особистий кабінет:",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні особистого кабінету: {e}")
        await message.answer("Вибачте, сталася помилка.")

# Обробники для кнопок навігаційного меню
@router.callback_query(F.data == "guides")
async def show_guides(callback: CallbackQuery):
    await callback.answer("Розділ гайдів у розробці")

@router.callback_query(F.data == "heroes")
async def show_heroes(callback: CallbackQuery):
    await callback.answer("Розділ героїв у розробці")

@router.callback_query(F.data == "counter_picks")
async def show_counter_picks(callback: CallbackQuery):
    await callback.answer("Розділ контр-піків у розробці")

@router.callback_query(F.data == "builds")
async def show_builds(callback: CallbackQuery):
    await callback.answer("Розділ збірок у розробці")

@router.callback_query(F.data == "voting")
async def show_voting(callback: CallbackQuery):
    await callback.answer("Розділ голосування у розробці")

# Обробники для кнопок особистого кабінету
@router.callback_query(F.data == "statistics")
async def show_statistics(callback: CallbackQuery):
    await callback.answer("Розділ статистики у розробці")

@router.callback_query(F.data == "achievements")
async def show_achievements(callback: CallbackQuery):
    await callback.answer("Розділ досягнень у розробці")

@router.callback_query(F.data == "settings")
async def show_settings(callback: CallbackQuery):
    await callback.answer("Розділ налаштувань у розробці")

# Загальний обробник для кнопки "Назад"
@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    try:
        await callback.message.delete()  # Видаляємо повідомлення з inline клавіатурою
        await callback.message.answer(
            "Головне меню:",
            reply_markup=MainMenu.get_main_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при поверненні до головного меню: {e}")
        await callback.answer("Вибачте, сталася помилка")
