from CONSTANTS import APPS
import subprocess
import webbrowser
from mss import mss
from aiogram.types import FSInputFile
import asyncio
from config import TOKEN, IDS
import keyboard
from utils import is_admin

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram import F

bot = Bot(token=TOKEN)
dp = Dispatcher()



@dp.message(CommandStart())
async def start(message: Message):
    if not is_admin(message):
        await message.answer("ты ниче не можеш")
        return
    await message.answer("Введите текст")

@dp.message(Command("youtube"))
async def open_youtube(message: Message):
    if not is_admin(message):
        await message.answer("ты ниче не можеш")
        return
    webbrowser.open("https://www.youtube.com/")
    await message.answer("открыл ютуб")





@dp.message(Command("screen"))
async def screenshot(message: Message):

    if not is_admin(message):
        await message.answer("ты ниче не можеш")
        return

    path = "screen.png"

    with mss() as sct:
        sct.shot(output=path)

    photo = FSInputFile(path)

    await message.answer_photo(photo, caption="на скрин уебок")



@dp.message(Command("space"))
async def space(message: Message):
    if not is_admin(message):
        await message.answer("ты ниче не можеш")
        return
    keyboard.write(" ")
    await message.answer("поставил пробел")


@dp.message()
async def write_text(message: Message):
    if not is_admin(message):
        await message.answer("ты ниче не можеш")

        return

    text = message.text.lower()

    if text in APPS:
        subprocess.Popen(APPS[text])

        await message.answer(f"открыл {text}")

        return

    if message.text:

        if message.text.lower() == "enter":
            keyboard.press_and_release("enter")
            await message.answer("нажал enter")
            return

        if message.text.lower() == "win":
            keyboard.press_and_release("win")
            await message.answer("нажал win")
            return


        keyboard.write(message.text)

        await message.answer(f"Получилось, ты написал: {message.text}")
        print(message.text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)

asyncio.run(main())