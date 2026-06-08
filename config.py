from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

WEATHER_API = os.getenv("WEATHER_API")

TEST_TOKEN = os.getenv("TEST_TOKEN")

CURRENCY_API = os.getenv("CURRENCY_API")

DATABASE_URL = os.getenv("DATABASE_URL")