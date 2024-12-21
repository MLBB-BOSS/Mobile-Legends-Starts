import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models.user
import models.user_stats
from keyboards.menus import (
    MenuButton, get_main_menu, get_profile_menu, get_navigation_menu,
    get_heroes_menu, get_hero_class_menu, get_guides_menu, get_counter_picks_menu,
    get_builds_menu, get_voting_menu, get_statistics_menu, get_achievements_menu,
    get_settings_menu, get_feedback_menu, get_help_menu, get_tournaments_menu,
    get_meta_menu, get_m6_menu, get_gpt_menu
)
from keyboards.inline_menus import (
    get_generic_inline_keyboard, get_intro_page_1_keyboard, get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION, MAIN_MENU_ERROR_TEXT, NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT, PROFILE_MENU_TEXT, PROFILE_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT, HEROES_MENU_TEXT, HEROES_INTERACTIVE_TEXT,
    HERO_CLASS_MENU_TEXT, HERO_CLASS_INTERACTIVE_TEXT, GUIDES_MENU_TEXT,
    GUIDES_INTERACTIVE_TEXT, COUNTER_PICKS_MENU_TEXT, COUNTER_PICKS_INTERACTIVE_TEXT,
    BUILDS_MENU_TEXT, BUILDS_INTERACTIVE_TEXT, VOTING_MENU_TEXT, VOTING_INTERACTIVE_TEXT,
    STATISTICS_MENU_TEXT, STATISTICS_INTERACTIVE_TEXT, ACHIEVEMENTS_MENU_TEXT,
    ACHIEVEMENTS_INTERACTIVE_TEXT, SETTINGS_MENU_TEXT, SETTINGS_INTERACTIVE_TEXT,
    FEEDBACK_MENU_TEXT, FEEDBACK_INTERACTIVE_TEXT, HELP_MENU_TEXT,
    HELP_INTERACTIVE_TEXT, GENERIC_ERROR_MESSAGE_TEXT, USE_BUTTON_NAVIGATION_TEXT,
    SEARCH_HERO_RESPONSE_TEXT, CHANGE_USERNAME_RESPONSE_TEXT, MLS_BUTTON_RESPONSE_TEXT,
    UNHANDLED_INLINE_BUTTON_TEXT, TOURNAMENT_CREATE_TEXT, TOURNAMENT_VIEW_TEXT,
    META_HERO_LIST_TEXT, META_RECOMMENDATIONS_TEXT, META_UPDATES_TEXT,
    M6_INFO_TEXT, M6_STATS_TEXT, M6_NEWS_TEXT
)
from utils.message_utils import safe_delete_message, check_and_edit_message
from utils.db import get_user_profile
from utils.text_formatter import format_profile_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
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
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    SEARCH_HERO = State()
    SEARCH_TOPIC = State()
    TOURNAMENTS_MENU = State()
    META_MENU = State()
    M6_MENU = State()
    GPT_MENU = State()

async def increment_step(state: FSMContext):
    data = await state.get_data()
    step_count = data.get("step_count", 0) + 1
    if step_count >= 3:
        await state.clear()
        step_count = 0
    await state.update_data(step_count=step_count)

async def send_or_update_interactive_message(
    bot: Bot,
    chat_id: int,
    text: str,
    keyboard,
    message_id: int = None,
    state: FSMContext = None,
    parse_mode: str = ParseMode.HTML
) -> int:
    if message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode=parse_mode
            )
            logger.info(f"Edited message {message_id} successfully.")
            return message_id
        except Exception as e:
            logger.warning(f"Failed to edit message {message_id}: {e}")
    try:
        new_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode
        )
        logger.info(f"Sent new interactive message {new_message.message_id}.")
        if state:
            await state.update_data(interactive_message_id=new_message.message_id)
        return new_message.message_id
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return message_id

async def transition_state(state: FSMContext, new_state: State):
    await state.clear()
    await state.set_state(new_state)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    await safe_delete_message(bot, message.chat.id, message.message_id)
    user_id = message.from_user.id
    async with db.begin():
        user_result = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
        user = user_result.scalars().first()
        if not user:
            new_user = models.user.User(telegram_id=user_id, username=message.from_user.username)
            db.add(new_user)
            await db.flush()
            new_stats = models.user_stats.UserStats(user_id=new_user.id)
            db.add(new_stats)
            await db.commit()
            logger.info(f"Registered new user: {user_id}")
        else:
            logger.info(f"Existing user: {user_id}")
    await transition_state(state, MenuStates.INTRO_PAGE_1)
    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_1_keyboard()
        )
        await state.update_data(
            interactive_message_id=interactive_message.message_id,
            last_text=INTRO_PAGE_1_TEXT,
            last_keyboard=get_intro_page_1_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send intro page 1: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if await state.get_state() != MenuStates.INTRO_PAGE_1.state:
        await bot.answer_callback_query(callback.id, text="Invalid action.", show_alert=True)
        return
    await increment_step(state)
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')
    await check_and_edit_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        new_text=INTRO_PAGE_2_TEXT,
        new_keyboard=get_intro_page_2_keyboard(),
        state=state,
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if await state.get_state() != MenuStates.INTRO_PAGE_2.state:
        await bot.answer_callback_query(callback.id, text="Invalid action.", show_alert=True)
        return
    await increment_step(state)
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')
    await check_and_edit_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        new_text=INTRO_PAGE_3_TEXT,
        new_keyboard=get_intro_page_3_keyboard(),
        state=state,
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot, db: AsyncSession):
    cs = await state.get_state()
    if cs not in [MenuStates.INTRO_PAGE_1.state, MenuStates.INTRO_PAGE_2.state, MenuStates.INTRO_PAGE_3.state]:
        await bot.answer_callback_query(callback.id, text="Invalid action.", show_alert=True)
        return
    await increment_step(state)
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')
    user_first_name = callback.from_user.first_name or "User"
    try:
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=MAIN_MENU_TEXT.format(user_first_name=user_first_name),
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_menu_message.message_id)
    except Exception as e:
        logger.error(f"Failed to send main menu: {e}")
    await send_or_update_interactive_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        text=MAIN_MENU_DESCRIPTION,
        keyboard=get_generic_inline_keyboard(),
        message_id=interactive_message_id,
        state=state,
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

async def process_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)
    await safe_delete_message(bot, message.chat.id, message.message_id)
    if profile_data:
        try:
            formatted_profile_text = format_profile_text(PROFILE_INTERACTIVE_TEXT, profile_data)
        except ValueError as e:
            logger.error(f"Profile formatting error: {e}")
            formatted_profile_text = GENERIC_ERROR_MESSAGE_TEXT
        data = await state.get_data()
        old_bot_message_id = data.get('bot_message_id')
        interactive_message_id = data.get('interactive_message_id')
        if interactive_message_id:
            await check_and_edit_message(
                bot=bot,
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                new_text=formatted_profile_text,
                new_keyboard=get_generic_inline_keyboard(),
                state=state
            )
        else:
            new_im_id = await send_or_update_interactive_message(
                bot=bot,
                chat_id=message.chat.id,
                text=formatted_profile_text,
                keyboard=get_generic_inline_keyboard(),
                message_id=None,
                state=state
            )
        try:
            my_profile_message = await bot.send_message(
                chat_id=message.chat.id,
                text="🪪 Мій Профіль\nОберіть опцію:",
                reply_markup=get_profile_menu()
            )
            new_bot_id = my_profile_message.message_id
        except Exception as e:
            logger.error(f"Failed to send profile msg: {e}")
            new_bot_id = None
        if old_bot_message_id:
            await safe_delete_message(bot, message.chat.id, old_bot_message_id)
        if new_bot_id:
            await state.update_data(bot_message_id=new_bot_id)
        await state.set_state(MenuStates.PROFILE_MENU)
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❌ Дані профілю не знайдено.",
            reply_markup=get_generic_inline_keyboard()
        )
        await state.set_state(MenuStates.MAIN_MENU)

@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in MAIN_MENU")
    await safe_delete_message(bot, message.chat.id, message.message_id)
    await increment_step(state)
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        try:
            mm = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=mm.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error: {e}")
        return
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    updated_state = MenuStates.MAIN_MENU
    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        updated_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        await process_my_profile(message, state, db, bot)
        return
    elif user_choice == MenuButton.TOURNAMENTS.value:
        new_main_text = "Меню Турніри"
        new_main_keyboard = get_tournaments_menu()
        new_interactive_text = "Оберіть опцію Турнірів"
        updated_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = "Меню META"
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "Оберіть опцію META"
        updated_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = "Меню M6"
        new_main_keyboard = get_m6_menu()
        new_interactive_text = "Оберіть опцію M6"
        updated_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = "Меню GPT"
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Оберіть опцію GPT"
        updated_state = MenuStates.GPT_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"
        updated_state = MenuStates.MAIN_MENU
    try:
        new_mm = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = new_mm.message_id
    except Exception as e:
        logger.error(f"Failed to send new MAIN_MENU message: {e}")
        return
    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(updated_state)

@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Unknown message from {message.from_user.id}: {message.text}")
    await safe_delete_message(bot, message.chat.id, message.message_id)
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    current_state = await state.get_state()
    new_main_text = UNKNOWN_COMMAND_TEXT
    new_main_keyboard = get_main_menu()
    new_interactive_text = MAIN_MENU_DESCRIPTION
    new_state = MenuStates.MAIN_MENU
    try:
        main_msg = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_msg.message_id
    except Exception as e:
        logger.error(f"Failed to send new unknown cmd msg: {e}")
        return
    if bot_message_id:
        await safe_delete_message(bot, message.chat.id, bot_message_id)
    if interactive_message_id:
        await check_and_edit_message(
            bot=bot,
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            new_text=new_interactive_text,
            new_keyboard=get_generic_inline_keyboard(),
            state=state
        )
    else:
        try:
            im = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=im.message_id)
        except Exception as e:
            logger.error(f"Failed to send interactive unknown cmd: {e}")
    await state.set_state(new_state)
    await state.update_data(bot_message_id=new_bot_message_id)

def setup_handlers(dp: Router):
    dp.include_router(router)