"""
/start command handler
Create by : PINLON-YOUTH
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import register_user, register_group


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Welcome message with user commands."""
    user = update.effective_user
    chat = update.effective_chat

    # Register user
    register_user(user.id, user.username, user.first_name)

    # Register group if in group chat
    if chat.type in ["group", "supergroup"]:
        register_group(chat.id, chat.title)

    welcome_text = (
        f"🙏 *မင်္ဂလာပါ {user.first_name}!*\n\n"
        "⛪ *Church Community Bot* မှ ကြိုဆိုပါတယ်။\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "📋 *User Commands*\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "📖 /about - အသင်းတော်အကြောင်း\n"
        "📞 /contact - ဆက်သွယ်ရန် ဖုန်းနံပါတ်များ\n"
        "✝️ /verse - ယနေ့အတွက် ကျမ်းချက်\n"
        "📅 /events - လာမည့် အစီအစဉ်များ\n"
        "🎂 /birthday - ယခုလ မွေးနေ့စာရင်း\n"
        "🙏 /pray <text> - ဆုတောင်းချက် ပေးပို့ရန်\n"
        "📝 /praylist - ဆုတောင်းချက်စာရင်း\n"
        "🧠 /quiz - Quiz ဖြေရန်\n"
        "🏆 /tops - Quiz အမှတ် Ranking\n"
        "📩 /report <text> - အကြောင်းအရာ တင်ပြရန်\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "🤖 *Create by : PINLON-YOUTH*"
    )

    await update.message.reply_text(welcome_text, parse_mode="Markdown")
