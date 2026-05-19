import csv
from datetime import datetime
from config import IDS
from aiogram.types import Message


def is_admin(message: Message):
    return message.from_user.id in IDS

def write_logs(admin_id, username, text):
    with open("logs.csv", "a", encoding="utf-8") as file:
        log = f"{datetime.now()};{admin_id};{username};{text}\n"
        file.write(log)