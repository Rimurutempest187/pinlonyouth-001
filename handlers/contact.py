"""
/contact and /edcontact command handlers
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from database import get_contacts, set_contacts
from utils.decorators import admin_only

WAITING_CONTACTS = 0


async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /contact - Show contact list."""
    contacts = get_contacts()
    if not contacts:
        await update.message.reply_text("📞 ဆက်သွယ်ရန် အချက်အလက် မရှိသေးပါ။")
        return

    text = "📞 *တာဝန်ခံ လူငယ်ခေါင်းဆောင်များ*\n\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, contact in enumerate(contacts, 1):
        text += f"👤 {contact}\n"
    text += "\n━━━━━━━━━━━━━━━━━━━"

    await update.message.reply_text(text, parse_mode="Markdown")


@admin_only
async def edcontact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edcontact - Edit contacts."""
    await update.message.reply_text(
        "✏️ ဆက်သွယ်ရန် အချက်အလက်များကို ရေးပေးပါ:\n\n"
        "📌 ပုံစံ - တစ်ကြောင်းလျှင် တစ်ခုစီ:\n"
        "ဥပမာ:\n"
        "ကိုမင်း - 09123456789\n"
        "မမေ - 09987654321\n\n"
        "(ပယ်ဖျက်ရန် /cancel )"
    )
    return WAITING_CONTACTS


async def receive_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and save contacts."""
    lines = [line.strip() for line in update.message.text.strip().split("\n") if line.strip()]
    set_contacts(lines)
    await update.message.reply_text(f"✅ ဆက်သွယ်ရန် {len(lines)} ခု သိမ်းဆည်းပြီးပါပြီ!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
    return ConversationHandler.END


def get_contact_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler("edcontact", edcontact_command)],
        states={
            WAITING_CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_contacts)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
