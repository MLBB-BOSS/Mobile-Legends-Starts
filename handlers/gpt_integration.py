# gpt_integration.py

import openai
import asyncio
from config import settings

def sync_get_gpt_response(question: str) -> str:
    openai.api_key = settings.OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"Error in GPT response: {e}")
        return "Виникла помилка при обробці вашого запитання."

async def get_gpt_response(question: str) -> str:
    return await asyncio.to_thread(sync_get_gpt_response, question)
