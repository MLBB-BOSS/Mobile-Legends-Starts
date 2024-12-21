# escape_texts.py

import re

# Словник замін
replacements = {
    '╔': '\\u2554',
    '╗': '\\u2557',
    '╚': '\\u255A',
    '╝': '\\u255D',
    '╠': '\\u2560',
    '╣': '\\u2563',
    '═': '\\u2550',
    '║': '\\u2551',
    '❗': '\\u2757',
    '⚠️': '\\u26A0\\uFE0F',
    '🔄': '\\U0001F504',
    '🔘': '\\U0001F518',
    '🖱️': '\\U0001F5B1\\uFE0F',
    '🏆': '\\U0001F3C6',
    '📞': '\\U0001F4DE',
    '✅': '\\u2705',
    '💖': '\\U0001F496',
    '💬': '\\U0001F4AC',
    '🧭': '\\U0001F9ED',
    '👋': '\\U0001F44B',
    '🤖': '\\U0001F916',
    '📘': '\\U0001F4D8',
    '🤝': '\\U0001F91D',
    '📄': '\\U0001F4C4',
    '🛠️': '\\U0001F6E0\\uFE0F',
    '🥷': '\\U0001F977',
    '⚔️': '\\u2694\\uFE0F',
    '❤️': '\\u2764\\uFE0F',
    '🗡️': '\\U0001F5E1\\uFE0F',
    '🆕': '\\U0001F195',
    '🌟': '\\U0001F31F',
    '📈': '\\U0001F4CA',
    '🏅': '\\U0001F3C6',
    '📍': '\\U0001F4CD',
    '📝': '\\U0001F4DD',
    '🐛': '\\U0001F41B',
    '❓': '\\u2753',
    'ℹ️': '\\u2139\\uFE0F',
    '✏️': '\\u270F\\uFE0F',
    '➡️': '\\U000027A1\\uFE0F',
    '🔹': '\\U0001F539',
    '🔧': '\\U0001F527',
    '🔔': '\\U0001F514',
    '🎯': '\\U0001F3AF',
    '📅': '\\U0001F4C5',
    '🗳️': '\\U0001F5F3\\uFE0F',
    '📊': '\\U0001F4CA',
    '🏟️': '\\U0001F3DF\\uFE0F',
    '🎉': '\\U0001F389',
    '📰': '\\U0001F4F0',
    '🚀': '\\U0001F680',
    '🎖️': '\\U0001F396\\uFE0F',
    '💡': '\\U0001F4A1',
    # Додайте інші символи за необхідності
}

def escape_special_characters(text):
    return ''.join(replacements.get(char, char) for char in text)

def process_texts_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Функція для екранування всередині потрійних лапок
        def replace_in_triple_quotes(match):
            original = match.group(0)
            # Витягуємо текст між потрійними лапками
            inner_text = match.group(1)
            # Екрануємо спеціальні символи
            escaped_text = escape_special_characters(inner_text)
            return f'"""{escaped_text}"""'
        
        # Замінюємо текст у потрійних лапках
        escaped_content = re.sub(r'"""(.*?)"""', replace_in_triple_quotes, content, flags=re.DOTALL)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(escaped_content)
        
        print(f"Файл {input_file} успішно екрановано та збережено як {output_file}!")
    
    except FileNotFoundError:
        print(f"Файл {input_file} не знайдено. Перевірте шлях до файлу.")
    except Exception as e:
        print(f"Виникла помилка: {e}")

if __name__ == "__main__":
    input_filename = 'texts.py'
    output_filename = 'texts_escaped.py'
    process_texts_file(input_filename, output_filename)
