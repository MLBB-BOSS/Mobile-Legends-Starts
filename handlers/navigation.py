# handlers/navigation.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
import logging

router = Router()
logger = logging.getLogger(__name__)

# Функція для створення клавіатури навігації
def get_navigation_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎮 Герої"),
                KeyboardButton(text="🗺 Карта")
            ],
            [
                KeyboardButton(text="⚔️ Предмети"),
                KeyboardButton(text="🏆 Ранги")
            ],
            [
                KeyboardButton(text="📖 Гайди"),
                KeyboardButton(text="🔄 Мета")
            ],
            [
                KeyboardButton(text="🔙 Головне меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Оберіть розділ..."
    )
    return keyboard

# Функція для створення клавіатури героїв
def get_heroes_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🗡 Файтери"),
                KeyboardButton(text="🎯 Стрілки")
            ],
            [
                KeyboardButton(text="🔮 Маги"),
                KeyboardButton(text="🛡 Танки")
            ],
            [
                KeyboardButton(text="🗝 Підтримка"),
                KeyboardButton(text="🔪 Асасини")
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
                KeyboardButton(text="🔙 Головне меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Оберіть клас героїв..."
    )
    return keyboard

@router.message(F.text == "🧭 Навігація")
async def show_navigation_menu(message: Message):
    await message.answer(
        "🎮 Навігаційне меню Mobile Legends\n\n"
        "Оберіть розділ, який вас цікавить:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🎮 Герої")
async def show_heroes_menu(message: Message):
    await message.answer(
        "👥 Оберіть клас героїв:\n\n"
        "🗡 Файтери - Сильні бійці ближнього бою\n"
        "🎯 Стрілки - Герої дальнього бою\n"
        "🔮 Маги - Майстри магічних умінь\n"
        "🛡 Танки - Витривалі захисники\n"
        "🗝 Підтримка - Помічники команди\n"
        "🔪 Асасини - Швидкі вбивці",
        reply_markup=get_heroes_keyboard()
    )

@router.message(F.text == "🗺 Карта")
async def show_map_info(message: Message):
    await message.answer(
        "🗺 Карта гри\n\n"
        "• Три основні лінії: Top, Mid, Bot\n"
        "• Джунглі між лініями\n"
        "• Важливі об'єкти: Lord, Turtle\n"
        "• Башти та інгібітори\n\n"
        "Оберіть розділ для детальнішої інформації:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "⚔️ Предмети")
async def show_items_info(message: Message):
    await message.answer(
        "⚔️ Предмети та спорядження\n\n"
        "• Атакуючі предмети\n"
        "• Захисні предмети\n"
        "• Магічні предмети\n"
        "• Чоботи та аксесуари\n\n"
        "Виберіть категорію для детальної інформації:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🏆 Ранги")
async def show_ranks_info(message: Message):
    await message.answer(
        "🏆 Рангова система\n\n"
        "• Warrior\n"
        "• Elite\n"
        "• Master\n"
        "• Grandmaster\n"
        "• Epic\n"
        "• Legend\n"
        "• Mythic\n\n"
        "Виберіть ранг для детальної інформації:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "📖 Гайди")
async def show_guides(message: Message):
    await message.answer(
        "📖 Гайди та поради\n\n"
        "• Базові механіки\n"
        "• Просунуті тактики\n"
        "• Мета-стратегії\n"
        "• Командна гра\n\n"
        "Оберіть розділ для вивчення:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🔄 Мета")
async def show_meta_info(message: Message):
    await message.answer(
        "🔄 Поточна мета гри\n\n"
        "• Популярні герої\n"
        "• Ефективні стратегії\n"
        "• Найкращі збірки\n"
        "• Контр-піки\n\n"
        "Оберіть розділ для деталей:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🔙 Головне меню")
async def return_to_main_menu(message: Message):
    from .start import get_main_keyboard
    await message.answer(
        "Ви повернулися до головного меню.",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "⬅️ Назад")
async def go_back(message: Message):
    await show_navigation_menu(message)
