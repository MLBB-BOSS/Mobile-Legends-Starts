# keyboards/profile_menu.py
class ProfileMenu:
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.statistics") or "📊 Статистика"),
                        KeyboardButton(text=loc.get_message("buttons.achievements") or "🏆 Досягнення")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.settings") or "⚙️ Налаштування"),
                        KeyboardButton(text=loc.get_message("buttons.feedback") or "📝 Зворотній зв'язок")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення профільного меню: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")]],
                resize_keyboard=True
            )
