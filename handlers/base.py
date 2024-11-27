# handlers/base.py

import logging
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.menus import (
    MenuButton,
    menu_button_to_class,
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_hero_class_menu,
    get_profile_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu,
    heroes_by_class,
)

from keyboards.inline_menus import get_guides_inline_menu

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = Router()

# Визначаємо стани меню
class MenuStates(StatesGroup):
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    GUIDES_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
    PROFILE_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    SETTINGS_MENU = State()
    FEEDBACK_MENU = State()
    HELP_MENU = State()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await state.set_state(MenuStates.MAIN_MENU)
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

# Головне Меню
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu(),
    )

@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu(),
    )

# Розділ "Навігація"
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await state.set_state(MenuStates.HEROES_MENU)
    await message.answer(
        "Виберіть категорію героїв:",
        reply_markup=get_heroes_menu(),
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await state.set_state(MenuStates.GUIDES_MENU)
    sent_message = await message.answer(
        "📝 **Гайди**\n\nОберіть одну з опцій нижче:",
        reply_markup=get_guides_inline_menu(),
        parse_mode="Markdown"
    )
    await state.update_data(last_message_id=sent_message.message_id)

# Обробник для інлайн-кнопок у розділі "Гайди"
@router.callback_query(MenuStates.GUIDES_MENU, F.data.startswith("guide_"))
async def callback_guides(call: types.CallbackQuery, state: FSMContext):
    action = call.data
    logger.info(f"Користувач {call.from_user.id} натиснув {action}")

    if action == "guide_new":
        new_text = "🆕 **Нові Гайди**\n\nСписок нових гайдів:"
    elif action == "guide_popular":
        new_text = "🌟 **Популярні Гайди**\n\nСписок популярних гайдів:"
    elif action == "guide_beginner":
        new_text = "📘 **Гайди для Початківців**\n\nПоради та рекомендації для новачків:"
    elif action == "guide_advanced":
        new_text = "🧙 **Просунуті Техніки**\n\nДетальні гайди для досвідчених гравців:"
    elif action == "guide_teamplay":
        new_text = "🛡️ **Командна Гра**\n\nСтратегії та тактики командної гри:"
    else:
        new_text = "❗ Невідома дія."

    await call.message.edit_text(
        new_text,
        reply_markup=get_guides_inline_menu(),
        parse_mode="Markdown"
    )
    await call.answer()

# Обробник для кнопки "Назад" в інлайн-кнопках
@router.callback_query(MenuStates.GUIDES_MENU, F.data == "back_to_navigation")
async def callback_back_to_navigation(call: types.CallbackQuery, state: FSMContext):
    logger.info(f"Користувач {call.from_user.id} натиснув Назад в гайдах")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await call.message.delete()
    await call.message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu()
    )
    await call.answer()

# Розділ "Персонажі" залишаємо без змін, якщо вам не потрібно додавати інлайн-кнопки

# Кнопка "Назад" універсальна
@router.message(F.text == MenuButton.BACK.value)
async def cmd_back(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == MenuStates.NAVIGATION_MENU.state:
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu(),
        )
    elif current_state in [
        MenuStates.HEROES_MENU.state,
        # MenuStates.GUIDES_MENU.state,  # Видалено, оскільки ми використовуємо інлайн-кнопку "Назад"
        # Інші стани...
    ]:
        await state.set_state(MenuStates.NAVIGATION_MENU)
        await message.answer(
            "🔙 Повернення до меню Навігація:",
            reply_markup=get_navigation_menu(),
        )
    elif current_state == MenuStates.PROFILE_MENU.state:
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu(),
        )
    # Додайте інші умови, якщо потрібно

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    if current_state == MenuStates.MAIN_MENU.state:
        reply_markup = get_main_menu()
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        reply_markup = get_navigation_menu()
    elif current_state == MenuStates.HEROES_MENU.state:
        reply_markup = get_heroes_menu()
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        data = await state.get_data()
        hero_class = data.get('hero_class', 'Танк')
        reply_markup = get_hero_class_menu(hero_class)
    elif current_state == MenuStates.PROFILE_MENU.state:
        reply_markup = get_profile_menu()
    else:
        reply_markup = get_main_menu()
        await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
        reply_markup=reply_markup,
    )

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
