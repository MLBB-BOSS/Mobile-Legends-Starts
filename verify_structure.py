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
        "test_services.py",
        "test_structure.py",
        "test_example.py"  # Ваш новий тестовий файл
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
    "verify_structure.py": None,
    "main.py": None
}

def check_structure(base_path, structure, current_path=""):
    missing = []
    misplaced = []
    
    for name, content in structure.items():
        path = os.path.join(base_path, current_path, name)
        
        if isinstance(content, list):
            # Це папка з файлами або підпапками
            if not os.path.isdir(path):
                missing.append(f"Directory '{os.path.join(current_path, name)}' is missing.")
                continue
            for item in content:
                # Розділення на підпапку та файл, якщо є "/"
                if '/' in item:
                    sub_folder, sub_file = item.split('/', 1)
                    sub_path = os.path.join(current_path, name, sub_folder, sub_file)
                    full_sub_path = os.path.join(base_path, sub_path)
                    if not os.path.isdir(os.path.join(base_path, current_path, name, sub_folder)):
                        missing.append(f"Sub-directory '{os.path.join(current_path, name, sub_folder)}' is missing.")
                        continue
                    if not os.path.isfile(full_sub_path):
                        missing.append(f"File '{sub_file}' is missing in '{os.path.join(current_path, name, sub_folder)}'.")
                else:
                    item_path = os.path.join(base_path, current_path, name, item)
                    if not os.path.isfile(item_path):
                        missing.append(f"File '{os.path.join(current_path, name, item)}' is missing.")
        else:
            # Це файл у кореневій папці або підпапці
            if not os.path.isfile(path):
                missing.append(f"File '{os.path.join(current_path, name)}' is missing.")
    
    return missing, misplaced

def main():
    base_path = os.path.abspath(os.path.dirname(__file__))
    missing, misplaced = check_structure(base_path, expected_structure)
    
    if missing:
        print("❌ Відсутні файли або папки:")
        for item in missing:
            print(f" - {item}")
    else:
        print("✅ Всі файли та папки присутні.")
    
    if misplaced:
        print("⚠️ Файли або папки знаходяться не на потрібному місці:")
        for item in misplaced:
            print(f" - {item}")
    else:
        print("✅ Всі файли та папки знаходяться на правильних місцях.")
    
    if missing or misplaced:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
