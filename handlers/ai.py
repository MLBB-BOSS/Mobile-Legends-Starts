# handlers/ai.py

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import logging

from keyboards import get_generic_inline_keyboard
from texts import (
    AI_INTRO_TEXT,
    AI_RESPONSE_TEXT,
    USE_BUTTON_NAVIGATION_TEXT,
    # Додайте всі інші текстові константи тут
)
from gpt_integration import get_gpt_response

logger = logging.getLogger(__name__)

router = Router()

class GPTStates(StatesGroup):
    GPT_MENU = State()
    GPT_ASK_QUESTION = State()

@router.message(commands=["gpt"])
async def cmd_gpt(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} запитує GPT")
    await message.delete()
    await bot.send_message(
        chat_id=message.chat.id,
        text=AI_INTRO_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )
    await state.set_state(GPTStates.GPT_MENU)

@router.message(GPTStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню GPT")

    await message.delete()

    if user_choice == "🤖 Поставити питання":
        await bot.send_message(
            chat_id=message.chat.id,
            text="📝 Введіть ваше питання щодо гри:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(GPTStates.GPT_ASK_QUESTION)
    elif user_choice == "📚 Отримати поради":
        await bot.send_message(
            chat_id=message.chat.id,
            text="📝 Введіть тему, з якої ви хотіли б отримати поради:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(GPTStates.GPT_ASK_QUESTION)
    elif user_choice == "🧠 Складні запитання":
        await bot.send_message(
            chat_id=message.chat.id,
            text="📝 Введіть складне запитання, і GPT спробує його розв'язати:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(GPTStates.GPT_ASK_QUESTION)
    elif user_choice == "🔙 Назад":
        # Повернення до головного меню
        await state.set_state(MenuStates.MAIN_MENU)
        # Відправка головного меню
        main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=main_menu_text_formatted,
            reply_markup=get_main_menu()
        )
        # Оновлення стану
        await state.update_data(bot_message_id=main_message.message_id)
        # Оновлення інтерактивного повідомлення
        data = await state.get_data()
        interactive_message_id = data.get('interactive_message_id')
        if interactive_message_id:
            try:
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=interactive_message_id,
                    text=MAIN_MENU_DESCRIPTION,
                    reply_markup=get_generic_inline_keyboard()
                )
            except Exception as e:
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        return
    else:
        # Невідома команда
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_gpt_menu()
        )
        await state.set_state(MenuStates.GPT_MENU)

@router.message(GPTStates.GPT_ASK_QUESTION)
async def handle_gpt_question(message: Message, state: FSMContext, bot: Bot):
    question = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} ставить питання: {question}")

    await message.delete()

    if question:
        response = await get_gpt_response(question)
        await bot.send_message(
            chat_id=message.chat.id,
            text=AI_RESPONSE_TEXT.format(response=response),
            reply_markup=get_generic_inline_keyboard()
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❗ Будь ласка, введіть ваше питання.",
            reply_markup=get_generic_inline_keyboard()
        )

    # Повернення до меню GPT
    await state.set_state(GPTStates.GPT_MENU)
