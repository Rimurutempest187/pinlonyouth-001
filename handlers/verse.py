"""
/verse and /edverse command handlers
Create by : PINLON-YOUTH
"""

import random
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from database import get_verses, add_verse
from utils.decorators import admin_only

WAITING_VERSE = 0


async def verse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /verse - Show a random verse."""
    verses = get_verses()
    if not verses:
        await update.message.reply_text("📖 ကျမ်းချက် မရှိသေးပါ။ Admin မှ ထည့်ပေးရန် လိုအပ်ပါသည်။")
        return

    verse = random.choice(verses)
    await update.message.reply_text(
        f"📖 *ယနေ့အတွက် ကျမ်းချက်*\n\n"
        f"✝️ {verse}\n\n"
        f"🙏 _ဘုရားသခင်က သင့်ကို ကောင်းချီးပေးပါစေ!_",
        parse_mode="Markdown"
    )


@admin_only
async def edverse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edverse - Add new verses."""
    current_count = len(get_verses())
    await update.message.reply_text(
        f"✏️ ကျမ်းချက်အသစ် ထည့်ပေးပါ:\n\n"
        f"📌 လက်ရှိ ကျမ်းချက် အရေအတွက်: {current_count}\n\n"
        f"တစ်ကြောင်းလျှင် ကျမ်းချက် တစ်ခုစီ ရေးပေးပါ:\n"
        f"ဥပမာ:\n"
        f"ယောဟန် ၃:၁၆ - ဘုရားသခင်သည် လောကီသားတို့ကို...\n"
        f"ဆာလံ ၂၃:၁ - ထာဝရဘုရားသည် ငါ့သိုးထိန်းဖြစ်တော်မူ၏...\n\n"
        f"(ပယ်ဖျက်ရန် /cancel )"
    )
    return WAITING_VERSE


async def receive_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and save verses."""
    lines = [line.strip() for line in update.message.text.strip().split("\n") if line.strip()]
    for line in lines:
        add_verse(line)
    await update.message.reply_text(f"✅ ကျမ်းချက် {len(lines)} ခု ထည့်သွင်းပြီးပါပြီ!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
    return ConversationHandler.END


def get_verse_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler("edverse", edverse_command)],
        states={
            WAITING_VERSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_verse)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
