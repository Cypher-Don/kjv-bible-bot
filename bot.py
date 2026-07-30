import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
BIBLE_API = "https://bible-api.com/"

app = Flask(__name__)

@app.route('/')
def home():
    return "KJV Bible Bot is Live 👑"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 Welcome! Send me a verse like: John 3:16")

async def get_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"Searching for {query}...")
    
    try:
        res = requests.get(BIBLE_API + query + "?translation=kjv")
        data = res.json()
        verse = data.get("text", "Verse not found.")
        ref = data.get("reference", query)
        await update.message.reply_text(f"*{ref}*\n\n{verse}", parse_mode="Markdown")
    except:
        await update.message.reply_text("Sorry, I couldn't find that verse. Try: John 3:16")

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_verse))
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()
    run_bot()
