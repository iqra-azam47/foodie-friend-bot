"""All settings in one place. Change a value here and the whole app follows."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Reads the optional .env file (GOOGLE_API_KEY=...). A real environment variable wins over .env.
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
MENU_FILE = BASE_DIR / "data" / "menu.json"

# AI model. If Google removes it one day, run scripts/list_models.py and pick a new name.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
# Restaurant and bot
BOT_NAME = "Foodie Friend"
RESTAURANT_NAME = "Fire Flame"
CREATOR = "Iqra Azam"
LOCATION = "Model Town, Gujranwala"
DELIVERY_AREA = "Gujranwala"
DELIVERY_FEE = 200
DELIVERY_TIME = "40-50 minutes"

# Limits
MAX_MESSAGE_LENGTH = 500     # longest message a customer can send
MAX_ITEM_QUANTITY = 20       # most of one item in a single order
MAX_HISTORY_MESSAGES = 16    # 8 turns of chat is enough (the cart is kept separately)
MAX_STORED_CHARS = 600       # long replies are shortened when saved, so the cookie stays small
