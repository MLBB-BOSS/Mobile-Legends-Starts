# keyboards/navigation_menu.py
class NavigationMenu:
    def get_main_navigation(self) -> ReplyKeyboardMarkup:
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.guides") or "📖 Гайди"),
                        KeyboardButton(text=loc.get_message("buttons.characters") or "👥 Персонажі")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.counter_picks") or "⚔️ Контр-піки"),
                        KeyboardButton(text=loc.get_message("buttons.builds") or "🛠️ Білди")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.voting") or "📊 Голосування"),
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення навігаційного меню: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")]],
                resize_keyboard=True
            )

    # Add similar error handling to other menu methods...
