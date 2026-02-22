"""
/birthday and /edbirthday command handlers
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from database import get_birthdays, set_birthdays
from utils.decorators import admin_only

WAITING_BIRTHDAYS = 0


async def birthday_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /birthday - Show this month's birthdays."""
    birthdays = get_birthdays()
    if not birthdays:
        await update.message.reply_text("🎂 ယခုလအတွင်း မွေးနေ့စာရင်း မရှိသေးပါ။")
        return

    text = "🎂 *ယခုလအတွင်း မွေးနေ့ကျရောက်သူများ*\n\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, bday in enumerate(birthdays, 1):
        text += f"🎉 {i}. {bday}\n"
    text += "\n━━━━━━━━━━━━━━━━━━━\n"
    text += "🎊 _မွေးနေ့မှာ ပျော်ရွှင်ကြပါစေ!_"

    await update.message.reply_text(text, parse_mode="Markdown")


@admin_only
async def edbirthday_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edbirthday - Edit birthday list."""
    await update.message.reply_text(
        "✏️ ယခုလ မွေးနေ့စာရင်းကို ရေးပေးပါ:\n\n"
        "📌 တစ်ကြောင်းလျှင် တစ်ခုစီ:\n"
        "ဥပမာ:\n"
        "ကိုမင်း - မတ်လ ၅ ရက်\n"
        "မမေ - မတ်လ ၁၂ ရက်\n\n"
        "(ပယ်ဖျက်ရန် /cancel )"
    )
    return WAITING_BIRTHDAYS


async def receive_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and save birthdays."""
    lines = [line.strip() for line in update.message.text.strip().split("\n") if line.strip()]
    set_birthdays(lines)
    await update.message.reply_text(f"✅ မွေးနေ့စာရင်း {len(lines)} ခု သိမ်းဆည်းပြီးပါပြီ!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
    return ConversationHandler.END


def get_birthday_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler("edbirthday", edbirthday_command)],
        states={
            WAITING_BIRTHDAYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_birthdays)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
