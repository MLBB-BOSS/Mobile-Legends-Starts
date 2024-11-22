# handlers/statistics_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.statistics_menu import StatisticsMenu
from keyboards.profile_menu import ProfileMenu

router = Router()

@router.message(F.text == "📊 Загальна Актив
