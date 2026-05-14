from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
IDS = list(
    map(int, os.getenv("IDS").split(","))
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")