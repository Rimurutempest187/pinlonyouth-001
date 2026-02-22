"""
Admin check decorator
Create by : PINLON-YOUTH
"""

from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS


def admin_only(func):
    """Decorator to restrict commands to admin users only."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("⛔ သင်သည် Admin မဟုတ်ပါ။ ဤ command ကို အသုံးပြုခွင့် မရှိပါ။")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
