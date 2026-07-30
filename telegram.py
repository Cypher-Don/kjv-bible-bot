import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8982498067:AAH3mNJIRa7t-j2ZsBCWTEJX_RUFppsNPow"
BIBLE_API_URL = "https://kjv-bible-bot.onrender.com/api/verse"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 Welcome to The Don's KJV-BIBLE-BOT\n"
        "Just send me any verse like:\n"
        "• John 3:16\n"
        "• Psalm 23\n"
        "• Romans 8:28\n\n"
        "I’ll bring you the KJV version instantly 🙏"
    )

async def get_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    try:
        r = requests.get(f"{BIBLE_API_URL}?q={query}")
        data = r.json()
        if "verse" in data:
            await update.message.reply_text(f"📖 {data['verse']}\n\n— {data['reference']} KJV")
        else:
            await update.message.reply_text("Sorry bro, I couldn’t find that verse. Try John 3:16")
    except:
        await update.message.reply_text("Something went wrong. Try again in a bit.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_verse))
    app.run_polling()

if __name__ == "__main__":
    main()
