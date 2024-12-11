# handlers/tournaments.py

from aiogram import Router, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.menus import get_tournaments_menu
from texts import TOURNAMENT_CREATED_TEXT, GENERIC_ERROR_MESSAGE_TEXT
import logging

logger = logging.getLogger(__name__)

router = Router()

class TournamentForm(StatesGroup):
    waiting_for_tournament_type = State()
    waiting_for_tournament_name = State()

@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: types.Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Турніри")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    if user_choice == MenuButton.CREATE_TOURNAMENT.value:
        await TournamentForm.waiting_for_tournament_type.set()
        await bot.send_message(
            chat_id=message.chat.id,
            text="🏆 <b>Створення Турніру</b>\n\nОберіть тип турніру:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="5х5"), KeyboardButton(text="2х2")],
                    [KeyboardButton(text="1 на 1")],
                    [KeyboardButton(text=MenuButton.BACK.value)]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
    elif user_choice == MenuButton.VIEW_TOURNAMENTS.value:
        # Логіка перегляду турнірів
        await bot.send_message(
            chat_id=message.chat.id,
            text="📋 <b>Активні Турніри</b>",
            reply_markup=get_tournaments_menu()
        )
    elif user_choice == MenuButton.BACK.value:
        # Повернення до навігаційного меню
        await bot.send_message(
            chat_id=message.chat.id,
            text="🔙 <b>Навігація</b>",
            reply_markup=get_navigation_menu()
        )
        await state.set_state(MenuStates.NAVIGATION_MENU)
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❗ Невідома команда. Будь ласка, виберіть опцію з меню.",
            reply_markup=get_tournaments_menu()
        )

@router.message(TournamentForm.waiting_for_tournament_type)
async def process_tournament_type(message: types.Message, state: FSMContext, bot: Bot):
    tournament_type = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} обрав тип турніру: {tournament_type}")

    if tournament_type not in ["5х5", "2х2", "1 на 1"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❗ Будь ласка, оберіть коректний тип турніру.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="5х5"), KeyboardButton(text="2х2")],
                    [KeyboardButton(text="1 на 1")],
                    [KeyboardButton(text=MenuButton.BACK.value)]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        return

    await state.update_data(tournament_type=tournament_type)
    await TournamentForm.next()

    await bot.send_message(
        chat_id=message.chat.id,
        text="📝 Введіть назву турніру:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=MenuButton.BACK.value)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

@router.message(TournamentForm.waiting_for_tournament_name)
async def process_tournament_name(message: types.Message, state: FSMContext, bot: Bot):
    tournament_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} створює турнір: {tournament_name}")

    if tournament_name == MenuButton.BACK.value:
        await TournamentForm.previous()
        await bot.send_message(
            chat_id=message.chat.id,
            text="🔙 <b>Створення Турніру</b>\n\nОберіть тип турніру:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="5х5"), KeyboardButton(text="2х2")],
                    [KeyboardButton(text="1 на 1")],
                    [KeyboardButton(text=MenuButton.BACK.value)]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        return

    if not tournament_name:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❗ Назва турніру не може бути порожньою. Будь ласка, введіть назву турніру:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=MenuButton.BACK.value)]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        return

    # Тут додайте логіку збереження турніру в базі даних
    # Наприклад, save_tournament(tournament_name, tournament_type)

    await bot.send_message(
        chat_id=message.chat.id,
        text=TOURNAMENT_CREATED_TEXT.format(tournament_name=tournament_name),
        reply_markup=get_tournaments_menu()
    )

    await state.finish()
