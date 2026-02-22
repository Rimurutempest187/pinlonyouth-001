"""
/edit command handler - Show admin commands
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only


@admin_only
async def edit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edit command - Show admin commands list."""
    admin_text = (
        "🔐 *Admin Commands*\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "✏️ /edabout - အသင်းတော်အကြောင်း ပြင်ဆင်ရန်\n"
        "✏️ /edcontact - ဆက်သွယ်ရန် ပြင်ဆင်ရန်\n"
        "✏️ /edverse - ကျမ်းချက် ထည့်ရန်\n"
        "✏️ /edevents - အစီအစဉ် ပြင်ဆင်ရန်\n"
        "✏️ /edbirthday - မွေးနေ့စာရင်း ပြင်ဆင်ရန်\n"
        "✏️ /edquiz - Quiz ထည့်ရန်\n"
        "⚙️ /set <number> - Quiz အတွက် message count သတ်မှတ်ရန်\n"
        "📢 /broadcast - Group များသို့ သတင်းပို့ရန်\n"
        "📊 /stats - Users/Groups စာရင်း\n"
        "💾 /backup - Data Backup\n"
        "♻️ /restore - Data ပြန်ယူရန်\n"
        "🗑️ /allclear - Data အားလုံး ဖျက်ရန်\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "🤖 *Create by : PINLON-YOUTH*"
    )

    await update.message.reply_text(admin_text, parse_mode="Markdown")
