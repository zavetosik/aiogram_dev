from config import TOKEN, GROQ_API_KEY
# from aiogram import Bot, Dispatcher
# from aiogram.types import Message
# from aiogram.filters import CommandStart, Command
#
#
# from groq import Groq
#
# client = Groq(api_key=GROQ_API_KEY)
#
#


import asyncio
from groq import AsyncGroq


async def main():
    client = AsyncGroq(api_key=GROQ_API_KEY)  # Ключ подтянется из окружения

    # 1. Просим пользователя ввести текст с клавиатуры
    user_question = input("Напиши свой вопрос для нейросети: ")

    # 2. Подставляем ПЕРЕМЕННУЮ user_question вместо жестко заданного текста
    dialog = [
        {"role": "system", "content": "Ты полезный ассистент."},
        {"role": "user", "content": user_question}
    ]

    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=dialog
    )

    print("Ответ Groq:", response.choices[0].message.content)


asyncio.run(main())