from groq import Groq
import asyncio

from config import TOKEN, GROQ_API_KEY
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

bot = Bot(token=TOKEN)
dp = Dispatcher()

client = Groq(api_key=GROQ_API_KEY)

@dp.message(Command("ai"))
async def ai_chat(message: Message):

    text = message.text.replace("ai", "").strip() if message.text else None
    if not text:
        await message.answer("Напиши сообщение")
        return
    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": text
            }
        ]
    )

    ai_response = response.choices[0].message.content

    await message.answer(ai_response)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())