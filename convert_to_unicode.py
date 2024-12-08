import re

def escape_unicode(s):
    return ''.join(['\\u{:04x}'.format(ord(c)) if ord(c) > 127 else c for c in s])

input_file = 'texts.py'
output_file = 'texts_unicode.py'

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Регулярний вираз для пошуку рядкових констант
# Підтримує потрійні лапки (''' або """) та одиночні лапки (' або ")
pattern = re.compile(r'("""(.*?)""")|("([^"\\]*(\\.[^"\\]*)*)")|(\'([^\'\\]*(\\.[^\'\\]*)*)\')', re.DOTALL)

def replacer(match):
    if match.group(2):
        original = match.group(2)
        escaped = escape_unicode(original)
        return f'"""{escaped}"""'
    elif match.group(4):
        original = match.group(4)
        escaped = escape_unicode(original)
        return f'"{escaped}"'
    elif match.group(7):
        original = match.group(7)
        escaped = escape_unicode(original)
        return f"'{escaped}'"
    else:
        return match.group(0)

escaped_content = pattern.sub(replacer, content)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(escaped_content)

print(f"Перетворення завершено. Новий файл збережено як {output_file}.")
