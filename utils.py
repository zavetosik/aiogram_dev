import csv
from datetime import datetime
from aiogram.types import Message
import sqlite3


def is_admin(message: Message):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute(
        "SELECT * FROM admins WHERE telegram_id = ?",
        (user_id,)
    )
    admin = cursor.fetchone()
    if admin:
        return True
    else:
        return False

def is_owner(message: Message):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute(
        "SELECT * FROM owners WHERE telegram_id = ?",
        (user_id,)
    )
    owner = cursor.fetchone()
    if owner:
        return True
    else:
        return False


def write_logs(admin_id, username, text):
    with open("logs.csv", "a", encoding="utf-8") as file:
        log = f"{datetime.now()};{admin_id};{username};{text}\n"
        file.write(log)