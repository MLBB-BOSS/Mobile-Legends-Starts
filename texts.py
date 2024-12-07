# texts.py

from rich.table import Table
from rich.console import Console
from rich.box import DOUBLE
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

def create_inline_table(title: str, headers: list[str], rows: list[list[str]]) -> str:
    """
    Створює ASCII-таблицю з використанням rich та повертає її як текст.
    Використовуйте <pre></pre> у повідомленні Telegram для збереження форматування.
    """
    console = Console(record=True)
    table = Table(
        title=title,
        box=DOUBLE,
        show_header=True,
        header_style="bold cyan",
        style="dim"
    )

    for header in headers:
        table.add_column(header, style="bold yellow", justify="center")

    for row in rows:
        table.add_row(*row)

    console.print(table)
    return console.export_text()

# Текстові константи

WELCOME_NEW_USER_TEXT = (
    """🔥 <b>Ласкаво просимо до Mobile Legends: Starts</b> – вашого нового незамінного партнера у світі <b>Mobile Legends: Bang Bang!</b> 🔥

🎮 Тут ви отримаєте доступ до широкого спектра можливостей, які допоможуть зрозуміти гру глибше, вдосконалити свої навички та вивести ігровий досвід на новий рівень.

Ви зможете:
• Досліджувати характеристики та ролі різних героїв.
• Отримувати покрокові гайди, тактичні поради та рекомендації щодо білдів.
• Аналізувати власну статистику та прогрес, щоб робити більш обґрунтовані рішення у грі.
• Брати участь у турнірах, виявляти нові стратегії та здобувати унікальні нагороди.

🏆 <b>Готові до нових пригод?</b> Натискайте нижче, щоб розпочати подорож до найвищих вершин Mobile Legends!

<b>Цей застосунок створено з любов’ю для справжніх поціновувачів Mobile Legends. 💖</b>
"""
)

INTRO_PAGE_1_TEXT = WELCOME_NEW_USER_TEXT

INTRO_PAGE_2_TEXT = (
    """💡 <b>Функції Mobile Legends: Starts:</b>

🧭 <b>Навігація:</b> Зручний інтерфейс допоможе вам швидко знайти потрібний розділ – від героїв до гайдів, білдів та статистики.

🪪 <b>Мій профіль:</b> Переглядайте свій рівень, рейтинг і досягнення, а також налаштовуйте персональні дані.

🥷 <b>Персонажі:</b> Отримуйте інформацію про кожного героя: роль, навички, сильні та слабкі сторони.

📚 <b>Гайди:</b> Матеріали для новачків і досвідчених гравців, тактики, поради.

📊 <b>Статистика:</b> Аналізуйте ігрові дані – перемоги, поразки, улюблених героїв.

🛡️ <b>Білди:</b> Створюйте та редагуйте спорядження, експериментуйте з комбінаціями.

🏆 <b>Турніри:</b> Дізнавайтеся про змагання, нагороди та перевіряйте свої навички.

Натисніть <b>«Далі»</b>, щоб продовжити.
"""
)

INTRO_PAGE_3_TEXT = (
    """🪪 <b>Ваш Профіль:</b>

Тут зведена інформація про ваш прогрес:
• 🏅 <b>Ім'я користувача:</b> {username}
• 🧬 <b>Рівень:</b> {level}
• 📈 <b>Рейтинг:</b> {rating}
• 🎯 <b>Досягнення:</b> {achievements_count}

🧭 <b>Навігація:</b> Внизу меню для переходу до розділів.
🚀 <b>Розпочніть подорож зараз!</b> Натисніть <b>«Розпочати»</b>, щоб перейти до головного меню.
"""
)

MAIN_MENU_TEXT = (
    """👋 <b>Вітаю, {user_first_name}, у Mobile Legends: Starts!</b>

Оберіть розділ для дослідження.
"""
)

MAIN_MENU_DESCRIPTION = (
    """🎮 <b>Mobile Legends: Starts допоможе вам:</b>

🏆 <b>Турніри</b>: Створюйте та керуйте змаганнями.
📸 <b>Скріншоти</b>: Зберігайте важливі моменти.
📊 <b>Активність</b>: Аналізуйте свою гру.
🏅 <b>Досягнення</b>: Отримуйте винагороди.

Оберіть потрібний розділ нижче.
"""
)

MAIN_MENU_ERROR_TEXT = (
    """❗ <b>Сталася помилка.</b>

Спробуйте ще раз або зверніться до підтримки.
"""
)

NAVIGATION_MENU_TEXT = (
    """🧭 <b>Навігація</b>

Оберіть категорію:
"""
)

NAVIGATION_INTERACTIVE_TEXT = (
    """🧭 <b>Доступні розділи:</b>

🥷 Персонажі
📚 Гайди
🛡️ Білди
⚖️ Контр-піки
📊 Голосування

Оберіть потрібний розділ.
"""
)

PROFILE_MENU_TEXT = (
    """🪪 <b>Мій Профіль</b>

Перегляньте та налаштуйте дані профілю.
"""
)

PROFILE_INTERACTIVE_TEXT = (
    """🔍 <b>Ваш Профіль:</b>

• 🏅 Ім'я: {username}
• 🧬 Рівень: {level}
• 📈 Рейтинг: {rating}
• 🎯 Досягнення: {achievements_count}

Оберіть опцію для редагування профілю або перегляду статистики.
"""
)

BACK_TO_MAIN_MENU_TEXT = "🔙 Повернутися до головного меню"

HEROES_MENU_TEXT = (
    """🥷 <b>Персонажі</b>

Оберіть клас героїв.
"""
)

HEROES_INTERACTIVE_TEXT = (
    """🥷 <b>Персонажі:</b>

Оберіть клас: Танки, Маги, Стрільці, Асасіни, Сапорти, Бійці.
"""
)

HERO_CLASS_MENU_TEXT = (
    """🔹 <b>{hero_class}</b>

Оберіть опцію для інформації про {hero_class}.
"""
)

HERO_CLASS_INTERACTIVE_TEXT = (
    """🔹 <b>Клас: {hero_class}</b>

Оберіть дію: опис, статистика, білди, стратегії, назад.
"""
)

GUIDES_MENU_TEXT = (
    """📚 <b>Гайди</b>

Оберіть категорію гайдів:
Нові, Топ, Для новачків, Стратегії, Команда
"""
)

GUIDES_INTERACTIVE_TEXT = (
    """📚 <b>Гайди</b>:

Оберіть категорію: Нові, Популярні, Початківцям, Просунуті техніки, Команда.
"""
)

NEW_GUIDES_TEXT = (
    """🆕 Нові гайди:

Гайд 1, Гайд 2, Гайд 3.
"""
)

POPULAR_GUIDES_TEXT = (
    """🌟 Топ гайди:

Гайд A, Гайд B, Гайд C.
"""
)

BEGINNER_GUIDES_TEXT = (
    """📘 Для початківців:

Основи, Вибір героя, Перша гра.
"""
)

ADVANCED_TECHNIQUES_TEXT = (
    """🧙 Стратегії:

Техніка X, Y, Z.
"""
)

TEAMPLAY_GUIDES_TEXT = (
    """🤝 Команда:

Координація, Ролі гравців, Стратегії.
"""
)

COUNTER_PICKS_MENU_TEXT = (
    """⚖️ Протидії

Виберіть: Шукати контр-пік або Список.
"""
)

COUNTER_PICKS_INTERACTIVE_TEXT = (
    """⚖️ Протидії:

🔎 Шукати контр-пік
📄 Список контр-піків
🔙 Назад
"""
)

COUNTER_SEARCH_TEXT = (
    """🔎 Шукати контр-пік:

Введіть ім'я героя.
"""
)

COUNTER_LIST_TEXT = (
    """📄 Список контр-піків:

Герой 1: Контр-пік 1
...
"""
)

BUILDS_MENU_TEXT = (
    """🛡️ Снаряга

Оберіть: Новий білд, Збережені, Популярні.
"""
)

BUILDS_INTERACTIVE_TEXT = (
    """🛡️ Снаряга:

Новий, Мої білди, Популярні білди.
"""
)

CREATE_BUILD_TEXT = (
    """🏗️ Новий білд:

Введіть назву білду.
"""
)

MY_BUILDS_TEXT = (
    """📄 Збережені білди:

Білд 1, 2, 3.
"""
)

POPULAR_BUILDS_TEXT = (
    """🔥 Популярні білди:

Білд A, B, C.
"""
)

VOTING_MENU_TEXT = (
    """📊 Опитування:

Оберіть: Активні, Ваші, Ідея.
"""
)

VOTING_INTERACTIVE_TEXT = (
    """📊 Опитування:

📍 Активні
📋 Ваші
➕ Ідея
🔙 Назад
"""
)

CURRENT_VOTES_TEXT = (
    """📍 Активні опитування:

1, 2, 3.
"""
)

MY_VOTES_TEXT = (
    """📋 Ваші голосування:

A, B, C.
"""
)

SUGGEST_TOPIC_TEXT = (
    """➕ Ідея:

Введіть тему.
"""
)

SUGGESTION_RESPONSE_TEXT = (
    """✅ Пропозиція "{topic}" прийнята.
"""
)

STATISTICS_MENU_TEXT = (
    """📈 Дані

Оберіть: Активність, Рейтинг, Ігри.
"""
)

STATISTICS_INTERACTIVE_TEXT = (
    """📈 Статистика:

📊 Активність
🥇 Рейтинг
🎮 Ігри
🔙 Назад
"""
)

ACTIVITY_TEXT = (
    """📊 Активність:

Граєте: {games_played}, Виграно: {wins}, Програно: {losses}.
"""
)

RANKING_TEXT = (
    """🥇 Рейтинг:

Ваш рейтинг: {rating}.
"""
)

GAME_STATS_TEXT = (
    """🎮 Ігри:

Вбивств: {kills}, Смертей: {deaths}, Асистів: {assists}.
"""
)

ACHIEVEMENTS_MENU_TEXT = (
    """🏆 Успіхи

Бейджі, Прогрес, Турнірна статистика, Нагороди.
"""
)

ACHIEVEMENTS_INTERACTIVE_TEXT = (
    """🏆 Досягнення:

🎖️ Бейджі
🚀 Прогрес
🏅 Турнірна статистика
🎟️ Нагороди
🔙 Назад
"""
)

BADGES_TEXT = (
    """🎖️ Бейджі:

1, 2, 3.
"""
)

PROGRESS_TEXT = (
    """🚀 Прогрес:

Рівень: {level}, Досвід: {experience}%, Нові досягнення: {new_achievements}.
"""
)

TOURNAMENT_STATS_TEXT = (
    """🏅 Турнірна статистика:

Участь: {tournaments_participated}, Виграно: {tournaments_won}, Програно: {tournaments_lost}.
"""
)

AWARDS_TEXT = (
    """🎟️ Нагороди:

Нагорода 1, 2, 3.
"""
)

SETTINGS_MENU_TEXT = (
    """⚙️ Опції

Мова, Нік, ID, Алєрти.
"""
)

SETTINGS_INTERACTIVE_TEXT = (
    """⚙️ Налаштування:

🌐 Мова
ℹ️ Нік
🆔 ID
🔔 Алєрти
🔙 Назад
"""
)

LANGUAGE_TEXT = (
    """🌐 Мова:

Оберіть мову: Українська, Англійська.
"""
)

CHANGE_USERNAME_TEXT = (
    """ℹ️ Нік:

Введіть новий нік.
"""
)

UPDATE_ID_TEXT = (
    """🆔 ID:

Введіть новий ID.
"""
)

NOTIFICATIONS_TEXT = (
    """🔔 Алєрти:

Налаштуйте сповіщення.
"""
)

FEEDBACK_MENU_TEXT = (
    """💌 Відгук

✏️ Пропозиція
🐛 Помилка
🔙 Назад
"""
)

FEEDBACK_INTERACTIVE_TEXT = (
    """💌 Зворотний зв'язок:

✏️ Пропозиція
🐛 Помилка
🔙 Назад
"""
)

SEND_FEEDBACK_TEXT = (
    """✏️ Пропозиція:

Опишіть ваш відгук.
"""
)

REPORT_BUG_TEXT = (
    """🐛 Помилка:

Опишіть помилку.
"""
)

FEEDBACK_RECEIVED_TEXT = (
    """✅ Відгук отримано.
"""
)

BUG_REPORT_RECEIVED_TEXT = (
    """✅ Помилку отримано, працюємо над виправленням.
"""
)

HELP_MENU_TEXT = (
    """❓ Питання

📄 Гайд
❔ FAQ
📞 Контакти
🔙 Назад
"""
)

HELP_INTERACTIVE_TEXT = (
    """❓ Допомога:

📄 Гайд
❔ FAQ
📞 Контакти
🔙 Назад
"""
)

INSTRUCTIONS_TEXT = (
    """📄 Гайд:

Інструкції щодо користування.
"""
)

FAQ_TEXT = (
    """❔ FAQ:

Найчастіші питання.
"""
)

HELP_SUPPORT_TEXT = (
    """📞 Контакти:

Email, Телефон.
"""
)

GENERIC_ERROR_MESSAGE_TEXT = (
    "⚠️ Сталася технічна помилка. Повторіть пізніше."
)

USE_BUTTON_NAVIGATION_TEXT = (
    "🔘 Використовуйте кнопки нижче для навігації."
)

SEARCH_HERO_RESPONSE_TEXT = (
    """🔎 Пошук героя {hero_name}:

Поки що недоступно.
"""
)

CHANGE_USERNAME_RESPONSE_TEXT = (
    """ℹ️ Новий нік {new_username} прийнято.
"""
)

MLS_BUTTON_RESPONSE_TEXT = (
    "🔹 MLS кнопка натиснута. Функція в розробці."
)

UNHANDLED_INLINE_BUTTON_TEXT = (
    "⚠️ Кнопка не підтримується."
)

MAIN_MENU_BACK_TO_PROFILE_TEXT = (
    "🔙 Повернення до «Мій Профіль»"
)
