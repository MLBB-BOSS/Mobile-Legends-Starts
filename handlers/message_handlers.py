from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import MainMenu
from keyboards.hero_menu import HeroMenu
from utils.localization import LocalizationManager
import logging

logger = logging.getLogger(__name__)
router = Router()

# Define FSM States
class HeroStates(StatesGroup):
    SelectingClass = State()
    SelectingHero = State()

# Function to get user locale (implement as needed)
def get_user_locale(user_id: int) -> str:
    # Example: Fetch from database or default to 'uk'
    return 'uk'

@router.message()
async def handle_messages(message: Message, state: FSMContext):
    user_locale = get_user_locale(message.from_user.id)
    loc = LocalizationManager(locale=user_locale)

    if message.text == loc.get_message("buttons.back_to_hero_classes"):
        await back_to_hero_classes(message, state, loc)
    elif message.text == loc.get_message("buttons.back_to_hero_list"):
        await back_to_hero_list(message, state, loc)
    elif message.text in loc.messages.get("heroes", {}).get("classes", {}).keys():
        await select_hero_class(message, state, loc)
    elif await state.get_state() == HeroStates.SelectingHero.state and message.text in loc.messages.get("heroes", {}).get("info", {}).keys():
        await select_hero(message, state, loc)
    else:
        await unhandled_message(message, state, loc)

async def back_to_hero_classes(message: Message, state: FSMContext, loc: LocalizationManager):
    try:
        await state.set_state(HeroStates.SelectingClass)
        logger.info(f"User {message.from_user.id} set state to SelectingClass")
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu(locale=loc.locale).get_heroes_menu()
        )
    except Exception as e:
        logger.exception(f"Error in back_to_hero_classes handler: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

async def back_to_hero_list(message: Message, state: FSMContext, loc: LocalizationManager):
    try:
        data = await state.get_data()
        selected_class = data.get("selected_class")
        if selected_class:
            await state.set_state(HeroStates.SelectingHero)
            logger.info(f"User {message.from_user.id} set state to SelectingHero for class {selected_class}")
            await message.answer(
                loc.get_message("messages.hero_menu.select_hero").format(class_name=loc.get_message(f"heroes.classes.{selected_class.lower()}.name")),
                reply_markup=HeroMenu(locale=loc.locale).get_heroes_by_class(selected_class.lower())
            )
        else:
            # If no class selected, go back to classes menu
            await back_to_hero_classes(message, state, loc)
    except Exception as e:
        logger.exception(f"Error in back_to_hero_list handler: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

async def select_hero_class(message: Message, state: FSMContext, loc: LocalizationManager):
    try:
        selected_class = message.text.lower()  # Ensure class names are lowercase to match JSON keys
        if selected_class in loc.messages.get("heroes", {}).get("classes", {}):
            await state.update_data(selected_class=selected_class)
            await state.set_state(HeroStates.SelectingHero)
            logger.info(f"User {message.from_user.id} selected class {selected_class} and set state to SelectingHero")
            class_display_name = loc.get_message(f"heroes.classes.{selected_class}.name")
            await message.answer(
                loc.get_message("messages.hero_menu.select_hero").format(class_name=class_display_name),
                reply_markup=HeroMenu(locale=loc.locale).get_heroes_by_class(selected_class)
            )
        else:
            await message.answer(
                loc.get_message("errors.class_not_found"),
                reply_markup=MainMenu().get_main_menu()
            )
    except Exception as e:
        logger.exception(f"Error in select_hero_class handler: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

async def select_hero(message: Message, state: FSMContext, loc: LocalizationManager):
    try:
        selected_hero = message.text
        hero_info = loc.get_hero_info(selected_hero)
        if hero_info == loc.get_message("errors.hero_not_found"):
            await message.answer(
                loc.get_message("errors.hero_not_found"),
                reply_markup=HeroMenu(locale=loc.locale).get_heroes_by_class(selected_class.lower())
            )
        else:
            await message.answer(
                hero_info,
                reply_markup=MainMenu().get_main_menu()
            )
            logger.info(f"User {message.from_user.id} selected hero {selected_hero}")
            await state.clear()
    except Exception as e:
        logger.exception(f"Error in select_hero handler: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

async def unhandled_message(message: Message, state: FSMContext, loc: LocalizationManager):
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
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
                        )
