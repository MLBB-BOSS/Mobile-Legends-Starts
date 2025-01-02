# texts.py
# =============================================================================
# Повний та структурований файл із текстовими константами для бота.
# Тексти були удосконалені та очищені для покращення якості комунікації.
# =============================================================================

from enum import Enum

# ============================[ENUM CONSTANTS]===============================
# Константи, що представляють кнопки меню та мови інтерфейсу.

class MenuButton(Enum):
    CREATE_TOURNAMENT = "Створити Турнір"
    VIEW_TOURNAMENTS = "Переглянути Турніри"
    M6_INFO = "Інформація про M6"
    M6_STATS = "Статистика M6"
    M6_NEWS = "Новини M6"
    META = "META Інформація"
    COMPARISON = "Порівняння Героїв"
    VOTING = "Голосування"
    SEARCH_HERO = "Пошук Героя"
    COUNTER_SEARCH = "Пошук Контр-Піка"
    COUNTER_LIST = "Список Контр-Піків"
    CREATE_TEAM = "Створити Команду"
    VIEW_TEAMS = "Переглянути Команди"
    CREATE_TRADE = "Створити Торгівлю"
    VIEW_TRADES = "Переглянути Торгівлі"
    MANAGE_TRADES = "Управління Торгівлями"
    GPT_DATA_GENERATION = "Генерація Даних GPT"
    GPT_HINTS = "Поради GPT"
    GPT_HERO_STATS = "Статистика Героя GPT"

class LanguageButton(Enum):
    UKRAINIAN = "🇺🇦 Українська"
    ENGLISH = "🇬🇧 Англійська"
    BACK = "🔙 Назад"

# ============================[MENU BUTTON TO CLASS MAPPING]===================
# Мапінг кнопок меню до класів героїв та інших опцій.

MENU_BUTTON_TO_CLASS = {
    MenuButton.CREATE_TOURNAMENT.value: "Створити Турнір",
    MenuButton.VIEW_TOURNAMENTS.value: "Переглянути Турніри",
    MenuButton.M6_INFO.value: "Інформація про M6",
    MenuButton.M6_STATS.value: "Статистика M6",
    MenuButton.M6_NEWS.value: "Новини M6",
    MenuButton.META.value: "META Інформація",
    MenuButton.COMPARISON.value: "Порівняння Героїв",
    MenuButton.VOTING.value: "Голосування",
    MenuButton.SEARCH_HERO.value: "Пошук Героя",
    MenuButton.COUNTER_SEARCH.value: "Пошук Контр-Піка",
    MenuButton.COUNTER_LIST.value: "Список Контр-Піків",
    MenuButton.CREATE_TEAM.value: "Створити Команду",
    MenuButton.VIEW_TEAMS.value: "Переглянути Команди",
    MenuButton.CREATE_TRADE.value: "Створити Торгівлю",
    MenuButton.VIEW_TRADES.value: "Переглянути Торгівлі",
    MenuButton.MANAGE_TRADES.value: "Управління Торгівлями",
    MenuButton.GPT_DATA_GENERATION.value: "Генерація Даних GPT",
    MenuButton.GPT_HINTS.value: "Поради GPT",
    MenuButton.GPT_HERO_STATS.value: "Статистика Героя GPT",
    "Танк": "Танк",
    "Маг": "Маг",
    "Стрілець": "Стрілець",
    "Асасін": "Асасін",
    "Підтримка": "Підтримка",
    "Боєць": "Боєць"
}

# ============================[HEROES BY CLASS]===============================
# Інформація про героїв, згрупованих за класами.

heroes_by_class = {
    "Танк": [
        {"name": "Танк Герой 1", "description": "Сильний та витривалий, здатний витримувати великий обсяг шкоди."},
        {"name": "Танк Герой 2", "description": "Має здібності до контролю та захисту команди."},
    ],
    "Маг": [
        {"name": "Маг Герой 1", "description": "Використовує потужні магічні атаки для завдання шкоди ворогам."},
        {"name": "Маг Герой 2", "description": "Спеціалізується на масових атаках та контролі поля бою."},
    ],
    "Стрілець": [
        {"name": "Стрілець Герой 1", "description": "Відмінний у дальніх атаках, завдає значної шкоди з безпечної відстані."},
        {"name": "Стрілець Герой 2", "description": "Має високу мобільність та здатність швидко змінювати позицію."},
    ],
    "Асасін": [
        {"name": "Асасін Герой 1", "description": "Має високу швидкість та здатність швидко нейтралізувати ключових ворогів."},
        {"name": "Асасін Герой 2", "description": "Відмінний у швидких атаках та розриві ліній оборони."},
    ],
    "Підтримка": [
        {"name": "Підтримка Герой 1", "description": "Забезпечує лікування та бафи для команди, підсилюючи її ефективність."},
        {"name": "Підтримка Герой 2", "description": "Використовує здібності для контролю ворогів та захисту союзників."},
    ],
    "Боєць": [
        {"name": "Боєць Герой 1", "description": "Збалансований героїй зі здібностями до атаки та захисту."},
        {"name": "Боєць Герой 2", "description": "Має високий показник швидкості атаки та здатність завдавати критичної шкоди."},
    ],
}

# ============================[ERROR MESSAGES]===========================
# Набір текстових повідомлень, що інформують користувача про помилки.

LANGUAGE_TEXT = {
    "en": {
        "welcome": "Welcome to the Mobile Legends Starts bot!",
        "help": "Here is a list of commands you can use..."
    },
    "uk": {
        "welcome": "Ласкаво просимо до Mobile Legends Starts бота!",
        "help": "Ось список команд, які ви можете використовувати..."
    }
}

MAIN_MENU_ERROR_TEXT = """
❗ <b>Щось пішло не так.</b>
Ми перепрошуємо за незручності.
Спробуйте знову або зверніться до служби підтримки.
🔄 <i>Почати заново?</i>
"""

UNKNOWN_COMMAND_TEXT = """
❗ <b>Невідома команда.</b>
Вибачте, я не розумію ваш запит.
Скористайтеся меню нижче.
🔘 <i>Виберіть пункт меню для продовження.</i>
"""

GENERIC_ERROR_MESSAGE_TEXT = """
⚠️ <b>Трапилася помилка.</b>
Будь ласка, спробуйте пізніше або зверніться до підтримки.
"""

ERROR_MESSAGE_TEXT = """
⚠️ <b>Сталася помилка.</b>
Ми перепрошуємо за незручності.
Будь ласка, спробуйте знову або зверніться до технічної підтримки.
📞 <i>Зверніться:</i> support@mobilelegendsbot.com
"""

USE_BUTTON_NAVIGATION_TEXT = """
🖱️ Використовуйте кнопки для навігації.

Використання текстових команд може призвести до неочікуваних результатів.
🖱️ <i>Оберіть потрібний пункт меню.</i>
"""

UNHANDLED_INLINE_BUTTON_TEXT = """
⚠️ Ця кнопка наразі недоступна.

🔘 <i>Виберіть інший пункт з меню.</i>
"""

WELCOME_NEW_USER_TEXT = """
🌟 <b>Ласкаво просимо до Mobile Legends Starts!</b> 🌟

Вітаємо у спільноті <b>Mobile Legends Starts</b> – вашому надійному помічнику у світі <b>Mobile Legends</b>. Ми допоможемо вам вдосконалити ігрові навички, покращити стратегії та підкорити нові вершини в грі.

<b>Ось що ми пропонуємо:</b>
• Виконуйте цікаві місії й отримуйте нагороди, розвивайте свої можливості.
• Професійні поради та докладні огляди для вашого розвитку.
• Аналізуйте прогрес, знаходьте слабкі місця та вдосконалюйтесь.
• Експериментуйте зі спорядженням і знаходьте найкращі комбінації предметів для героїв.
• Спільне планування стратегій і пошук однодумців.
• Змагайтеся, набирайтесь досвіду та здобувайте призи.
• Збирайте унікальні нагороди та бейджі за ваші успіхи.
• Дізнавайтеся більше про героїв та їх сильні та слабкі сторони.

Натисніть <b>"Розпочати"</b>, щоб дізнатися більше! 🚀
"""

INTRO_PAGE_1_TEXT = """
🌟 <b>Ласкаво просимо до Mobile Legends Starts!</b> 🌟

Привіт, <b>{user_first_name}</b>! 🎉 Ви щойно приєдналися до найактивнішої спільноти гравців <b>Mobile Legends</b>. Ми тут, щоб допомогти вам досягти нових висот у грі! 🚀

<b>Основні можливості нашого бота:</b>
• Виконуйте цікаві місії та отримуйте щедрі нагороди.
• Отримуйте професійні поради та детальні огляди для покращення своїх навичок.
• Аналізуйте свій прогрес та вдосконалюйтесь завдяки детальній статистиці.

➡️ <i>Продовжити</i>
"""

INTRO_PAGE_2_TEXT = """
🤝 <b>Командна гра та Турніри</b>

Об'єднуйтесь з іншими гравцями та створюйте непереможні команди! 👫 Разом ви зможете планувати стратегії, брати участь у турнірах та здобувати цінні призи. 🏆

<b>Наші додаткові функції:</b>
• Збирайте унікальні нагороди та бейджі за ваші успіхи.
• Дізнавайтеся більше про героїв, їхні сильні та слабкі сторони, та знаходьте ідеальні билд-комбінації.
"""

INTRO_PAGE_3_TEXT = """
🚀 <b>Готові розпочати?</b>

Наш бот постійно вдосконалюється, щоб надати вам найкращий досвід гри. 🔧 Слідкуйте за оновленнями та використовуйте всі можливості, які ми пропонуємо:

• Використовуйте передові функції для аналізу ігрового процесу та вдосконалення своїх стратегій.
• Будьте в курсі актуальних оновлень, нових героїв та змін у балансі, щоб завжди бути на крок попереду.
• Отримуйте детальні звіти про ваші матчі, визначайте сильні та слабкі сторони та працюйте над їх удосконаленням.
• Отримуйте рекомендації щодо вибору героїв, білдів та стратегій, що підходять саме вам.
• З'єднуйтесь з іншими гравцями та ентузіастами <b>Mobile Legends</b>, обмінюйтесь досвідом та беріть участь у спільних заходах.
• Встановлюйте особисті цілі, відстежуйте свій прогрес та отримуйте нагороди за досягнення.
• Організовуйте свої ігрові сесії, плануйте участь у турнірах та координуйте команди для максимальної ефективності.
• Отримуйте миттєві повідомлення про важливі події, такі як початок турніру або оновлення гри, щоб завжди бути вчасно поінформованими.

✅ <i>Розпочати</i>
"""

MAIN_MENU_TEXT = """
👋 <b>Вітаємо, {user_first_name}, у Mobile Legends Tournament Bot!</b>
Обери опцію з меню нижче 👇
"""

MAIN_MENU_DESCRIPTION = """
🎮 <b>Цей бот допоможе вам:</b>
• Організовувати турніри
• Зберігати скріншоти персонажів
• Відстежувати активність
• Отримувати досягнення
• Використовувати GPT для порад і тактик
"""

MAIN_MENU_BACK_TO_PROFILE_TEXT = """
🔙 <b>Повернення до меню «Мій Профіль»:</b>
"""

NAVIGATION_MENU_TEXT = """
🧭 <b>Навігація</b>
Оберіть розділ для подальших дій:
"""

NAVIGATION_INTERACTIVE_TEXT = """
🧭 <b>Доступні розділи:</b>

• Персонажі: Оберіть героя, щоб дізнатися про його здібності.
• Гайди: Ознайомтеся з гайдами та стратегіями.
• Білди: Створіть або перегляньте спорядження для героїв.
• Контр-піки: Дізнайтеся, як протистояти героям-суперникам.
• Голосування: Висловлюйте свою думку або пропонуйте ідеї.
• GPT: Використовуйте GPT для генерації даних та порад.

👇 Оберіть кнопку нижче, щоб продовжити.
"""

CHALLENGES_TEXT = """
🚀 <b>Виклики:</b>

Виберіть виклик для отримання нагороди!
"""

STATISTICS_TEXT = """
📊 <b>Статистика</b>

Оберіть підрозділ статистики:
• Загальна Активність
• Рейтинг
• Ігрова Статистика
"""

PROFILE_MENU_TEXT = """
🪪 <b>Мій Профіль</b>

Оберіть опцію для перегляду:
"""

PROFILE_INTERACTIVE_TEXT = """
🌟 <b>Епічний профіль гравця</b>

👤 <b>Ім'я:</b> {username}
🎯 <b>Рівень:</b> {level}
🌟 <b>Рейтинг:</b> {rating}

🏆 <b>Досягнення</b>
• Завдань: {achievements_count}
• Місій: {missions_count}
• Вікторин: {quizzes_count}
• Скріншотів: {screenshots_count}

⚔️ <b>Матчі</b>
• Матчів: {total_matches}
• Виграші: {total_wins}
• Поразки: {total_losses}

🏅 <b>Турніри</b>
• Участь: {tournament_participations}
• Бейджів: {badges_count}
• Останнє оновлення: {last_update}

🤖 Готові підкорювати нові вершини у Mobile Legends?
⚔️ Вибирайте свій шлях і ставайте ще сильнішими! Разом до перемоги!
"""

VIEW_PROFILE_TEXT = """
👁️ <b>Перегляд Профілю</b>

Ваш профіль виглядає наступним чином:
Ім'я: {username}
Рівень: {level}
Рейтинг: {rating}

⚔️ <i>Інші деталі профілю доступні після реєстрації.</i>
"""

EDIT_PROFILE_TEXT = """
✏️ <b>Редагувати Профіль</b>

Ви можете змінити своє ім'я користувача або інші дані.
⚠️ Ця функція ще в розробці.
"""

HEROES_MENU_TEXT = """
🥷 <b>Персонажі</b>

Оберіть категорію героїв:
"""

META_MENU_TEXT = """
📈 <b>META Інформація</b>

Дізнайтеся про найефективніших героїв у поточній META та отримайте рекомендації для покращення своєї гри.
"""

HEROES_INTERACTIVE_TEXT = """
📂 <b>Категорії героїв:</b>

• Танк: Герої з високим рівнем захисту, які поглинають шкоду.
• Маг: Використовують магічні здібності для потужних атак та контролю ворогів.
• Стрілець: Спеціалізуються на дальніх атаках та завданні великої шкоди.
• Асасін: Герої, що спеціалізуються на швидких атаках та високій мобільності, здатні швидко нейтралізувати ворогів.
• Підтримка: Герої, які допомагають команді, забезпечуючи лікування, бафи та інші підтримуючі ефекти.
• Боєць: Збалансовані герої, здатні атакувати та захищатися.
"""

BUST_TEXT = """
🚀 Підвищуйте досвід — обирайте потрібну опцію.
"""

HERO_CLASS_MENU_TEXT = """
🔹 <b>Оберіть героя з класу {hero_class}:</b>
"""

HERO_CLASS_INTERACTIVE_TEXT = """
📜 <b>Герої класу {hero_class}:</b>

{heroes_list}

Натисніть на героя для більш детальної інформації (білди, тактики тощо).
"""

def generate_heroes_list(hero_class, heroes):
    """Функція для генерації списку героїв з їхніми описами."""
    heroes_info = ""
    for hero in heroes:
        heroes_info += f"{hero['name']}: {hero['description']}\n"
    return heroes_info

TOURNAMENTS_MENU_TEXT = """
🏆 <b>Меню Турнірів</b>

• Створення турніру
• Перегляд поточних турнірів
• Історія турнірів
"""

TOURNAMENT_CREATE_TEXT = """
🆕 <b>Створити Турнір</b>

Натисніть, щоб створити новий турнір.
⚠️ Ця функція ще в розробці. Скоро ви зможете створювати власні турніри та запрошувати інших гравців.
"""

TOURNAMENT_VIEW_TEXT = """
👁️ <b>Переглянути Турніри</b>

Перегляньте активні та завершені турніри.
⚠️ Ця функція ще в розробці. Скоро ви зможете переглядати всі турніри та їхні результати.
"""

TRADING_TEXT = """
💱 <b>Торгівля:</b>

Обмінюйтеся предметами з іншими гравцями, щоб оптимізувати своє спорядження.
"""

MY_TEAM_TEXT = """
👥 <b>Моя Команда:</b>

• Назва Команди: {team_name}
• Рівень Команди: {team_level}
• Рейтинг: {team_rating}
• Досягнення: {team_achievements}

Опції:
• Редагувати команду
• Запрошувати учасників
• Перегляд статистики
• Спілкування

🔄 <i>Покращення командного функціоналу в розробці.</i>
"""

VIEW_PROFILE_TEXT = """
👁️ <b>Перегляд Профілю</b>

Ваш профіль виглядає наступним чином:
Ім'я: {username}
Рівень: {level}
Рейтинг: {rating}

⚔️ <i>Інші деталі профілю доступні після реєстрації.</i>
"""

EDIT_PROFILE_TEXT = """
✏️ <b>Редагувати Профіль</b>

Ви можете змінити своє ім'я користувача або інші дані.
⚠️ Ця функція ще в розробці.
"""

HEROES_MENU_TEXT = """
🥷 <b>Персонажі</b>

Оберіть категорію героїв:
"""

META_MENU_TEXT = """
📈 <b>META Інформація</b>

Дізнайтеся про найефективніших героїв у поточній META та отримайте рекомендації для покращення своєї гри.
"""

HEROES_INTERACTIVE_TEXT = """
📂 <b>Категорії героїв:</b>

• Танк: Герої з високим рівнем захисту, які поглинають шкоду.
• Маг: Використовують магічні здібності для потужних атак та контролю ворогів.
• Стрілець: Спеціалізуються на дальніх атаках та завданні великої шкоди.
• Асасін: Герої, що спеціалізуються на швидких атаках та високій мобільності, здатні швидко нейтралізувати ворогів.
• Підтримка: Герої, які допомагають команді, забезпечуючи лікування, бафи та інші підтримуючі ефекти.
• Боєць: Збалансовані герої, здатні атакувати та захищатися.
"""

BUST_TEXT = """
🚀 Підвищуйте досвід — обирайте потрібну опцію.
"""

HERO_CLASS_MENU_TEXT = """
🔹 <b>Оберіть героя з класу {hero_class}:</b>
"""

HERO_CLASS_INTERACTIVE_TEXT = """
📜 <b>Герої класу {hero_class}:</b>

{heroes_list}

Натисніть на героя для більш детальної інформації (білди, тактики тощо).
"""

# ============================[TOURNAMENT MENU]=============================
# Розділ, що містить інформацію про турніри, їх створення та перегляд.

TOURNAMENTS_MENU_TEXT = """
🏆 <b>Меню Турнірів</b>

• Створення турніру
• Перегляд поточних турнірів
• Історія турнірів
"""

ACHIEVEMENTS_TEXT = """
🎖️ <b>Досягнення</b>

Оберіть підрозділ досягнень:
• Мої Бейджі
• Прогрес
• Турнірна Статистика
• Отримані Нагороди
"""

# ============================[ACHIEVEMENTS INTERACTIVE TEXT]=========================
ACHIEVEMENTS_INTERACTIVE_TEXT = """
🎖️ <b>Підрозділи досягнень:</b>

• Мої Бейджі
• Прогрес
• Турнірна Статистика
• Отримані Нагороди

Оберіть підрозділ для перегляду своїх досягнень.
"""

BADGES_TEXT = """
🎖️ <b>Ваші бейджі:</b>

Список ваших бейджів ще не доступний. Поверніться пізніше або досягайте нових цілей!
"""

PROGRESS_TEXT = """
🚀 <b>Ваш прогрес:</b>

Ваш прогрес ще не доступний. Продовжуйте грати та досягати нових вершин!
"""

TOURNAMENT_STATS_TEXT = """
🏅 <b>Турнірна статистика:</b>

Турнірна статистика ще не доступна. Скоро ви зможете переглядати свої результати у змаганнях.
"""

AWARDS_TEXT = """
🎟️ <b>Ваші нагороди:</b>

Список отриманих нагород ще не доступний. Поверніться пізніше або здобувайте нові нагороди!
"""

# ============================[META MENU]=============================
META_MENU_TEXT = """
📈 <b>Меню Метагри</b>

Ознайомтесь з актуальною метагрою та отримуйте рекомендації для покращення своєї гри.
"""

META_HERO_LIST_TEXT = """
🔍 <b>Список Героїв META:</b>

Список героїв, які є найпопулярнішими та найефективнішими у поточній META гри. Дізнайтеся, які герої варто обрати для покращення вашої гри!
"""

META_RECOMMENDATIONS_TEXT = """
🌟 <b>Рекомендації META:</b>

• Топ-герої
• Оптимальні білди
• Найкращі командні стратегії
• Адаптація під патчі
"""

META_UPDATES_TEXT = """
📈 <b>Оновлення META:</b>

• Баланс героїв
• Нові герої
• Оновлені гайди
• Сезонні події
"""

# ============================[GUIDES MENU]===============================
GUIDES_MENU_TEXT = """
📚 <b>Гайди</b>

Оберіть опцію для доступу до гайдів:
• Нові Гайди
• Популярні Гайди
• Гайди для Початківців
• Просунуті Техніки
• Гайди по Командній Грі
"""

M6_TEXT = """
ℹ️ <b>Інформація про M6:</b>

M6 — головний світовий турнір з Mobile Legends.
• Команди з різних куточків світу
• Величезні призи
• Прямі трансляції
• Неймовірні баталії
"""

GUIDES_INTERACTIVE_TEXT = """
📖 <b>Підрозділи гайдів:</b>

• Нові Гайди
• Популярні Гайди
• Гайди для Початківців
• Просунуті Техніки
• Гайди по Командній Грі

Оберіть категорію, щоб переглянути доступні гайди.
"""

NEW_GUIDES_TEXT = """
🆕 <b>Нові Гайди</b>

Список нових гайдів скоро буде доступний. Залишайтесь на зв'язку!
"""

POPULAR_GUIDES_TEXT = """
🌟 <b>Популярні Гайди</b>

Список популярних гайдів скоро буде доступний. Слідкуйте за оновленнями!
"""

BEGINNER_GUIDES_TEXT = """
🎓 <b>Гайди для Початківців</b>

Список гайдів для початківців скоро буде доступний. Допоможемо вам швидко освоїтися!
"""

ADVANCED_TECHNIQUES_TEXT = """
🚀 <b>Просунуті Техніки</b>

Список просунутих технік скоро буде доступний. Покращуйте свої навички разом з нами!
"""

TEAMPLAY_GUIDES_TEXT = """
🤝 <b>Гайди по Командній Грі</b>

Список гайдів по командній грі скоро буде доступний. Навчіться грати ефективно разом з командою!
"""

GUIDES_TEXT = """
📂 <b>Оберіть гайди, які вас цікавлять.</b>
"""

# ============================[COUNTER PICKS]=============================
COUNTER_PICKS_MENU_TEXT = """
⚖️ <b>Контр-піки</b>

Оберіть опцію контр-піків:
• Переглянути контр-піки для героя
• Створити власний контр-пік
• Переглянути популярні контр-піки
"""

COUNTER_PICKS_INTERACTIVE_TEXT = """
🕵️‍♂️ <b>Контр-піки:</b>

• Переглянути контр-піки для конкретного героя
• Створити власний контр-пік
• Переглянути популярні контр-піки

Оберіть опцію для продовження.
"""

COUNTER_SEARCH_TEXT = """
🔎 Будь ласка, введіть ім'я персонажа для пошуку контр-піка:
"""

COUNTER_LIST_TEXT = """
📃 <b>Список контр-піків:</b>

Список контр-піків для обраного героя скоро буде доступний. Поверніться пізніше або оберіть іншого героя.
"""

# ============================[TEAMS MENU]===============================
TEAMS_TEXT = """
🧑‍🤝‍🧑 <b>Команди</b>

• Створити команду
• Мої команди
• Знайти команду
"""

# ============================[BUILDS MENU]===============================
BUILDS_MENU_TEXT = """
🛠️ <b>Білди</b>

Оберіть опцію білдів:
• Створити білд
• Мої білди
• Популярні білди
"""

BUILDS_INTERACTIVE_TEXT = """
🔧 <b>Опції білдів:</b>

• Створити білд
• Мої білди
• Популярні білди

Оберіть опцію для продовження.
"""

CREATE_BUILD_TEXT = """
🏗️ <b>Створення білду:</b>

Функція створення білду ще в розробці. Скоро ви зможете налаштовувати оптимальні комплекти спорядження для своїх героїв.
"""

MY_BUILDS_TEXT = """
📄 <b>Мої білди:</b>

Список ваших білдів ще не доступний. Поверніться пізніше або створіть новий білд.
"""

POPULAR_BUILDS_TEXT = """
🔥 <b>Популярні білди:</b>

Список популярних білдів ще не доступний. Слідкуйте за оновленнями!
"""

# ============================[VOTING MENU]===============================
VOTING_MENU_TEXT = """
🗳️ <b>Голосування</b>

Оберіть опцію голосування:
• Поточні Опитування
• Мої Голосування
• Запропонувати Тему
"""

VOTING_INTERACTIVE_TEXT = """
🗳️ <b>Опції голосування:</b>

• Поточні Опитування
• Мої Голосування
• Запропонувати Тему

Оберіть опцію для продовження.
"""

CURRENT_VOTES_TEXT = """
📍 <b>Поточні голосування:</b>

Список поточних опитувань скоро буде доступний. Беріть участь у вирішенні важливих питань!
"""

MY_VOTES_TEXT = """
📋 <b>Мої голосування:</b>

Список ваших голосувань ще не доступний. Поверніться пізніше або долучайтесь до поточних опитувань.
"""

SUGGEST_TOPIC_TEXT = """
➕ <b>Запропонувати Тему</b>:

Будь ласка, введіть тему для пропозиції нового голосування:
"""

SUGGESTION_RESPONSE_TEXT = """
✅ <b>Ви запропонували тему:</b> "<i>{topic}</i>"

⚠️ Ця функція ще в розробці. Ми розглянемо вашу пропозицію та додамо її найближчим часом.
"""

# ============================[STATISTICS MENU]===========================
STATISTICS_MENU_TEXT = """
📊 <b>Статистика</b>

Оберіть підрозділ статистики:
• Загальна Активність
• Рейтинг
• Ігрова Статистика
"""

STATISTICS_INTERACTIVE_TEXT = """
📈 <b>Підрозділи статистики:</b>

• Загальна Активність
• Рейтинг
• Ігрова Статистика

Оберіть підрозділ для перегляду детальної статистики.
"""

ACTIVITY_TEXT = """
📊 <b>Загальна активність:</b>

Статистика загальної активності ще не доступна. Поверніться пізніше або перегляньте інші підрозділи.
"""

RANKING_TEXT = """
🥇 <b>Рейтинг:</b>

Ваш рейтинг ще не доступний. Слідкуйте за оновленнями, щоб дізнатися свій поточний рейтинг у грі.
"""

GAME_STATS_TEXT = """
🎮 <b>Ігрова статистика:</b>

Ігрова статистика ще не доступна. Скоро ви зможете переглядати детальний аналіз своїх ігрових показників у боях.
"""

# ============================[SETTINGS MENU]=============================
SETTINGS_MENU_TEXT = """
⚙️ <b>Налаштування</b>

Оберіть опцію налаштувань:
• Мова Інтерфейсу
• Змінити Username
• Оновити ID
• Сповіщення
"""

SETTINGS_INTERACTIVE_TEXT = """
🔧 <b>Опції налаштувань:</b>

• Мова Інтерфейсу
• Змінити Username
• Оновити ID
• Сповіщення

Оберіть опцію для налаштування своїх параметрів.
"""

LANGUAGE_SELECTION_TEXT = """
🌐 <b>Вибір мови:</b>

Оберіть мову інтерфейсу бота:
• 🇺🇦 Українська
• 🇬🇧 Англійська

Виберіть мову, щоб продовжити.
"""

LANGUAGE_CHANGED_TEXT = """
✅ Мову успішно змінено!

Обрана мова: {language}
"""

LANGUAGE_ERROR_TEXT = """
❌ Помилка при зміні мови

Спробуйте ще раз або зверніться до підтримки.
"""

CHANGE_USERNAME_TEXT = """
✏️ <b>Зміна Username:</b>

Будь ласка, введіть новий <b>Username</b>:
"""

CHANGE_USERNAME_RESPONSE_TEXT = """
✅ <b>Username оновлено:</b> <i>{new_username}</i>

Ця функція ще в розробці. Дякуємо за ваше терпіння!
"""

UPDATE_ID_TEXT = """
🆔 <b>Оновлення ID:</b>

Функція оновлення ID ще в розробці. Ми працюємо над її впровадженням для вашої зручності.
"""

UPDATE_ID_SUCCESS_TEXT = """
🆔 <b>ID оновлено:</b>

Ваш ігровий ID було успішно оновлено. Тепер ваш профіль відображатиме найновішу інформацію.
"""

NOTIFICATIONS_TEXT = """
🔔 <b>Сповіщення:</b>

• Часові
• Турнірні
• Оновлення бота
"""

NOTIFICATIONS_SETTINGS_TEXT = """
🔔 <b>Налаштування сповіщень:</b>

Функція налаштування сповіщень ще в розробці. Скоро ви зможете обирати, які сповіщення отримувати.
"""

# ============================[FEEDBACK MENU]=============================
FEEDBACK_MENU_TEXT = """
💌 <b>Зворотний Зв'язок</b>

Оберіть опцію зворотного зв'язку:
• Надіслати відгук
• Повідомити про помилку
"""

FEEDBACK_INTERACTIVE_TEXT = """
✏️ <b>Опції зворотного зв'язку:</b>

• Надіслати відгук
• Повідомити про помилку

Оберіть опцію для надання зворотного зв'язку.
"""

SEND_FEEDBACK_TEXT = """
💬 <b>Надіслати Відгук:</b>

Ми цінуємо вашу думку! Надішліть нам ваш відгук або пропозиції, щоб ми могли покращити наш бот.
"""

SEND_FEEDBACK_INPUT_TEXT = """
📝 Будь ласка, введіть ваш відгук:
{user_feedback}
"""

REPORT_BUG_TEXT = """
🐛 Будь ласка, опишіть помилку, яку ви знайшли:
{bug_description}
"""

FEEDBACK_RECEIVED_TEXT = """
✅ <b>Відгук отримано!</b>

Ми розглянемо ваші пропозиції та докладемо зусиль, щоб покращити наш сервіс. Дякуємо за вашу участь!
"""

BUG_REPORT_RECEIVED_TEXT = """
✅ <b>Звіт про помилку надіслано!</b>

Дякуємо! Ми працюємо над усуненням недоліків.
"""

# ============================[HELP MENU]=============================
HELP_MENU_TEXT = """
❓ <b>Допомога</b>

Оберіть опцію допомоги:
• Інструкції
• FAQ
• Підтримка
"""

HELP_INTERACTIVE_TEXT = """
📄 <b>Опції допомоги:</b>

• Інструкції
• FAQ
• Підтримка

Оберіть опцію для отримання допомоги.
"""

INSTRUCTIONS_TEXT = """
📄 <b>Інструкції:</b>

Інструкції ще не доступні. Поверніться пізніше, щоб дізнатися більше про використання бота.
"""

FAQ_TEXT = """
❔ <b>Часті питання (FAQ):</b>

FAQ ще не доступне. Скоро ми додамо відповіді на найпоширеніші питання користувачів.
"""

HELP_SUPPORT_TEXT = """
📞 <b>Підтримка:</b>

Якщо у вас виникли питання або потрібна допомога, зверніться до нашої технічної підтримки через офіційний канал або напишіть на електронну пошту:
<a href="mailto:support@mobilelegendsbot.com">support@mobilelegendsbot.com</a>
"""

# ============================[GPT Functionality]===========================
# Константи, що дозволяють відображати додаткову інформацію чи тексти, пов’язані з GPT.

GPT_MENU_TEXT = """
🤖 <b>GPT:</b>

Ставте запитання, просіть поради чи стратегії — і GPT допоможе вам швидше розвиватися в Mobile Legends!
"""

GPT_DATA_GENERATION_TEXT = """
🤖 <b>Генерація Даних GPT:</b>

Використовуйте GPT для створення унікальних даних, аналізу ігрових показників та отримання аналітичних звітів.
"""

GPT_HINTS_TEXT = """
💡 <b>Поради GPT:</b>

Отримуйте корисні поради та рекомендації від GPT, щоб покращити свої ігрові навички та стратегії.
"""

GPT_HERO_STATS_TEXT = """
📈 <b>Статистика Героя GPT:</b>

Отримуйте детальний аналіз статистики обраного героя, включаючи показники виграшів, поразок та ефективності.
"""

# ============================[OTHER CONSTANTS]=============================
# Інші константи та відповіді на базові дії користувачів.

SEARCH_HERO_RESPONSE_TEXT = """
🔎 <b>Результати пошуку для обраного героя:</b>

Ось інформація, яку ми знайшли для вашого героя.
"""

CHANGE_USERNAME_RESPONSE_TEXT = """
✅ Ваше ім'я користувача успішно змінено.

Ця функція ще в розробці. Дякуємо за ваше терпіння!
"""

MLS_BUTTON_RESPONSE_TEXT = """
ℹ️ Деталі MLS доступні за цим посиланням:
<a href="https://mls.mobilelegends.com">Перейти до MLS</a>
"""

UNHANDLED_INLINE_BUTTON_TEXT = """
⚠️ Ця кнопка наразі недоступна.

🔘 <i>Виберіть інший пункт з меню.</i>
"""

MAIN_MENU_BACK_TO_PROFILE_TEXT = """
🔙 <b>Повернутися до профілю</b>

Оберіть опцію нижче, щоб повернутися до свого профілю.
"""

TOURNAMENT_CREATE_TEXT = """
🆕 <b>Створити Турнір</b>

Натисніть, щоб створити новий турнір.
⚠️ Ця функція ще в розробці. Скоро ви зможете створювати власні турніри та запрошувати інших гравців.
"""

TOURNAMENT_VIEW_TEXT = """
👁️ <b>Переглянути Турніри</b>

Перегляньте активні та завершені турніри.
⚠️ Ця функція ще в розробці. Скоро ви зможете переглядати всі турніри та їхні результати.
"""

META_HERO_LIST_TEXT = """
🔍 <b>Список Героїв META:</b>

Список героїв, які є найпопулярнішими та найефективнішими у поточній META гри. Дізнайтеся, які герої варто обрати для покращення вашої гри!
"""

META_RECOMMENDATIONS_TEXT = """
🌟 <b>Рекомендації META:</b>

• Топ-герої
• Оптимальні білди
• Найкращі командні стратегії
• Адаптація під патчі
"""

META_UPDATES_TEXT = """
📈 <b>Оновлення META:</b>

• Баланс героїв
• Нові герої
• Оновлені гайди
• Сезонні події
"""

# ============================[END OF TEXTS.PY]=============================
# Кінець файлу. Бажаємо вдалої розробки і приємного користування!