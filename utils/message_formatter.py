# utils/message_formatter.py

class MessageFormatter:
    @staticmethod
    def format_menu_title(title: str) -> str:
        """Форматує заголовок меню"""
        decorated_title = title.center(30, '═')
        return (
            f"<b>┏{decorated_title}┓</b>\n"
            f"<b>┗{'═' * len(decorated_title)}┛</b>"
        )
    
    @staticmethod
    def format_menu_content(text: str, items: list = None) -> str:
        """Форматує основний контент меню"""
        content = [f"<i>{text}</i>"]
        
        if items:
            content.append("\n<b>📌 Доступні опції:</b>")
            for item in items:
                content.append(f"• <code>{item}</code>")
                
        return "\n".join(content)

# В файлі handlers/base.py модифікуємо функцію send_menu_response:

from utils.message_formatter import MessageFormatter

async def send_menu_response(message: Message, description: str, detailed_text: str, reply_markup=None):
    """
    Надсилає відформатовану відповідь меню
    
    :param message: Об'єкт повідомлення
    :param description: Заголовок меню
    :param detailed_text: Детальний опис
    :param reply_markup: Клавіатура (опціонально)
    """
    # Форматуємо і надсилаємо заголовок
    title = MessageFormatter.format_menu_title(description)
    await message.answer(
        text=title,
        parse_mode="HTML"
    )
    
    # Форматуємо і надсилаємо контент
    content = MessageFormatter.format_menu_content(detailed_text)
    await message.answer(
        text=content,
        parse_mode="HTML",
        reply_markup=reply_markup
    )
