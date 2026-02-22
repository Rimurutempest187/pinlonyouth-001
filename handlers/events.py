"""
/events and /edevents command handlers
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from database import get_events, set_events
from utils.decorators import admin_only

WAITING_EVENTS = 0


async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /events - Show upcoming events."""
    events = get_events()
    if not events:
        await update.message.reply_text("📅 လာမည့် အစီအစဉ် မရှိသေးပါ။")
        return

    text = "📅 *လာမည့် အသင်းတော် အစီအစဉ်များ*\n\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, event in enumerate(events, 1):
        text += f"📌 {i}. {event}\n\n"
    text += "━━━━━━━━━━━━━━━━━━━"

    await update.message.reply_text(text, parse_mode="Markdown")


@admin_only
async def edevents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edevents - Edit events."""
    await update.message.reply_text(
        "✏️ လာမည့် အစီအစဉ်များကို ရေးပေးပါ:\n\n"
        "📌 တစ်ကြောင်းလျှင် တစ်ခုစီ:\n"
        "ဥပမာ:\n"
        "၂၀၂၆ မတ်လ ၁ - ဝတ်ပြုကိုးကွယ်ခြင်း (နံနက် ၉:၀၀)\n"
        "၂၀၂၆ မတ်လ ၈ - လူငယ်အစည်းအဝေး (ညနေ ၃:၀၀)\n\n"
        "(ပယ်ဖျက်ရန် /cancel )"
    )
    return WAITING_EVENTS


async def receive_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and save events."""
    lines = [line.strip() for line in update.message.text.strip().split("\n") if line.strip()]
    set_events(lines)
    await update.message.reply_text(f"✅ အစီအစဉ် {len(lines)} ခု သိမ်းဆည်းပြီးပါပြီ!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
    return ConversationHandler.END


def get_events_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler("edevents", edevents_command)],
        states={
            WAITING_EVENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_events)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
