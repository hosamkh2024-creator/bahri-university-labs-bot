import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

LABS = {
    "physics": "🔬 معمل الفيزياء",
    "chemistry": "🧪 معمل الكيمياء",
    "computer": "💻 معمل الحاسوب",
    "biology": "🧬 معمل الأحياء",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 عرض المعامل", callback_data="labs")],
        [InlineKeyboardButton("📅 حجز معمل", callback_data="book")],
        [InlineKeyboardButton("ℹ️ عن الجامعة", callback_data="about")],
    ]
    text = "أهلاً بيك في بوت مختبرات جامعة بحري 🎓\n\nاختار من القائمة:"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "labs":
        txt = "المعامل المتوفرة:\n\n"
        for v in LABS.values():
            txt += f"- {v}\n"
        txt += "\nللحجز اضغط حجز معمل"
        kb = [[InlineKeyboardButton("📅 حجز معمل", callback_data="book")],
              [InlineKeyboardButton("🔙 رجوع", callback_data="home")]]
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))
    elif q.data == "book":
        kb = [[InlineKeyboardButton(v, callback_data=f"book_{k}")] for k,v in LABS.items()]
        kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="home")])
        await q.edit_message_text("اختار المعمل العايز تحجزو:", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data.startswith("book_"):
        lab = LABS.get(q.data.replace("book_",""), "المعمل")
        context.user_data["lab"] = lab
        await q.edit_message_text(f"اخترت: {lab}\n\nاكتب اسمك الكامل و رقمك و اليوم العايزو، مثال:\nمحمد علي - 0912345678 - الأحد")
    elif q.data == "about":
        await q.edit_message_text("جامعة بحري - مختبرات الكليات\nللاستفسار تواصل مع إدارة المعامل.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="home")]]))
    elif q.data == "home":
        await start(update, context)

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lab = context.user_data.get("lab", "معمل")
    await update.message.reply_text(f"✅ تم استلام طلب حجزك!\n\nالمعمل: {lab}\nالتفاصيل: {update.message.text}\n\nسيتم التواصل معاك للتأكيد. شكراً لك!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("Bot is running...")
    app.run_polling()
