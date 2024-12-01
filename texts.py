# texts.py

import gettext
import os
from string import Template

# Локалізація
def get_translator(language_code: str):
    locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
    translator = gettext.translation('messages', localedir=locales_dir, languages=[language_code], fallback=True)
    translator.install()
    return translator.gettext

# Welcome Messages
WELCOME_TEXTS = {
    "new_user": """🔥 <b>Ласкаво просимо до Mobile Legends: Starts</b> – твого нового епічного союзника у світі <b>Mobile Legends: Bang Bang!</b> 🔥

🎮 Готовий до неймовірних пригод? Приєднуйся до нас та розкрий всі можливості для покращення своєї гри.

🎮 <b>Розпочнемо цю пригоду разом!</b> 🕹️

<b>Зроблено з любов'ю для справжніх фанатів Mobile Legends. 💖</b>""",
    "intro_page_1": """🔥 <b>Ласкаво просимо до Mobile Legends: Starts</b> – твого нового епічного союзника у світі <b>Mobile Legends: Bang Bang!</b> 🔥

🎮 Готовий до неймовірних пригод? Приєднуйся до нас та розкрий всі можливості для покращення своєї гри.

🎮 <b>Розпочнемо цю пригоду разом!</b> 🕹️

<b>Зроблено з любов'ю для справжніх фанатів Mobile Legends. 💖</b>""",
    "intro_page_2": """💡 <b>Функції Mobile Legends: Starts:</b>

• 🧭 <b>Навігація:</b> Інтуїтивно зрозумілий інтерфейс, що дозволяє швидко знаходити потрібні функції.

• 🪪 <b>Мій профіль:</b> Переглядай та редагуй свої особисті дані, налаштовуй профіль для кращої взаємодії.

• 🥷 <b>Персонажі:</b> Дізнавайся більше про кожного героя, їхні здібності та оптимальні стратегії гри.

• 📚 <b>Гайди:</b> Отримуй детальні поради, покрокові інструкції та стратегії для покращення своєї гри.

• 📊 <b>Статистика:</b> Відстежуй свій прогрес, аналізуй ігрові показники та працюй над слабкими місцями.

• 🛡️ <b>Білди:</b> Створюй оптимальні комплекти спорядження для кожного героя або обирай з готових наборів.

• 🏆 <b>Турніри:</b> Бери участь у змаганнях, організовуй власні турніри та вигравай цінні призи.

Натисни кнопку <b>«Далі»</b>, щоб продовжити ознайомлення."""
}

# Main Menu Texts
MAIN_MENU_TEXTS = {
    "greeting": "👋 Вітаємо, <b>{user_first_name}</b>, у <b>Mobile Legends: Starts</b>!",
    "description": """🎮 <b>MLS</b> допоможе тобі:

• 🏆 <b>Організовувати турніри:</b> Створюй та управляй змаганнями для себе та своїх друзів.
• 📸 <b>Зберігати скріншоти персонажів:</b> Зберігай важливі моменти та обмінюйся ними з іншими гравцями.
• 📊 <b>Відстежувати активність:</b> Слідкуй за своєю та командною активністю в грі.
• 🏅 <b>Отримувати досягнення:</b> Заробляй нагороди за свої успіхи та досягнення."""
}

# Menu Texts
MENU_TEXTS = {
    "navigation": """🧭 <b>Навігація</b>

Оберіть розділ для подальших дій:""",
    "profile": """🪪 <b>Мій Профіль</b>

Оберіть опцію для перегляду:""",
    "heroes": """🥷 <b>Персонажі</b>

Оберіть категорію героїв:""",
    # Додайте інші меню за потребою
}

# Error Messages
ERROR_TEXTS = {
    "unknown_command": "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче для навігації.",
    "generic_error": "⚠️ Сталася помилка. Будь ласка, спробуйте ще раз.",
    "cannot_edit_message": "⚠️ Не вдалося оновити повідомлення. Спробуйте ще раз або зверніться до підтримки."
}

# Feedback Messages
FEEDBACK_TEXTS = {
    "send_feedback_prompt": "📝 Будь ласка, введіть ваш відгук:",
    "report_bug_prompt": "🐛 Будь ласка, опишіть помилку, яку ви знайшли:",
    "feedback_received": "✅ Дякуємо за ваш відгук! Ми його розглянемо.",
    "bug_report_received": "✅ Дякуємо за ваш звіт! Ми виправимо помилку якнайшвидше."
}

# Button Texts
BUTTON_TEXTS = {
    "start": "🚀 Розпочати",
    "back": "🔙 Назад",
    "profile": "🪪 Профіль",
    "help": "❓ Допомога",
    "send_feedback": "📝 Надіслати відгук",
    "report_bug": "🐛 Повідомити про помилку",
    # Додайте інші кнопки за потребою
}

# Templates
MENU_TEMPLATE = Template("""🔧 <b>${menu_name}</b>

Оберіть опцію для продовження:
${options}
""")

ERROR_TEMPLATE = Template("""⚠️ <b>Помилка:</b> ${description}. Будь ласка, спробуйте ще раз.""")

# Functions for Dynamic Texts
def generate_profile_text(username: str, level: int, rating: int, achievements_count: int) -> str:
    """Генерує текст профілю користувача."""
    return f"""🪪 <b>Ваш Профіль:</b>

• 🏅 <b>Ім'я користувача:</b> {username}
• 🧬 <b>Рівень:</b> {level}
• 📈 <b>Рейтинг:</b> {rating}
• 🎯 <b>Досягнення:</b> {achievements_count} досягнень
"""

def generate_statistics_text(played_matches: int, wins: int, losses: int, average_rating: int) -> str:
    """Генерує текст статистики користувача."""
    return f"""📊 <b>Статистика:</b>

• 🎮 Граних матчів: {played_matches}
• 🏆 Перемог: {wins}
• 💔 Поразок: {losses}
• 📈 Середній рейтинг: {average_rating}
"""

def generate_error_message(description: str) -> str:
    """Генерує повідомлення про помилку."""
    return ERROR_TEMPLATE.substitute(description=description)

def generate_menu(menu_name: str, options: str) -> str:
    """Генерує текст меню."""
    return MENU_TEMPLATE.substitute(menu_name=menu_name, options=options)

# Локалізація
def get_translator(language_code: str):
    locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
    translator = gettext.translation('messages', localedir=locales_dir, languages=[language_code], fallback=True)
    translator.install()
    return translator.gettext
