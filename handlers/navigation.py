from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import (
    get_navigation_keyboard,
    get_characters_keyboard,
    get_guides_keyboard,
    get_counterpicks_keyboard,
    get_builds_keyboard,
    get_voting_keyboard,
    get_help_keyboard
)
from keyboards.main_menu import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🧭 Навігація")
async def show_navigation(message: Message):
    logger.info(f"Entering show_navigation handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} opened navigation menu")
        await message.answer(
            "Оберіть розділ навігації:",
            reply_markup=get_navigation_keyboard()
        )
        logger.info(f"Navigation menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in navigation menu handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🛡️ Персонажі")
async def show_characters_menu(message: Message):
    logger.info(f"Entering show_characters_menu handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} selected 'Персонажі'")
        await message.answer(
            "Оберіть тип героя:",
            reply_markup=get_characters_keyboard()
        )
        logger.info(f"Characters menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in characters menu handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "📖 Гайди")
async def show_guides(message: Message):
    logger.info(f"Entering show_guides handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} selected 'Гайди'")
        await message.answer(
            "Оберіть розділ гайдів:",
            reply_markup=get_guides_keyboard()
        )
        logger.info(f"Guides menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in guides handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "⚔️ Контр-піки")
async def show_counterpicks(message: Message):
    logger.info(f"Entering show_counterpicks handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} selected 'Контр-піки'")
        await message.answer(
            "Оберіть опцію контр-піків:",
            reply_markup=get_counterpicks_keyboard()
        )
        logger.info(f"Counterpicks menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in counterpicks handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🛠️ Білди")
async def show_builds(message: Message):
    logger.info(f"Entering show_builds handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} selected 'Білди'")
        await message.answer(
            "Оберіть опцію білдів:",
            reply_markup=get_builds_keyboard()
        )
        logger.info(f"Builds menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in builds handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "📊 Голосування")
async def show_voting(message: Message):
    logger.info(f"Entering show_voting handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} selected 'Голосування'")
        await message.answer(
            "Оберіть опцію голосування:",
            reply_markup=get_voting_keyboard()
        )
        logger.info(f"Voting menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in voting handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "❓ Допомога")
async def show_help(message: Message):
    logger.info(f"Entering show_help handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} selected 'Допомога'")
        await message.answer(
            "Оберіть розділ допомоги:",
            reply_markup=get_help_keyboard()
        )
        logger.info(f"Help menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in help handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text.in_({"🔙 Назад до Головного", "🔙 Назад"}))
async def return_to_main_menu(message: Message):
    logger.info(f"Entering return_to_main_menu handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} returned to main menu")
        await message.answer(
            "Головне меню:",
            reply_markup=get_main_keyboard()
        )
        logger.info(f"Main menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in return to main menu handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "◀️ Назад до Навігації")
async def return_to_navigation(message: Message):
    logger.info(f"Entering return_to_navigation handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} returned to navigation menu")
        await message.answer(
            "Меню навігації:",
            reply_markup=get_navigation_keyboard()
        )
        logger.info(f"Navigation menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in return to navigation handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🎵 MP3 Плеєр")
async def show_mp3_player(message: Message):
    logger.info(f"Entering show_mp3_player handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        logger.info(f"User {message.from_user.id} selected 'MP3 Плеєр'")
        await message.answer(
            "MP3 Плеєр у розробці.\nТут буде функціонал для відтворення музики.",
            reply_markup=get_navigation_keyboard()
        )
        logger.info(f"MP3 player menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in MP3 player handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

# Обробники для підменю персонажів
@router.message(F.text.in_({
    "🗡️ Бійці", "🏹 Стрільці", "🔮 Маги",
    "🛡️ Танки", "🏥 Саппорти", "⚔️ Гібриди",
    "🔥 Метові"
}))
async def handle_character_type(message: Message):
    logger.info(f"Entering handle_character_type handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        hero_type = message.text
        logger.info(f"User {message.from_user.id} selected hero type: {hero_type}")
        
        # Тут буде додана логіка для кожного типу героїв
        await message.answer(
            f"Розділ {hero_type} у розробці.\nТут буде список героїв цього типу.",
            reply_markup=get_characters_keyboard()
        )
        logger.info(f"Character type {hero_type} menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in hero type handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

# Обробники для підменю гайдів
@router.message(F.text.in_({
    "🆕 Нові гайди", "🌟 Популярні гайди",
    "📘 Для початківців", "🧙 Просунуті техніки",
    "🛡️ Командні стратегії"
}))
async def handle_guide_type(message: Message):
    logger.info(f"Entering handle_guide_type handler for user {message.from_user.id}")
    try:
        if not message or not message.from_user:
            raise ValueError("Invalid message or user data")
        guide_type = message.text
        logger.info(f"User {message.from_user.id} selected guide type: {guide_type}")
        
        await message.answer(
            f"Розділ {guide_type} у розробці.\nТут будуть відповідні гайди.",
            reply_markup=get_guides_keyboard()
        )
        logger.info(f"Guide type {guide_type} menu displayed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in guide type handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

# Додамо інші обробники для підменю по мірі їх розробки...
