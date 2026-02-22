"""
Church Community Telegram Bot - Configuration
Create by : PINLON-YOUTH
"""

import os

# Bot Token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "8035830285:AAEaLoGVLAo1my_dlZEqNm5ihT7bMw0C8Wc")

# Admin User IDs (Telegram user IDs)
# Add admin Telegram user IDs here
ADMIN_IDS = [1812962224]
             # Data file paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Scheduled verse times (24-hour format, UTC)
MORNING_VERSE_HOUR = 6   # 6:00 AM
MORNING_VERSE_MINUTE = 0
NIGHT_VERSE_HOUR = 20    # 8:00 PM
NIGHT_VERSE_MINUTE = 0

# Quiz settings
DEFAULT_MESSAGE_COUNT_FOR_QUIZ = 5  # Default messages before quiz triggers

