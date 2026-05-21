from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")