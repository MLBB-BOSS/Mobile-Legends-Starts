# handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import MainMenu
from keyboards.hero_menu import HeroMenu
from utils.localization import loc  # Імпортуємо глобальний екземпляр
import logging

logger = logging.getLogger(__name__)
router = Router()

# Визначення станів FSM
class HeroStates(StatesGroup):
    SelectingClass = State()
    SelectingHero = State()

@router.message(F.text == loc.get_message("buttons.back_to_hero_classes"))
async def back_to_hero_classes(message: Message, state: FSMContext):
    try:
        await state.set_state(HeroStates.SelectingClass)
        logger.info(f"User {message.from_user.id} set state to SelectingClass")
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu(locale=loc.locale).get_heroes_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка у back_to_hero_classes хендлері: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.back_to_hero_list"))
async def back_to_hero_list(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        selected_class = data.get("selected_class")
        if selected_class:
            await state.set_state(HeroStates.SelectingHero)
            logger.info(f"User {message.from_user.id} set state to SelectingHero for class {selected_class}")
            class_display_name = loc.get_message(f"heroes.classes.{selected_class}.name")
            await message.answer(
                loc.get_message("messages.hero_menu.select_hero").format(class_name=class_display_name),
                reply_markup=HeroMenu(locale=loc.locale).get_heroes_by_class(selected_class)
            )
        else:
            # Якщо клас не вибрано, повертаємося до вибору класу
            await back_to_hero_classes(message, state)
    except Exception as e:
        logger.exception(f"Помилка у back_to_hero_list хендлері: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text.in_(["Танк", "Бійці", "Асасини", "Маги", "Стрільці", "Підтримка"]))
async def select_hero_class(message: Message, state: FSMContext):
    try:
        # Знаходимо ключ класу за його назвою
        class_name = None
        for key, value in loc.messages["heroes"]["classes"].items():
            if value["name"] == message.text:
                class_name = key
                break

        if class_name:
            await state.update_data(selected_class=class_name)
            await state.set_state(HeroStates.SelectingHero)
            logger.info(f"User {message.from_user.id} selected class {class_name} and set state to SelectingHero")
            class_display_name = loc.get_message(f"heroes.classes.{class_name}.name")
            await message.answer(
                loc.get_message("messages.hero_menu.select_hero").format(class_name=class_display_name),
                reply_markup=HeroMenu(locale=loc.locale).get_heroes_by_class(class_name)
            )
        else:
            await message.answer(
                loc.get_message("messages.errors.class_not_found"),
                reply_markup=MainMenu().get_main_menu()
            )
    except Exception as e:
        logger.exception(f"Помилка у select_hero_class хендлері: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(HeroStates.SelectingHero)
async def select_hero(message: Message, state: FSMContext):
    try:
        selected_hero = message.text
        hero_info = loc.get_hero_info(selected_hero)
        if hero_info == loc.get_message("messages.errors.hero_not_found"):
            await message.answer(
                loc.get_message("messages.errors.hero_not_found"),
                reply_markup=HeroMenu(locale=loc.locale).get_heroes_by_class(state_data.get("selected_class"))
            )
        else:
            await message.answer(
                hero_info,
                reply_markup=MainMenu().get_main_menu()
            )
            logger.info(f"User {message.from_user.id} selected hero {selected_hero}")
            await state.clear()
    except Exception as e:
        logger.exception(f"Помилка у select_hero хендлері: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message()
async def unhandled_message(message: Message, state: FSMContext):
    logger.info(f"Отримано необроблене повідомлення: {message.text}")
    try:
        response_text = loc.get_message("messages.unhandled_message", message=message.text)
        await message.answer(
            response_text,
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відправці повідомлення: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )
