# handlers/tournaments.py

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup  # Оновлений імпорт
from keyboards.menus import (
    MenuButton,
    get_tournaments_menu,
    get_tournament_type_menu,
    get_active_tournaments_menu,
    get_navigation_menu
)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
from datetime import datetime

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

# Валідація формату дати та часу
def validate_datetime(date_text: str) -> bool:
    try:
        datetime.strptime(date_text, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

# Обробник кнопки "🏆 Турніри"
@router.message(lambda message: message.text == MenuButton.TOURNAMENTS.value)
async def tournaments_menu_handler(message: types.Message):
    await message.answer("Оберіть дію з Турнірами:", reply_markup=get_tournaments_menu())

# Обробник кнопки "🆕 Створити Турнір"
@router.message(lambda message: message.text == MenuButton.CREATE_TOURNAMENT.value)
async def create_tournament_handler(message: types.Message, state: FSMContext):
    await state.set_state(TournamentCreation.waiting_for_tournament_type)
    await message.answer("Будь ласка, оберіть тип турніру:", reply_markup=get_tournament_type_menu())

# Обробник кнопки "📋 Переглянути Турніри"
@router.message(lambda message: message.text == MenuButton.VIEW_TOURNAMENTS.value)
async def view_tournaments_handler(message: types.Message):
    # Заглушка для перегляду турнірів
    await message.answer("Перегляд турнірів ще не реалізовано.", reply_markup=get_tournaments_menu())

# Обробник вибору типу турніру (наприклад, "5х5", "2х2", "1 на 1")
@router.message(
    lambda message: message.text in ["5х5", "2х2", "1 на 1"],
    TournamentCreation.waiting_for_tournament_type
)
async def tournament_type_selected_handler(message: types.Message, state: FSMContext):
    await state.update_data(tournament_type=message.text)
    await state.set_state(TournamentCreation.waiting_for_tournament_name)
    await message.answer("Введіть назву турніру:")

# Обробник введення назви турніру
@router.message(TournamentCreation.waiting_for_tournament_name)
async def tournament_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(tournament_name=message.text)
    await state.set_state(TournamentCreation.waiting_for_tournament_description)
    await message.answer("Введіть опис турніру:")

# Обробник введення опису турніру
@router.message(TournamentCreation.waiting_for_tournament_description)
async def tournament_description_handler(message: types.Message, state: FSMContext):
    await state.update_data(tournament_description=message.text)
    await state.set_state(TournamentCreation.waiting_for_tournament_date_time)
    await message.answer(
        "Введіть дату та час турніру у форматі YYYY-MM-DD HH:MM:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

# Обробник введення некоректного формату дати та часу
@router.message(
    lambda message: not validate_datetime(message.text),
    TournamentCreation.waiting_for_tournament_date_time
)
async def invalid_datetime_handler(message: types.Message):
    await message.answer("Невірний формат дати та часу. Будь ласка, використовуйте формат YYYY-MM-DD HH:MM.")

# Обробник введення коректного формату дати та часу
@router.message(
    lambda message: validate_datetime(message.text),
    TournamentCreation.waiting_for_tournament_date_time
)
async def valid_datetime_handler(message: types.Message, state: FSMContext):
    await state.update_data(tournament_date_time=message.text)
    await state.set_state(TournamentCreation.waiting_for_tournament_requirements)
    await message.answer("Введіть вимоги до турніру:")

# Обробник введення вимог до турніру
@router.message(TournamentCreation.waiting_for_tournament_requirements)
async def tournament_requirements_handler(message: types.Message, state: FSMContext):
    await state.update_data(tournament_requirements=message.text)
    await state.set_state(TournamentCreation.confirmation)
    
    # Отримання всіх даних з FSM
    data = await state.get_data()
    tournament_info = (
        f"**Створення Турніру:**\n\n"
        f"**Тип:** {data.get('tournament_type')}\n"
        f"**Назва:** {data.get('tournament_name')}\n"
        f"**Опис:** {data.get('tournament_description')}\n"
        f"**Дата та Час:** {data.get('tournament_date_time')}\n"
        f"**Вимоги:** {data.get('tournament_requirements')}\n\n"
        f"Підтверджуєте створення турніру?"
    )
    
    # Створення клавіатури для підтвердження
    confirmation_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Так"), KeyboardButton(text="❌ Ні")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(tournament_info, reply_markup=confirmation_keyboard)

# Обробник підтвердження створення турніру
@router.message(
    lambda message: message.text == "✅ Так",
    TournamentCreation.confirmation
)
async def confirm_tournament_creation_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    # Тут ви можете додати логіку збереження турніру до бази даних
    # Наприклад:
    # await save_tournament_to_db(data)
    
    await message.answer("Турнір успішно створено!", reply_markup=get_tournaments_menu())
    await state.clear()

# Обробник відміни створення турніру
@router.message(
    lambda message: message.text == "❌ Ні",
    TournamentCreation.confirmation
)
async def cancel_tournament_creation_handler(message: types.Message, state: FSMContext):
    await message.answer("Створення турніру відмінено.", reply_markup=get_tournaments_menu())
    await state.clear()

def setup_handlers(router: Router):
    # Реєструємо всі обробники
    pass  # У aiogram 3.x обробники вже зареєстровані через декоратори