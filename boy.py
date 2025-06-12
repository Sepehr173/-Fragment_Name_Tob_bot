import logging
import os
import random
import re
import string
import sys
import time
from datetime import datetime

import openai
import requests
import telebot
from telebot import types
from transliterate import translit

TOKEN = os.getenv("8140626997:AAGVJMOoSWPfYBzubK51beuDqNVnCTfsLbM")
CHANNEL_ID = os.getenv("@Fragment_User")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_USERNAME = os.getenv("@Fragment_Name_Tob_bot")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

used_names = set()
username_data = []

def load_used_names():
    try:
        with open("used_names.txt", "r") as file:
            for line in file:
                used_names.add(line.strip())
    except FileNotFoundError:
        pass

def save_used_name(name):
    with open("used_names.txt", "a") as file:
        file.write(f"{name}\n")

def is_valid_username(name):
    if not (5 <= len(name) <= 32):
        return False
    if re.search(r"[^a-zA-Z0-9_]", name):
        return False
    if name.lower() in used_names:
        return False
    return True

def generate_random_username():
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(random.randint(5, 10)))

def transliterate_name(name):
    return translit(name, "ru", reversed=True)

def evaluate_username(name):
    prompt = f"Evaluate the Telegram username '{name}' for potential value, branding, and aesthetics."
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error evaluating username: {e}")
        return "Error evaluating username."

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    next_btn = types.InlineKeyboardButton("🎲 Next", callback_data="next_name")
    markup.add(next_btn)
    bot.send_message(message.chat.id, "Welcome! Press the button below to get a username evaluated.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "next_name")
def handle_next_name(call):
    name = generate_random_username()
    while not is_valid_username(name):
        name = generate_random_username()
    save_used_name(name)
    used_names.add(name)

    transliterated = transliterate_name(name)
    evaluation = evaluate_username(name)

    caption = f"💎 Username: `{name}`\n🔤 Transliteration: `{transliterated}`\n🧠 Evaluation: {evaluation}"

    try:
        bot.send_message(CHANNEL_ID, caption, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to send message to channel: {e}")

    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=caption, parse_mode="Markdown", reply_markup=call.message.reply_markup)

if __name__ == "__main__":
    load_used_names()
    print("Bot is running...")
    bot.infinity_polling()
