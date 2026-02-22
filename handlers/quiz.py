"""
/quiz, /edquiz, /tops, /set command handlers
Create by : PINLON-YOUTH
"""

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, MessageHandler, filters,
    CommandHandler, CallbackQueryHandler
)
from database import (
    get_quizzes, add_quiz, get_top_scores, add_score,
    get_quiz_msg_count, set_quiz_msg_count, increment_msg_count,
    reset_msg_count
)
from utils.decorators import admin_only

# Conversation states for edquiz
QUIZ_QUESTION, QUIZ_OPTION_A, QUIZ_OPTION_B, QUIZ_OPTION_C, QUIZ_OPTION_D, QUIZ_ANSWER = range(6)


async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quiz - Send a random quiz."""
    quizzes = get_quizzes()
    if not quizzes:
        await update.message.reply_text("🧠 Quiz မရှိသေးပါ။ Admin မှ ထည့်ပေးရန် လိုအပ်ပါသည်။")
        return

    quiz = random.choice(quizzes)
    options = quiz["options"]

    text = (
        f"🧠 *Quiz Time!*\n\n"
        f"❓ {quiz['question']}\n\n"
        f"🅰️ {options['A']}\n"
        f"🅱️ {options['B']}\n"
        f"©️ {options['C']}\n"
        f"🅳 {options['D']}"
    )

    keyboard = [
        [
            InlineKeyboardButton("🅰️ A", callback_data=f"quiz_A_{quizzes.index(quiz)}"),
            InlineKeyboardButton("🅱️ B", callback_data=f"quiz_B_{quizzes.index(quiz)}"),
        ],
        [
            InlineKeyboardButton("©️ C", callback_data=f"quiz_C_{quizzes.index(quiz)}"),
            InlineKeyboardButton("🅳 D", callback_data=f"quiz_D_{quizzes.index(quiz)}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)


async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer callback."""
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    if len(data) < 3:
        return

    selected = data[1]  # A, B, C, or D
    quiz_index = int(data[2])
    quizzes = get_quizzes()

    if quiz_index >= len(quizzes):
        await query.edit_message_text("❌ Quiz ရှာမတွေ့ပါ။")
        return

    quiz = quizzes[quiz_index]
    correct = quiz["answer"]
    user = query.from_user
    username = f"@{user.username}" if user.username else user.first_name

    if selected == correct:
        add_score(user.id, username, 1)
        await query.edit_message_text(
            f"✅ *မှန်ပါတယ်!* 🎉\n\n"
            f"❓ {quiz['question']}\n"
            f"✅ အဖြေ: {correct} - {quiz['options'][correct]}\n\n"
            f"🏆 {username} +1 point!",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text(
            f"❌ *မှားပါတယ်!*\n\n"
            f"❓ {quiz['question']}\n"
            f"❌ သင့်အဖြေ: {selected}\n"
            f"✅ မှန်ကန်သောအဖြေ: {correct} - {quiz['options'][correct]}",
            parse_mode="Markdown"
        )


async def tops_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tops - Show quiz score ranking."""
    top_scores = get_top_scores(10)
    if not top_scores:
        await update.message.reply_text("🏆 Quiz အမှတ်စာရင်း မရှိသေးပါ။")
        return

    text = "🏆 *Quiz Ranking - Top 10*\n\n━━━━━━━━━━━━━━━━━━━\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for i, (uid, info) in enumerate(top_scores):
        medal = medals[i] if i < 3 else f"  {i+1}."
        text += f"{medal} {info['username']} - {info['score']} pts\n"
    text += "\n━━━━━━━━━━━━━━━━━━━"

    await update.message.reply_text(text, parse_mode="Markdown")


@admin_only
async def set_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /set <number> - Set message count for quiz trigger."""
    if not context.args or not context.args[0].isdigit():
        current = get_quiz_msg_count()
        await update.message.reply_text(
            f"⚙️ Quiz message count သတ်မှတ်ရန်:\n\n"
            f"ဥပမာ: /set 2\n"
            f"(Group မှာ message {current} ခါ ပို့ရင် Quiz ကျလာမယ်)\n\n"
            f"📌 လက်ရှိ: {current} messages"
        )
        return

    count = int(context.args[0])
    if count < 1:
        count = 1
    set_quiz_msg_count(count)
    await update.message.reply_text(
        f"✅ Quiz trigger message count: {count}\n"
        f"(Group မှာ message {count} ခါ ပို့ရင် Quiz ကျလာမယ်)"
    )


# ─── /edquiz Conversation Handler ────────────────────────

@admin_only
async def edquiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edquiz - Add new quiz."""
    current_count = len(get_quizzes())
    await update.message.reply_text(
        f"✏️ Quiz အသစ်ထည့်ပါ:\n\n"
        f"📌 လက်ရှိ Quiz အရေအတွက်: {current_count}\n\n"
        f"❓ မေးခွန်းကို ရေးပေးပါ:\n\n"
        f"(ပယ်ဖျက်ရန် /cancel )"
    )
    return QUIZ_QUESTION


async def receive_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz_question"] = update.message.text
    await update.message.reply_text("🅰️ Option A ကို ရေးပေးပါ:")
    return QUIZ_OPTION_A


async def receive_option_a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz_a"] = update.message.text
    await update.message.reply_text("🅱️ Option B ကို ရေးပေးပါ:")
    return QUIZ_OPTION_B


async def receive_option_b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz_b"] = update.message.text
    await update.message.reply_text("©️ Option C ကို ရေးပေးပါ:")
    return QUIZ_OPTION_C


async def receive_option_c(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz_c"] = update.message.text
    await update.message.reply_text("🅳 Option D ကို ရေးပေးပါ:")
    return QUIZ_OPTION_D


async def receive_option_d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz_d"] = update.message.text
    await update.message.reply_text(
        "✅ မှန်ကန်သော အဖြေကို ရွေးပါ:\n\n"
        "A, B, C, သို့မဟုတ် D ကို ရေးပေးပါ:"
    )
    return QUIZ_ANSWER


async def receive_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text.strip().upper()
    if answer not in ["A", "B", "C", "D"]:
        await update.message.reply_text("⚠️ A, B, C, D ထဲမှ တစ်ခုကို ရွေးပါ:")
        return QUIZ_ANSWER

    question = context.user_data["quiz_question"]
    options = {
        "A": context.user_data["quiz_a"],
        "B": context.user_data["quiz_b"],
        "C": context.user_data["quiz_c"],
        "D": context.user_data["quiz_d"],
    }

    add_quiz(question, options, answer)

    await update.message.reply_text(
        f"✅ Quiz ထည့်သွင်းပြီးပါပြီ!\n\n"
        f"❓ {question}\n"
        f"🅰️ {options['A']}\n"
        f"🅱️ {options['B']}\n"
        f"©️ {options['C']}\n"
        f"🅳 {options['D']}\n"
        f"✅ အဖြေ: {answer}"
    )

    # Clean up user data
    for key in ["quiz_question", "quiz_a", "quiz_b", "quiz_c", "quiz_d"]:
        context.user_data.pop(key, None)

    return ConversationHandler.END


async def quiz_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for key in ["quiz_question", "quiz_a", "quiz_b", "quiz_c", "quiz_d"]:
        context.user_data.pop(key, None)
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
    return ConversationHandler.END


def get_quiz_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler("edquiz", edquiz_command)],
        states={
            QUIZ_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_question)],
            QUIZ_OPTION_A: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option_a)],
            QUIZ_OPTION_B: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option_b)],
            QUIZ_OPTION_C: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option_c)],
            QUIZ_OPTION_D: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option_d)],
            QUIZ_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_answer)],
        },
        fallbacks=[CommandHandler("cancel", quiz_cancel)],
    )


# ─── Message Counter + Auto Quiz Trigger ─────────────────

async def message_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count messages in group and trigger quiz when threshold reached."""
    if not update.message or not update.effective_chat:
        return
    if update.effective_chat.type not in ["group", "supergroup"]:
        return

    chat_id = update.effective_chat.id
    count = increment_msg_count(chat_id)
    threshold = get_quiz_msg_count()

    if count >= threshold:
        reset_msg_count(chat_id)
        # Trigger quiz
        quizzes = get_quizzes()
        if not quizzes:
            return

        quiz = random.choice(quizzes)
        options = quiz["options"]
        idx = quizzes.index(quiz)

        text = (
            f"🧠 *Auto Quiz Time!* 🎯\n\n"
            f"❓ {quiz['question']}\n\n"
            f"🅰️ {options['A']}\n"
            f"🅱️ {options['B']}\n"
            f"©️ {options['C']}\n"
            f"🅳 {options['D']}"
        )

        keyboard = [
            [
                InlineKeyboardButton("🅰️ A", callback_data=f"quiz_A_{idx}"),
                InlineKeyboardButton("🅱️ B", callback_data=f"quiz_B_{idx}"),
            ],
            [
                InlineKeyboardButton("©️ C", callback_data=f"quiz_C_{idx}"),
                InlineKeyboardButton("🅳 D", callback_data=f"quiz_D_{idx}"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
