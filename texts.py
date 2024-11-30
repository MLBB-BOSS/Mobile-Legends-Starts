# texts.py

# Intro Pages
INTRO_TEXTS = {
    "page_1": """🌟 Ласкаво просимо до Mobile Legends Starts! 🌟
    
    Твій незамінний помічник у світі Mobile Legends – де стратегія зустрічається з епічними битвами!
    
    ---
    
    ✨ <b>Що вас чекає?</b>
    
    • 🗺️ <b>Завдання:</b> Виконуй місії, заробляй бали, підвищуй рівень!
    • 📘 <b>Гайди:</b> Доступ до унікальних порад і стратегій.
    • 📊 <b>Статистика:</b> Аналізуй свій прогрес.
    • ⚙️ <b>Білди:</b> Створюй ідеальне спорядження для героїв.
    • 🤝 <b>Команди:</b> Шукай союзників для гри.
    • 🏆 <b>Турніри:</b> Організовуй або долучайся до змагань.
    • 🎖️ <b>Досягнення:</b> Відстежуй успіхи, отримуй нагороди.
    • 🥷 <b>Персонажі:</b> Обирай героїв, порівнюй їх здібності та досягай перемог!
    
    ---
    
    🚀 <b>Розпочни свою подорож вже зараз!</b>
    
    Натисни кнопку «Далі» і поринь у світ безмежних можливостей Mobile Legends Starts.
    
    Пам'ятай, твій успіх – це наша місія!
    
    ---
    
    <b>Зроблено з любов'ю для гравців Mobile Legends. 💖</b>""",
    "page_2": """💡 <b>Функції нашого бота:</b>
    
    • 🧭 <b>Навігація:</b> Легко орієнтуйся у всіх можливостях бота.
    • 🪪 <b>Мій профіль:</b> Переглядай і редагуй свої дані.
    • 🥷 <b>Персонажі:</b> Дізнавайся більше про героїв та їхні можливості.
    • 📚 <b>Гайди:</b> Отримуй корисні поради та стратегії.
    • 📊 <b>Статистика:</b> Відстежуй свій прогрес і досягнення.
    • ⚙️ <b>Білди:</b> Створюй оптимальні спорядження для героїв.
    • 🏆 <b>Турніри:</b> Беріть участь у змаганнях та вигравайте нагороди.
    
    ---
    
    Натисни кнопку «Далі», щоб продовжити ознайомлення.""",
    "page_3": """🚀 <b>Готові розпочати?</b>
    
    Натисни кнопку «Розпочати», щоб перейти до основного меню і розпочати використання бота.
    
    ---
    
    <b>Залишайся з нами, і разом досягнемо нових висот у Mobile Legends!</b>"""
}

# Main Menu
MAIN_MENU = {
    "text": "👋 Вітаємо, {user_first_name}, у Mobile Legends Tournament Bot!\n\nОберіть опцію з меню нижче 👇",
    "description": """🎮 Цей бот допоможе вам:
• Організовувати турніри
• Зберігати скріншоти персонажів
• Відстежувати активність
• Отримувати досягнення""",
    "error_text": "Щось пішло не так. Почнімо спочатку."
}

# Navigation Menu
NAVIGATION_MENU = {
    "text": "🧭 Навігація\nОберіть розділ для подальших дій:",
    "interactive_text": """🧭 <b>Доступні розділи:</b>

🥷 <b>Персонажі:</b> Оберіть героя, щоб дізнатися про його здібності.
📘 <b>Гайди:</b> Ознайомтесь із гайдами та стратегіями.
⚙️ <b>Білди:</b> Створіть чи перегляньте спорядження для героїв.
⚖️ <b>Контр-піки:</b> Дізнайтесь, як протистояти героям-суперникам.
📊 <b>Голосування:</b> Висловлюйте свою думку або пропонуйте ідеї.

👇 Оберіть кнопку нижче, щоб продовжити."""
}

# Profile Menu
PROFILE_MENU = {
    "text": "🪪 Мій Профіль\nОберіть опцію для перегляду:",
    "interactive_text": "Профіль користувача"
}

# Heroes Menu
HEROES_MENU = {
    "text": "🥷 Персонажі\nОберіть категорію героїв:",
    "interactive_text": "Список категорій героїв"
}

# Hero Class Menu
HERO_CLASS_MENU = {
    "text": "Виберіть героя з класу {hero_class}:",
    "interactive_text": "Список героїв класу {hero_class}"
}

# Guides Menu
GUIDES_MENU = {
    "text": "📚 Гайди\nВиберіть підрозділ гайдів:",
    "interactive_text": "Список гайдів",
    "submenus": {
        "new_guides": "Список нових гайдів ще не доступний.",
        "popular_guides": "Список популярних гайдів ще не доступний.",
        "beginner_guides": "Список гайдів для початківців ще не доступний.",
        "advanced_techniques": "Список просунутих технік ще не доступний.",
        "teamplay_guides": "Список гайдів по командній грі ще не доступний."
    }
}

# Counter Picks Menu
COUNTER_PICKS_MENU = {
    "text": "🔄 Контр-піки\nВиберіть опцію контр-піків:",
    "interactive_text": "Список контр-піків",
    "submenus": {
        "counter_search": "Введіть ім'я персонажа для пошуку контр-піку:",
        "counter_list": "Список персонажів для контр-піків ще не доступний."
    }
}

# Builds Menu
BUILDS_MENU = {
    "text": "🛠️ Білди\nВиберіть опцію білдів:",
    "interactive_text": "Список білдів",
    "submenus": {
        "create_build": "Функція створення білду ще в розробці.",
        "my_builds": "Список ваших білдів ще не доступний.",
        "popular_builds": "Список популярних білдів ще не доступний."
    }
}

# Voting Menu
VOTING_MENU = {
    "text": "🗳️ Голосування\nВиберіть опцію голосування:",
    "interactive_text": "Список голосувань",
    "submenus": {
        "current_votes": "Список поточних опитувань ще не доступний.",
        "my_votes": "Список ваших голосувань ще не доступний.",
        "suggest_topic": "Будь ласка, введіть тему для пропозиції:",
        "suggestion_response": "Ви пропонуєте тему: {topic}. Ця функція ще в розробці."
    }
}

# Statistics Menu
STATISTICS_MENU = {
    "text": "📊 Статистика\nВиберіть підрозділ статистики:",
    "interactive_text": "Статистика",
    "submenus": {
        "activity": "Статистика загальної активності ще не доступна.",
        "ranking": "Рейтинг ще не доступний.",
        "game_stats": "Ігрова статистика ще не доступна."
    }
}

# Achievements Menu
ACHIEVEMENTS_MENU = {
    "text": "🎖️ Досягнення\nВиберіть підрозділ досягнень:",
    "interactive_text": "Досягнення",
    "submenus": {
        "badges": "Список ваших бейджів ще не доступний.",
        "progress": "Ваш прогрес ще не доступний.",
        "tournament_stats": "Турнірна статистика ще не доступна.",
        "awards": "Список отриманих нагород ще не доступний."
    }
}

# Settings Menu
SETTINGS_MENU = {
    "text": "⚙️ Налаштування\nВиберіть опцію налаштувань:",
    "interactive_text": "Налаштування",
    "submenus": {
        "language": "Функція зміни мови ще в розробці.",
        "change_username": "Будь ласка, введіть новий Username:",
        "update_id": "Функція оновлення ID ще в розробці.",
        "notifications": "Функція налаштування сповіщень ще в розробці."
    }
}

# Feedback Menu
FEEDBACK_MENU = {
    "text": "🤝 Зворотний Зв'язок\nВиберіть опцію зворотного зв'язку:",
    "interactive_text": "Зворотний зв'язок",
    "submenus": {
        "send_feedback": "Будь ласка, введіть ваш відгук:",
        "report_bug": "Будь ласка, опишіть помилку, яку ви знайшли:",
        "feedback_received": "Дякуємо за ваш відгук! Ми його розглянемо.",
        "bug_report_received": "Дякуємо за ваш звіт про помилку! Ми його розглянемо."
    }
}

# Help Menu
HELP_MENU = {
    "text": "🆘 Допомога\nВиберіть опцію допомоги:",
    "interactive_text": "Допомога",
    "submenus": {
        "instructions": "Інструкції ще не доступні.",
        "faq": "FAQ ще не доступне.",
        "help_support": "Зв'яжіться з підтримкою через наш канал або електронну пошту."
    }
}

# Unknown Command
UNKNOWN_COMMAND_TEXT = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."

# Generic Error Messages
GENERIC_ERROR_MESSAGE_TEXT = "Сталася помилка. Будь ласка, спробуйте знову."
ERROR_MESSAGE_TEXT = "Сталася помилка. Будь ласка, спробуйте пізніше або зверніться до підтримки."

# Generic Navigation Prompt
USE_BUTTON_NAVIGATION_TEXT = "Будь ласка, використовуйте кнопки для навігації."

# Additional Responses
SEARCH_HERO_RESPONSE_TEXT = "Ви шукаєте героя: {hero_name}. Ця функція ще в розробці."
CHANGE_USERNAME_RESPONSE_TEXT = "Ваш новий Username: {new_username} буде доданий після перевірки. Ця функція ще в розробці."

# Inline Button Responses
MLS_BUTTON_RESPONSE_TEXT = "Ви натиснули кнопку MLS"
UNHANDLED_INLINE_BUTTON_TEXT = "Ця кнопка поки не оброблена."

# Main Menu Back to Profile
MAIN_MENU_BACK_TO_PROFILE_TEXT = "🔙 Повернення до меню Профіль:"

# Додана константа
HERO_COMPARISON_NOT_AVAILABLE_TEXT = "Функція порівняння героїв ще не доступна."

# Додайте інші текстові константи за потребою
