import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import modes

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Flask app for GET route (to satisfy Render)
flask_app = Flask(__name__)

@flask_app.get("/")
def home():
    return "Bot is running ✅", 200


user_modes = {}

DEV_KEYWORDS = [
    "developer", "owner", "creator", "made you", "who built you",
    "who created you", "your boss", "who coded you", "who is your maker", "dhaya", "dhayanithi", "who built you"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello, I'm Rose AI 🌹\n\nAvailable modes:\n"
        "/ratchasi\n/emoji\n/subha\n/straightforward\n/normal\n\n"
        "Type your question after choosing a model"
    )

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE, mode_name: str):
    user_id = update.effective_user.id
    user_modes[user_id] = mode_name
    await update.message.reply_text(f"Mode set to {mode_name}. Please enter your question.")

async def ratchasi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "ratchasi")

async def emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "emoji")

async def subha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "subha")

async def straightforward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "straightforward")

async def normal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "normal")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    if any(keyword in text for keyword in DEV_KEYWORDS):
        dev_reply = (
            "I was developed by **Dhaya** with love ❤️\n\n"
            "🔗 Connect with him here:\n"
            "- [LinkedIn](https://www.linkedin.com/in/dhayanithi-anandan-69199a322/)\n"
            "- [GitHub](https://github.com/Dhayanithi545)\n"
            "- [Instagram](https://www.instagram.com/dhaya_545/)\n"
            "- [Portfolio](https://dhayanithi.vercel.app)\n"
            "- [Twitter/X](https://x.com/Dhayanithi545)"
        )
        await update.message.reply_text(dev_reply, disable_web_page_preview=True, parse_mode="Markdown")
        return

    if any(keyword in text for keyword in ["subha", "who is subha", "tell me about subha", "subha poem", "about subha"]):
        subha_poem = (
            "She is a distant star\n"
            "so bright it guides me,\n"
            "so far I can never touch her.\n"
            "Yet I keep walking in her light,\n"
            "even knowing it will never shine for me.\n"
            "                           -By Dhaya"
        )
        await update.message.reply_text(subha_poem)
        return

    mode = user_modes.get(user_id, "normal")

    if mode == 'ratchasi':
        reply = await modes.ratchasi_mode(text)
    elif mode == 'emoji':
        reply = await modes.emoji_mode(text)
    elif mode == 'subha':
        reply = await modes.subha_mode(text)
    elif mode == 'straightforward':
        reply = await modes.straightforward_mode(text)
    elif mode == 'normal':
        reply = await modes.normal_mode(text)

    await update.message.reply_text(reply)


# ✅ Function to run bot polling in a new thread
def run_bot():
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ratchasi", ratchasi))
    app.add_handler(CommandHandler("emoji", emoji))
    app.add_handler(CommandHandler("subha", subha))
    app.add_handler(CommandHandler("straightforward", straightforward))
    app.add_handler(CommandHandler("normal", normal))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    loop.run_until_complete(app.initialize())
    loop.run_until_complete(app.start())
    loop.run_until_complete(app.updater.start_polling())
    loop.run_forever()


def main():
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    main()
