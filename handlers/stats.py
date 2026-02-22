"""
/stats command handler
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes
from database import get_users, get_groups
from utils.decorators import admin_only


@admin_only
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats - Show users and groups statistics."""
    users = get_users()
    groups = get_groups()

    text = "📊 *Bot Statistics*\n\n━━━━━━━━━━━━━━━━━━━\n\n"

    # Users
    text += f"👥 *Users: {len(users)}*\n\n"
    for uid, info in list(users.items())[:20]:  # Show max 20
        uname = info.get("username", "")
        fname = info.get("first_name", "Unknown")
        display = f"@{uname}" if uname else fname
        text += f"  • {display} (ID: {uid})\n"

    if len(users) > 20:
        text += f"  ... +{len(users) - 20} more\n"

    text += "\n"

    # Groups
    text += f"💬 *Groups: {len(groups)}*\n\n"
    for gid, info in groups.items():
        title = info.get("title", "Unknown")
        text += f"  • {title} (ID: {gid})\n"

    text += "\n━━━━━━━━━━━━━━━━━━━"

    await update.message.reply_text(text, parse_mode="Markdown")
