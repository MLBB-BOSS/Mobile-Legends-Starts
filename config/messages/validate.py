# File: config/messages/validate.py
from config.messages.base import Messages
import sys

def validate_messages():
    """Validate all message files"""
    for lang in ["uk"]:  # Додайте інші мови за потреби
        try:
            Messages.load_messages(lang)
            print(f"✓ {lang}.json is valid")
        except Exception as e:
            print(f"✗ Error in {lang}.json: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    validate_messages()
