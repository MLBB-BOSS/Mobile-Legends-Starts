# tests/test_localization.py

import unittest
from utils.localization import loc

class TestLocalizationManager(unittest.TestCase):
    def test_get_existing_message(self):
        message = loc.get_message("messages.welcome")
        self.assertEqual(message, "Вітаємо у головному меню! Оберіть необхідну опцію нижче.")

    def test_get_missing_message(self):
        message = loc.get_message("messages.non_existent_key")
        self.assertEqual(message, "Сталася непередбачена помилка.")

    def test_get_hero_info_existing(self):
        hero_info = loc.get_hero_info("Akai")
        self.assertEqual(hero_info, "Інформація про героя Akai.")

    def test_get_hero_info_missing(self):
        hero_info = loc.get_hero_info("NonExistentHero")
        self.assertEqual(hero_info, "Вибраного героя не знайдено. Будь ласка, спробуйте інший вибір.")

if __name__ == '__main__':
    unittest.main()
