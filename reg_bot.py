from utils import is_owner
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
async def do_start(message: Message):
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
        if username:
            await message.answer(f"@{username} регистрация прошла успешно")
        else:
            await message.answer(f"{name} регистрация прошла успешно")

        cursor.execute("""
        UPDATE users
        SET username = ?, name = ?
        WHERE telegram_id = ?""", (username, name, user_id))

        conn.commit()

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


@dp.message(Command("profile"))
async def get_profile(message: Message):

    user_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name

    cursor.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user:
        await message.answer(f"id: {user_id}\nusername: @{username}\nname: {name}")

    else:
        await message.answer("Напишите команду /start для регистрации")

@dp.message(Command("users"))
async def get_users(message: Message):
    if not is_owner(message):
        await message.answer("У тебя нету прав!")
        return
    cursor.execute("""
    SELECT COUNT(*)
    FROM users
    """)

    count = cursor.fetchone()[0]

    await message.answer(f"В боте сейчас {count} зарегистрированных пользователей")

@dp.message(Command("all_users"))
async def get_all_users(message: Message):
    if not is_owner(message):
        await message.answer("У тебя нету прав!")
        return
    cursor.execute("""
    SELECT id,telegram_id, username, name
    FROM users
    """)
    users = cursor.fetchall()

    text = ""

    for user in users:
        text += (
            f" ID DB: {user[0]}\n"
            f" ID: {user[1]}\n"
            f" Username: {user[2]}\n"
            f" Name: {user[3]}\n\n"
        )

    await message.answer(text)

@dp.message(Command("admin"))
async def get_admin_info(message: Message):
    if not is_owner(message):
        await message.answer("У тебя нету прав!")
        return
    await message.answer("/users - показывает число зарегистрированных пользователей\n"
                         "/all_users - показывает данные всех пользователей")







async def main():
    await dp.start_polling(bot)


asyncio.run(main())