class Localization:
    """
    Локалізація повідомлень для різних мов.
    """
    def __init__(self, lang: str = "uk"):
        self.lang = lang
        self.messages = {
            "uk": {
                "messages.main_menu": "Вітаємо в головному меню! Оберіть дію:"
            },
            "en": {
                "messages.main_menu": "Welcome to the main menu! Choose an action:"
            }
        }

    def get_message(self, key: str) -> str:
        """
        Отримує локалізоване повідомлення за ключем.

        :param key: Ключ повідомлення.
        :return: Локалізований текст.
        """
        return self.messages.get(self.lang, {}).get(key, "Message not found.")
