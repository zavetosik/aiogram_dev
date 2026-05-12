from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
IDS = list(
    map(int, os.getenv("IDS").split(","))
)