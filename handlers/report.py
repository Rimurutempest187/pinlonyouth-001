"""
/report command handler
Create by : PINLON-YOUTH
"""

from telegram import Update
from telegram.ext import ContextTypes
from database import add_report
from config import ADMIN_IDS


async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /report <text> - Submit a report."""
    if not context.args:
        await update.message.reply_text(
            "📩 အကြောင်းအရာ တင်ပြရန်:\n\n"
            "ဥပမာ: /report ဝတ်ပြုကိုးကွယ်ခြင်းအချိန် ပြောင်းလဲပေးပါ"
        )
        return

    text = " ".join(context.args)
    user = update.effective_user
    username = f"@{user.username}" if user.username else user.first_name

    add_report(user.id, username, text)

    await update.message.reply_text(
        f"📩 *Report လက်ခံပြီးပါပြီ!*\n\n"
        f"📝 {text}\n\n"
        f"✅ _Admin များထံ ပေးပို့ပြီးပါပြီ။ ကျေးဇူးတင်ပါသည်။_",
        parse_mode="Markdown"
    )

    # Notify admins
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    f"📩 *Report အသစ်*\n\n"
                    f"👤 {username}\n"
                    f"📝 {text}"
                ),
                parse_mode="Markdown"
            )
        except Exception:
            pass
