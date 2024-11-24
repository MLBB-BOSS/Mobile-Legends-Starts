def get_localized_text(key):
    texts = {
        "greeting": "Привіт! Раді вітати вас у нашому боті.",
        "profile": "Це ваш профіль.",
        "navigation_prompt": "Виберіть опцію навігації:",
        "option_one_response": "Ви обрали Опцію 1.",
        "option_two_response": "Ви обрали Опцію 2.",
        "back_to_main_menu": "Повертаємося до головного меню.",
        "unknown_command": "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки на клавіатурі.",
    }
    return texts.get(key, "Текст не знайдено.")
