import os
import sys
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("code_check.log", encoding='utf-8')
    ]
)

def is_empty(file_path):
    """Перевіряє, чи файл порожній."""
    return os.path.getsize(file_path) == 0

def get_file_content(file_path):
    """Повертає вміст файлу."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return "[Не вдалося прочитати файл: кодування не UTF-8]"
    except Exception as e:
        return f"[Не вдалося прочитати файл: {e}]"

def scan_directory(directory, extensions=None, exclude_dirs=None):
    """
    Сканує директорію рекурсивно, перевіряє файли з вказаними розширеннями.
    
    :param directory: Коренева директорія для сканування.
    :param extensions: Список розширень файлів для перевірки (наприклад, ['.py']).
    :param exclude_dirs: Список директорій для виключення зі сканування.
    """
    if extensions is None:
        extensions = ['.py']
    if exclude_dirs is None:
        exclude_dirs = ['venv', '__pycache__', 'tests']  # Додайте директорії, які потрібно виключити

    for root, dirs, files in os.walk(directory):
        # Виключаємо зазначені директорії
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                empty = is_empty(file_path)
                content = get_file_content(file_path)
                relative_path = os.path.relpath(file_path, directory)
                if empty:
                    logging.warning(f"Файл: {relative_path} є порожнім.")
                else:
                    logging.info(f"Файл: {relative_path}\nВміст:\n{content}\n")

def main():
    """
    Основна функція для запуску сканування.
    """
    if len(sys.argv) < 2:
        logging.error("Використання: python check_code.py <шлях_до_проекту> [розширення_файлів]")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    if not os.path.isdir(project_dir):
        logging.error(f"'{project_dir}' не є директорією.")
        sys.exit(1)
    
    extensions = ['.py']  # За замовчуванням перевіряються Python файли
    if len(sys.argv) > 2:
        extensions = sys.argv[2].split(',')

    scan_directory(project_dir, extensions=extensions)

if __name__ == "__main__":
    main()
