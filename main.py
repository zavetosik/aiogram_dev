import asyncio
from config import TOKEN

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram import F
from aiogram.types import ReplyKeyboardRemove


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Бот работает")

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Обратись к @rrmagedonnn чтобы получить ответ на свой вопрос ")

@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")





async def main():
    await dp.start_polling(bot)

asyncio.run(main())