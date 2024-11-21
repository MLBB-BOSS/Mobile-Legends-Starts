import os
import re

# Directory to scan
PROJECT_DIR = "./"  # Change to your project's root directory

# Incorrect and correct import paths
IMPORT_FIXES = {
    "from aiogram.filters import Text": "from aiogram.filters.text import Text",
}

def fix_imports(file_path):
    """Fix imports in the given file."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    modified = False
    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            for incorrect, correct in IMPORT_FIXES.items():
                if incorrect in line:
                    line = line.replace(incorrect, correct)
                    modified = True
            file.write(line)

    if modified:
        print(f"Fixed imports in: {file_path}")

def scan_and_fix(directory):
    """Recursively scan and fix Python files in the directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                fix_imports(file_path)

if __name__ == "__main__":
    print("Scanning for incorrect imports...")
    scan_and_fix(PROJECT_DIR)
    print("All imports have been updated.")
