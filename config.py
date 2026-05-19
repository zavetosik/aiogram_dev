from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")