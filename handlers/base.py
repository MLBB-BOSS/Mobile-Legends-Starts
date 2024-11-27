# handlers.py

import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command, Text
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

def setup_handlers(dp: Dispatcher):
    # Команда /start
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
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
    @dp.message_handler(lambda message: message.text == MenuButton.NAVIGATION.value)
    async def cmd_navigation(message: types.Message):
        logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
        await message.answer(
            "Виберіть опцію навігації:",
            reply_markup=get_navigation_menu(),
        )

    @dp.message_handler(lambda message: message.text == MenuButton.PROFILE.value)
    async def cmd_profile(message: types.Message):
        logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
        await message.answer(
            "Виберіть опцію профілю:",
            reply_markup=get_profile_menu(),
        )

    # Callback Query Handlers
    @dp.callback_query_handler(lambda call: call.data.startswith("navigate_"))
    async def handle_navigation(callback_query: types.CallbackQuery):
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
        await callback_query.answer()

    @dp.callback_query_handler(lambda call: call.data.startswith("heroes_"))
    async def handle_heroes(callback_query: types.CallbackQuery):
        action = callback_query.data.split("_")[1]
        logger.info(f"Користувач {callback_query.from_user.id} обрав Персонажі -> {action}")

        if action == "back":
            await callback_query.message.edit_text(
                "Виберіть опцію навігації:",
                reply_markup=get_navigation_menu()
            )
        elif action == "search":
            await callback_query.answer("Пошук персонажа поки недоступний.", show_alert=True)
        else:
            # Перевірка, чи це клас героїв
            hero_class = None
            for key, value in menu_button_to_class.items():
                if action == key.lower():
                    hero_class = value
                    break
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

    @dp.callback_query_handler(lambda call: call.data.startswith("guides_"))
    async def handle_guides(callback_query: types.CallbackQuery):
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

    @dp.callback_query_handler(lambda call: call.data.startswith("counter_"))
    async def handle_counter_picks(callback_query: types.CallbackQuery):
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

    @dp.callback_query_handler(lambda call: call.data.startswith("builds_"))
    async def handle_builds(callback_query: types.CallbackQuery):
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

    @dp.callback_query_handler(lambda call: call.data.startswith("voting_"))
    async def handle_voting(callback_query: types.CallbackQuery):
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

    @dp.callback_query_handler(lambda call: call.data.startswith("profile_"))
    async def handle_profile(callback_query: types.CallbackQuery):
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

    @dp.callback_query_handler(lambda call: call.data.startswith("hero_"))
    async def handle_hero_selection(callback_query: types.CallbackQuery):
        hero_name = callback_query.data.split("_")[1]
        logger.info(f"Користувач {callback_query.from_user.id} обрав героя {hero_name}")
        # Тут можна додати логіку для відображення інформації про героя
        await callback_query.message.edit_text(
            f"Ви обрали героя **{hero_name}**. Інформація про героя буде додана пізніше.",
            parse_mode="Markdown",
            reply_markup=get_navigation_menu()
        )
        await callback_query.answer()

    # Обробник для невідомих Callback Queries
    @dp.callback_query_handler()
    async def unknown_callback(callback_query: types.CallbackQuery):
        logger.warning(f"Невідома Callback Query від {callback_query.from_user.id}: {callback_query.data}")
        await callback_query.answer("❗ Невідома дія.", show_alert=True)

    # Обробник для невідомих повідомлень
    @dp.message_handler()
    async def unknown_command(message: types.Message):
        logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
        await message.answer(
            "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
            reply_markup=get_main_menu(),
        )
