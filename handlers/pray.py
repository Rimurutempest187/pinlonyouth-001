"""
/pray and /praylist command handlers
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes
from database import add_prayer, get_prayers


async def pray_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pray <text> - Submit a prayer request."""
    if not context.args:
        await update.message.reply_text(
            "🙏 ဆုတောင်းချက်ကို ရေးပေးပါ:\n\n"
            "ဥပမာ: /pray ကျန်းမာရေးအတွက် ဆုတောင်းပေးပါ"
        )
        return

    text = " ".join(context.args)
    user = update.effective_user
    username = f"@{user.username}" if user.username else user.first_name

    add_prayer(username, text)
    await update.message.reply_text(
        f"🙏 ဆုတောင်းချက် လက်ခံပြီးပါပြီ။\n\n"
        f"📝 \"{text}\"\n\n"
        f"💝 _သင့်အတွက် ဆုတောင်းပေးပါမည်။_",
        parse_mode="Markdown"
    )


async def praylist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /praylist - Show prayer requests list."""
    prayers = get_prayers()
    if not prayers:
        await update.message.reply_text("🙏 ဆုတောင်းချက် မရှိသေးပါ။")
        return

    text = "🙏 *ဆုတောင်းခံချက် စာရင်း*\n\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, prayer in enumerate(prayers, 1):
        text += f"📌 {i}. {prayer['username']}\n"
        text += f"   📝 {prayer['text']}\n"
        text += f"   🕐 {prayer['date']}\n\n"
    text += "━━━━━━━━━━━━━━━━━━━\n"
    text += "💝 _အတူတကွ ဆုတောင်းကြပါစို့!_"

    await update.message.reply_text(text, parse_mode="Markdown")
