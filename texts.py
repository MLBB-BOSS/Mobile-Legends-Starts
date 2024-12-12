# texts.py

# Привітальні повідомлення
class WelcomeMessages:
    WELCOME_NEW_USER = """🔥 <b>Ласкаво просимо до Mobile Legends: Starts</b> – твого нового епічного союзника у світі <b>Mobile Legends: Bang Bang!</b> 🔥

🎮 Готовий до неймовірних пригод? Приєднуйся до нас та розкрий всі можливості для покращення своєї гри.

🎮 <b>Розпочнемо цю пригоду разом!</b> 🕹️

<b>Зроблено з любов'ю для справжніх фанатів Mobile Legends. 💖</b>"""

# Сторінки введення
class IntroPages:
    INTRO_PAGE_1 = """🌟 Ласкаво просимо до Mobile Legends Starts! 🌟

Твій незамінний помічник у світі Mobile Legends – де стратегія зустрічається з епічними битвами!

---

✨ <b>Що вас чекає?</b>

• 🗺️ <b>Завдання:</b> Виконуй місії, заробляй бали, підвищуй рівень!
• 📘 <b>Гайди:</b> Доступ до унікальних порад і стратегій.
• 📊 <b>Статистика:</b> Аналізуй свій прогрес і досягнення.
• ⚙️ <b>Білди:</b> Створюй оптимальні спорядження для героїв.
• 🤝 <b>Команди:</b> Шукай союзників для гри.
• 🏆 <b>Турніри:</b> Організовуй або долучайся до змагань.
• 🎖️ <b>Досягнення:</b> Відстежуй успіхи, отримуй нагороди.
• 🥷 <b>Персонажі:</b> Обирай героїв, порівнюй їх здібності та досягай перемог!

---

🚀 <b>Розпочни свою подорож вже зараз!</b>

Натисни кнопку «Далі» і поринь у світ безмежних можливостей Mobile Legends Starts.

Пам'ятай, твій успіх – це наша місія!

---

<b>Зроблено з любов'ю для гравців Mobile Legends. 💖</b>"""

    INTRO_PAGE_2 = """💡 <b>Функції Mobile Legends: Starts:</b>

• 🧭 <b>Навігація:</b> Інтуїтивно зрозумілий інтерфейс, що дозволяє швидко знаходити потрібні функції.

• 🪪 <b>Мій профіль:</b> Переглядай та редагуй свої особисті дані, налаштовуй профіль для кращої взаємодії.

• 🥷 <b>Персонажі:</b> Дізнавайся більше про кожного героя, їхні здібності та оптимальні стратегії гри.

• 📚 <b>Гайди:</b> Отримуй детальні поради, покрокові інструкції та стратегії для покращення своєї гри.

• 📊 <b>Статистика:</b> Відстежуй свій прогрес, аналізуй ігрові показники та працюй над слабкими місцями.

• 🛡️ <b>Білди:</b> Створюй оптимальні комплекти спорядження для кожного героя або обирай з готових наборів.

• 🏆 <b>Турніри:</b> Бери участь у змаганнях, організовуй власні турніри та вигравай цінні призи.

Натисни кнопку <b>«Далі»</b>, щоб продовжити ознайомлення.
"""

    INTRO_PAGE_3 = """🪪 <b>Ваш Профіль:</b>

• 🏅 <b>Ім'я користувача:</b> {username}
• 🧬 <b>Рівень:</b> {level}
• 📈 <b>Рейтинг:</b> {rating}
• 🎯 <b>Досягнення:</b> {achievements_count} досягнень

🧭 <b>Навігація:</b> Використовуйте меню нижче, щоб отримати доступ до всіх функцій MLS та налаштувати свій ігровий досвід.

🚀 <b>Розпочни свою подорож вже зараз!</b>

Натисни кнопку <b>«Розпочати»</b>, щоб перейти до основного меню та скористатися всіма можливостями MLS.

<b>Залишайся з нами, і разом досягнемо нових висот у Mobile Legends!</b>
"""

# Головне меню
class MainMenu:
    TEXT = """👋 Вітаємо, {user_first_name}, у Mobile Legends Tournament Bot!

Обери опцію з меню нижче 👇
"""
    DESCRIPTION = """🎮 Цей бот допоможе вам:
• Організовувати турніри
• Зберігати скріншоти персонажів
• Відстежувати активність
• Отримувати досягнення
"""
    ERROR = "❗ Щось пішло не так. Почнімо спочатку."
    BACK_TO_PROFILE = "🔙 Повернення до меню <b>«Мій Профіль»</b>:"

# Меню навігації
class NavigationMenu:
    TEXT = """🧭 Навігація
Оберіть розділ для подальших дій:
"""
    INTERACTIVE_TEXT = """🧭 <b>Доступні розділи:</b>

• 🥷 <b>Персонажі:</b> Обери героя, щоб дізнатися про його здібності.
• 📚 <b>Гайди:</b> Ознайомся з гайдами та стратегіями.
• 🛡️ <b>Білди:</b> Створи чи переглянь спорядження для героїв.
• ⚖️ <b>Контр-піки:</b> Дізнайся, як протистояти героям-суперникам.
• 📊 <b>Голосування:</b> Висловлюй свою думку або пропонуй ідеї.

👇 Оберіть кнопку нижче, щоб продовжити.
"""

# Меню профілю
class ProfileMenu:
    TEXT = """🪪 Мій Профіль
Оберіть опцію для перегляду:
"""
    INTERACTIVE_TEXT = """🔍 <b>Ваш Профіль:</b>

• 🏅 <b>Ім'я користувача:</b> {username}
• 🧬 <b>Рівень:</b> {level}
• 📈 <b>Рейтинг:</b> {rating}
• 🎯 <b>Досягнення:</b> {achievements_count} досягнень

Оберіть опцію, щоб редагувати свій профіль чи переглянути статистику.
"""
    BACK_TO_MAIN_MENU = "🔙 Повернення до головного меню:"

# Меню персонажів
class HeroesMenu:
    TEXT = """🥷 Персонажі

Оберіть категорію героїв:
"""
    INTERACTIVE_TEXT = """📂 <b>Категорії героїв:</b>

• 🛡️ <b>Танк:</b> Герої з високим рівнем захисту, які поглинають шкоду.
• 🧙‍♂️ <b>Маг:</b> Використовують магічні здібності для потужних атак та контролю ворогів.
• 🏹 <b>Стрілець:</b> Спеціалізуються на дальніх атаках та завданні великої шкоди.
• ⚔️ <b>Асасін:</b> Герої, що спеціалізуються на швидких атаках та високій мобільності, здатні швидко нейтралізувати ворогів.
• ❤️ <b>Підтримка:</b> Герої, які допомагають команді, забезпечуючи лікування, бафи та інші підтримуючі ефекти.
• 🗡️ <b>Боєць:</b> Збалансовані герої, здатні атакувати та захищатися.

Оберіть категорію, щоб переглянути список героїв.
"""

# Меню класу героїв
class HeroClassMenu:
    TEXT = """Виберіть героя з класу <b>{hero_class}</b>:"""
    INTERACTIVE_TEXT = """📜 <b>Герої класу {hero_class}:</b>

{heroes_list}
"""

# Меню гайдів
class GuidesMenu:
    TEXT = """📚 Гайди

Оберіть підрозділ гайдів:
"""
    INTERACTIVE_TEXT = """📖 <b>Підрозділи гайдів:</b>

• 🆕 <b>Нові Гайди:</b> Найсвіжіші матеріали та оновлення.
• 🌟 <b>Популярні Гайди:</b> Найпопулярніші та найбільш корисні гайди серед гравців.
• 📘 <b>Для Початківців:</b> Основи гри та перші кроки для новачків.
• 🧙 <b>Стратегії гри:</b> Складні стратегії та тактики для досвідчених гравців.
• 🤝 <b>Командна Гра:</b> Гайди, що фокусуються на ефективній взаємодії в команді.

Оберіть підрозділ, щоб переглянути доступні гайди.
"""
    NEW_GUIDES = """📄 <b>Нові гайди:</b>

Список нових гайдів скоро буде доступний. Залишайтесь на зв'язку!
"""
    POPULAR_GUIDES = """🌟 <b>Популярні гайди:</b>

Список популярних гайдів скоро буде доступний. Слідкуйте за оновленнями!
"""
    BEGINNER_GUIDES = """📘 <b>Гайди для Початківців:</b>

Список гайдів для початківців скоро буде доступний. Допоможемо вам швидко освоїтися!
"""
    ADVANCED_TECHNIQUES = """🧙 <b>Стратегії гри:</b>

Список просунутих технік скоро буде доступний. Покращуйте свої навички разом з нами!
"""
    TEAMPLAY_GUIDES = """🤝 <b>Командна Гра:</b>

Список гайдів по командній грі скоро буде доступний. Навчіться грати ефективно разом з командою!
"""

# Меню контр-піків
class CounterPicksMenu:
    TEXT = """⚖️ Контр-піки

Оберіть опцію контр-піків:
"""
    INTERACTIVE_TEXT = """🕵️‍♂️ <b>Контр-піки:</b>

• 🔎 <b>Переглянути контр-піки для конкретного героя</b>
• 📝 <b>Створити власний контр-пік</b>
• 🔥 <b>Переглянути популярні контр-піки</b>

Оберіть опцію для продовження.
"""
    SEARCH_PROMPT = "🔎 Будь ласка, введіть ім'я персонажа для пошуку контр-піку:"
    LIST_TEXT = """📃 <b>Список контр-піків:</b>

Список контр-піків для обраного героя скоро буде доступний. Поверніться пізніше або оберіть іншого героя.
"""

# Меню білдів
class BuildsMenu:
    TEXT = """🛠️ Білди

Оберіть опцію білдів:
"""
    INTERACTIVE_TEXT = """🔧 <b>Опції білдів:</b>

• 🏗️ <b>Створити новий білд:</b> Налаштуйте власний набір спорядження для вашого героя.
• 📄 <b>Мої білди:</b> Перегляньте та керуйте своїми збереженими білдами.
• 🔥 <b>Популярні білди:</b> Ознайомтеся з найпопулярнішими білдами серед гравців.

Оберіть опцію для продовження.
"""
    CREATE_BUILD = """🏗️ <b>Створення білду:</b>

Функція створення білду ще в розробці. Скоро ви зможете налаштовувати оптимальні комплекти спорядження для своїх героїв.
"""
    MY_BUILDS = """📄 <b>Мої білди:</b>

Список ваших білдів ще не доступний. Поверніться пізніше або створіть новий білд.
"""
    POPULAR_BUILDS = """🔥 <b>Популярні білди:</b>

Список популярних білдів ще не доступний. Слідкуйте за оновленнями!
"""

# Меню голосування
class VotingMenu:
    TEXT = """🗳️ Голосування

Оберіть опцію голосування:
"""
    INTERACTIVE_TEXT = """🗳️ <b>Опції голосування:</b>

• 📍 <b>Поточні Опитування:</b> Долучайтеся до активних опитувань.
• 📋 <b>Мої Голосування:</b> Перегляньте свої попередні участі.
• ➕ <b>Запропонувати Тему:</b> Внесіть свої ідеї для майбутніх голосувань.

Оберіть опцію для продовження.
"""
    CURRENT_VOTES = """📍 <b>Поточні голосування:</b>

Список поточних опитувань скоро буде доступний. Беріть участь у вирішенні важливих питань!
"""
    MY_VOTES = """📋 <b>Мої голосування:</b>

Список ваших голосувань ще не доступний. Поверніться пізніше або долучайтесь до поточних опитувань.
"""
    SUGGEST_TOPIC_PROMPT = "➕ Будь ласка, введіть тему для пропозиції нового голосування:"
    SUGGESTION_RESPONSE = """✅ Ви запропонували тему: "<i>{topic}</i>".

Ця функція ще в розробці. Ми розглянемо вашу пропозицію та додамо її найближчим часом.
"""

# Меню статистики
class StatisticsMenu:
    TEXT = """📊 Статистика

Оберіть підрозділ статистики:
"""
    INTERACTIVE_TEXT = """📈 <b>Підрозділи статистики:</b>

• 📊 <b>Загальна Активність:</b> Перегляньте свою та командну активність у грі.
• 🥇 <b>Рейтинг:</b> Відстежуйте свій рейтинг та порівнюйте з іншими гравцями.
• 🎮 <b>Ігрова Статистика:</b> Детальний аналіз ваших ігрових показників.

Оберіть підрозділ для перегляду детальної статистики.
"""
    ACTIVITY = """📊 <b>Загальна активність:</b>

Статистика загальної активності ще не доступна. Поверніться пізніше або перегляньте інші підрозділи.
"""
    RANKING = """🥇 <b>Рейтинг:</b>

Ваш рейтинг ще не доступний. Слідкуйте за оновленнями, щоб дізнатися свій поточний рейтинг у грі.
"""
    GAME_STATS = """🎮 <b>Ігрова статистика:</b>

Ігрова статистика ще не доступна. Скоро ви зможете переглядати детальний аналіз своїх ігрових показників.
"""

# Меню досягнень
class AchievementsMenu:
    TEXT = """🎖️ Досягнення

Оберіть підрозділ досягнень:
"""
    INTERACTIVE_TEXT = """🎖️ <b>Підрозділи досягнень:</b>

• 🎖️ <b>Мої Бейджі:</b> Перегляньте свої набрані бейджі за різні досягнення.
• 🚀 <b>Прогрес:</b> Відстежуйте свій прогрес у грі та досягнення мети.
• 🏅 <b>Турнірна Статистика:</b> Перегляньте свої результати в турнірах.
• 🎟️ <b>Отримані Нагороди:</b> Ознайомтеся з отриманими нагородами за видатні досягнення.

Оберіть підрозділ для перегляду своїх досягнень.
"""
    BADGES = """🎖️ <b>Ваші бейджі:</b>

Список ваших бейджів ще не доступний. Поверніться пізніше або досягайте нових цілей!
"""
    PROGRESS = """🚀 <b>Ваш прогрес:</b>

Ваш прогрес ще не доступний. Продовжуйте грати та досягати нових вершин!
"""
    TOURNAMENT_STATS = """🏅 <b>Турнірна статистика:</b>

Турнірна статистика ще не доступна. Скоро ви зможете переглядати свої результати у змаганнях.
"""
    AWARDS = """🎟️ <b>Ваші нагороди:</b>

Список отриманих нагород ще не доступний. Поверніться пізніше або здобувайте нові нагороди!
"""

# Меню налаштувань
class SettingsMenu:
    TEXT = """⚙️ Налаштування

Оберіть опцію налаштувань:
"""
    INTERACTIVE_TEXT = """🔧 <b>Опції налаштувань:</b>

• 🌐 <b>Мова Інтерфейсу:</b> Оберіть мову інтерфейсу бота.
• ℹ️ <b>Змінити Username:</b> Оновіть своє ім'я користувача.
• 🆔 <b>Оновити ID:</b> Оновіть свій ігровий ID для коректної статистики.
• 🔔 <b>Сповіщення:</b> Налаштуйте отримання сповіщень від бота.

Оберіть опцію для налаштування своїх параметрів.
"""
    LANGUAGE_CHANGE = """🌐 <b>Зміна мови:</b>

Функція зміни мови ще в розробці. Скоро ви зможете обирати з декількох мов інтерфейсу.
"""
    CHANGE_USERNAME_PROMPT = "ℹ️ Будь ласка, введіть новий <b>Username</b>:"
    UPDATE_ID_TEXT = """🆔 <b>Оновлення ID:</b>

Функція оновлення ID ще в розробці. Ми працюємо над її впровадженням для твоєї зручності.
"""
    NOTIFICATIONS_SETTINGS = """🔔 <b>Налаштування сповіщень:</b>

Функція налаштування сповіщень ще в розробці. Скоро ви зможете обирати, які сповіщення отримувати.
"""

# Меню зворотного зв'язку
class FeedbackMenu:
    TEXT = """💌 Зворотний Зв'язок

Оберіть опцію зворотного зв'язку:
"""
    INTERACTIVE_TEXT = """✏️ <b>Опції зворотного зв'язку:</b>

• 📝 <b>Надіслати відгук:</b> Поділіться своїми враженнями та пропозиціями.
• 🐛 <b>Повідомити про помилку:</b> Сповістіть нас про будь-які виявлені помилки чи несправності.

Оберіть опцію для надання зворотного зв'язку.
"""
    SEND_FEEDBACK_PROMPT = "📝 Будь ласка, введіть ваш відгук:"
    REPORT_BUG_PROMPT = "🐛 Будь ласка, опишіть помилку, яку ви знайшли:"
    FEEDBACK_RECEIVED = "✅ Дякуємо за ваш відгук! Ми його розглянемо."
    BUG_REPORT_RECEIVED = "✅ Дякуємо за ваш звіт! Ми виправимо помилку якнайшвидше."

# Меню допомоги
class HelpMenu:
    TEXT = """❓ Допомога

Оберіть опцію допомоги:
"""
    INTERACTIVE_TEXT = """📄 <b>Опції допомоги:</b>

• 📄 <b>Інструкції:</b> Дізнайся, як користуватися різними функціями бота.
• ❔ <b>FAQ:</b> Відповіді на найпоширеніші питання.
• 📞 <b>Підтримка:</b> Зв'яжись з нашою технічною підтримкою для додаткової допомоги.

Оберіть опцію для отримання допомоги.
"""
    INSTRUCTIONS = """📄 <b>Інструкції:</b>

Інструкції ще не доступні. Поверніться пізніше, щоб дізнатися більше про використання бота.
"""
    FAQ = """❔ <b>Часті питання (FAQ):</b>

FAQ ще не доступне. Скоро ми додамо відповіді на найпоширеніші питання користувачів.
"""
    SUPPORT_CONTACT = """📞 <b>Підтримка:</b>

Якщо у вас виникли питання або потрібна допомога, зверніться до нашої технічної підтримки через офіційний канал або напишіть на електронну пошту: <a href="mailto:support@mobilelegendsbot.com">support@mobilelegendsbot.com</a>
"""

# Повідомлення про невідому команду та помилки
class ErrorMessages:
    UNKNOWN_COMMAND = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
    GENERIC_ERROR = "⚠️ Сталася помилка. Будь ласка, спробуйте ще раз."
    ERROR_MESSAGE = "⚠️ Сталася помилка. Спробуйте пізніше або зверніться до підтримки для отримання допомоги."
    USE_BUTTON_NAVIGATION = "🔘 Будь ласка, використовуйте кнопки нижче для навігації."

# Додаткові відповіді
class AdditionalResponses:
    SEARCH_HERO_RESPONSE = """🔎 Ви шукаєте героя: <i>{hero_name}</i>.

Ця функція ще в розробці. Скоро ви зможете отримувати детальну інформацію про будь-якого героя.
"""
    CHANGE_USERNAME_RESPONSE = """ℹ️ Ваш новий Username: <b>{new_username}</b> буде доданий після перевірки.

Ця функція ще в розробці. Дякуємо за ваше терпіння!
"""

# Відповіді на натискання інлайн кнопок
class InlineButtonResponses:
    MLS_BUTTON_RESPONSE = "🔹 Ви натиснули кнопку MLS. Функція обробки цієї кнопки ще не реалізована."
    UNHANDLED_INLINE_BUTTON = "⚠️ Ця кнопка поки що не оброблена. Будь ласка, скористайтеся іншими опціями меню."

# Текст для турнірів
class TournamentTexts:
    CREATE_TOURNAMENT = """🏗️ <b>Створення Турніру:</b>
    
Введіть інформацію про турнір:
• Назва турніру
• Опис
• Дата та час
• Формат змагань

⚠️ Ця функція ще в розробці. Скоро ви зможете створювати власні турніри та запрошувати інших гравців.
"""
    VIEW_TOURNAMENTS = """📄 <b>Перегляд Турнірів:</b>
    
Список поточних та минулих турнірів скоро буде доступний. Приєднуйтесь до змагань та вигравайте призи!
"""

# Текст для META
class MetaTexts:
    HERO_LIST = """🔍 <b>Список Героїв META:</b>
    
Список героїв, які є найпопулярнішими та найефективнішими у поточній META гри. Дізнайтеся, які герої варто обрати для покращення вашої гри!
"""
    RECOMMENDATIONS = """🌟 <b>Рекомендації META:</b>
    
Отримайте поради щодо вибору героїв, спорядження та стратегій, які допоможуть вам бути кращими в поточній META.
"""
    UPDATES = """📈 <b>Оновлення META:</b>
    
Будьте в курсі останніх змін у грі, включаючи оновлення героїв, балансування та нові стратегії.
"""

# Текст для M6
class M6Texts:
    INFO = """ℹ️ <b>Інформація про M6:</b>
    
Дізнайтеся більше про функції та можливості M6, нашого нового інструменту для аналізу та покращення вашої гри.
"""
    STATS = """📊 <b>Статистика M6:</b>
    
Перегляньте детальну статистику вашої гри, включаючи показники ефективності, вибір героїв та інші важливі дані.
"""
    NEWS = """📰 <b>Новини M6:</b>
    
Отримуйте найсвіжіші новини та оновлення щодо M6, включаючи нові функції, покращення та інші важливі повідомлення.
"""

# Топ-рівневі змінні для сумісності
WELCOME_NEW_USER_TEXT = WelcomeMessages.WELCOME_NEW_USER

INTRO_PAGE_1_TEXT = IntroPages.INTRO_PAGE_1
INTRO_PAGE_2_TEXT = IntroPages.INTRO_PAGE_2
INTRO_PAGE_3_TEXT = IntroPages.INTRO_PAGE_3

MAIN_MENU_TEXT = MainMenu.TEXT
MAIN_MENU_DESCRIPTION = MainMenu.DESCRIPTION
MAIN_MENU_ERROR_TEXT = MainMenu.ERROR
MAIN_MENU_BACK_TO_PROFILE_TEXT = MainMenu.BACK_TO_PROFILE

NAVIGATION_MENU_TEXT = NavigationMenu.TEXT
NAVIGATION_INTERACTIVE_TEXT = NavigationMenu.INTERACTIVE_TEXT

PROFILE_MENU_TEXT = ProfileMenu.TEXT
PROFILE_INTERACTIVE_TEXT = ProfileMenu.INTERACTIVE_TEXT
BACK_TO_MAIN_MENU_TEXT = ProfileMenu.BACK_TO_MAIN_MENU

HEROES_MENU_TEXT = HeroesMenu.TEXT
HEROES_INTERACTIVE_TEXT = HeroesMenu.INTERACTIVE_TEXT

HERO_CLASS_MENU_TEXT = HeroClassMenu.TEXT
HERO_CLASS_INTERACTIVE_TEXT = HeroClassMenu.INTERACTIVE_TEXT

GUIDES_MENU_TEXT = GuidesMenu.TEXT
GUIDES_INTERACTIVE_TEXT = GuidesMenu.INTERACTIVE_TEXT
NEW_GUIDES_TEXT = GuidesMenu.NEW_GUIDES
POPULAR_GUIDES_TEXT = GuidesMenu.POPULAR_GUIDES
BEGINNER_GUIDES_TEXT = GuidesMenu.BEGINNER_GUIDES
ADVANCED_TECHNIQUES_TEXT = GuidesMenu.ADVANCED_TECHNIQUES
TEAMPLAY_GUIDES_TEXT = GuidesMenu.TEAMPLAY_GUIDES

COUNTER_PICKS_MENU_TEXT = CounterPicksMenu.TEXT
COUNTER_PICKS_INTERACTIVE_TEXT = CounterPicksMenu.INTERACTIVE_TEXT
COUNTER_SEARCH_TEXT = CounterPicksMenu.SEARCH_PROMPT
COUNTER_LIST_TEXT = CounterPicksMenu.LIST_TEXT

BUILDS_MENU_TEXT = BuildsMenu.TEXT
BUILDS_INTERACTIVE_TEXT = BuildsMenu.INTERACTIVE_TEXT
CREATE_BUILD_TEXT = BuildsMenu.CREATE_BUILD
MY_BUILDS_TEXT = BuildsMenu.MY_BUILDS
POPULAR_BUILDS_TEXT = BuildsMenu.POPULAR_BUILDS

VOTING_MENU_TEXT = VotingMenu.TEXT
VOTING_INTERACTIVE_TEXT = VotingMenu.INTERACTIVE_TEXT
CURRENT_VOTES_TEXT = VotingMenu.CURRENT_VOTES
MY_VOTES_TEXT = VotingMenu.MY_VOTES
SUGGEST_TOPIC_TEXT = VotingMenu.SUGGEST_TOPIC_PROMPT
SUGGESTION_RESPONSE_TEXT = VotingMenu.SUGGESTION_RESPONSE

STATISTICS_MENU_TEXT = StatisticsMenu.TEXT
STATISTICS_INTERACTIVE_TEXT = StatisticsMenu.INTERACTIVE_TEXT
ACTIVITY_TEXT = StatisticsMenu.ACTIVITY
RANKING_TEXT = StatisticsMenu.RANKING
GAME_STATS_TEXT = StatisticsMenu.GAME_STATS

ACHIEVEMENTS_MENU_TEXT = AchievementsMenu.TEXT
ACHIEVEMENTS_INTERACTIVE_TEXT = AchievementsMenu.INTERACTIVE_TEXT
BADGES_TEXT = AchievementsMenu.BADGES
PROGRESS_TEXT = AchievementsMenu.PROGRESS
TOURNAMENT_STATS_TEXT = AchievementsMenu.TOURNAMENT_STATS
AWARDS_TEXT = AchievementsMenu.AWARDS

SETTINGS_MENU_TEXT = SettingsMenu.TEXT
SETTINGS_INTERACTIVE_TEXT = SettingsMenu.INTERACTIVE_TEXT
LANGUAGE_TEXT = SettingsMenu.LANGUAGE_CHANGE
CHANGE_USERNAME_TEXT = SettingsMenu.CHANGE_USERNAME_PROMPT
UPDATE_ID_TEXT = SettingsMenu.UPDATE_ID_TEXT
NOTIFICATIONS_TEXT = SettingsMenu.NOTIFICATIONS_SETTINGS

FEEDBACK_MENU_TEXT = FeedbackMenu.TEXT
FEEDBACK_INTERACTIVE_TEXT = FeedbackMenu.INTERACTIVE_TEXT
SEND_FEEDBACK_TEXT = FeedbackMenu.SEND_FEEDBACK_PROMPT
REPORT_BUG_TEXT = FeedbackMenu.REPORT_BUG_PROMPT
FEEDBACK_RECEIVED_TEXT = FeedbackMenu.FEEDBACK_RECEIVED
BUG_REPORT_RECEIVED_TEXT = FeedbackMenu.BUG_REPORT_RECEIVED

HELP_MENU_TEXT = HelpMenu.TEXT
HELP_INTERACTIVE_TEXT = HelpMenu.INTERACTIVE_TEXT
INSTRUCTIONS_TEXT = HelpMenu.INSTRUCTIONS
FAQ_TEXT = HelpMenu.FAQ
HELP_SUPPORT_TEXT = HelpMenu.SUPPORT_CONTACT

UNKNOWN_COMMAND_TEXT = ErrorMessages.UNKNOWN_COMMAND
GENERIC_ERROR_MESSAGE_TEXT = ErrorMessages.GENERIC_ERROR
ERROR_MESSAGE_TEXT = ErrorMessages.ERROR_MESSAGE
USE_BUTTON_NAVIGATION_TEXT = ErrorMessages.USE_BUTTON_NAVIGATION

SEARCH_HERO_RESPONSE_TEXT = AdditionalResponses.SEARCH_HERO_RESPONSE
CHANGE_USERNAME_RESPONSE_TEXT = AdditionalResponses.CHANGE_USERNAME_RESPONSE

MLS_BUTTON_RESPONSE_TEXT = InlineButtonResponses.MLS_BUTTON_RESPONSE
UNHANDLED_INLINE_BUTTON_TEXT = InlineButtonResponses.UNHANDLED_INLINE_BUTTON

TOURNAMENT_CREATE_TEXT = TournamentTexts.CREATE_TOURNAMENT
TOURNAMENT_VIEW_TEXT = TournamentTexts.VIEW_TOURNAMENTS

META_HERO_LIST_TEXT = MetaTexts.HERO_LIST
META_RECOMMENDATIONS_TEXT = MetaTexts.RECOMMENDATIONS
META_UPDATES_TEXT = MetaTexts.UPDATES

M6_INFO_TEXT = M6Texts.INFO
M6_STATS_TEXT = M6Texts.STATS
M6_NEWS_TEXT = M6Texts.NEWS

# Додаткові текстові константи (у випадку, якщо є)
# Переконайтесь, що всі необхідні тексти додані в відповідні класи вище