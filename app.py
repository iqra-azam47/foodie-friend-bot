"""Foodie Friend: a restaurant chatbot built with Flask and the Gemini API.
This file only has the web routes. The order system is in bot/orders.py,
the menu in data/menu.json and the settings in config.py."""
import logging
import os

from flask import Flask, jsonify, render_template, request, session
from google import genai
from google.genai import types

import config  # imported first: it also loads the optional .env file
from bot.orders import OrderTools, new_order_state
from bot.prompt import SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise SystemExit("GOOGLE_API_KEY is missing. Copy .env.example to .env and put your key inside.")
client = genai.Client(api_key=api_key)

app = Flask(__name__)

secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    logger.warning("SECRET_KEY is not set, so a temporary key is used. "
                   "Chats will reset on restart. Set SECRET_KEY on a real server.")
    secret_key = os.urandom(24)
app.secret_key = secret_key


def trim_history(history):
    """Keep only the latest messages (a browser cookie can only hold about 4 KB)."""
    history = history[-config.MAX_HISTORY_MESSAGES:]
    while history and history[0]["role"] != "user":
        history.pop(0)
    return history


def to_gemini_messages(history):
    """Turn our simple list [{"role": "user", "text": "hi"}, ...] into the SDK format."""
    return [types.Content(role=m["role"], parts=[types.Part(text=m["text"])]) for m in history]


@app.route("/")
def index():
    session["history"] = []
    session["order"] = new_order_state()
    return render_template("index.html", bot_name=config.BOT_NAME,
                           max_message_length=config.MAX_MESSAGE_LENGTH)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Please type a message."}), 400
    if len(user_message) > config.MAX_MESSAGE_LENGTH:
        return jsonify({"error": f"Your message is too long. Please keep it under "
                                 f"{config.MAX_MESSAGE_LENGTH} characters."}), 400

    try:
        history = trim_history(session.get("history", []))

        # The cart lives in our own code, not in the AI's memory
        tools = OrderTools(session.get("order") or new_order_state())

        chat_session = client.chats.create(
            model=config.MODEL_NAME,
            history=to_gemini_messages(history),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[tools.add_to_cart, tools.remove_from_cart, tools.view_cart,
                       tools.prepare_order, tools.confirm_order, tools.start_new_order],
            ),
        )
        response = chat_session.send_message(user_message)
        reply = response.text or "Sorry, I could not answer that. Please try again."

        history.append({"role": "user", "text": user_message})
        history.append({"role": "model", "text": reply[:config.MAX_STORED_CHARS]})
        session["history"] = history
        session["order"] = tools.get_state()

        return jsonify({"response": reply})
    except Exception:
        logger.exception("Chat request failed")
        return jsonify({"error": "Sorry, a server error occurred. Please try again."}), 500


if __name__ == "__main__":
    # 127.0.0.1 = only your own computer can open the app (safer while testing)
    app.run(host="127.0.0.1", port=5000)