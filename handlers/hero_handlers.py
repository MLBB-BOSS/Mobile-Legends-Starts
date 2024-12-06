# handlers/hero_handlers.py
import logging
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import MenuStates

from keyboards.menus import (
    MenuButton,
    menu_button_to_class,
    get_heroes_menu,
    get_hero_class_menu,
    heroes_by_class
)
from keyboards.inline_menus import get_generic_inline_keyboard
from texts import (
    MAIN_MENU_ERROR_TEXT,
    HEROES_MENU_TEXT,
    HEROES_INTERACTIVE_TEXT,
    HERO_CLASS_MENU_TEXT,
    HERO_CLASS_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT,
    SEARCH_HERO_RESPONSE_TEXT,
    NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT
)
from aiogram import types
import os
import json

logger = logging.getLogger(__name__)
hero_router = Router()

def load_hero_details(hero_name: str) -> str:
    """
    Завантажує інформацію про героя з JSON-файлу або повертає шаблонний текст.
    Припустимо, що файли зберігаються у папці 'heroes_data/',
    іменуються за шаблоном hero_name.lower() + '.json'.
    """
    file_path = os.path.join("heroes_data", f"{hero_name.lower()}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Припустимо, в JSON є поля "name", "class", "role", "skills" тощо.
        # Формуємо текстове представлення
        info = f"Інформація про героя: {data['name']}\nКлас: {data.get('class','N/A')}\n"
        if "skills" in data:
            info += "Скілли:\n"
            for skill in data["skills"]:
                info += f" - {skill['name']}: {skill['description']}\n"
        return info
    else:
        # Якщо файл не знайдено, повертаємо дефолтний текст
        return f"Інформація про героя: {hero_name}\nДетальні дані відсутні."

@hero_router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Персонажі")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_heroes_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    hero_classes = [
        MenuButton.TANK.value,
        MenuButton.MAGE.value,
        MenuButton.MARKSMAN.value,
        MenuButton.ASSASSIN.value,
        MenuButton.SUPPORT.value,
        MenuButton.FIGHTER.value
    ]

    if user_choice in hero_classes:
        # Користувач обрав клас героїв
        hero_class = menu_button_to_class.get(user_choice)
        new_main_text = HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class)
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name="")
        new_main_keyboard = types.ReplyKeyboardRemove()
        new_interactive_text = "Пошук героя"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "Функція порівняння героїв ще в розробці."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Порівняння героїв"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        from keyboards.menus import get_navigation_menu
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        # Якщо раніше було вибрано клас, ми можемо його використати, якщо ні - дефолт.
        hero_class = data.get('hero_class', 'Танк')
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HEROES_MENU

    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

@hero_router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    data = await state.get_data()
    hero_class = data.get('hero_class', 'Танк')

    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню класу {hero_class}")

    await message.delete()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        from keyboards.menus import get_main_menu
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    heroes_list = heroes_by_class.get(hero_class, [])

    if user_choice == MenuButton.BACK.value:
        # Повертаємось до меню Персонажі
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    elif user_choice in heroes_list:
        # Користувач обрав конкретного героя
        hero_info = load_hero_details(user_choice)
        new_main_text = hero_info
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU

    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)
