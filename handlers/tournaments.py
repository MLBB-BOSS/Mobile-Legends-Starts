from aiogram import Router, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.menus import MenuButton, get_tournaments_menu, get_tournament_type_menu, get_active_tournaments_menu, get_navigation_menu
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

def register_handlers(dp: Dispatcher):
    # Обробник кнопки "🏆 Турніри"
    @dp.message_handler(lambda message: message.text == MenuButton.TOURNAMENTS.value)
    async def tournaments_menu_handler(message: types.Message):
        await message.answer("Оберіть дію з Турнірами:", reply_markup=get_tournaments_menu())

    # Обробник кнопки "🆕 Створити Турнір"
    @dp.message_handler(lambda message: message.text == MenuButton.CREATE_TOURNAMENT.value)
    async def create_tournament_handler(message: types.Message):
        await TournamentCreation.waiting_for_tournament_type.set()
        await message.answer("Будь ласка, оберіть тип турніру:", reply_markup=get_tournament_type_menu())

    # Обробник кнопки "📋 Переглянути Турніри"
    @dp.message_handler(lambda message: message.text == MenuButton.VIEW_TOURNAMENTS.value)
    async def view_tournaments_handler(message: types.Message):
        # Заглушка для перегляду турнірів
        await message.answer("Перегляд турнірів ще не реалізовано.", reply_markup=get_tournaments_menu())

    # Обробник вибору типу турніру (наприклад, "5х5", "2х2", "1 на 1")
    @dp.message_handler(lambda message: message.text in ["5х5", "2х2", "1 на 1"], state=TournamentCreation.waiting_for_tournament_type)
    async def tournament_type_selected_handler(message: types.Message, state: FSMContext):
        await state.update_data(tournament_type=message.text)
        await TournamentCreation.next()
        await message.answer("Введіть назву турніру:")

    # Обробник введення назви турніру
    @dp.message_handler(state=TournamentCreation.waiting_for_tournament_name)
    async def tournament_name_handler(message: types.Message, state: FSMContext):
        await state.update_data(tournament_name=message.text)
        await TournamentCreation.next()
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
    @dp.message_handler(lambda message: not validate_datetime(message.text), state=TournamentCreation.waiting_for_tournament_date_time)
    async def invalid_datetime_handler(message: types.Message):
        await message.answer("Невірний формат дати та часу. Будь ласка, використовуйте формат YYYY-MM-DD HH:MM.")

    # Обробник введення коректного формату дати та часу
    @dp.message_handler(lambda message: validate_datetime(message.text), state=TournamentCreation.waiting_for_tournament_date_time)
    async def tournament_date_time_handler(message: types.Message, state: FSMContext):
        await state.update_data(tournament_date_time=message.text)
        await TournamentCreation.next()
        await message.answer("Вкажіть умови участі:")

    # Обробник введення умов участі
    @dp.message_handler(state=TournamentCreation.waiting_for_tournament_requirements)
    async def tournament_requirements_handler(message: types.Message, state: FSMContext):
        await state.update_data(tournament_requirements=message.text)
        user_data = await state.get_data()

        # Формуємо підтвердження
        confirmation_text = (
            f"Будь ласка, підтвердіть створення турніру:\n\n"
            f"Тип: {user_data['tournament_type']}\n"
            f"Назва: {user_data['tournament_name']}\n"
            f"Опис: {user_data['tournament_description']}\n"
            f"Дата та Час: {user_data['tournament_date_time']}\n"
            f"Умови Участі: {user_data['tournament_requirements']}\n"
        )

        # Кнопки підтвердження
        confirmation_buttons = [
            KeyboardButton(text="Підтвердити"),
            KeyboardButton(text="Відхилити")
        ]
        confirmation_keyboard = ReplyKeyboardMarkup(keyboard=[confirmation_buttons], resize_keyboard=True)

        await TournamentCreation.next()
        await message.answer(confirmation_text, reply_markup=confirmation_keyboard)

    # Обробник підтвердження створення турніру
    @dp.message_handler(lambda message: message.text == "Підтвердити", state=TournamentCreation.confirmation)
    async def tournament_confirm_handler(message: types.Message, state: FSMContext):
        user_data = await state.get_data()
        # Заглушка для підтвердження турніру
        await message.answer("Турнір успішно створено та надіслано на підтвердження адміністратору.", reply_markup=get_navigation_menu())
        await state.finish()

    # Обробник відхилення створення турніру
    @dp.message_handler(lambda message: message.text == "Відхилити", state=TournamentCreation.confirmation)
    async def tournament_cancel_handler(message: types.Message, state: FSMContext):
        await message.answer("Створення турніру відхилено.", reply_markup=get_tournaments_menu())
        await state.finish()

    # Обробники для підтвердження та відхилення турнірів (заглушки)
    from aiogram.dispatcher.filters import Text

    @dp.message_handler(Text(startswith="Підтвердити Турнір "), state=None)
    async def approve_tournament_handler(message: types.Message):
        # Заглушка для підтвердження турніру
        await message.answer("Турнір підтверджено (заглушка).", reply_markup=get_navigation_menu())

    @dp.message_handler(Text(startswith="Відхилити Турнір "), state=None)
    async def reject_tournament_handler(message: types.Message):
        # Заглушка для відхилення турніру
        await message.answer("Турнір відхилено (заглушка).", reply_markup=get_navigation_menu())

    # Обробник реєстрації на турнір (заглушка)
    @dp.message_handler(lambda message: message.text.startswith("Зареєструватися на Турнір "), state=None)
    async def register_tournament_handler(message: types.Message):
        # Заглушка для реєстрації на турнір
        await message.answer("Ви успішно зареєструвалися на турнір (заглушка).", reply_markup=get_navigation_menu())