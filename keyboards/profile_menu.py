from aiogram import Router, F
from aiogram.types import Message
from keyboards.profile_menu import ProfileMenu
from keyboards.statistics_menu import StatisticsMenu

router = Router()

@router.message(F.text == "📊 Статистика")
async def handle_statistics(message: Message):
    await message.reply(
        "Меню 'Статистика'. Оберіть опцію:",
        reply_markup=StatisticsMenu.get_statistics_menu()
    )

@router.message(F.text == "🔄 Назад")
async def handle_back_to_profile(message: Message):
    await message.reply(
        "Повернення до меню профілю. Оберіть опцію:",
        reply_markup=ProfileMenu.get_profile_menu()
    )
