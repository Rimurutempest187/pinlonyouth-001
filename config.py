import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = [int(x.strip()) for x in os.getenv('ADMINS','').split(',') if x.strip()]
DB_FILE = os.getenv('DATABASE_FILE','data/churchbot.db')

# Bot-visible footer
FOOTER = "\n\nCreate by : PINLON-YOUTH"

# Default group setting for messages-to-trigger-quiz
DEFAULT_MESSAGES_TO_TRIGGER_QUIZ = 50
