# texts.py
from rich.text import Text

# Привітальні повідомлення
WELCOME_NEW_USER_TEXT = Text()
WELCOME_NEW_USER_TEXT.append("🔥 Ласкаво просимо до ", style="bold red")
WELCOME_NEW_USER_TEXT.append("Mobile Legends: Starts", style="bold blue")
WELCOME_NEW_USER_TEXT.append(" – вашого нового незамінного партнера у світі ", style="bold red")
WELCOME_NEW_USER_TEXT.append("Mobile Legends: Bang Bang! 🔥\n\n", style="bold green")
WELCOME_NEW_USER_TEXT.append("🎮 Тут ви отримаєте доступ до широкого спектра можливостей:\n")
WELCOME_NEW_USER_TEXT.append("• 🥷 Досліджувати характеристики та ролі різних героїв.\n", style="cyan")
WELCOME_NEW_USER_TEXT.append("• 📚 Отримувати покрокові гайди, тактичні поради та рекомендації щодо білдів.\n", style="cyan")
WELCOME_NEW_USER_TEXT.append("• 📊 Аналізувати власну статистику та прогрес, щоб робити більш обґрунтовані рішення у грі.\n", style="cyan")
WELCOME_NEW_USER_TEXT.append("• 🏆 Брати участь у турнірах, виявляти нові стратегії та здобувати унікальні нагороди.\n\n", style="cyan")
WELCOME_NEW_USER_TEXT.append("🏆 Готові до нових пригод? Натискайте нижче, щоб розпочати подорож до найвищих вершин Mobile Legends!\n\n", style="bold magenta")
WELCOME_NEW_USER_TEXT.append("💖 Цей застосунок створено з любов’ю для справжніх поціновувачів Mobile Legends. 💖\n", style="bold red")

# Сторінки вступу
INTRO_PAGE_1_TEXT = WELCOME_NEW_USER_TEXT

INTRO_PAGE_2_TEXT = Text()
INTRO_PAGE_2_TEXT.append("💡 Функції Mobile Legends: Starts:\n", style="bold magenta")
INTRO_PAGE_2_TEXT.append("🧭 Навігація: Зручний інтерфейс для швидкого доступу до героїв, гайдів, білдів та статистики.\n", style="bold cyan")
INTRO_PAGE_2_TEXT.append("👤 Мій профіль: Переглядайте свій рівень, рейтинг, досягнення та персональні дані.\n", style="bold cyan")
INTRO_PAGE_2_TEXT.append("🥷 Персонажі: Отримуйте вичерпну інформацію про кожного героя, його роль та стратегії.\n", style="bold cyan")
INTRO_PAGE_2_TEXT.append("📚 Гайди: Вивчайте матеріали для новачків і досвідчених гравців, опановуйте стратегії та поради.\n", style="bold cyan")
INTRO_PAGE_2_TEXT.append("📊 Статистика: Аналізуйте ігрові дані – перемоги, поразки, ефективність героїв.\n", style="bold cyan")
INTRO_PAGE_2_TEXT.append("🔧 Білди: Створюйте та редагуйте спорядження, адаптуйте його під різні ситуації.\n", style="bold cyan")
INTRO_PAGE_2_TEXT.append("🏆 Турніри: Дізнавайтеся про змагання, умови участі та нагороди, перевіряйте свої навички.\n\n", style="bold cyan")
INTRO_PAGE_2_TEXT.append("Натисніть «Далі», щоб дізнатися про інші можливості цього застосунку.\n", style="bold yellow")

# Головне меню
MAIN_MENU_TEXT = Text()
MAIN_MENU_TEXT.append("👋 Вітаємо, {user_first_name}, у Mobile Legends: Starts!\n", style="bold cyan")
MAIN_MENU_TEXT.append("Оберіть потрібну опцію нижче, щоб досліджувати можливості та вдосконалювати свій ігровий досвід.\n", style="bold green")

MAIN_MENU_ERROR_TEXT = Text()
MAIN_MENU_ERROR_TEXT.append("❗ Сталася помилка.\n", style="bold red")
MAIN_MENU_ERROR_TEXT.append("Будь ласка, спробуйте ще раз або поверніться до головного меню. Якщо проблема не зникне, зверніться до підтримки.\n", style="bold yellow")

# Меню персонажів
HEROES_MENU_TEXT = Text()
HEROES_MENU_TEXT.append("🥷 Персонажі\n", style="bold blue")
HEROES_MENU_TEXT.append("Оберіть категорію героїв, щоб дізнатися про їхні можливості та розробити ефективні стратегії.\n", style="bold green")

HEROES_INTERACTIVE_TEXT = Text()
HEROES_INTERACTIVE_TEXT.append("📂 Категорії героїв:\n", style="bold magenta")
HEROES_INTERACTIVE_TEXT.append("🛡️ Танк: міцні герої для захисту команди.\n", style="cyan")
HEROES_INTERACTIVE_TEXT.append("🧙‍♂️ Маг: завдають магічної шкоди та контролюють хід бою.\n", style="cyan")
HEROES_INTERACTIVE_TEXT.append("🏹 Стрілець: стабільна шкода з дистанції.\n", style="cyan")
HEROES_INTERACTIVE_TEXT.append("⚔️ Асасін: швидкі атаки по ключових цілях.\n", style="cyan")
HEROES_INTERACTIVE_TEXT.append("❤️ Підтримка: лікування та посилення союзників.\n", style="cyan")
HEROES_INTERACTIVE_TEXT.append("🗡️ Боєць: збалансовані герої з атакою і захистом.\n", style="cyan")

# Використання
if __name__ == "__main__":
    from rich.console import Console

    console = Console()
    console.print(WELCOME_NEW_USER_TEXT)
    console.print(MAIN_MENU_TEXT.format(user_first_name="Гравець"))
    console.print(HEROES_MENU_TEXT)
    console.print(HEROES_INTERACTIVE_TEXT)
    console.print(MAIN_MENU_ERROR_TEXT)
