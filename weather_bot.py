import json
import requests
from constants import WEATHER_URL, CURRENCIES
from config import TOKEN, TEST_TOKEN, WEATHER_API, CURRENCY_API
import asyncio
from twelvedata import TDClient
from twelvedata.exceptions import TwelveDataError

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

bot = Bot(token=TEST_TOKEN)
dp = Dispatcher()

td = TDClient(apikey=CURRENCY_API)

@dp.message(Command('weather'))
async def get_weather(message: Message):

    city = message.text.replace('/weather ', '').strip()

    url = (
        f"{WEATHER_URL}"
        f"?appid={WEATHER_API}"
        f"&q={city}"
        f"&units=metric"
        f"&lang=ua"
    )

    response = requests.get(url)

    data = response.json()

    print(data)

    status = data["cod"]


    if data["cod"] != 200:
        await message.answer(f"Ошибка: {data['message']}\nСтатус: {status}")
        return

    temp = data["main"]["temp"]

    base = data["base"]

    feels_like = data["main"]["feels_like"]

    humidity = data["main"]["humidity"]

    description = data["weather"][0]["description"]

    all_clouds = data["clouds"]["all"]

    country = data["sys"]["country"]


    await message.answer(
        f"""
🌤 Погода в {city} 
ℹ️ Информация с {base}

🌡 Температура: {temp}°C
🤔 Ощущается как: {feels_like}°C
💧 Влажность: {humidity}%
☁️ Погода: {description}
💨 Количество облаков: {all_clouds}
🌏 Страна: {country}
🧑‍💻 Статус: {status}
"""
    )

@dp.message(Command("currency"))
async def get_currency(message: Message):
    price = td.price(symbol="USD/UAH").as_json()["price"]
    price = round(float(price), 2)
    await message.answer(f"Курс доллара к гривне: {price}")



@dp.message(Command("check_currency"))
async def check_currency(message: Message):

    currency = message.text.replace("/check_currency ", "").strip()

    if currency not in CURRENCIES:
        await message.answer(
            "Такая валютная пара не поддерживается"
        )
        return
    data = td.price(symbol=currency).as_json()
    print(data["price"])
    price = round(float(data["price"]), 2)
    await message.answer(f"Курс равняется: {price}")

@dp.message(Command("currencies"))
async def get_currencies(message: Message):
    await message.answer(
        "Доступные валютные пары:\n\n" +
        "\n\n".join(CURRENCIES)
    )



async def main():
    await dp.start_polling(bot)

asyncio.run(main())