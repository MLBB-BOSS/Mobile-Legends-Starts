from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class StatisticsMenu:
    @staticmethod
    def get_statistics_menu():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📈 Загальна Активність"), KeyboardButton(text="🥇 Рейтинг")],
                [KeyboardButton(text="🎮 Ігрова Статистика"), KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )
