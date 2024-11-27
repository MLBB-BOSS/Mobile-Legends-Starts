# handlers.py

import logging
from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.menus import (
    MenuButton,
    menu_button_to_class,
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_profile_menu,
    get_hero_class_menu,
    heroes_by_class,
)

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Створюємо роутер
router = Router()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обробник команди /start.
    Відправляє привітальне повідомлення та показує головне меню.
    """
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await message.answer(
        f"👋 Вітаємо, {user_name}, у Mobile Legends Tournament Bot!\n\n"
        "🎮 Цей бот допоможе вам:\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення\n\n"
        "Оберіть опцію з меню нижче 👇",
        reply_markup=get_main_menu(),
    )

# Обробники для Reply Keyboard (Головне меню)
@router.message(F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu(),
    )

@router.message(F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu(),
    )

# Callback Query Handlers
@router.callback_query(Text(startswith="navigate_"))
async def handle_navigation(callback_query: CallbackQuery):
    action = callback_query.data.split("_")[1]
    logger.info(f"Користувач {callback_query.from_user.id} обрав Навігацію -> {action}")
    
    if action == "heroes":
        await callback_query.message.edit_text(
            "Виберіть категорію героїв:",
            reply_markup=get_heroes_menu()
        )
    elif action == "guides":
        await callback_query.message.edit_text(
            "Виберіть гайди:",
            reply_markup=get_guides_menu()
        )
    elif action == "counter":
        await callback_query.message.edit_text(
            "Виберіть контр-піки:",
            reply_markup=get_counter_picks_menu()
        )
    elif action == "builds":
        await callback_query.message.edit_text(
            "Виберіть білди:",
            reply_markup=get_builds_menu()
        )
    elif action == "voting":
        await callback_query.message.edit_text(
            "Виберіть опцію голосування:",
            reply_markup=get_voting_menu()
        )
    elif action == "back":
        await callback_query.message.edit_text(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu()
        )
    await callback_query.answer()  # Відповідь для Callback Query

@router.callback_query(Text(startswith="heroes_"))
async def handle_heroes(callback_query: CallbackQuery):
    action = callback_query.data.split("_")[1]
    logger.info(f"Користувач {callback_query.from_user.id} обрав Персонажі -> {action}")
    
    if action == "back":
        await callback_query.message.edit_text(
            "Виберіть опцію навігації:",
            reply_markup=get_navigation_menu()
        )
    else:
        # Перевірка, чи це клас героїв
        hero_class = menu_button_to_class.get(MenuButton(action).value, None)
        if hero_class:
            await callback_query.message.edit_text(
                f"Виберіть героя з класу **{hero_class}**:",
                parse_mode="Markdown",
                reply_markup=get_hero_class_menu(hero_class)
            )
        else:
            # Якщо це конкретний герой
            await callback_query.message.edit_text(
                f"Ви обрали героя **{action}**. Інформація про героя буде додана пізніше.",
                parse_mode="Markdown",
                reply_markup=get_main_menu()
            )
    await callback_query.answer()

@router.callback_query(Text(startswith="guides_"))
async def handle_guides(callback_query: CallbackQuery):
    action = callback_query.data.split("_")[1]
    logger.info(f"Користувач {callback_query.from_user.id} обрав Гайди -> {action}")
    
    if action == "back":
        await callback_query.message.edit_text(
            "Виберіть опцію навігації:",
            reply_markup=get_navigation_menu()
        )
    else:
        # Обробка різних типів гайдів
        await callback_query.message.edit_text(
            f"Ви обрали гайди: **{action.replace('_', ' ').title()}**.",
            parse_mode="Markdown",
            reply_markup=get_guides_menu()
        )
    await callback_query.answer()

@router.callback_query(Text(startswith="counter_"))
async def handle_counter_picks(callback_query: CallbackQuery):
    action = callback_query.data.split("_")[1]
    logger.info(f"Користувач {callback_query.from_user.id} обрав Контр-піки -> {action}")
    
    if action == "back":
        await callback_query.message.edit_text(
            "Виберіть опцію навігації:",
            reply_markup=get_navigation_menu()
        )
    else:
        # Обробка різних типів контр-піків
        await callback_query.message.edit_text(
            f"Ви обрали контр-піки: **{action.replace('_', ' ').title()}**.",
            parse_mode="Markdown",
            reply_markup=get_counter_picks_menu()
        )
    await callback_query.answer()

@router.callback_query(Text(startswith="builds_"))
async def handle_builds(callback_query: CallbackQuery):
    action = callback_query.data.split("_")[1]
    logger.info(f"Користувач {callback_query.from_user.id} обрав Білди -> {action}")
    
    if action == "back":
        await callback_query.message.edit_text(
            "Виберіть опцію навігації:",
            reply_markup=get_navigation_menu()
        )
    else:
        # Обробка різних типів білів
        await callback_query.message.edit_text(
            f"Ви обрали білди: **{action.replace('_', ' ').title()}**.",
            parse_mode="Markdown",
            reply_markup=get_builds_menu()
        )
    await callback_query.answer()

@router.callback_query(Text(startswith="voting_"))
async def handle_voting(callback_query: CallbackQuery):
    action = callback_query.data.split("_")[1]
    logger.info(f"Користувач {callback_query.from_user.id} обрав Голосування -> {action}")
    
    if action == "back":
        await callback_query.message.edit_text(
            "Виберіть опцію навігації:",
            reply_markup=get_navigation_menu()
        )
    else:
        # Обробка різних типів голосувань
        await callback_query.message.edit_text(
            f"Ви обрали голосування: **{action.replace('_', ' ').title()}**.",
            parse_mode="Markdown",
            reply_markup=get_voting_menu()
        )
    await callback_query.answer()

@router.callback_query(Text(startswith="profile_"))
async def handle_profile(callback_query: CallbackQuery):
    action = callback_query.data.split("_")[1]
    logger.info(f"Користувач {callback_query.from_user.id} обрав Профіль -> {action}")
    
    if action == "back":
        await callback_query.message.edit_text(
            "Виберіть опцію профілю:",
            reply_markup=get_profile_menu()
        )
    else:
        # Обробка різних аспектів профілю
        await callback_query.message.edit_text(
            f"Ви обрали: **{action.replace('_', ' ').title()}**.",
            parse_mode="Markdown",
            reply_markup=get_profile_menu()
        )
    await callback_query.answer()

@router.callback_query(Text(startswith="hero_"))
async def handle_hero_selection(callback_query: CallbackQuery):
    hero_name = callback_query.data.split("_")[1]
    logger.info(f"Користувач {callback_query.from_user.id} обрав героя {hero_name}")
    # Тут можна додати логіку для відображення інформації про героя
    await callback_query.message.edit_text(
        f"Ви обрали героя **{hero_name}**. Інформація про героя буде додана пізніше.",
        parse_mode="Markdown",
        reply_markup=get_navigation_menu()
    )
    await callback_query.answer()

# Обробники для кнопок "Назад" у різних меню
@router.callback_query(Text(equals="navigate_back"))
async def handle_navigation_back(callback_query: CallbackQuery):
    logger.info(f"Користувач {callback_query.from_user.id} повернувся до головного меню")
    await callback_query.message.edit_text(
        "🔙 Повернення до головного меню:",
        reply_markup=get_main_menu()
    )
    await callback_query.answer()

@router.callback_query(Text(equals="heroes_back"))
async def handle_heroes_back(callback_query: CallbackQuery):
    logger.info(f"Користувач {callback_query.from_user.id} повернувся до меню Персонажів")
    await callback_query.message.edit_text(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu()
    )
    await callback_query.answer()

@router.callback_query(Text(equals="guides_back"))
async def handle_guides_back(callback_query: CallbackQuery):
    logger.info(f"Користувач {callback_query.from_user.id} повернувся до меню Гайди")
    await callback_query.message.edit_text(
        "Виберіть гайди:",
        reply_markup=get_guides_menu()
    )
    await callback_query.answer()

@router.callback_query(Text(equals="counter_back"))
async def handle_counter_back(callback_query: CallbackQuery):
    logger.info(f"Користувач {callback_query.from_user.id} повернувся до меню Контр-піки")
    await callback_query.message.edit_text(
        "Виберіть контр-піки:",
        reply_markup=get_counter_picks_menu()
    )
    await callback_query.answer()

@router.callback_query(Text(equals="builds_back"))
async def handle_builds_back(callback_query: CallbackQuery):
    logger.info(f"Користувач {callback_query.from_user.id} повернувся до меню Білди")
    await callback_query.message.edit_text(
        "Виберіть білди:",
        reply_markup=get_builds_menu()
    )
    await callback_query.answer()

@router.callback_query(Text(equals="voting_back"))
async def handle_voting_back(callback_query: CallbackQuery):
    logger.info(f"Користувач {callback_query.from_user.id} повернувся до меню Голосування")
    await callback_query.message.edit_text(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu()
    )
    await callback_query.answer()

@router.callback_query(Text(equals="profile_back"))
async def handle_profile_back(callback_query: CallbackQuery):
    logger.info(f"Користувач {callback_query.from_user.id} повернувся до меню Профіль")
    await callback_query.message.edit_text(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu()
    )
    await callback_query.answer()

# Обробник для невідомих Callback Queries
@router.callback_query()
async def unknown_callback(callback_query: CallbackQuery):
    logger.warning(f"Невідома Callback Query від {callback_query.from_user.id}: {callback_query.data}")
    await callback_query.answer("❗ Невідома дія.", show_alert=True)
