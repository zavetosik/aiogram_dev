import csv
from datetime import datetime
from utils import is_admin, is_owner, is_user, write_logs, write_admin_logs
from config import TOKEN, CHANNEL_ID
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS owners (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,
    text TEXT,
    status TEXT

)
""")

conn.commit()

@dp.message(CommandStart())
async def do_start(message: Message):

    user_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name

    cursor.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user:

        await message.answer("Сделать пост:\n/send текст")

        cursor.execute("""
        UPDATE users
        SET username = ?, name = ?
        WHERE telegram_id = ?
        """, (username, name, user_id))

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

        if username:
            await message.answer(
                f"@{username} регистрация прошла успешно"
            )

        else:
            await message.answer(
                f"{name} регистрация прошла успешно"
            )


@dp.message(Command("profile"))
async def show_profile(message: Message):

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
    if not is_admin(message):
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
    if not is_admin(message):
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
            f"ID DB: {user[0]}\n"
            f"ID: {user[1]}\n"
            f"Username: @{user[2] or '-'}\n"
            f"Name: {user[3]}\n\n"
        )

    await message.answer(text)





@dp.message(Command("add_admin"))
async def add_admin(message: Message):
    if not is_owner(message):
        await message.answer("У тебя нету прав!")
        return
    admin_id = message.text.replace("/add_admin", "").strip()
    if not admin_id:
        await message.answer("Укажи ID пользователя")
        return
    admin_id = int(admin_id)
    cursor.execute(
        "SELECT * FROM admins WHERE telegram_id = ?",
        (admin_id,)
    )
    admin = cursor.fetchone()
    if admin:
        await message.answer("Этот пользователь уже админ")
        return
    else:
        cursor.execute(
            "INSERT INTO admins (telegram_id) VALUES (?)",
            (admin_id,)
        )
        await message.answer("Админ успешно добавлен")
        write_admin_logs(
            "add_admin",
            message.from_user.id,
            admin_id
        )
    conn.commit()

@dp.message(Command("remove_admin"))
async def remove_admin(message: Message):
    if not is_owner(message):
        await message.answer("У тебя нету прав!")
        return
    admin_id = message.text.replace("/remove_admin", "").strip()
    if not admin_id:
        await message.answer("Укажи ID админа")
        return
    admin_id = int(admin_id)
    cursor.execute(
        "SELECT * FROM admins WHERE telegram_id = ?",
        (admin_id,)
    )
    admin = cursor.fetchone()
    if admin:
        cursor.execute(
            "DELETE FROM admins WHERE telegram_id = ?",
            (admin_id,)
        )
        await message.answer("Админ успешно удален")
        write_admin_logs(
            "remove_admin",
            message.from_user.id,
            admin_id
        )
    else:
        await message.answer("Такой админ не найден")
    conn.commit()

@dp.message(Command("send"))
@dp.message(F.photo)
async def send_confession(message: Message):

    if not is_user(message):
        await message.answer("Для начала напиши /start")
        return

    cursor.execute(
        "SELECT telegram_id FROM admins"
    )

    admins = cursor.fetchall()

    # PHOTO
    if message.photo:

        photo = message.photo[-1].file_id
        text = message.caption.replace("/send", "").strip() if message.caption else None

        cursor.execute(
            """
            INSERT INTO posts (user_id, text, status, photo)
            VALUES (?, ?, ?, ?)
            """,
            (message.from_user.id, text, "pending", photo)
        )

        conn.commit()

        post_id = cursor.lastrowid

        caption = f"""
    📩 Новый пост

    POST ID: {post_id}

    Username: @{message.from_user.username}
    ID: {message.from_user.id}
    """

        if text:
            caption += f"\n\nText:\n{text}"

        for admin in admins:
            await bot.send_photo(
                admin[0],
                photo=photo,
                caption=caption
            )

        await message.answer("Пост отправлен на модерацию")

    # TEXT
    else:

        text = message.text.replace("/send", "").strip()

        if not text:
            await message.answer("Напишите текст для поста")
            return

        cursor.execute(
            """
            INSERT INTO posts (user_id, text, status, photo)
            VALUES (?, ?, ?, ?)
            """,
            (message.from_user.id, text, "pending", None)
        )

        conn.commit()

        post_id = cursor.lastrowid

        for admin in admins:
            await bot.send_message(
                admin[0],
                f"""
    📩 Новый пост

    POST ID: {post_id}

    Username: @{message.from_user.username}
    ID: {message.from_user.id}

    Text:
    {text}
    """
            )

        await message.answer("Пост отправлен на модерацию")




@dp.message(Command("accept"))
async def accept(message: Message):

    if not is_admin(message):
        await message.answer("У тебя нету прав!")
        return

    post_id = message.text.replace("/accept", "").strip()

    if not post_id:
        await message.answer("Введите ID поста")
        return

    post_id = int(post_id)

    cursor.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    )

    post = cursor.fetchone()

    if not post:
        await message.answer("Пост не найден")
        return

    if post[3] == "accepted":
        await message.answer("Пост уже опубликован")
        return

    # PHOTO
    if post[4]:

        await bot.send_photo(
            CHANNEL_ID,
            photo=post[4],
            caption=post[2] if post[2] else None
        )

    # TEXT
    else:

        await bot.send_message(
            CHANNEL_ID,
            post[2]
        )

    cursor.execute(
        """
        UPDATE posts
        SET status = ?
        WHERE id = ?
        """,
        ("accepted", post_id)
    )

    conn.commit()

    await bot.send_message(
        post[1],
        f"""
✅ Ваш пост был одобрен

💌 Text:
{post[2] if post[2] else "Фото без текста"}
"""
    )

    await message.answer("Пост опубликован")


@dp.message(Command("reject"))
async def reject(message: Message):

    if not is_admin(message):
        await message.answer("У тебя нету прав!")
        return

    post_id = message.text.replace("/reject", "").strip()

    if not post_id:
        await message.answer("Введите ID поста")
        return

    post_id = int(post_id)

    cursor.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    )

    post = cursor.fetchone()

    if not post:
        await message.answer("Пост не найден")
        return

    if post[3] == "rejected":
        await message.answer("Пост уже отклонен")
        return

    cursor.execute(
        """
        UPDATE posts
        SET status = ?
        WHERE id = ?
        """,
        ("rejected", post_id)
    )

    conn.commit()

    await bot.send_message(
        post[1],
        f"""
❌ Ваш пост был отклонен

💌 Text:
{post[2] if post[2] else "Фото без текста"}
"""
    )

    await message.answer("Пост отклонен")




@dp.message(Command("broadcast"))
async def make_broadcast(message: Message):
    if not is_admin(message):
        await message.answer("У тебя нету прав!")
        return
    cursor.execute("""
    SELECT telegram_id
    FROM users""")
    users = cursor.fetchall()
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        await message.answer("Напиши текст для рассылки")
    else:
        for user in users:
            await bot.send_message(user[0], text)
        write_logs(
        message.from_user.id,
        message.from_user.username,
        text
    )




@dp.message(Command("admin"))
async def get_admin_info(message: Message):
    if not is_admin(message):
        await message.answer("У тебя нету прав!")
        return
    await message.answer(
    "/users - показывает число зарегистрированных пользователей\n"
    "/all_users - показывает данные всех пользователей\n"
    "/broadcast - делает рассылку сообщения"
    )

@dp.message(Command("all_admins"))
async def get_all_admins(message: Message):
    if not is_admin(message):
        await message.answer("У тебя нету прав!")
        return
    cursor.execute("""
    SELECT id, telegram_id
    FROM admins
    """)
    admins = cursor.fetchall()

    text = ""

    for admin in admins:
        text += (
            f"ID DB: {admin[0]}\n"
            f"ID: {admin[1]}\n\n"
        )

    await message.answer(text)



async def main():
    await dp.start_polling(bot)


asyncio.run(main())

