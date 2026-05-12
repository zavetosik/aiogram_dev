from config import IDS
from aiogram.types import Message


def is_owner(message: Message):
    return message.from_user.id in IDS