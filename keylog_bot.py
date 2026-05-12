import asyncio
from config import TOKEN, IDS
import keyboard

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram import F

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Введите текст")

@dp.message(Command("space"))
async def space(message: Message):
    keyboard.write(" ")
    await message.answer("поставил пробел")


@dp.message()
async def write_text(message: Message):
    if message.from_user.id not in IDS:
        await message.answer(
            "Бот доступен только владельцу уебище 👑"
        )

        return

    if message.text:
        keyboard.write(message.text)
        await message.answer(f"Получилось, ты написал: {message.text}")
    else:
        await message.answer("пошел нахуй вместе со своим подсосуном")



async def main():
    await dp.start_polling(bot)

asyncio.run(main())