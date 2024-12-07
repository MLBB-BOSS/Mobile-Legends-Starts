# gpt_integration.py

import openai
import config

from config import settings
openai.api_key = settings.OPENAI_API_KEY

async def get_gpt_response(question: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ви допомагаєте користувачам Mobile Legends: Bang Bang."},
                {"role": "user", "content": question},
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        # Логування помилки
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Помилка при отриманні відповіді від GPT: {e}")
        return "Вибачте, виникла помилка при обробці вашого запитання."
