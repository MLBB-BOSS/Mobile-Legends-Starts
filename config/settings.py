# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
ENABLE_QUIZZES = os.getenv('ENABLE_QUIZZES', 'false').lower() == 'true'
ENABLE_NEWS = os.getenv('ENABLE_NEWS', 'false').lower() == 'true'# Основні налаштування (токени, URL-адреси тощо)
