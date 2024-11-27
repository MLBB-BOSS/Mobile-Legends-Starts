# utils/menu_messages.py

class MenuMessages:
    @staticmethod
    def get_heroes_menu_text():
        return {
            "title": "🛡️ Меню Персонажів",
            "description": (
                "Тут ви можете знайти інформацію про всіх героїв Mobile Legends!\n\n"
                "🔹 Пошук за класами\n"
                "🔹 Детальні характеристики\n"
                "🔹 Рекомендовані білди\n"
                "🔹 Контр-піки\n"
                "🔹 Гайди по грі"
            )
        }
    
    @staticmethod
    def get_guides_menu_text():
        return {
            "title": "📚 Гайди",
            "description": (
                "Вивчайте гру разом з нашими гайдами!\n\n"
                "🔹 Базові механіки\n"
                "🔹 Просунуті тактики\n"
                "🔹 Мета-стратегії\n"
                "🔹 Командна гра\n"
                "🔹 Контр-піки"
            )
        }
    
    @staticmethod
    def get_builds_menu_text():
        return {
            "title": "⚔️ Білди",
            "description": (
                "Створюйте та діліться своїми білдами!\n\n"
                "🔹 Популярні білди\n"
                "🔹 Створити новий білд\n"
                "🔹 Мої збережені білди\n"
                "🔹 Рейтинг білдів"
            )
        }
    
    # Додайте інші методи для різних меню
