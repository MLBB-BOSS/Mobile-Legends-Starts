# scripts/setup_structure.py
import os
import sys
from github import Github, GithubException

# Отримання GitHub Token з середовища
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("GITHUB_TOKEN is not set.")
    sys.exit(1)

# Ініціалізація GitHub клієнта
g = Github(GITHUB_TOKEN)

# Отримання репозиторія
repo_name = os.getenv('GITHUB_REPOSITORY')
if not repo_name:
    print("GITHUB_REPOSITORY is not set.")
    sys.exit(1)

try:
    repo = g.get_repo(repo_name)
except GithubException as e:
    print(f"Error accessing repository: {e}")
    sys.exit(1)

# Визначення структури репозиторія
structure = {
    ".github/workflows": {
        "ci.yml": """# CI/CD Workflow (existing content or leave empty)"""
    },
    "handlers": {
        "__init__.py": "",
        "main_menu.py": "# Головне меню бота",
        "characters.py": "# Інформація про персонажів",
        "guides.py": "# Гайди по грі",
        "tournaments.py": "# Інформація про турніри",
        "updates.py": "# Оновлення та новини",
        "beginner.py": "# Підказки для новачків",
        "news.py": "# Актуальні новини",
        "help_menu.py": "# Меню допомоги",
        "quizzes.py": "# Вікторини та опитування",
        "search.py": "# Пошук по контенту",
        "items.py": "# Інформація про предмети",
        "spells.py": "# Інформація про заклинання",
        "emblems.py": "# Інформація про емблеми",
        "recommendations.py": "# Рекомендації",
        "comparisons.py": "# Порівняння предметів/героїв",
        "screenshots_handler.py": "# Обробка отримання скріншотів від користувачів",
        "myscreenshots_handler.py": "# Відображення збережених скріншотів користувача",
    },
    "utils": {
        "__init__.py": "",
        "data_loader.py": "# Завантаження даних з файлів",
        "openai_api.py": "# Інтеграція з OpenAI API",
        "templates.py": "# Шаблони для відповідей бота",
        "recommendations_engine.py": "# Логіка рекомендацій",
        "data_updater.py": "# Автоматичне оновлення даних",
        "keyboards.py": "# Налаштування клавіатур бота",
        "points.py": "# Система очок",
        "badges.py": "# Система нагород",
    },
    "services": {
        "__init__.py": "",
        "s3_service.py": "# Завантаження скріншотів на S3 або інший сервер",
        "image_recognition.py": "# Обробка та розпізнавання зображень",
        "google_auth.py": "# Google OAuth 2.0 авторизація",
    },
    "models": {
        "__init__.py": "",
        "user.py": "# Модель користувача",
        "screenshot.py": "# Модель скріншоту",
        "badge.py": "# Модель нагороди",
    },
    "data": {
        "badges.json": """[
    {
        "id": 1,
        "name": "Collector",
        "description": "Завантажте 10 скріншотів"
    },
    {
        "id": 2,
        "name": "Super Collector",
        "description": "Завантажте 50 скріншотів"
    },
    {
        "id": 3,
        "name": "Master Collector",
        "description": "Завантажте 100 скріншотів"
    }
    ]""",
        "heroes.json": "# Базова інформація про героїв",
        "characters.json": "# Повний список персонажів",
        "prompts.json": "# Промпти для OpenAI API",
        "builds": {
            "optimal_builds.json": "# Рекомендовані оптимальні білди",
            "counter_builds.json": "# Рекомендовані контр-білди",
            "build_comparisons.json": "# Порівняння білдів",
        },
    },
    "screenshots": {},
    "config": {
        "__init__.py": "",
        "settings.py": "# Основні налаштування (токени, URL-адреси тощо)",
    },
    "tests": {
        "__init__.py": "",
        "test_main_menu.py": "# Тести для головного меню",
        "test_items.py": "# Тести для предметів",
        "test_spells.py": "# Тести для заклинань",
        "test_emblems.py": "# Тести для емблем",
        "test_recommendations.py": "# Тести для рекомендацій",
        "test_handlers.py": "# Тести для обробників скріншотів",
        "test_services.py": "# Тести для сервісів (S3, Google Auth)",
        "test_models.py": "# Тести для моделей даних",
    },
    "docs": {
        "architecture.md": "# Документація з архітектури",
        "features": {
            "items.md": "# Документ про предмети",
            "spells.md": "# Документ про заклинання",
            "emblems.md": "# Документ про емблеми",
            "recommendations.md": "# Документ про рекомендації",
            "comparisons.md": "# Документ про порівняння",
            "screenshots.md": "# Документ про функціонал збору скріншотів",
        },
    },
    "scripts": {
        "deploy.sh": "# Сценарій для деплойменту бота",
    },
    ".env.example": """# Приклад налаштувань середовища
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=your_database_url
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_S3_BUCKET_NAME=your_s3_bucket_name
AWS_REGION=your_aws_region
DEBUG=True
""",
    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class

# Environment
.env
venv/
ENV/
env/
env.bak/
venv.bak/

# Logs
logs/
*.log

# Docker
docker-compose.yml
Dockerfile
*.dockerfile

# VS Code
.vscode/

# MacOS
.DS_Store

# Windows
Thumbs.db
""",
    "Procfile": """web: python main.py""",
    "requirements.txt": """# Перелік залежностей Python
python-telegram-bot==13.7
SQLAlchemy==1.4.22
alembic==1.7.1
boto3==1.18.20
python-dotenv==0.19.0
openai==0.11.3
pytest==6.2.4
flake8==3.9.2
""",
    "README.md": """# Telegram ML Bot

## Опис

Telegram-бот для Mobile Legends: Starts (MLS), який надає інформацію про персонажів, гайди, турніри, новини та багато іншого.

## Встановлення

1. Клонуйте репозиторій:
    ```bash
    git clone https://github.com/yourusername/telegram-ml-bot.git
    cd telegram-ml-bot
    ```

2. Створіть та активуйте віртуальне середовище:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3. Встановіть залежності:
    ```bash
    pip install -r requirements.txt
    ```

4. Створіть файл `.env` на основі `.env.example` та заповніть необхідні поля.

5. Запустіть бота:
    ```bash
    python main.py
    ```

## Використання

Опишіть, як використовувати бота, команди та функціонал.

## Внесок

Будь ласка, дотримуйтеся інструкцій у файлі `CONTRIBUTING.md` для внесення змін до проекту.

## Ліцензія

Цей проект ліцензований під [MIT License](LICENSE).
""",
    "main.py": """# main.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot.handlers import main_menu
from core.config import settings
from core.logging import setup_logging

# Налаштування логування
setup_logging()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я MLSnap бот. Як я можу допомогти?")

def main():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Додавання обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(main_menu.router)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
""",
    "Dockerfile": """# Dockerfile
FROM python:3.9-slim as builder

# Встановлення залежностей
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Створення кінцевого образу
FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
""",
}

def create_structure(current_path, structure):
    for name, content in structure.items():
        path = os.path.join(current_path, name)
        if isinstance(content, dict):
            # Створення папки
            try:
                repo.get_contents(path)
                print(f"Папка '{path}' вже існує.")
            except GithubException as e:
                if e.status == 404:
                    repo.create_file(path + '/.gitkeep', "Add .gitkeep to keep the folder", "")
                    print(f"Папка '{path}' створена з файлом .gitkeep.")
                else:
                    print(f"Помилка при створенні папки '{path}': {e}")
            # Рекурсивний виклик для вкладених папок
            create_structure(path, content)
        else:
            # Створення файлу
            try:
                repo.get_contents(path)
                print(f"Файл '{path}' вже існує.")
            except GithubException as e:
                if e.status == 404:
                    repo.create_file(path, f"Create {name}", content)
                    print(f"Файл '{path}' створено.")
                else:
                    print(f"Помилка при створенні файлу '{path}': {e}")

def main():
    create_structure("", structure)

if __name__ == "__main__":
    main()
