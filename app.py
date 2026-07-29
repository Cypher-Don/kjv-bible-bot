from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import requests
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_kjv_verse(reference):
    url = f"https://bible-api.com/{reference}?translation=kjv"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return data.get('text', 'Verse not found')
    return "Verse not found"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.json["message"]
    verse_text = ""
    words = user_msg.split()
    for word in words:
        if ":" in word:
            verse_text = get_kjv_verse(word)
            break

    system_prompt = """You are a KJV Bible Teacher and Q&A Assistant.
    Rules:
    1. Always base answers on scripture. Use KJV.
    2. If a verse is provided, quote it and explain it simply.
    3. Be respectful, biblical, and practical. Give application.
    4. Never make up verses.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {user_msg}\nKJV Verse: {verse_text}"}
        ]
    )
    return jsonify({"answer": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)
