import os
import shutil
import json
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Визначте основні шляхи
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def consolidate_keyboards():
    keyboards_dir = os.path.join(BASE_DIR, 'keyboards')
    consolidated_file = os.path.join(keyboards_dir, 'keyboards.py')

    if os.path.exists(consolidated_file):
        os.remove(consolidated_file)
        logging.info(f"Deleted existing {consolidated_file}")

    with open(consolidated_file, 'w') as outfile:
        outfile.write("# Consolidated keyboards\n\n")
        for filename in os.listdir(keyboards_dir):
            if filename.endswith('.py') and filename != 'keyboards.py' and filename != '__init__.py':
                filepath = os.path.join(keyboards_dir, filename)
                with open(filepath, 'r') as infile:
                    content = infile.read()
                    outfile.write(f"# From {filename}\n")
                    outfile.write(content + "\n\n")
                os.remove(filepath)
                logging.info(f"Consolidated {filename} into keyboards.py")

def consolidate_handlers():
    handlers_dir = os.path.join(BASE_DIR, 'handlers')
    consolidated_file = os.path.join(handlers_dir, 'handlers.py')

    if os.path.exists(consolidated_file):
        os.remove(consolidated_file)
        logging.info(f"Deleted existing {consolidated_file}")

    with open(consolidated_file, 'w') as outfile:
        outfile.write("# Consolidated handlers\n\n")
        for filename in os.listdir(handlers_dir):
            if filename.endswith('.py') and filename not in ['handlers.py', '__init__.py']:
                filepath = os.path.join(handlers_dir, filename)
                with open(filepath, 'r') as infile:
                    content = infile.read()
                    outfile.write(f"# From {filename}\n")
                    outfile.write(content + "\n\n")
                os.remove(filepath)
                logging.info(f"Consolidated {filename} into handlers.py")

def consolidate_characters():
    heroes_dir = os.path.join(BASE_DIR, 'heroes')
    characters_file = os.path.join(heroes_dir, 'characters.json')
    consolidated_data = {}

    if os.path.exists(characters_file):
        with open(characters_file, 'r') as cf:
            try:
                consolidated_data = json.load(cf)
            except json.JSONDecodeError:
                logging.error(f"Error decoding JSON from {characters_file}")
                consolidated_data = {}

    for class_name in os.listdir(heroes_dir):
        class_dir = os.path.join(heroes_dir, class_name)
        if os.path.isdir(class_dir) and class_name in ['Assassin', 'Fighter', 'Mage', 'Marksman', 'Support', 'Tank']:
            for file in os.listdir(class_dir):
                if file.endswith('.json'):
                    filepath = os.path.join(class_dir, file)
                    with open(filepath, 'r') as f:
                        try:
                            character_data = json.load(f)
                            character_name = character_data.get('name')
                            if character_name:
                                consolidated_data[class_name] = consolidated_data.get(class_name, {})
                                consolidated_data[class_name][character_name] = character_data
                                os.remove(filepath)
                                logging.info(f"Added {character_name} to {characters_file}")
                            else:
                                logging.warning(f"No 'name' field in {filepath}")
                        except json.JSONDecodeError:
                            logging.error(f"Error decoding JSON from {filepath}")
    with open(characters_file, 'w') as cf:
        json.dump(consolidated_data, cf, indent=4)
        logging.info(f"Consolidated all characters into {characters_file}")

def main():
    consolidate_keyboards()
    consolidate_handlers()
    consolidate_characters()
    # Додайте інші функції консолідації за потребою

if __name__ == "__main__":
    main()
