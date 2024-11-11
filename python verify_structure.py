import os
import sys

# Визначте очікувану структуру репозиторію
expected_structure = {
    "config": ["__init__.py", "settings.py"],
    "data": [
        "badges.json",
        "heroes.json",
        "characters.json",
        "prompts.json",
        "builds/optimal_builds.json",
        "builds/counter_builds.json",
        "builds/build_comparisons.json"
    ],
    "docs": ["README.md", "architecture.md"],
    "handlers": [
        "__init__.py",
        "main_menu.py",
        "characters.py",
        "guides.py",
        "tournaments.py",
        "news.py",
        "help_menu.py",
        "quizzes.py",
        "search.py",
        "emblems.py",
        "recommendations.py",
        "comparisons.py",
        "screenshots_handler.py",
        "myscreenshots_handler.py"
    ],
    "models": ["__init__.py", "user.py", "screenshot.py", "badge.py"],
    "scripts": ["deploy.sh"],
    "services": ["__init__.py", "s3_service.py", "image_recognition.py", "google_auth.py"],
    "tests": [
        "__init__.py",
        "test_main_menu.py",
        "test_items.py",
        "test_spells.py",
        "test_emblems.py",
        "test_recommendations.py",
        "test_handlers.py",
        "test_services.py"
    ],
    "utils": [
        "__init__.py",
        "data_loader.py",
        "openai_api.py",
        "templates.py",
        "recommendations_engine.py",
        "data_updater.py",
        "keyboards.py",
        "points.py",
        "badges.py",
        "logging_setup.py"
    ],
    "logging": [
        "elasticsearch/elasticsearch.yml",
        "logstash/logstash.conf",
        "kibana/kibana.yml",
        "filebeat/filebeat.yml"
    ],
    "monitoring": [
        "prometheus/prometheus.yml",
        "grafana/dashboards/example_dashboard.json"
    ],
    "docker": [
        "docker-compose.yml",
        "Dockerfile.api",
        "Dockerfile.bot",
        "Dockerfile.db"
    ],
    "security": [
        "secrets.yaml",
        "firewall_rules.sh"
    ],
    ".env.example": None,
    ".gitignore": None,
    "Procfile": None,
    "requirements.txt": None,
    "README.md": None,
    "main.py": None
}

def check_structure(base_path, structure):
    all_ok = True
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, list):
            # Це папка з файлами
            if not os.path.isdir(path):
                print(f"❌ Директорія '{name}' відсутня.")
                all_ok = False
                continue
            for item in content:
                item_path = os.path.join(path, item)
                if '/' in item:
                    # Це вкладена папка та файл
                    sub_folder, sub_file = item.split('/', 1)
                    full_sub_folder = os.path.join(path, sub_folder)
                    full_sub_file = os.path.join(full_sub_folder, sub_file)
                    if not os.path.isdir(full_sub_folder):
                        print(f"❌ Директорія '{sub_folder}' відсутня у '{name}'.")
                        all_ok = False
                        continue
                    if not os.path.isfile(full_sub_file):
                        print(f"❌ Файл '{sub_file}' відсутній у '{sub_folder}'.")
                        all_ok = False
                else:
                    if not os.path.isfile(item_path):
                        print(f"❌ Файл '{item}' відсутній у '{name}'.")
                        all_ok = False
        else:
            # Це файл у кореневій папці
            if not os.path.isfile(path):
                print(f"❌ Файл '{name}' відсутній у корені репозиторію.")
                all_ok = False
    return all_ok

if __name__ == "__main__":
    base_path = os.getcwd()  # Базовий шлях - поточна робоча директорія
    if check_structure(base_path, expected_structure):
        print("✅ Структура файлів відповідає очікуваній.")
        sys.exit(0)
    else:
        print("❌ Структура файлів не відповідає очікуваній.")
        sys.exit(1)
