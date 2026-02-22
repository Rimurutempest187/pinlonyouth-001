"""
/broadcast command handler
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from database import get_groups
from utils.decorators import admin_only
import logging

logger = logging.getLogger(__name__)

WAITING_BROADCAST = 0


@admin_only
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast - Broadcast message to all groups."""
    groups = get_groups()
    if not groups:
        await update.message.reply_text("📢 Group မရှိသေးပါ။")
        return ConversationHandler.END

    await update.message.reply_text(
        f"📢 Group {len(groups)} ခု သို့ သတင်းစကား ပို့ပါမည်။\n\n"
        f"📝 ပို့လိုသော စာ သို့မဟုတ် ပုံ(caption ပါ)ကို ပေးပို့ပါ:\n\n"
        f"(ပယ်ဖျက်ရန် /cancel )"
    )
    return WAITING_BROADCAST


async def receive_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and broadcast message to all groups."""
    groups = get_groups()
    success = 0
    fail = 0

    for chat_id in groups:
        try:
            if update.message.photo:
                # Send photo with caption
                await context.bot.send_photo(
                    chat_id=int(chat_id),
                    photo=update.message.photo[-1].file_id,
                    caption=update.message.caption or "",
                    parse_mode="Markdown"
                )
            elif update.message.text:
                # Send text message
                await context.bot.send_message(
                    chat_id=int(chat_id),
                    text=update.message.text,
                    parse_mode="Markdown"
                )
            success += 1
        except Exception as e:
            logger.error(f"Broadcast failed for {chat_id}: {e}")
            fail += 1

    await update.message.reply_text(
        f"📢 *Broadcast ရလဒ်*\n\n"
        f"✅ အောင်မြင်: {success} groups\n"
        f"❌ မအောင်မြင်: {fail} groups",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
    return ConversationHandler.END


def get_broadcast_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler("broadcast", broadcast_command)],
        states={
            WAITING_BROADCAST: [
                MessageHandler(filters.PHOTO, receive_broadcast),
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_broadcast),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
