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

console = Console(record=True)
profile_table = Table(
    title="Ваш Профіль",
    box=DOUBLE,
    show_header=True,
    header_style="bold cyan",
    style="dim"
)
profile_table.add_column("Параметр", style="bold yellow", no_wrap=True)
profile_table.add_column("Значення", style="magenta", justify="center")

profile_table.add_row("Ім'я користувача", "{username}")
profile_table.add_row("Рівень", "{level}")
profile_table.add_row("Рейтинг", "{rating}")
profile_table.add_row("Досягнення", "{achievements_count}")

console.print(profile_table)
PROFILE_TABLE_TEXT = console.export_text()

WELCOME_NEW_USER_TEXT = (
    """🔥 <b>Ласкаво просимо до Mobile Legends: Starts</b> – вашого нового незамінного партнера у світі <b>Mobile Legends: Bang Bang!</b> 🔥

🎮 Тут ви отримаєте доступ до широкого спектра можливостей, які допоможуть зрозуміти гру глибше, <i>вдосконалити навички</i> та вивести ігровий досвід на новий рівень.

Ви зможете:
• 🥷 <b>Досліджувати</b> характеристики та ролі різних героїв.
• 📚 <i>Отримувати</i> покрокові гайди, тактичні поради та рекомендації щодо білдів.
• 📊 <u>Аналізувати</u> власну статистику та прогрес для обґрунтованих рішень у грі.
• 🏆 <b>Брати участь</b> у турнірах, знаходити нові стратегії та здобувати унікальні нагороди.

🏆 <b>Готові до нових пригод?</b> Натискайте нижче, щоб розпочати подорож до найвищих вершин Mobile Legends!

<i>Цей застосунок створено з любов’ю для справжніх поціновувачів Mobile Legends.</i> 💖
"""
)

INTRO_PAGE_1_TEXT = WELCOME_NEW_USER_TEXT

INTRO_PAGE_2_TEXT = (
    """💡 <b>Функції Mobile Legends: Starts:</b>

🧭 <b>Навігація:</b> швидкий доступ до героїв, гайдів, білдів та статистики.
👤 <b>Мій профіль:</b> переглядайте рівень, рейтинг, досягнення та персональні дані.
🥷 <b>Персонажі:</b> детальна інформація про кожного героя.
📚 <b>Гайди:</b> стратегії та поради для новачків і досвідчених гравців.
📊 <b>Статистика:</b> аналізуйте ігрові дані, результати матчів.
🔧 <b>Білди:</b> створюйте та редагуйте спорядження під різні ситуації.
🏆 <b>Турніри:</b> дізнавайтеся про змагання, нагороди та покращуйте навички.

<i>Натисніть «Далі», щоб дізнатися про інші можливості цього застосунку.</i>
"""
)

INTRO_PAGE_3_TEXT = (
    f"""<b>Ось ваш профіль у форматі таблиці (демо вигляд):</b>

<pre>{PROFILE_TABLE_TEXT}</pre>

Скористайтеся меню внизу, щоб перейти до будь-якого розділу.
Натисніть «Розпочати» для переходу до головного меню.
"""
)

MAIN_MENU_TEXT = (
    """👋 <b>Вітаємо, {user_first_name}, у Mobile Legends: Starts!</b>

Оберіть потрібну опцію нижче, щоб вдосконалювати свій ігровий досвід.
"""
)

MAIN_MENU_DESCRIPTION = (
    """🎮 <b>Mobile Legends: Starts</b> допоможе вам:

🏆 <i>Організовувати турніри</i>: створюйте та керуйте змаганнями.
📸 <i>Зберігати скріншоти</i> персонажів: діліться стратегічними нотатками.
📊 <i>Відстежувати активність</i>: аналізуйте матчі, результати та тенденції.
🥇 <i>Отримувати досягнення</i>: здобувайте винагороди за ваші зусилля.
"""
)

MAIN_MENU_ERROR_TEXT = (
    """❗ <b>Сталася помилка.</b>

Будь ласка, спробуйте ще раз або поверніться до головного меню.
"""
)

# Решта текстів залишено за аналогією, тому що вони вже відформатовані.
# Нижче - лише посилання на змінні. Їх можна використовувати без змін:

NAVIGATION_MENU_TEXT = """🧭 <b>Навігація</b>\n\nОберіть розділ: герої, гайди, білди, контр-піки чи голосування."""
NAVIGATION_SUBMENU_TEXT = """🔥 <b>META:</b> актуальні тенденції гри.\n🏆 <b>M6:</b> спеціальні події та нагороди.\n👾 <b>GPT:</b> AI підтримка та відповіді на ваші запитання.\n\nОберіть категорію, щоб переглянути список героїв."""
NAVIGATION_INTERACTIVE_TEXT = """🧭 <b>Доступні розділи:</b>\n\n🥷 Персонажі\n📚 Гайди\n🔧 Білди\n⚖️ Контр-піки\n📊 Голосування\n🔥 META\n🏆 M6\n👾 GPT"""

PROFILE_MENU_TEXT = """🪪 <b>Мій Профіль</b>\n\nТут ви можете редагувати дані профілю, переглянути свій рейтинг, рівень та досягнення."""
PROFILE_INTERACTIVE_TEXT = """🔍 <b>Ваш Профіль:</b>\n\n🏅 Ім'я користувача: {username}\n🧬 Рівень: {level}\n📈 Рейтинг: {rating}\n🎯 Досягнення: {achievements_count}\n\nОберіть опцію для редагування профілю чи перегляду детальної статистики."""
BACK_TO_MAIN_MENU_TEXT = "🔙 Повернення до головного меню"

HEROES_MENU_TEXT = """🥷 <b>Персонажі</b>\n\nОберіть категорію героїв для формування стратегій."""
HEROES_INTERACTIVE_TEXT = """📂 <b>Категорії героїв:</b>\n\n🛡️ Танк\n🧙‍♂️ Маг\n🏹 Стрілець\n⚔️ Асасін\n❤️ Підтримка\n🗡️ Боєць\n🔥 META\n🏆 M6\n👾 GPT"""
HERO_CLASS_MENU_TEXT = """Виберіть героя з класу <b>{hero_class}</b>, щоб отримати докладну інформацію."""
HERO_CLASS_INTERACTIVE_TEXT = """📜 <b>Герої класу {hero_class}:</b>\n\nОбравши героя, ви дізнаєтеся про здібності, білди та стратегії."""

GUIDES_MENU_TEXT = """📚 <b>Гайди</b>\n\nОберіть розділ гайдів."""
GUIDES_INTERACTIVE_TEXT = """📖 <b>Підрозділи гайдів:</b>\n\n🆕 Нові Гайди\n🌟 Популярні Гайди\n📘 Початківці\n🧙 Стратегії\n🤝 Командна Гра"""
NEW_GUIDES_TEXT = """📄 <b>Нові гайди:</b>\n\nПоки відсутні. Слідкуйте за оновленнями."""
POPULAR_GUIDES_TEXT = """🌟 <b>Популярні гайди:</b>\n\nНаразі немає списку."""
BEGINNER_GUIDES_TEXT = """📘 <b>Гайди для Початківців:</b>\n\nСкоро будуть доступні."""
ADVANCED_TECHNIQUES_TEXT = """🧙 <b>Стратегії гри:</b>\n\nМатеріали з'являться пізніше."""
TEAMPLAY_GUIDES_TEXT = """🤝 <b>Командна Гра:</b>\n\nНезабаром гайди для командної взаємодії."""

COUNTER_PICKS_MENU_TEXT = """⚖️ <b>Контр-піки</b>\n\nОберіть опцію для перегляду або створення контр-піків."""
COUNTER_PICKS_INTERACTIVE_TEXT = """🕵️‍♂️ <b>Контр-піки:</b>\n\n🔎 Переглянути контр-піки\n📝 Створити власний контр-пік\n🔥 Популярні контр-піки"""
COUNTER_SEARCH_TEXT = "🔎 Введіть ім'я героя для пошуку контр-піків:"
COUNTER_LIST_TEXT = """📃 <b>Список контр-піків:</b>\n\nІнформація наразі відсутня."""

BUILDS_MENU_TEXT = """🛡️ <b>Білди</b>\n\nСтворюйте і керуйте білдами."""
BUILDS_INTERACTIVE_TEXT = """🔧 <b>Опції білдів:</b>\n\n🏗️ Створити новий білд\n📄 Обрані білди\n🔥 Популярні білди"""
CREATE_BUILD_TEXT = """🏗️ <b>Створення білду:</b>\n\nФункція буде доступна незабаром."""
MY_BUILDS_TEXT = """📄 <b>Мої білди:</b>\n\nПоки немає збережених білдів."""
POPULAR_BUILDS_TEXT = """🔥 <b>Популярні білди:</b>\n\nНаразі недоступно."""

VOTING_MENU_TEXT = """📊 <b>Голосування</b>\n\nБеріть участь в опитуваннях і впливайте на розвиток."""
VOTING_INTERACTIVE_TEXT = """🗳️ <b>Опції голосування:</b>\n\n📍 Поточні Опитування\n📋 Мої Голосування\n➕ Запропонувати Тему"""
CURRENT_VOTES_TEXT = """📍 <b>Поточні голосування:</b>\n\nНемає активних опитувань."""
MY_VOTES_TEXT = """📋 <b>Мої голосування:</b>\n\nІсторія відсутня."""
SUGGEST_TOPIC_TEXT = "➕ Введіть тему нового голосування:"
SUGGESTION_RESPONSE_TEXT = """✅ Ви запропонували тему: "<i>{topic}</i>"\n\nПропозиція буде розглянута."""

STATISTICS_MENU_TEXT = """📈 <b>Статистика</b>\n\nОберіть розділ для аналізу."""
STATISTICS_INTERACTIVE_TEXT = """📈 <b>Підрозділи статистики:</b>\n\n📊 Загальна Активність\n🥇 Рейтинг\n🎮 Ігрова Статистика"""
ACTIVITY_TEXT = """📊 <b>Загальна активність:</b>\n\nДані недоступні."""
RANKING_TEXT = """🥇 <b>Рейтинг:</b>\n\nІнформація недоступна."""
GAME_STATS_TEXT = """🎮 <b>Ігрова статистика:</b>\n\nЗ'явиться пізніше."""

ACHIEVEMENTS_MENU_TEXT = """🏆 <b>Досягнення</b>\n\nПерегляньте свої здобутки."""
ACHIEVEMENTS_INTERACTIVE_TEXT = """🎖️ <b>Підрозділи досягнень:</b>\n\n🎖️ Мої Бейджі\n🚀 Прогрес\n🏅 Турнірна Статистика\n🎟️ Отримані Нагороди"""
BADGES_TEXT = """🎖️ <b>Ваші бейджі:</b>\n\nПоки немає бейджів."""
PROGRESS_TEXT = """🚀 <b>Ваш прогрес:</b>\n\nДані з'являться пізніше."""
TOURNAMENT_STATS_TEXT = """🏅 <b>Турнірна статистика:</b>\n\nНаразі даних немає."""
AWARDS_TEXT = """🎟️ <b>Ваші нагороди:</b>\n\nПоки немає нагород."""

SETTINGS_MENU_TEXT = """⚙️ <b>Налаштування</b>\n\nАдаптуйте застосунок під себе."""
SETTINGS_INTERACTIVE_TEXT = """🔧 <b>Опції налаштувань:</b>\n\n🌐 Мова Інтерфейсу\nℹ️ Змінити Username\n🆔 Оновити ID\n🔔 Сповіщення"""
LANGUAGE_TEXT = """🌐 <b>Зміна мови:</b>\n\nФункція поки недоступна."""
CHANGE_USERNAME_TEXT = "ℹ️ Введіть новий Username:"
UPDATE_ID_TEXT = """🆔 <b>Оновлення ID:</b>\n\nФункція в розробці."""
NOTIFICATIONS_TEXT = """🔔 <b>Налаштування сповіщень:</b>\n\nНедоступно поки що."""

FEEDBACK_MENU_TEXT = """💌 <b>Зворотний Зв'язок</b>\n\nНадішліть відгук або повідомте про помилку."""
FEEDBACK_INTERACTIVE_TEXT = """✏️ <b>Опції зворотного зв'язку:</b>\n\n📝 Надіслати Відгук\n🐛 Повідомити про Помилку"""
SEND_FEEDBACK_TEXT = "📝 Введіть ваш відгук:"
REPORT_BUG_TEXT = "🐛 Опишіть помилку:"
FEEDBACK_RECEIVED_TEXT = """✅ Дякуємо за ваш відгук! Ми врахуємо ваші пропозиції."""
BUG_REPORT_RECEIVED_TEXT = """✅ Дякуємо за звіт про помилку! Ми спробуємо виправити її якомога швидше."""

HELP_MENU_TEXT = """❓ <b>Допомога</b>\n\nОтримайте додаткові інструкції або зверніться до підтримки."""
HELP_INTERACTIVE_TEXT = """📄 <b>Опції допомоги:</b>\n\n📄 Інструкції\n❔ FAQ\n📞 Підтримка"""
INSTRUCTIONS_TEXT = """📄 <b>Інструкції:</b>\n\nНаразі відсутні, але скоро будуть додані."""
FAQ_TEXT = """❔ <b>FAQ:</b>\n\nПоки немає. Залишайтесь з нами."""
HELP_SUPPORT_TEXT = """📞 <b>Підтримка:</b>\n\nЯкщо у вас виникли питання, пишіть на: <a href="mailto:support@mobilelegendsbot.com">support@mobilelegendsbot.com</a>"""

UNKNOWN_COMMAND_TEXT = """❗ <b>Невідома команда.</b>\n\nСкористайтеся меню або зверніться до розділу «Допомога»."""
GENERIC_ERROR_MESSAGE_TEXT = """⚠️ <b>Сталася технічна помилка.</b>\n\nСпробуйте пізніше."""
ERROR_MESSAGE_TEXT = """⚠️ <b>Сталася помилка.</b>\n\nЯкщо проблема не зникне, зверніться до підтримки."""
USE_BUTTON_NAVIGATION_TEXT = """🔘 Використовуйте кнопки нижче для навігації."""
SEARCH_HERO_RESPONSE_TEXT = """🔎 Ви шукаєте героя: <i>{hero_name}</i>.\n\nПошук поки не підтримується."""
CHANGE_USERNAME_RESPONSE_TEXT = """ℹ️ Новий Username: <b>{new_username}</b> буде застосовано пізніше."""
MLS_BUTTON_RESPONSE_TEXT = """🔹 Ви натиснули кнопку MLS.\n\nЦя функція поки не реалізована."""
UNHANDLED_INLINE_BUTTON_TEXT = """⚠️ Ця кнопка поки не оброблена. Оберіть іншу опцію."""
MAIN_MENU_BACK_TO_PROFILE_TEXT = """🔙 Повернення до «Мій Профіль»."""
AI_INTRO_TEXT = """🤖 <b>AI Підтримка</b>\n\nМожете ставити запитання про гру, героїв і стратегії."""
AI_RESPONSE_TEXT = """<b>Відповідь AI:</b>\n{response}"""
LAST_MATCH_ANALYSIS_TEXT = """🎮 <b>Аналіз останнього матчу:</b>\n\nОтримайте детальний розбір: вибір героїв, результат, ключові фактори."""
META_MENU_TEXT = """🔥 <b>META</b>\n\nАналіз актуальних тенденцій гри та стратегій."""
META_INTERACTIVE_TEXT = """🔥 <b>META:</b>\n\n📈 Аналіз тенденцій\n🥇 Топ герої\n🧠 Стратегії"""
M6_MENU_TEXT = """🏆 <b>M6</b>\n\nСпеціальні події та ексклюзивні нагороди."""
M6_INTERACTIVE_TEXT = """🏆 <b>M6:</b>\n\n🎉 Події\n🏅 Нагороди\n🚀 Можливості"""
GPT_MENU_TEXT = """👾 <b>GPT</b>\n\nAI підтримка та відповіді на ваші запитання."""
GPT_INTERACTIVE_TEXT = """👾 <b>GPT:</b>\n\n🤖 Поставте питання\n📚 Отримайте поради\n🧠 Складні питання"""

if __name__ == "__main__":
    # Демонстрація створення таблиці для героїв
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
    print(table_text)

    # Приклад створення графіку за допомогою Matplotlib:
    # Наприклад, статистика за останні 5 матчів: кількість вбивств
    kills = [5, 2, 7, 3, 6]
    matches = [1, 2, 3, 4, 5]
    plt.figure(figsize=(5,3))
    plt.plot(matches, kills, marker='o', color='blue', label='Вбивства')
    plt.title('Статистика останніх 5 матчів')
    plt.xlabel('Матч')
    plt.ylabel('Кількість вбивств')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('last_5_matches_stats.png')
    # Цей файл 'last_5_matches_stats.png' можна відправити користувачу як photo через Telegram-бот.

    # Аналогічно можна використовувати Seaborn чи Plotly для більш просунутих або інтерактивних графіків.
    # Seaborn приклад:
    data = pd.DataFrame({'Матч': matches, 'Вбивства': kills})
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(5,3))
    sns.barplot(x='Матч', y='Вбивства', data=data, palette='pastel')
    plt.title('Статистика Вбивств (Seaborn)')
    plt.tight_layout()
    plt.savefig('kills_seaborn.png')

    # Plotly приклад (статичний):
    fig = px.line(x=matches, y=kills, markers=True, title='Статистика Вбивств (Plotly)')
    fig.write_image('kills_plotly.png')
    # 'kills_plotly.png' також можна відправити користувачу.
