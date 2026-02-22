"""
/about and /edabout command handlers
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from database import get_about, set_about
from utils.decorators import admin_only

WAITING_ABOUT = 0


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about - Show about info."""
    text = get_about()
    await update.message.reply_text(
        f"⛪ *အသင်းတော်အကြောင်း*\n\n{text}",
        parse_mode="Markdown"
    )


@admin_only
async def edabout_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edabout - Edit about info."""
    await update.message.reply_text(
        "✏️ အသင်းတော်/လူငယ်အဖွဲ့ အကြောင်းကို ရေးပေးပါ:\n\n"
        "(ပယ်ဖျက်ရန် /cancel )"
    )
    return WAITING_ABOUT


async def receive_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and save about text."""
    set_about(update.message.text)
    await update.message.reply_text("✅ အသင်းတော်အကြောင်း သိမ်းဆည်းပြီးပါပြီ!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation."""
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
    return ConversationHandler.END


def get_about_conversation():
    """Return ConversationHandler for edabout."""
    return ConversationHandler(
        entry_points=[CommandHandler("edabout", edabout_command)],
        states={
            WAITING_ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_about)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
