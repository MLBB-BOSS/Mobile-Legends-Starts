from rich.console import Console

console = Console()

# Привітальні повідомлення
WELCOME_NEW_USER_TEXT = (
    "[bold red]🔥 Ласкаво просимо до Mobile Legends: Starts! 🔥[/bold red]\n\n"
    "[bold cyan]🎮 Тут ви отримаєте доступ до широкого спектра можливостей, які допоможуть зрозуміти гру глибше, "
    "вдосконалити навички та вивести ігровий досвід на новий рівень.[/bold cyan]\n\n"
    "Ви зможете:\n"
    "- 🥷 [bold yellow]Досліджувати[/bold yellow] характеристики та ролі різних героїв.\n"
    "- 📚 [italic green]Отримувати[/italic green] покрокові гайди, тактичні поради та рекомендації щодо білдів.\n"
    "- 📊 [underline magenta]Аналізувати[/underline magenta] власну статистику та прогрес.\n"
    "- 🏆 [bold blue]Брати участь[/bold blue] у турнірах, виявляти нові стратегії та здобувати унікальні нагороди.\n\n"
    "[bold white]🏆 Готові до нових пригод?[/bold white] "
    "[italic cyan]Розпочніть подорож до найвищих вершин Mobile Legends![/italic cyan]\n"
    "[bold magenta]Цей застосунок створено з любов’ю для справжніх поціновувачів Mobile Legends.[/bold magenta] 💖"
)

# Сторінки вступу
INTRO_PAGE_1_TEXT = WELCOME_NEW_USER_TEXT

INTRO_PAGE_2_TEXT = (
    "[bold cyan]💡 Функції Mobile Legends: Starts:[/bold cyan]\n\n"
    "- 🧭 [bold blue]Навігація:[/bold blue] Зручний інтерфейс для швидкого доступу до героїв, гайдів, білдів та статистики.\n"
    "- 👤 [bold yellow]Мій профіль:[/bold yellow] Переглядайте свій рівень, рейтинг, досягнення та персональні дані.\n"
    "- 🥷 [bold green]Персонажі:[/bold green] Отримуйте вичерпну інформацію про кожного героя, його роль та стратегії.\n"
    "- 📚 [italic magenta]Гайди:[/italic magenta] Вивчайте матеріали для новачків і досвідчених гравців.\n"
    "- 📊 [underline blue]Статистика:[/underline blue] Аналізуйте ігрові дані – перемоги, поразки, ефективність героїв.\n"
    "- 🔧 [bold white]Білди:[/bold white] Створюйте та редагуйте спорядження, адаптуйте його під різні ситуації.\n"
    "- 🏆 [bold red]Турніри:[/bold red] Дізнавайтеся про змагання, умови участі та нагороди.\n\n"
    "[italic yellow]Натисніть 'Далі', щоб дізнатися більше![/italic yellow]"
)

INTRO_PAGE_3_TEXT = (
    "[bold cyan]🪪 Ваш Профіль:[/bold cyan]\n\n"
    "- 🏅 [bold yellow]Ім'я користувача:[/bold yellow] {username} – ваш унікальний псевдонім у світі Mobile Legends.\n"
    "- 🧬 [bold green]Рівень:[/bold green] {level} – показник вашого загального розвитку в грі.\n"
    "- 📈 [bold blue]Рейтинг:[/bold blue] {rating} – відображає ваші результати та позицію відносно інших гравців.\n"
    "- 🎯 [bold magenta]Досягнення:[/bold magenta] {achievements_count} – кількість здобутих нагород, що свідчать про ваш ігровий досвід.\n\n"
    "[italic cyan]Скористайтеся меню внизу, щоб перейти до будь-якого розділу та почати дослідження функцій.[/italic cyan]\n"
    "[bold yellow]🚀 Розпочніть свою подорож прямо зараз![/bold yellow]"
)

# Головне меню
MAIN_MENU_TEXT = (
    "[bold cyan]👋 Вітаємо, {user_first_name}, у Mobile Legends: Starts![/bold cyan]\n\n"
    "[italic yellow]Оберіть потрібну опцію нижче, щоб досліджувати можливості та вдосконалювати свій ігровий досвід.[/italic yellow]"
)

MAIN_MENU_DESCRIPTION = (
    "[bold white]🎮 Mobile Legends: Starts допоможе вам:[/bold white]\n\n"
    "- 🏆 [bold yellow]Організовувати турніри:[/bold yellow] Створюйте власні змагання, керуйте ними та запрошуйте друзів.\n"
    "- 📸 [italic cyan]Зберігати скріншоти персонажів:[/italic cyan] Робіть візуальні нотатки про героїв.\n"
    "- 📊 [underline blue]Відстежувати активність:[/underline blue] Контролюйте частоту матчів та аналізуйте свою гру.\n"
    "- 🥇 [bold magenta]Отримувати досягнення:[/bold magenta] Здобувайте винагороди за ваші зусилля."
)

MAIN_MENU_ERROR_TEXT = (
    "[bold red]❗ Сталася помилка.[/bold red]\n\n"
    "[italic yellow]Будь ласка, спробуйте ще раз або зверніться до підтримки.[/italic yellow]"
)

# Меню профілю
PROFILE_INTERACTIVE_TEXT = (
    "[bold cyan]🔍 Ваш Профіль:[/bold cyan]\n\n"
    "- 🏅 [bold yellow]Ім'я користувача:[/bold yellow] {username} – ваш персональний нікнейм.\n"
    "- 🧬 [bold green]Рівень:[/bold green] {level} – показник вашого розвитку.\n"
    "- 📈 [bold blue]Рейтинг:[/bold blue] {rating} – ваше місце серед гравців.\n"
    "- 🎯 [bold magenta]Досягнення:[/bold magenta] {achievements_count} – кількість нагород.\n\n"
    "[italic yellow]Оберіть опцію для редагування профілю чи перегляду статистики.[/italic yellow]"
)

# Меню персонажів
HEROES_MENU_TEXT = (
    "[bold cyan]🥷 Персонажі[/bold cyan]\n\n"
    "[italic yellow]Оберіть категорію героїв, щоб дізнатися про їхні можливості та розробити стратегії.[/italic yellow]"
)

HEROES_INTERACTIVE_TEXT = (
    "[bold cyan]📂 Категорії героїв:[/bold cyan]\n\n"
    "- 🛡️ [bold blue]Танк:[/bold blue] Міцні герої для захисту команди.\n"
    "- 🧙‍♂️ [italic green]Маг:[/italic green] Завдають магічної шкоди.\n"
    "- 🏹 [underline yellow]Стрілець:[/underline yellow] Шкода з дистанції.\n"
    "- ⚔️ [bold red]Асасін:[/bold red] Швидкі атаки по ключових цілях.\n"
    "- ❤️ [italic magenta]Підтримка:[/italic magenta] Лікування союзників.\n"
    "- 🗡️ [bold white]Боєць:[/bold white] Баланс атаки і захисту."
)

# Виведення
if __name__ == "__main__":
    # Вивести привітання
    console.print(WELCOME_NEW_USER_TEXT)

    # Вивести текст профілю
    console.print(PROFILE_INTERACTIVE_TEXT.format(username="Player123", level=25, rating=1800, achievements_count=10))
