import os
import re

# Specify the root directory of your project
PROJECT_DIR = "./"  # Update this if running outside the project directory

# Common imports to check for aiogram 3.14 compatibility
KNOWN_IMPORTS = {
    "aiogram.filters.Text": "from aiogram.filters.text import Text",
    "aiogram.filters.Command": "from aiogram.filters.command import Command",
    # Add other known aiogram imports as necessary
}

# Regular expression to match import statements
IMPORT_REGEX = re.compile(r"from\s+aiogram\.(.*?)\s+import\s+(.*?)")

def scan_files(directory):
    """Recursively scan Python files in the directory."""
    errors = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.readlines()
                    for idx, line in enumerate(content):
                        match = IMPORT_REGEX.search(line)
                        if match:
                            full_import = f"aiogram.{match.group(1)}.{match.group(2)}"
                            if full_import not in KNOWN_IMPORTS:
                                errors.append({
                                    "file": filepath,
                                    "line_number": idx + 1,
                                    "invalid_import": full_import,
                                    "suggestion": KNOWN_IMPORTS.get(full_import, "No suggestion available")
                                })
    return errors

def print_report(errors):
    """Print a report of errors found."""
    if not errors:
        print("No compatibility issues found!")
        return

    print("Compatibility Issues Found:\n")
    for error in errors:
        print(f"File: {error['file']}")
        print(f"Line {error['line_number']}: {error['invalid_import']}")
        print(f"Suggestion: {error['suggestion']}\n")
    print("Please fix these issues and re-run the script.")

if __name__ == "__main__":
    print("Scanning project for aiogram 3.14 compatibility issues...")
    compatibility_issues = scan_files(PROJECT_DIR)
    print_report(compatibility_issues)
