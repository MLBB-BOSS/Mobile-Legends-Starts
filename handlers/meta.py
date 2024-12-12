# handlers/tournaments.py

from aiogram import Router, types
from aiogram.fsm.context import FSMContext  # Оновлений імпорт
from aiogram.fsm.state import State, StatesGroup  # Оновлений імпорт для aiogram 3.x
from keyboards.menus import (
    MenuButton,
    get_tournaments_menu,
    get_tournament_type_menu,
    get_active_tournaments_menu,
    get_navigation_menu,
)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

# Визначення станів для створення турніру
class TournamentCreation(StatesGroup):
    waiting_for_tournament_type = State()
    waiting_for_tournament_name = State()
    waiting_for_tournament_description = State()
    waiting_for_tournament_date_time = State()
    waiting_for_tournament_requirements = State()
    confirmation = State()

logger = logging.getLogger(__name__)

router = Router()

def register_handlers(router: Router):
    # Обробник кнопки "🏆 Турніри"
    @router.message(MenuButton.TOURNAMENTS.value)
    async def tournaments_menu_handler(message: types.Message):
        await message.answer("Оберіть дію з Турнірами:", reply_markup=get_tournaments_menu())

    # Обробник кнопки "🆕 Створити Турнір"
    @router.message(MenuButton.CREATE_TOURNAMENT.value)
    async def create_tournament_handler(message: types.Message, state: FSMContext):
        await state.set_state(TournamentCreation.waiting_for_tournament_type)
        await message.answer("Будь ласка, оберіть тип турніру:", reply_markup=get_tournament_type_menu())

    # Обробник кнопки "📋 Переглянути Турніри"
    @router.message(MenuButton.VIEW_TOURNAMENTS.value)
    async def view_tournaments_handler(message: types.Message):
        # Заглушка для перегляду турнірів
        await message.answer("Перегляд турнірів ще не реалізовано.", reply_markup=get_tournaments_menu())

    # Обробник вибору типу турніру (наприклад, "5х5", "2х2", "1 на 1")
    @router.message(lambda message: message.text in ["5х5", "2х2", "1 на 1"], state=TournamentCreation.waiting_for_tournament_type)
    async def tournament_type_selected_handler(message: types.Message, state: FSMContext):
        await state.update_data(tournament_type=message.text)
        await state.set_state(TournamentCreation.waiting_for_tournament_name)
        await message.answer("Введіть назву турніру:")

    # Обробник введення назви турніру
    @router.message(state=TournamentCreation.waiting_for_tournament_name)
    async def tournament_name_handler(message: types.Message, state: FSMContext):
        await state.update_data(tournament_name=message.text)
        await state.set_state(TournamentCreation.waiting_for_tournament_description)
        await message.answer("Введіть опис турніру:")

    # Валідація формату дати та часу
    def validate_datetime(date_text):
        from datetime import datetime
        try:
            datetime.strptime(date_text, '%Y-%m-%d %H:%M')
            return True
        except ValueError:
            return False

    # Обробник введення некоректного формату дати та часу
    @router.message(lambda message: not validate_datetime(message.text), state=TournamentCreation.waiting_for_tournament_date_time)
    async def invalid_datetime_handler(message: types.Message):
        await message.answer("Невірний формат дати та часу. Будь ласка, використовуйте формат YYYY-MM-DD HH:MM.")

    # Обробник введення коректного формату дати та часу
    @router.message(lambda message: validate_datetime(message.text), state=TournamentCreation.waiting_for_tournament_date_time)
    async def tournament_date_time_handler(message: types.Message, state: FSMContext):
        await state.update_data(tournament_date_time=message.text)
        await state.set_state(TournamentCreation.waiting_for_tournament_requirements)
        await message.answer("Введіть вимоги до турніру:")

    # Обробник введення вимог до турніру
    @router.message(state=TournamentCreation.waiting_for_tournament_requirements)
    async def tournament_requirements_handler(message: types.Message, state: FSMContext):
        await state.update_data(tournament_requirements=message.text)
        await state.set_state(TournamentCreation.confirmation)

        # Отримання всіх даних для підтвердження
        data = await state.get_data()
        tournament_info = (
            f"Тип турніру: {data.get('tournament_type')}\n"
            f"Назва: {data.get('tournament_name')}\n"
            f"Опис: {data.get('tournament_description')}\n"
            f"Дата та час: {data.get('tournament_date_time')}\n"
            f"Вимоги: {data.get('tournament_requirements')}"
        )

        # Клавіатура для підтвердження
        confirmation_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Підтвердити"), KeyboardButton(text="❌ Відмінити")]
            ],
            resize_keyboard=True
        )

        await message.answer(f"Будь ласка, підтвердіть створення турніру:\n\n{tournament_info}", reply_markup=confirmation_keyboard)

    # Обробник підтвердження створення турніру
    @router.message(lambda message: message.text == "✅ Підтвердити", state=TournamentCreation.confirmation)
    async def confirm_tournament_handler(message: types.Message, state: FSMContext):
        data = await state.get_data()
        
        # Тут можна додати логіку збереження турніру у базу даних
        # Наприклад:
        # save_tournament_to_db(data)

        await message.answer("Турнір успішно створено!", reply_markup=get_tournaments_menu())
        await state.clear()

    # Обробник скасування створення турніру
    @router.message(lambda message: message.text == "❌ Відмінити", state=TournamentCreation.confirmation)
    async def cancel_tournament_handler(message: types.Message, state: FSMContext):
        await message.answer("Створення турніру скасовано.", reply_markup=get_tournaments_menu())
        await state.clear()