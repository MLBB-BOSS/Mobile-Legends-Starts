def _load_messages(self) -> dict:
    try:
        # Оновіть шлях до файлу
        base_path = Path(__file__).parent.parent
        file_path = base_path / "config" / "messages" / "locales" / f"{self.locale}.json"

        with open(file_path, "r", encoding="utf-8") as file:
            messages = json.load(file)
            self.logger.info(f"Localization file loaded: {file_path}")
            return messages
    except FileNotFoundError:
        self.logger.error(f"Localization file not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        self.logger.error(f"Error decoding JSON from {file_path}: {e}")
        return {}
    except Exception as e:
        self.logger.error(f"Error loading messages: {e}")
        return {}
