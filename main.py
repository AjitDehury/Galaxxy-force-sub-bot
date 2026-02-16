import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # Example: @yourchannelusername

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if chat_member.status in ["member", "administrator", "creator"]:
        await update.message.reply_text("✅ Welcome! You are verified.")
    else:
        keyboard = [
            [InlineKeyboardButton("🔔 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("✅ Refresh", callback_data="check")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "❌ Please join our channel first to use this bot.",
            reply_markup=reply_markup
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if chat_member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text("✅ You are now verified! You can use the bot.")
    else:
        await query.answer("❌ You haven't joined yet!", show_alert=True)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot is running...")
app.run_polling()
