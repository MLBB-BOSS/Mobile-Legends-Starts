import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def handle_gpt_query(prompt: str) -> str:
    """
    Виконує запит до OpenAI API і повертає відповідь.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Помилка запиту до OpenAI: {e}"
