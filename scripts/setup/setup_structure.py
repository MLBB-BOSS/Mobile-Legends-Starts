import os
import sys
import json
from github import Github, GithubException

# Отримання GitHub Token з оточення
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("GITHUB_TOKEN is not set.")
    sys.exit(1)

# Ініціалізація клієнта GitHub
g = Github(GITHUB_TOKEN)

# Отримання назви репозиторію з оточення
repo_name = os.getenv('GITHUB_REPOSITORY')
if not repo_name:
    print("GITHUB_REPOSITORY is not set.")
    sys.exit(1)

try:
    repo = g.get_repo(repo_name)
except GithubException as e:
    print(f"Error accessing repository: {e}")
    sys.exit(1)

# Визначення структури репозиторію, крім .github
structure = {
    "config": {
        "__init__.py": "",
        "settings.py": """# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
"""
    },
    "data": {
        "badges.json": """[
    {
        "id": 1,
        "name": "Collector",
        "description": "Upload 10 screenshots"
    },
    {
        "id": 2,
        "name": "Super Collector",
        "description": "Upload 50 screenshots"
    },
    {
        "id": 3,
        "name": "Master Collector",
        "description": "Upload 100 screenshots"
    }
]""",
        "heroes.json": "# Basic information about heroes",
        "characters.json": "# Complete list of characters",
        "prompts.json": "# Prompts for OpenAI API",
        "builds": {
            "optimal_builds.json": "# Recommended optimal builds",
            "counter_builds.json": "# Recommended counter builds",
            "build_comparisons.json": "# Build comparisons",
        },
    },
    "docs": {
        "README.md": """# Telegram ML Bot

## Description

A Telegram bot for Mobile Legends: Starts (MLS) providing information about heroes, guides, tournaments, news, and more.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/telegram-ml-bot.git
    cd telegram-ml-bot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\\Scripts\\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on `.env.example` and fill in the required fields.

5. Run the bot:
    ```bash
    python main.py
    ```

## Usage

Describe how to use the bot, commands, and features.

## Contributing

Please follow the guidelines in `CONTRIBUTING.md` to contribute to the project.

## License

This project is licensed under the [MIT License](LICENSE).
""",
        "architecture.md": """# Architecture Documentation

## Overview

Describe the overall architecture of the Telegram ML Bot, including key components, data flow, and integrations.

## Components

- **Handlers**: Manage different commands and user interactions.
- **Utils**: Utility functions and helpers.
- **Services**: External service integrations like S3, Google Auth.
- **Models**: Database models using SQLAlchemy.
- **Data**: Static data files including heroes, items, badges.
- **Scripts**: Deployment and setup scripts.
- **Tests**: Unit and integration tests.
- **Docs**: Additional documentation.

## Data Flow

1. **User Interaction**: Users interact with the bot via Telegram.
2. **Handlers**: Commands are processed by corresponding handlers.
3. **Utils and Services**: Handlers utilize utilities and services for processing.
4. **Database**: Data is stored and retrieved using SQLAlchemy models.
5. **External APIs**: Integrations with OpenAI, AWS S3, etc., are managed through services.
6. **Response Generation**: The bot generates and sends responses back to the user based on the processed data and user requests.

## Automation with GitHub Actions

- **Workflow Setup**: The `.github/workflows/create_structure.yml` workflow automates the setup of the repository structure by running the `setup_structure.py` script whenever the `heroes_data.json` file is updated or manually triggered.

- **Continuous Integration**: Tests located in the `tests` directory are executed to verify the integrity of the application before deployments.

## Deployment

- **Docker**: The `Dockerfile` defines the environment for deploying the bot, ensuring consistency across different deployment platforms.

- **Deployment Script**: The `deploy.sh` script automates the deployment process, including pulling the latest changes, installing dependencies, and restarting the bot service.

## Security

- **Environment Variables**: Sensitive information like API keys and tokens are managed through environment variables defined in the `.env` file, which is excluded from version control using `.gitignore`.

- **Access Control**: GitHub Actions are configured with appropriate permissions to interact with the repository without exposing sensitive tokens.

## Scalability

- **Modular Design**: The bot's features are divided into separate handlers and utilities, making it easy to add or modify features without affecting other parts of the application.

- **Database Management**: Using SQLAlchemy allows for flexible and efficient database interactions, supporting scaling as the user base grows.

## Future Enhancements

- **API Integration**: Integrate with official Mobile Legends APIs (if available) to fetch real-time data about heroes, items, and tournaments.

- **Enhanced AI Features**: Utilize OpenAI's capabilities to provide more interactive and intelligent responses to user queries.

- **User Personalization**: Implement features that personalize the user experience based on their preferences and activity within the bot.

- **Analytics and Monitoring**: Add monitoring tools to track the bot's performance and user engagement, aiding in maintenance and feature development.
"""
    },
    "handlers": {
        "__init__.py": "",
        "main_menu.py": """# handlers/main_menu.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from utils.keyboards import main_menu_keyboard

async def main_menu(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Main Menu!", reply_markup=main_menu_keyboard())

router = CommandHandler('menu', main_menu)
""",
        "characters.py": """# handlers/characters.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
import json

async def list_characters(update: Update, context: CallbackContext.DEFAULT_TYPE):
    with open('data/characters.json', 'r', encoding='utf-8') as f:
        characters = json.load(f)
    message = "List of Characters:\n" + "\n".join(characters)
    await update.message.reply_text(message)

router = CommandHandler('characters', list_characters)
""",
        "guides.py": """# handlers/guides.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

async def guides(update: Update, context: CallbackContext.DEFAULT_TYPE):
    guides = [
        "Guide 1: How to improve your gameplay.",
        "Guide 2: Best builds for each hero.",
        "Guide 3: Strategies for tournaments."
    ]
    message = "Game Guides:\n" + "\n".join(guides)
    await update.message.reply_text(message)

router = CommandHandler('guides', guides)
""",
        "tournaments.py": """# handlers/tournaments.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

async def tournaments(update: Update, context: CallbackContext.DEFAULT_TYPE):
    tournaments = [
        "Tournament 1: April 25 - May 5",
        "Tournament 2: June 10 - June 20",
        "Tournament 3: July 15 - July 25"
    ]
    message = "Upcoming Tournaments:\n" + "\n".join(tournaments)
    await update.message.reply_text(message)

router = CommandHandler('tournaments', tournaments)
""",
        "news.py": """# handlers/news.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

async def news(update: Update, context: CallbackContext.DEFAULT_TYPE):
    # Placeholder for fetching and displaying news
    news_items = [
        "Update 1.2 released with new heroes!",
        "Upcoming tournament starts next week.",
        "Maintenance scheduled for this weekend."
    ]
    message = "Latest News:\n" + "\n".join(news_items)
    await update.message.reply_text(message)

router = CommandHandler('news', news)
""",
        "help_menu.py": """# handlers/help_menu.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

async def help_menu(update: Update, context: CallbackContext.DEFAULT_TYPE):
    help_text = \"\"\"
Available Commands:
/menu - Show the main menu
/characters - List all characters
/guides - Show game guides
/tournaments - Upcoming tournaments
/news - Latest news
/quizzes - Take a quiz
/search <query> - Search for information
/emblems - View available emblems
/recommendations <hero_name> - Get build recommendations
/comparisons - Compare builds/items
/myscreenshots - View your uploaded screenshots
\"\"\"
    await update.message.reply_text(help_text)

router = CommandHandler('help', help_menu)
"""
        "quizzes.py": """# handlers/quizzes.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

async def quizzes(update: Update, context: CallbackContext.DEFAULT_TYPE):
    # Placeholder for quizzes
    quiz = "Quiz: What is the main role of a Tank?"
    await update.message.reply_text(quiz)

router = CommandHandler('quizzes', quizzes)
""",
        "search.py": """# handlers/search.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

async def search(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a search query. Usage: /search <query>")
        return
    query = ' '.join(context.args)
    # Placeholder for search functionality
    results = f"Search results for '{query}':\n1. Result A\n2. Result B\n3. Result C"
    await update.message.reply_text(results)

router = CommandHandler('search', search)
""",
        "emblems.py": """# handlers/emblems.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

async def emblems(update: Update, context: CallbackContext.DEFAULT_TYPE):
    emblems = [
        "Emblem 1: Strength",
        "Emblem 2: Agility",
        "Emblem 3: Intelligence"
    ]
    message = "Available Emblems:\n" + "\n".join(emblems)
    await update.message.reply_text(message)

router = CommandHandler('emblems', emblems)
""",
        "recommendations.py": """# handlers/recommendations.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from utils.recommendations_engine import recommend_build

async def recommendations(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a hero name. Usage: /recommendations <hero_name>")
        return
    hero_name = ' '.join(context.args).title()
    build = recommend_build(hero_name)
    message = f"Recommended Builds for {hero_name}:\n\nOptimal Build:\n" + "\n".join(build['optimal']) + "\n\nCounter Build:\n" + "\n".join(build['counter'])
    await update.message.reply_text(message)

router = CommandHandler('recommendations', recommendations)
""",
        "comparisons.py": """# handlers/comparisons.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

async def comparisons(update: Update, context: CallbackContext.DEFAULT_TYPE):
    comparisons = [
        "Comparison 1: Hero A vs Hero B",
        "Comparison 2: Item X vs Item Y",
        "Comparison 3: Spell M vs Spell N"
    ]
    message = "Comparisons:\n" + "\n".join(comparisons)
    await update.message.reply_text(message)

router = CommandHandler('comparisons', comparisons)
""",
        "screenshots_handler.py": """# handlers/screenshots_handler.py
from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackContext
from services.s3_service import upload_screenshot

async def handle_screenshot(update: Update, context: CallbackContext.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_content = await file.download_as_bytearray()
    file_name = f"screenshots/{file.file_id}.jpg"
    url = upload_screenshot(file_name, file_content)
    await update.message.reply_text(f"Screenshot uploaded: {url}")

router = MessageHandler(Filters.photo, handle_screenshot)
""",
        "myscreenshots_handler.py": """# handlers/myscreenshots_handler.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from models.user import User
from models.screenshot import Screenshot
from utils.data_loader import load_json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

async def myscreenshots(update: Update, context: CallbackContext.DEFAULT_TYPE):
    session = Session()
    user = session.query(User).filter_by(telegram_id=update.effective_user.id).first()
    if not user or not user.screenshots:
        await update.message.reply_text("You have no screenshots uploaded.")
        session.close()
        return
    urls = [screenshot.file_url for screenshot in user.screenshots]
    message = "Your Screenshots:\n" + "\n".join(urls)
    await update.message.reply_text(message)
    session.close()

router = CommandHandler('myscreenshots', myscreenshots)
"""
    },
    "utils": {
        "__init__.py": "",
        "data_loader.py": """# utils/data_loader.py
import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
""",
        "openai_api.py": """# utils/openai_api.py
import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
""",
        "templates.py": """# utils/templates.py

MAIN_MENU = """
Welcome to the Mobile Legends: Starts (MLS) Bot!

Please choose an option:
1. Characters
2. Guides
3. Tournaments
4. News
5. Help
"""
""",
        "recommendations_engine.py": """# utils/recommendations_engine.py

def recommend_build(hero_name):
    # Placeholder for build recommendation logic
    return {
        "optimal": ["Item1", "Item2", "Item3"],
        "counter": ["ItemA", "ItemB", "ItemC"]
    }
""",
        "data_updater.py": """# utils/data_updater.py
import json

def update_heroes_data(file_path, new_data):
    with open(file_path, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data.update(new_data)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.truncate()
""",
        "keyboards.py": """# utils/keyboards.py
from telegram import ReplyKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        ['Characters', 'Guides'],
        ['Tournaments', 'News'],
        ['Help']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
""",
        "points.py": """# utils/points.py

def add_points(user, points):
    user.points += points
    return user
""",
        "badges.py": """# utils/badges.py
import json

def get_badges():
    with open('data/badges.json', 'r', encoding='utf-8') as f:
        return json.load(f)
"""
    },
    "services": {
        "__init__.py": "",
        "s3_service.py": """# services/s3_service.py
import boto3
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME, AWS_REGION

s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_screenshot(file_name, file_content):
    s3_client.put_object(Bucket=AWS_S3_BUCKET_NAME, Key=file_name, Body=file_content)
    return f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
""",
        "image_recognition.py": """# services/image_recognition.py

def recognize_image(image_path):
    # Placeholder for image recognition logic
    return "Recognized content from image."
""",
        "google_auth.py": """# services/google_auth.py
from google.oauth2 import service_account
from google.auth.transport.requests import Request

def authenticate_google():
    credentials = service_account.Credentials.from_service_account_file('path/to/service_account.json')
    credentials.refresh(Request())
    return credentials
"""
    },
    "models": {
        "__init__.py": "",
        "user.py": """# models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    points = Column(Integer, default=0)
    
    screenshots = relationship("Screenshot", back_populates="user")
""",
        "screenshot.py": """# models/screenshot.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Screenshot(Base):
    __tablename__ = 'screenshots'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_url = Column(String, nullable=False)
    
    user = relationship("User", back_populates="screenshots")
""",
        "badge.py": """# models/badge.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Badge(Base):
    __tablename__ = 'badges'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
"""
    },
    "scripts": {
        "deploy.sh": """#!/bin/bash
# scripts/deploy.sh
# Deployment script for the Telegram ML Bot

# Pull the latest changes
git pull origin main

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Restart the bot (assuming using systemd)
sudo systemctl restart telegram-ml-bot
"""
    },
    "tests": {
        "__init__.py": "",
        "test_main_menu.py": """# tests/test_main_menu.py
import unittest
from handlers.main_menu import main_menu

class TestMainMenu(unittest.TestCase):
    def test_main_menu_response(self):
        # Implement tests for main_menu handler
        pass

if __name__ == '__main__':
    unittest.main()
""",
        "test_items.py": """# tests/test_items.py
import unittest
from handlers.items import items

class TestItems(unittest.TestCase):
    def test_items_response(self):
        # Implement tests for items handler
        pass

if __name__ == '__main__':
    unittest.main()
""",
        "test_spells.py": """# tests/test_spells.py
import unittest
from handlers.spells import spells

class TestSpells(unittest.TestCase):
    def test_spells_response(self):
        # Implement tests for spells handler
        pass

if __name__ == '__main__':
    unittest.main()
""",
        "test_emblems.py": """# tests/test_emblems.py
import unittest
from handlers.emblems import emblems

class TestEmblems(unittest.TestCase):
    def test_emblems_response(self):
        # Implement tests for emblems handler
        pass

if __name__ == '__main__':
    unittest.main()
""",
        "test_recommendations.py": """# tests/test_recommendations.py
import unittest
from handlers.recommendations import recommendations

class TestRecommendations(unittest.TestCase):
    def test_recommendations_response(self):
        # Implement tests for recommendations handler
        pass

if __name__ == '__main__':
    unittest.main()
""",
        "test_handlers.py": """# tests/test_handlers.py
import unittest
from handlers.main_menu import main_menu
from handlers.characters import list_characters

class TestHandlers(unittest.TestCase):
    def test_main_menu_handler(self):
        # Implement tests for main_menu handler
        pass

    def test_characters_handler(self):
        # Implement tests for characters handler
        pass

if __name__ == '__main__':
    unittest.main()
""",
        "test_services.py": """# tests/test_services.py
import unittest
from services.s3_service import upload_screenshot

class TestServices(unittest.TestCase):
    def test_upload_screenshot(self):
        # Implement tests for upload_screenshot function
        pass

if __name__ == '__main__':
    unittest.main()
"""
    },
    "logging": {
        "elasticsearch": {
            "elasticsearch.yml": """# logging/elasticsearch/elasticsearch.yml
# Elasticsearch configuration for logging
cluster.name: "mls-logging-cluster"
node.name: "node-1"
network.host: 0.0.0.0
http.port: 9200
"""
        },
        "logstash": {
            "logstash.conf": """# logging/logstash/logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Add any filters if necessary
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "mls-logs-%{+YYYY.MM.dd}"
  }
}
"""
        },
        "kibana": {
            "kibana.yml": """# logging/kibana/kibana.yml
server.port: 5601
elasticsearch.hosts: ["http://localhost:9200"]
"""
        },
        "filebeat": {
            "filebeat.yml": """# logging/filebeat/filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /app/logs/*.log

output.logstash:
  hosts: ["localhost:5044"]
"""
        }
    },
    "monitoring": {
        "prometheus": {
            "prometheus.yml": """# monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'telegram-ml-bot'
    static_configs:
      - targets: ['localhost:8000']  # Update with your bot's metrics endpoint if available
"""
        },
        "grafana": {
            "dashboards": {
                "example_dashboard.json": """{
  "annotations": {
    "list": []
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 1,
  "iteration": 1620354567796,
  "links": [],
  "panels": [],
  "schemaVersion": 27,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "Example Dashboard",
  "uid": "example-dashboard",
  "version": 1
}"""
            }
        }
    },
    "docker": {
        "docker-compose.yml": """# docker/docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - OTHER_ENV_VARS
    depends_on:
      - db

  bot:
    build:
      context: .
      dockerfile: Dockerfile.bot
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - DATABASE_URL=${DATABASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_S3_BUCKET_NAME=${AWS_S3_BUCKET_NAME}
      - AWS_REGION=${AWS_REGION}
    depends_on:
      - api

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: youruser
      POSTGRES_PASSWORD: yourpassword
      POSTGRES_DB: yourdb
    volumes:
      - db_data:/var/lib/postgresql/data

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.10.1
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.10.1
    ports:
      - "5044:5044"
    volumes:
      - ./logging/logstash/logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:7.10.1
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:7.10.1
    volumes:
      - ./logging/filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml
      - ./logs:/app/logs
    depends_on:
      - logstash

  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/dashboards
    depends_on:
      - prometheus

volumes:
  db_data:
  es_data:
  grafana_data:
""",
        "Dockerfile.api": """# docker/Dockerfile.api
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
        "Dockerfile.bot": """# docker/Dockerfile.bot
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
""",
        "Dockerfile.db": """# docker/Dockerfile.db
# Typically, you'd use an official image, no need to create a Dockerfile
FROM postgres:13
"""
    },
    "security": {
        "secrets.yaml": """# security/secrets.yaml
# Secrets should not be committed to the repository.
# Use GitHub Secrets or another secret management system.
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=your_database_url
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_S3_BUCKET_NAME=your_s3_bucket_name
AWS_REGION=your_aws_region
DEBUG=True
""",
        "firewall_rules.sh": """# security/firewall_rules.sh
#!/bin/bash
# Firewall setup script

# Allow SSH
ufw allow ssh

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow Prometheus and Grafana
ufw allow 9090/tcp
ufw allow 3000/tcp

# Allow Elasticsearch and Kibana
ufw allow 9200/tcp
ufw allow 5601/tcp

# Enable UFW
ufw enable
"""
    },
    "requirements.txt": """# requirements.txt
# Python dependencies
python-telegram-bot==13.7
SQLAlchemy==1.4.22
alembic==1.7.1
boto3==1.18.20
python-dotenv==0.19.0
openai==0.11.3
pytest==6.2.4
flake8==3.9.2
PyGithub==1.55
uvicorn==0.14.0
fastapi==0.68.1
""",
    ".env.example": """# .env.example
# Example environment variables
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=your_database_url
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_S3_BUCKET_NAME=your_s3_bucket_name
AWS_REGION=your_aws_region
DEBUG=True
""",
    ".gitignore": """# .gitignore
# Python
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
    "Procfile": """# Procfile
web: python main.py
""",
    "README.md": """# Telegram ML Bot

## Description

A Telegram bot for Mobile Legends: Starts (MLS) providing information about heroes, guides, tournaments, news, and more.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/telegram-ml-bot.git
    cd telegram-ml-bot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\\Scripts\\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on `.env.example` and fill in the required fields.

5. Run the bot:
    ```bash
    python main.py
    ```

## Usage

Describe how to use the bot, commands, and features.

## Contributing

Please follow the guidelines in `CONTRIBUTING.md` to contribute to the project.

## License

This project is licensed under the [MIT License](LICENSE).
""",
    "main.py": """# main.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from handlers import main_menu, characters, guides, tournaments, news, help_menu, quizzes, search, emblems, recommendations, comparisons, screenshots_handler, myscreenshots_handler
from config.settings import TELEGRAM_BOT_TOKEN
from utils.logging_setup import setup_logging

# Setup logging
setup_logging()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm MLSnap bot. How can I assist you?")

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(main_menu.router)
    application.add_handler(characters.router)
    application.add_handler(guides.router)
    application.add_handler(tournaments.router)
    application.add_handler(news.router)
    application.add_handler(help_menu.router)
    application.add_handler(quizzes.router)
    application.add_handler(search.router)
    application.add_handler(emblems.router)
    application.add_handler(recommendations.router)
    application.add_handler(comparisons.router)
    application.add_handler(screenshots_handler.router)
    application.add_handler(myscreenshots_handler.router)

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
""",
    "utils/logging_setup.py": """# utils/logging_setup.py
import logging

def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
"""
}

# Список героїв завантажується з 'heroes_data.json'
heroes_data_file = os.path.join(os.path.dirname(__file__), 'heroes_data.json')

def load_heroes_data(file_path):
    if not os.path.exists(file_path):
        print(f"Heroes data file '{file_path}' not found.")
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_existing_hero_files(repo):
    # Отримати всі файли в папці heroes/
    try:
        contents = repo.get_contents("heroes")
    except GithubException as e:
        if e.status == 404:
            return {}
        else:
            print(f"Error accessing 'heroes' folder: {e}")
            return {}

    hero_files = {}
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            try:
                contents.extend(repo.get_contents(file_content.path))
            except GithubException as e:
                print(f"Error accessing subfolder '{file_content.path}': {e}")
                continue
        else:
            # Extract hero name from file path
            hero_name = os.path.splitext(os.path.basename(file_content.path))[0].replace('_', ' ').title()
            class_name = os.path.basename(os.path.dirname(file_content.path))
            hero_files[hero_name] = class_name
    return hero_files

def create_file(repo, path, content, update=False):
    try:
        file_content = repo.get_contents(path)
        if update:
            repo.update_file(path, f"Update {path}", content, file_content.sha)
            print(f"File '{path}' updated.")
        else:
            print(f"File '{path}' already exists. Skipping creation.")
    except GithubException as e:
        if e.status == 404:
            repo.create_file(path, f"Create {path}", content)
            print(f"File '{path}' created.")
        else:
            print(f"Error creating file '{path}': {e}")

def create_folder(repo, path):
    try:
        repo.get_contents(path)
        print(f"Folder '{path}' already exists.")
    except GithubException as e:
        if e.status == 404:
            # GitHub не підтримує порожні папки, тому додаємо .gitkeep
            repo.create_file(f"{path}/.gitkeep", "Add .gitkeep to keep the folder", "")
            print(f"Folder '{path}' created with .gitkeep.")
        else:
            print(f"Error creating folder '{path}': {e}")

def move_file(repo, old_path, new_path):
    try:
        file_content = repo.get_contents(old_path)
        # Створюємо новий файл з вмістом старого
        repo.create_file(new_path, f"Move {old_path} to {new_path}", file_content.decoded_content.decode())
        # Видаляємо старий файл
        repo.delete_file(old_path, f"Delete old file {old_path} after moving to {new_path}", file_content.sha)
        print(f"Moved '{old_path}' to '{new_path}'.")
    except GithubException as e:
        print(f"Error moving file from '{old_path}' to '{new_path}': {e}")

def create_heroes(repo, heroes, existing_hero_files):
    for hero_class, hero_list in heroes.items():
        class_path = f"heroes/{hero_class}"
        create_folder(repo, class_path)
        
        for hero in hero_list:
            # Форматування імені героя для файлу
            hero_filename = hero.lower().replace(" ", "_").replace("-", "_").replace("&", "_").replace("/", "_")
            hero_file_path = f"{class_path}/{hero_filename}.json"
            correct_class = hero_class

            # Перевірка, чи герой вже існує в іншій категорії
            if hero in existing_hero_files:
                current_class = existing_hero_files[hero]
                if current_class != correct_class:
                    # Герой був у іншій категорії, переміщуємо його
                    old_file_path = f"heroes/{current_class}/{hero_filename}.json"
                    move_file(repo, old_file_path, hero_file_path)
                else:
                    # Герой вже в правильній категорії, оновлюємо файл
                    try:
                        file_content = repo.get_contents(hero_file_path)
                        # Можна оновити вміст файлу, якщо необхідно
                        # Наприклад, оновити інформацію про героя
                        hero_data = {
                            "name": hero,
                            "class": correct_class,
                            "role": "",  # Заповніть відповідно
                            "skills": [],
                            "builds": {
                                "optimal": [],
                                "counter": []
                            }
                        }
                        repo.update_file(
                            hero_file_path,
                            f"Update {hero_file_path}",
                            json.dumps(hero_data, ensure_ascii=False, indent=4),
                            file_content.sha
                        )
                        print(f"File '{hero_file_path}' updated with new data.")
                    except GithubException as e:
                        print(f"Error updating file '{hero_file_path}': {e}")
            else:
                # Герой не існує, створюємо новий файл
                hero_data = {
                    "name": hero,
                    "class": correct_class,
                    "role": "",  # Заповніть відповідно
                    "skills": [],
                    "builds": {
                        "optimal": [],
                        "counter": []
                    }
                }
                create_file(repo, hero_file_path, json.dumps(hero_data, ensure_ascii=False, indent=4))

def create_structure(current_path, structure, repo):
    for name, content in structure.items():
        path = os.path.join(current_path, name)
        if isinstance(content, dict):
            # Створення папки
            create_folder(repo, path)
            # Рекурсивний виклик для вкладених папок
            create_structure(path, content, repo)
        else:
            # Створення файлу
            create_file(repo, path, content)
    
    # Після створення всіх папок і файлів, створюємо героїв
    heroes = load_heroes_data(heroes_data_file)
    existing_hero_files = get_existing_hero_files(repo)
    create_heroes(repo, heroes, existing_hero_files)

def main():
    create_structure("", structure, repo)

if __name__ == "__main__":
    main()
