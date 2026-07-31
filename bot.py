from groq import Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import threading

app = Flask(__name__)
application = ApplicationBuilder().token("8982498067:AAH3mNJIRa7t-j2ZsBCWTEJX_RUFppsNPow").build()

# Replace this with your own verse lookup function
def get_verse(reference):
    # Example: call Bible API
    try:
        url = f"https://bible-api.com/{reference}?translation=kjv"
        res = requests.get(url)
        data = res.json()
        return data['text']
    except:
        return "Verse not found. Check the reference e.g. John 3:16"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /verse John 3:16 to get a verse\nUse /explain John 3:16 to get explanation")

async def verse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /verse John 3:16")
        return
    verse_ref = " ".join(context.args)
    verse_text = get_verse(verse_ref)
    await update.message.reply_text(f"📖 *{verse_ref}*\n{verse_text}", parse_mode='Markdown')

async def explain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /explain John 3:16")
        return
    
    verse_ref = " ".join(context.args)
    verse_text = get_verse(verse_ref)
    
    if "not found" in verse_text.lower():
        await update.message.reply_text(verse_text)
        return
    
    await update.message.reply_text(f"Finding explanation for {verse_ref}... ⏳")
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a Bible teacher. Explain KJV Bible verses in simple, friendly, 3-4 sentence language."},
            {"role": "user", "content": f"Explain this KJV Bible verse: {verse_ref} - {verse_text}"}
        ],
        model="llama3-8b-8192",
    )
    
    explanation = chat_completion.choices[0].message.content
    await update.message.reply_text(f"📖 *{verse_ref}*\n{verse_text}\n\n💡 *Explanation:*\n{explanation}", parse_mode='Markdown')

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("verse", verse_command))
application.add_handler(CommandHandler("explain", explain_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verse_command))

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def run_bot():
    application.run_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()
    run_bot()
