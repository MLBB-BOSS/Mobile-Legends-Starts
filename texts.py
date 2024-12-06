# texts.py

from rich.table import Table
from rich.console import Console
from rich.box import DOUBLE

def create_inline_table(title: str, headers: list[str], rows: list[list[str]]) -> str:
    """
    Створює ASCII-таблицю з використанням rich та повертає її як текст.
    
    :param title: Заголовок таблиці.
    :param headers: Список назв стовпчиків.
    :param rows: Дані для таблиці - список списків, де кожен внутрішній список - це рядок таблиці.
    :return: Рядок з ASCII-поданням таблиці.
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

# Створюємо консоль у пам'яті для профілю
console = Console(record=True)

# Створюємо та покращуємо таблицю профілю
profile_table = Table(
    title="Ваш Профіль",
    box=DOUBLE,
    show_header=True,
    header_style="bold cyan",
    style="dim"
)
profile_table.add_column("Параметр", style="bold yellow", no_wrap=True)
profile_table.add_column("Значення", style="magenta", justify="center")

# Використовуємо плейсхолдери {username}, {level}, {rating}, {achievements_count}
profile_table.add_row("Ім'я користувача", "{username}")
profile_table.add_row("Рівень", "{level}")
profile_table.add_row("Рейтинг", "{rating}")
profile_table.add_row("Досягнення", "{achievements_count}")

console.print(profile_table)
PROFILE_TABLE_TEXT = console.export_text()

WELCOME_NEW_USER_TEXT = (
    """🔥 Ласкаво просимо до Mobile Legends: Starts – вашого нового незамінного партнера у світі Mobile Legends: Bang Bang! 🔥

🎮 Тут ви отримаєте доступ до широкого спектра можливостей, які допоможуть зрозуміти гру глибше, вдосконалити навички та вивести ігровий досвід на новий рівень.

Ви зможете:
• 🥷 Досліджувати характеристики та ролі різних героїв.
• 📚 Отримувати покрокові гайди, тактичні поради та рекомендації щодо білдів.
• 📊 Аналізувати власну статистику та прогрес, щоб робити більш обґрунтовані рішення у грі.
• 🏆 Брати участь у турнірах, виявляти нові стратегії та здобувати унікальні нагороди.

🏆 Готові до нових пригод? Натискайте нижче, щоб розпочати подорож до найвищих вершин Mobile Legends!

Цей застосунок створено з любов’ю для справжніх поціновувачів Mobile Legends. 💖
"""
)

INTRO_PAGE_1_TEXT = WELCOME_NEW_USER_TEXT

INTRO_PAGE_2_TEXT = (
    """💡 Функції Mobile Legends: Starts:

🧭 Навігація: Зручний інтерфейс для швидкого доступу до героїв, гайдів, білдів та статистики.
👤 Мій профіль: Переглядайте свій рівень, рейтинг, досягнення та персональні дані.
🥷 Персонажі: Отримуйте вичерпну інформацію про кожного героя, його роль та стратегії.
📚 Гайди: Вивчайте матеріали для новачків і досвідчених гравців, опановуйте стратегії та поради.
📊 Статистика: Аналізуйте ігрові дані – перемоги, поразки, ефективність героїв.
🔧 Білди: Створюйте та редагуйте спорядження, адаптуйте його під різні ситуації.
🏆 Турніри: Дізнавайтеся про змагання, умови участі та нагороди, перевіряйте свої навички.

Натисніть «Далі», щоб дізнатися про інші можливості цього застосунку.
"""
)

INTRO_PAGE_3_TEXT = (
    f"""Ось ваш профіль у форматі таблиці (демо вигляд):

{PROFILE_TABLE_TEXT}

Скористайтеся меню внизу, щоб перейти до будь-якого розділу.
Натисніть «Розпочати» для переходу до головного меню.
"""
)

MAIN_MENU_TEXT = (
    """👋 Вітаємо, {user_first_name}, у Mobile Legends: Starts!

Оберіть потрібну опцію нижче, щоб досліджувати можливості та вдосконалювати свій ігровий досвід.
"""
)

MAIN_MENU_DESCRIPTION = (
    """🎮 Mobile Legends: Starts допоможе вам:

🏆 Організовувати турніри: Створюйте власні змагання та керуйте ними.
📸 Зберігати скріншоти персонажів: Робіть візуальні нотатки та діліться ними.
📊 Відстежувати активність: Аналізуйте частоту та результати матчів.
🥇 Отримувати досягнення: Здобувайте винагороди за ваші зусилля.
"""
)

MAIN_MENU_ERROR_TEXT = (
    """❗ Сталася помилка.

Будь ласка, спробуйте ще раз або поверніться до головного меню. Якщо проблема не зникне, зверніться до підтримки.
"""
)

NAVIGATION_MENU_TEXT = (
    """🧭 Навігація

Оберіть розділ: герої, гайди, білди, контр-піки чи голосування.
"""
)

NAVIGATION_SUBMENU_TEXT = (
    """🔥 META: актуальні тенденції гри.
🏆 M6: спеціальні події та нагороди.
👾 GPT: AI підтримка та відповіді на ваші запитання.

Оберіть категорію, щоб переглянути список героїв."""
)

NAVIGATION_INTERACTIVE_TEXT = (
    """🧭 Доступні розділи:

🥷 Персонажі
📚 Гайди
🔧 Білди
⚖️ Контр-піки
📊 Голосування
🔥 META
🏆 M6
👾 GPT
"""
)

PROFILE_MENU_TEXT = (
    """🪪 Мій Профіль

Тут ви можете редагувати дані профілю, переглянути свій рейтинг, рівень та досягнення.
"""
)

PROFILE_INTERACTIVE_TEXT = (
    """🔍 Ваш Профіль:

🏅 Ім'я користувача: {username}
🧬 Рівень: {level}
📈 Рейтинг: {rating}
🎯 Досягнення: {achievements_count}

Оберіть опцію для редагування профілю чи перегляду детальної статистики.
"""
)

BACK_TO_MAIN_MENU_TEXT = "🔙 Повернення до головного меню"

HEROES_MENU_TEXT = (
    """🥷 Персонажі

Оберіть категорію героїв для формування стратегій.
"""
)

HEROES_INTERACTIVE_TEXT = (
    """📂 Категорії героїв:

🛡️ Танк
🧙‍♂️ Маг
🏹 Стрілець
⚔️ Асасін
❤️ Підтримка
🗡️ Боєць
🔥 META
🏆 M6
👾 GPT
"""
)

HERO_CLASS_MENU_TEXT = (
    """Виберіть героя з класу <b>{hero_class}</b>, щоб отримати докладну інформацію."""
)

HERO_CLASS_INTERACTIVE_TEXT = (
    """📜 Герої класу {hero_class}:

Обравши героя, ви зможете дізнатися про здібності, білди та стратегії використання.
"""
)

GUIDES_MENU_TEXT = (
    """📚 Гайди

Оберіть розділ гайдів.
"""
)

GUIDES_INTERACTIVE_TEXT = (
    """📖 Підрозділи гайдів:

🆕 Нові Гайди
🌟 Популярні Гайди
📘 Початківці
🧙 Стратегії
🤝 Командна Гра
"""
)

NEW_GUIDES_TEXT = (
    """📄 Нові гайди:

Поки відсутні. Слідкуйте за оновленнями.
"""
)

POPULAR_GUIDES_TEXT = (
    """🌟 Популярні гайди:

Наразі немає списку.
"""
)

BEGINNER_GUIDES_TEXT = (
    """📘 Гайди для Початківців:

Скоро будуть доступні.
"""
)

ADVANCED_TECHNIQUES_TEXT = (
    """🧙 Стратегії гри:

Матеріали з'являться пізніше.
"""
)

TEAMPLAY_GUIDES_TEXT = (
    """🤝 Командна Гра:

Незабаром з'являться гайди для командної взаємодії.
"""
)

COUNTER_PICKS_MENU_TEXT = (
    """⚖️ Контр-піки

Оберіть опцію для перегляду або створення контр-піків.
"""
)

COUNTER_PICKS_INTERACTIVE_TEXT = (
    """🕵️‍♂️ Контр-піки:

🔎 Переглянути контр-піки
📝 Створити власний контр-пік
🔥 Популярні контр-піки
"""
)

COUNTER_SEARCH_TEXT = "🔎 Введіть ім'я героя для пошуку контр-піків:"
COUNTER_LIST_TEXT = (
    """📃 Список контр-піків:

Інформація наразі відсутня.
"""
)

BUILDS_MENU_TEXT = (
    """🛡️ Білди

Створюйте і керуйте білдами.
"""
)

BUILDS_INTERACTIVE_TEXT = (
    """🔧 Опції білдів:

🏗️ Створити новий білд
📄 Обрані білди
🔥 Популярні білди
"""
)

CREATE_BUILD_TEXT = (
    """🏗️ Створення білду:

Функція буде доступна незабаром.
"""
)

MY_BUILDS_TEXT = (
    """📄 Мої білди:

Поки немає збережених білдів.
"""
)

POPULAR_BUILDS_TEXT = (
    """🔥 Популярні білди:

Наразі недоступно.
"""
)

VOTING_MENU_TEXT = (
    """📊 Голосування

Беріть участь в опитуваннях та впливайте на розвиток.
"""
)

VOTING_INTERACTIVE_TEXT = (
    """🗳️ Опції голосування:

📍 Поточні Опитування
📋 Мої Голосування
➕ Запропонувати Тему
"""
)

CURRENT_VOTES_TEXT = (
    """📍 Поточні голосування:

Немає активних опитувань.
"""
)

MY_VOTES_TEXT = (
    """📋 Мої голосування:

Історія відсутня.
"""
)

SUGGEST_TOPIC_TEXT = "➕ Введіть тему нового голосування:"
SUGGESTION_RESPONSE_TEXT = (
    """✅ Ви запропонували тему: "<i>{topic}</i>"

Пропозиція буде розглянута.
"""
)

STATISTICS_MENU_TEXT = (
    """📈 Статистика

Оберіть розділ для аналізу.
"""
)

STATISTICS_INTERACTIVE_TEXT = (
    """📈 Підрозділи статистики:

📊 Загальна Активність
🥇 Рейтинг
🎮 Ігрова Статистика
"""
)

ACTIVITY_TEXT = (
    """📊 Загальна активність:

Дані недоступні.
"""
)

RANKING_TEXT = (
    """🥇 Рейтинг:

Інформація недоступна.
"""
)

GAME_STATS_TEXT = (
    """🎮 Ігрова статистика:

З'явиться пізніше.
"""
)

ACHIEVEMENTS_MENU_TEXT = (
    """🏆 Досягнення

Перегляньте свої здобутки.
"""
)

ACHIEVEMENTS_INTERACTIVE_TEXT = (
    """🎖️ Підрозділи досягнень:

🎖️ Мої Бейджі
🚀 Прогрес
🏅 Турнірна Статистика
🎟️ Отримані Нагороди
"""
)

BADGES_TEXT = (
    """🎖️ Ваші бейджі:

Поки немає бейджів.
"""
)

PROGRESS_TEXT = (
    """🚀 Ваш прогрес:

Дані з'являться пізніше.
"""
)

TOURNAMENT_STATS_TEXT = (
    """🏅 Турнірна статистика:

Наразі даних немає.
"""
)

AWARDS_TEXT = (
    """🎟️ Ваші нагороди:

Поки немає нагород.
"""
)

SETTINGS_MENU_TEXT = (
    """⚙️ Налаштування

Адаптуйте застосунок під себе.
"""
)

SETTINGS_INTERACTIVE_TEXT = (
    """🔧 Опції налаштувань:

🌐 Мова Інтерфейсу
ℹ️ Змінити Username
🆔 Оновити ID
🔔 Сповіщення
"""
)

LANGUAGE_TEXT = (
    """🌐 Зміна мови:

Функція поки недоступна.
"""
)

CHANGE_USERNAME_TEXT = "ℹ️ Введіть новий Username:"
UPDATE_ID_TEXT = (
    """🆔 Оновлення ID:

Функція в розробці.
"""
)

NOTIFICATIONS_TEXT = (
    """🔔 Налаштування сповіщень:

Недоступно поки що.
"""
)

FEEDBACK_MENU_TEXT = (
    """💌 Зворотний Зв'язок

Надішліть відгук або повідомте про помилку.
"""
)

FEEDBACK_INTERACTIVE_TEXT = (
    """✏️ Опції зворотного зв'язку:

📝 Надіслати Відгук
🐛 Повідомити про Помилку
"""
)

SEND_FEEDBACK_TEXT = "📝 Введіть ваш відгук:"
REPORT_BUG_TEXT = "🐛 Опишіть помилку:"
FEEDBACK_RECEIVED_TEXT = (
    """✅ Дякуємо за ваш відгук! Ми врахуємо ваші пропозиції."""
)

BUG_REPORT_RECEIVED_TEXT = (
    """✅ Дякуємо за звіт про помилку! Ми спробуємо виправити її якомога швидше."""
)

HELP_MENU_TEXT = (
    """❓ Допомога

Отримайте додаткові інструкції або зверніться до підтримки.
"""
)

HELP_INTERACTIVE_TEXT = (
    """📄 Опції допомоги:

📄 Інструкції
❔ FAQ
📞 Підтримка
"""
)

INSTRUCTIONS_TEXT = (
    """📄 Інструкції:

Наразі відсутні, але скоро будуть додані.
"""
)

FAQ_TEXT = (
    """❔ FAQ:

Поки немає. Залишайтесь з нами.
"""
)

HELP_SUPPORT_TEXT = (
    """📞 Підтримка:

Якщо у вас виникли питання, пишіть на: <a href="mailto:support@mobilelegendsbot.com">support@mobilelegendsbot.com</a>
"""
)

UNKNOWN_COMMAND_TEXT = (
    """❗ Невідома команда.

Скористайтеся меню або зверніться до розділу «Допомога»."""
)

GENERIC_ERROR_MESSAGE_TEXT = (
    """⚠️ Сталася технічна помилка.

Спробуйте пізніше."""
)

ERROR_MESSAGE_TEXT = (
    """⚠️ Сталася помилка.

Якщо проблема не зникне, зверніться до підтримки."""
)

USE_BUTTON_NAVIGATION_TEXT = (
    """🔘 Використовуйте кнопки нижче для навігації."""
)

SEARCH_HERO_RESPONSE_TEXT = (
    """🔎 Ви шукаєте героя: <i>{hero_name}</i>.

Пошук поки не підтримується."""
)

CHANGE_USERNAME_RESPONSE_TEXT = (
    """ℹ️ Новий Username: <b>{new_username}</b> буде застосовано пізніше."""
)

MLS_BUTTON_RESPONSE_TEXT = (
    """🔹 Ви натиснули кнопку MLS.

Ця функція поки не реалізована."""
)

UNHANDLED_INLINE_BUTTON_TEXT = (
    """⚠️ Ця кнопка поки не оброблена. Оберіть іншу опцію."""
)

MAIN_MENU_BACK_TO_PROFILE_TEXT = (
    """🔙 Повернення до «Мій Профіль»."""
)

AI_INTRO_TEXT = (
    """🤖 AI Підтримка

Можете ставити запитання про гру, героїв і стратегії."""
)

AI_RESPONSE_TEXT = (
    """<b>Відповідь AI:</b>
{response}"""
)

LAST_MATCH_ANALYSIS_TEXT = (
    """🎮 Аналіз останнього матчу:

Отримайте детальний розбір: вибір героїв, результат, ключові фактори."""
)

META_MENU_TEXT = (
    """🔥 META

Аналіз актуальних тенденцій гри та стратегій."""
)

META_INTERACTIVE_TEXT = (
    """🔥 META:

📈 Аналіз тенденцій
🥇 Топ герої
🧠 Стратегії"""
)

M6_MENU_TEXT = (
    """🏆 M6

Спеціальні події та ексклюзивні нагороди."""
)

M6_INTERACTIVE_TEXT = (
    """🏆 M6:

🎉 Події
🏅 Нагороди
🚀 Можливості"""
)

GPT_MENU_TEXT = (
    """👾 GPT

AI підтримка та відповіді на ваші запитання."""
)

GPT_INTERACTIVE_TEXT = (
    """👾 GPT:

🤖 Поставте питання
📚 Отримайте поради
🧠 Складні питання"""
)

# Приклад використання create_inline_table:
if __name__ == "__main__":
    # Приклад таблиці зі списком героїв
    heroes_data = [
        ["Alucard", "Fighter/Assassin", "Середня", "Висока"],
        ["Layla", "Marksman", "Легка", "Середня"],
        ["Tigreal", "Tank", "Важка", "Низька"]
    ]

    table_text = create_inline_table(
        title="Список героїв",
        headers=["Герой", "Клас", "Складність", "Потенціал"],
        rows=heroes_data
    )

    # У ботові можна використати:
    # await bot.send_message(chat_id, text=table_text)
    print(table_text)
