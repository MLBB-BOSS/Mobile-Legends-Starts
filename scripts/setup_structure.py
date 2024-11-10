import os
import json

# Список персонажів, розподілених по класах
heroes_structure = {
    "Fighter": [
        "Balmond", "Alucard", "Bane", "Zilong", "Freya", "Alpha", "Ruby", "Roger",
        "Gatotkaca", "Grock", "Jawhead", "Martis", "Aldous", "Minsitthar",
        "Terizla", "X.Borg", "Dyrroth", "Masha", "Silvanna", "Yu Zhong",
        "Khaleed", "Barats", "Paquito", "Phoveus", "Aulus", "Fiddrin",
        "Arlott", "Cici", "Kaja", "Leomord", "Thamuz", "Badang", "Guinivere"
    ],
    "Tank": [
        "Alice", "Tigreal", "Akai", "Franco", "Minotaur", "Lolita", "Gatotkaca",
        "Grock", "Hylos", "Uranus", "Belerick", "Khufra", "Esmeralda",
        "Terizla", "Baxia", "Masha", "Atlas", "Barats", "Edith", "Fredrinn",
        "Johnson", "Hilda", "Carmilla", "Gloo", "Chip"
    ],
    "Assassin": [
        "Saber", "Alucard", "Zilong", "Fanny", "Natalia", "Yi Sun-shin",
        "Lancelot", "Helcurt", "Lesley", "Selena", "Mathilda", "Paquito",
        "Yin", "Arlott", "Harley", "Suyou"
    ],
    "Marksman": [
        "Popol and Kupa", "Brody", "Beatrix", "Natan", "Melissa", "Ixia",
        "Hanabi", "Claude", "Kimmy", "Granger", "Wanwan", "Miya",
        "Bruno", "Clint", "Layla", "Yi Sun-shin", "Moskov", "Roger",
        "Karrie", "Irithel", "Lesley"
    ],
    "Mage": [
        "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier",
        "Valentina", "Harley", "Kagura", "Zhask", "Eudora", "Luo-Yi",
        "Yve", "Pharsa", "Cyclops", "Chang'e", "Lylia", "Harith",
        "Valir", "Aurora", "Nana", "Vexana", "Cecilion", "Gord",
        "Odette", "Helcurt"
    ],
    "Support": [
        "Rafaela", "Minotaur", "Lolita", "Estes", "Angela", "Faramis",
        "Mathilda", "Florin", "Johnson"
    ]
}

# Функція для очищення та форматування імені героя для використання в назві файлу
def format_hero_name(hero_name):
    # Замінюємо символи, що можуть бути проблемними в іменах файлів
    formatted_name = hero_name.lower().replace(" ", "_").replace("-", "_").replace("&", "_").replace(".", "_").replace("'", "").replace("/", "_")
    return formatted_name

# Функція для створення структури проєкту
def create_structure():
    base_path = os.path.join("data", "heroes")
    for hero_class, heroes in heroes_structure.items():
        class_path = os.path.join(base_path, hero_class)
        os.makedirs(class_path, exist_ok=True)
        print(f"Створено папку класу: {class_path}")
        for hero in heroes:
            hero_folder = os.path.join(class_path, hero)
            os.makedirs(hero_folder, exist_ok=True)
            print(f"  Створено папку героя: {hero_folder}")
            # Створення JSON-файлів для кожного героя
            create_hero_files(hero_folder, hero)

# Функція для створення JSON-файлів з шаблонним вмістом
def create_hero_files(path, hero_name):
    formatted_name = format_hero_name(hero_name)
    files = {
        f"{formatted_name}_description.json": {
            "name": hero_name,
            "class": get_hero_class(hero_name),
            "role": "",  # Заповніть роль за потребою
            "lore": f"Лор героя {hero_name}."
        },
        f"{formatted_name}_build.json": {
            "optimal_build": [],
            "counter_build": []
        },
        f"{formatted_name}_strategy.json": {
            "tips": [],
            "strategies": []
        }
    }
    
    for filename, content in files.items():
        file_path = os.path.join(path, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=4)
            print(f"    Створено файл: {file_path}")
        else:
            print(f"    Файл вже існує: {file_path}")

# Допоміжна функція для визначення класу героя за іменем
def get_hero_class(hero_name):
    for hero_class, heroes in heroes_structure.items():
        if hero_name in heroes:
            return hero_class
    return "Unknown"

# Функція для створення всіх зв'язків та інтеграцій
def setup_integrations():
    """
    Ця функція може бути використана для додавання зв'язків між створеними файлами та існуючим кодом.
    Наприклад, оновлення data_loader.py для завантаження даних героїв.
    """
    data_loader_path = os.path.join("utils", "data_loader.py")
    if not os.path.exists(data_loader_path):
        with open(data_loader_path, 'w', encoding='utf-8') as f:
            f.write("""import os
import json

def load_hero_data(hero_class, hero_name, data_type):
    """
    Завантажує JSON-файл з даними про героя.
    
    Параметри:
        - hero_class (str): Назва класу героя (Fighter, Tank, Assassin, Marksman, Mage, Support).
        - hero_name (str): Ім'я героя.
        - data_type (str): Тип даних ('description', 'build', 'strategy').
        
    Повертає:
        - dict: Дані з JSON-файлу.
    """
    formatted_name = hero_name.lower().replace(" ", "_").replace("-", "_").replace("&", "_").replace(".", "_").replace("'", "").replace("/", "_")
    file_path = os.path.join("data", "heroes", hero_class, hero_name, f"{formatted_name}_{data_type}.json")
    
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено")
        return {}
""")
        print(f"Створено файл: {data_loader_path}")
    else:
        print(f"Файл вже існує: {data_loader_path}")

    # Додаткові інтеграції можна додати тут

def main():
    create_structure()
    setup_integrations()
    print("Структура проєкту та інтеграції створені успішно.")

if __name__ == "__main__":
    main()
