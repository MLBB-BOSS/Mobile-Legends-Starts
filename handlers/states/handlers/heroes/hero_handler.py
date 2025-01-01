from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.hero_states import HeroStates

# Ініціалізація роутера
router = Router()

# Вибір класу героя
@router.message(Command("choose_class"))
async def choose_class(message: Message, state: FSMContext):
    """
    Обробник для вибору класу героя.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Асасіни", callback_data="class_assassin")],
            [InlineKeyboardButton(text="Маги", callback_data="class_mage")],
            [InlineKeyboardButton(text="Танки", callback_data="class_tank")],
            [InlineKeyboardButton(text="Стрільці", callback_data="class_marksman")],
        ]
    )
    
    await message.answer("Оберіть клас героя:", reply_markup=keyboard)
    await state.set_state(HeroStates.class_selection)

# Вибір конкретного героя
@router.callback_query(lambda callback: callback.data.startswith("class_"))
async def choose_hero(callback: CallbackQuery, state: FSMContext):
    """
    Обробник для вибору героя з вибраного класу.
    """
    hero_class = callback.data.split("_")[1]
    heroes = {
        "assassin": ["Alucard", "Gusion"],
        "mage": ["Eudora", "Kagura"],
        "tank": ["Tigreal", "Johnson"],
        "marksman": ["Miya", "Clint"],
    }

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=hero, callback_data=f"hero_{hero.lower()}")]
            for hero in heroes.get(hero_class, [])
        ]
    )
    
    await callback.message.edit_text(f"Оберіть героя з класу {hero_class.capitalize()}:", reply_markup=keyboard)
    await state.set_state(HeroStates.hero_selection)

# Перегляд інформації про героя
@router.callback_query(lambda callback: callback.data.startswith("hero_"))
async def hero_info(callback: CallbackQuery, state: FSMContext):
    """
    Обробник для перегляду інформації про героя.
    """
    hero_name = callback.data.split("_")[1].capitalize()
    # Тут варто підключити базу даних або JSON для отримання даних
    hero_data = {
        "alucard": "Alucard - відомий Асасін, який володіє потужним вампіризмом.",
        "gusion": "Gusion - маг-асасін із блискавичною швидкістю та магічними клинками.",
    }

    hero_description = hero_data.get(hero_name.lower(), "Інформація про цього героя недоступна.")
    await callback.message.edit_text(f"{hero_description}")
    await state.set_state(HeroStates.hero_info)
