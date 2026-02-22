"""
Daily Verse Scheduler
Create by : PINLON-YOUTH
"""

import random
import logging
from telegram.ext import ContextTypes
from database import get_verses, get_groups

logger = logging.getLogger(__name__)


async def send_daily_verse(context: ContextTypes.DEFAULT_TYPE):
    """Send a random verse to all registered groups."""
    verses = get_verses()
    if not verses:
        logger.info("No verses available for daily sending.")
        return

    verse = random.choice(verses)
    groups = get_groups()

    text = (
        "📖 *ယနေ့အတွက် ကျမ်းချက်*\n\n"
        f"{verse}\n\n"
        "🙏 _ဘုရားသခင်က သင့်ကို ကောင်းချီးပေးပါစေ!_"
    )

    for chat_id in groups:
        try:
            await context.bot.send_message(
                chat_id=int(chat_id),
                text=text,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Failed to send verse to {chat_id}: {e}")
