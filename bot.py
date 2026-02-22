import logging
from datetime import time
import pytz  # Timezone အတွက် လိုအပ်ပါတယ် (pip install pytz)

from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters
)
from config import BOT_TOKEN, MORNING_VERSE_HOUR, MORNING_VERSE_MINUTE, NIGHT_VERSE_HOUR, NIGHT_VERSE_MINUTE

# Import handlers
from handlers.start import start_command
from handlers.admin import edit_command
from handlers.about import about_command, get_about_conversation
from handlers.contact import contact_command, get_contact_conversation
from handlers.verse import verse_command, get_verse_conversation
from handlers.events import events_command, get_events_conversation
from handlers.birthday import birthday_command, get_birthday_conversation
from handlers.pray import pray_command, praylist_command
from handlers.quiz import (
    quiz_command, quiz_callback, tops_command, set_command,
    get_quiz_conversation, message_counter
)
from handlers.broadcast import get_broadcast_conversation
from handlers.stats import stats_command
from handlers.report import report_command
from handlers.backup import (
    backup_command, restore_command, restore_callback,
    allclear_command, clear_callback
)
from utils.scheduler import send_daily_verse
from database import register_user, register_group

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Myanmar Timezone
MMT = pytz.timezone('Asia/Yangon')

async def track_chat(update, context):
    """Track users and groups on any message."""
    if not update.effective_user:
        return
    user = update.effective_user
    register_user(user.id, user.username, user.first_name)

    if update.effective_chat and update.effective_chat.type in ["group", "supergroup"]:
        register_group(update.effective_chat.id, update.effective_chat.title)

def main():
    """Start the bot."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ BOT_TOKEN ကို config.py တွင် ထည့်ပေးပါ!")
        return

    # Build application
    app = Application.builder().token(BOT_TOKEN).build()

    # ─── Conversation Handlers ───
    app.add_handler(get_about_conversation())
    app.add_handler(get_contact_conversation())
    app.add_handler(get_verse_conversation())
    app.add_handler(get_events_conversation())
    app.add_handler(get_birthday_conversation())
    app.add_handler(get_quiz_conversation())
    app.add_handler(get_broadcast_conversation())

    # ─── Command Handlers ───
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("edit", edit_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("verse", verse_command))
    app.add_handler(CommandHandler("events", events_command))
    app.add_handler(CommandHandler("birthday", birthday_command))
    app.add_handler(CommandHandler("pray", pray_command))
    app.add_handler(CommandHandler("praylist", praylist_command))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CommandHandler(["tops", "Tops"], tops_command)) # List အနေနဲ့ သုံးလို့ရပါတယ်
    app.add_handler(CommandHandler("set", set_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("report", report_command))
    app.add_handler(CommandHandler("backup", backup_command))
    app.add_handler(CommandHandler("restore", restore_command))
    app.add_handler(CommandHandler("allclear", allclear_command))

    # ─── Callback Query Handlers ───
    app.add_handler(CallbackQueryHandler(quiz_callback, pattern=r"^quiz_"))
    app.add_handler(CallbackQueryHandler(restore_callback, pattern=r"^(confirm|cancel)_restore$"))
    app.add_handler(CallbackQueryHandler(clear_callback, pattern=r"^(confirm|cancel)_clear$"))

    # ─── Message Handler ───
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_counter), group=1)
    app.add_handler(MessageHandler(filters.ALL, track_chat), group=2)

    # ─── Scheduled Jobs (Daily Verse) ───
    job_queue = app.job_queue
    if job_queue:
        # Morning verse (MMT အချိန်ကို သုံးထားပါတယ်)
        job_queue.run_daily(
            send_daily_verse,
            time=time(hour=MORNING_VERSE_HOUR, minute=MORNING_VERSE_MINUTE, tzinfo=MMT),
            name="morning_verse"
        )
        # Night verse
        job_queue.run_daily(
            send_daily_verse,
            time=time(hour=NIGHT_VERSE_HOUR, minute=NIGHT_VERSE_MINUTE, tzinfo=MMT),
            name="night_verse"
        )
    else:
        logger.warning("⚠️ JobQueue is not available. Install: pip install python-telegram-bot[job-queue]")

    # Start bot
    logger.info("⛪ Church Community Bot started! Create by : PINLON-YOUTH")
    print("⛪ Church Community Bot is running...")
    app.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main()
