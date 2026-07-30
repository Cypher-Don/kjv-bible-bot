import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# ========= CONFIG =========
TOKEN = "8019398454:AAEMxT1jvW8u1n5vVvW1oR7kQ9zY3pL0sD4" # Your token
BIBLE_API = "https://bible-api.com/"

# ========= FLASK FOR RENDER =========
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "KJV Bible Bot is Live 👑"

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app_flask.run(host='0.0.0.0', port=port)

# ========= TELEGRAM BOT =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 Welcome to The Don's KJV-BIBLE-BOT\n"
        "Send me a verse like: John 3:16\n"
        "Or a chapter like: Psalm 23"
    )

async def get_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🔍 Looking up {query}...")
    
    try:
        url = f"{BIBLE_API}{query}?translation=kjv"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'verses' in data:
            verses = [v['text'] for v in data['verses']]
            message = f"📖 {data['reference']} KJV\n" + "\n".join(verses)
        else:
            message = "Sorry bro, I couldn't find that verse. Try 'John 3:16'"
            
        await update.message.reply_text(message[:4096]) # Telegram limit
        
    except Exception as e:
        await update.message.reply_text("Error fetching verse. Try again.")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_verse))
    print("Bot is running...")
    app.run_polling()

# ========= RUN BOTH =========
if __name__ == '__main__':
    # Run Flask in background thread
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Run Bot in main thread
    run_bot()
