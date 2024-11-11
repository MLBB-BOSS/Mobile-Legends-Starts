import os
import pytest

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
        "test_structure.py"
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
    "main.py": None,
    "verify_structure.py": None
}

def check_structure(base_path, structure):
    missing = []
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, list):
            # Це папка з файлами
            if not os.path.isdir(path):
                missing.append(f"Directory '{name}' is missing.")
                continue
            for item in content:
                item_path = os.path.join(path, item)
                if '/' in item:
                    # Це вкладена папка та файл
                    sub_folder, sub_file = item.split('/', 1)
                    full_sub_folder = os.path.join(path, sub_folder)
                    full_sub_file = os.path.join(full_sub_folder, sub_file)
                    if not os.path.isdir(full_sub_folder):
                        missing.append(f"Sub-directory '{sub_folder}' is missing in '{name}'.")
                        continue
                    if not os.path.isfile(full_sub_file):
                        missing.append(f"File '{sub_file}' is missing in '{sub_folder}'.")
                else:
                    if not os.path.isfile(item_path):
                        missing.append(f"File '{item}' is missing in '{name}'.")
        else:
            # Це файл у кореневій папці
            if not os.path.isfile(path):
                missing.append(f"File '{name}' is missing in the root directory.")
    return missing

@pytest.fixture
def base_path():
    return os.getcwd()

def test_repository_structure(base_path):
    missing_items = check_structure(base_path, expected_structure)
    if missing_items:
        for item in missing_items:
            print(f"❌ {item}")
    assert not missing_items, "Repository structure does not match the expected structure."
