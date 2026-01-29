from __future__ import annotations
import os

# --- Data Persistence Settings ---
DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "user_data.json")

# --- Economy Settings ---
DAILY_REWARD_AMOUNT = 1000
DAILY_COOLDOWN_SECONDS = 24 * 60 * 60 # 24 hours

# --- Game Settings ---
MIN_BET = 100
MAX_BET = 100000

# Slots configuration (Pillow related)
SLOTS_IMAGE_WIDTH = 500
SLOTS_IMAGE_HEIGHT = 200
SLOTS_SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]