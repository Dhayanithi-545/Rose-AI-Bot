import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import modes

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

user_modes = {}

# ✅ Keywords to detect "developer/owner" questions
DEV_KEYWORDS = [
    "developer", "owner", "creator", "made you", "who built you", 
    "who created you", "your boss", "who coded you", "who is your maker"
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
    text = update.message.text.lower()  # lowercase for easy matching

    # ✅ Custom override for developer/owner questions
    if any(keyword in text for keyword in DEV_KEYWORDS):
        dev_reply = (
            "I was developed by **Dhayanithi** with love ❤️\n\n"
            "🔗 Connect with him here:\n"
            "- [LinkedIn](https://www.linkedin.com/in/dhayanithi-anandan-69199a322/)\n"
            "- [GitHub](https://github.com/Dhayanithi545)\n"
            "- [Instagram](https://www.instagram.com/dhaya_545/)\n"
            "- [Portfolio](https://dhayanithi.vercel.app)\n"
            "- [Twitter/X](https://x.com/Dhayanithi545)"
        )
        await update.message.reply_text(dev_reply, disable_web_page_preview=True, parse_mode="Markdown")
        return  # stop here, don’t call AI

    # Normal AI flow
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


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ratchasi", ratchasi))
    app.add_handler(CommandHandler("emoji", emoji))
    app.add_handler(CommandHandler("subha", subha))
    app.add_handler(CommandHandler("straightforward", straightforward))
    app.add_handler(CommandHandler("normal", normal))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
#Rose Bot