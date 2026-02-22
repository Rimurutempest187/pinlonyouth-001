"""
/backup, /restore, /allclear command handlers
Create by : PINLON-YOUTH
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import backup_data, restore_data, clear_all_data
from utils.decorators import admin_only


@admin_only
async def backup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backup - Backup all data."""
    backup_path, count = backup_data()
    await update.message.reply_text(
        f"💾 *Backup အောင်မြင်ပါပြီ!*\n\n"
        f"📁 ဖိုင် {count} ခု backup ပြုလုပ်ပြီးပါပြီ။\n"
        f"📂 {backup_path}",
        parse_mode="Markdown"
    )


@admin_only
async def restore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /restore - Restore from latest backup."""
    keyboard = [[
        InlineKeyboardButton("✅ ပြန်ယူမည်", callback_data="confirm_restore"),
        InlineKeyboardButton("❌ မလုပ်ပါ", callback_data="cancel_restore"),
    ]]
    await update.message.reply_text(
        "♻️ *နောက်ဆုံး Backup မှ Data ပြန်ယူမှာ သေချာပါသလား?*\n\n"
        "⚠️ လက်ရှိ data များ အစားထိုးခံရပါမည်။",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def restore_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle restore confirmation."""
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_restore":
        success, message = restore_data()
        await query.edit_message_text(message)
    else:
        await query.edit_message_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")


@admin_only
async def allclear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /allclear - Clear all data."""
    keyboard = [[
        InlineKeyboardButton("✅ ဖျက်မည်", callback_data="confirm_clear"),
        InlineKeyboardButton("❌ မလုပ်ပါ", callback_data="cancel_clear"),
    ]]
    await update.message.reply_text(
        "🗑️ *Data အားလုံး ဖျက်မှာ သေချာပါသလား?*\n\n"
        "⚠️ ဤလုပ်ဆောင်ချက်ကို ပြန်ပြင်၍ မရပါ!\n"
        "💡 /backup ကို အရင် လုပ်ဆောင်ရန် အကြံပြုပါသည်။",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def clear_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle clear confirmation."""
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_clear":
        cleared = clear_all_data()
        await query.edit_message_text(f"🗑️ Data ဖိုင် {cleared} ခု ဖျက်ပြီးပါပြီ!")
    else:
        await query.edit_message_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
