from config import TOKEN
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message


bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    username TEXT,
    name TEXT
)
""")

conn.commit()


@dp.message(CommandStart())
async def start(message: Message):
    print(message.text)

    user_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name

    cursor.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user:
        await message.answer(f"@{username} ты уже зарегистрирован в нашем боте")

    else:
        cursor.execute(
            """
            INSERT INTO users (telegram_id, username, name)
            VALUES (?, ?, ?)
            """,
            (user_id, username, name)
        )

        conn.commit()

        await message.answer(f"@{username} регистрация прошла успешно")


# @dp.message(Command("profile"))
# async def get_profile(message: Message):







async def main():
    await dp.start_polling(bot)


asyncio.run(main())