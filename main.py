import telebot
import os
from utils import generate_username_image, evaluate_username

bot = telebot.TeleBot(os.getenv("8140626997:AAGVJMOoSWPfYBzubK51beuDqNVnCTfsLbM"))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! یک نام کاربری ارسال کن تا برات ارزیابی و تصویرشو بسازم.")

@bot.message_handler(func=lambda message: True)
def handle_username(message):
    username = message.text.strip()
    if not username.startswith("@"):
        bot.reply_to(message, "لطفاً یک نام کاربری با @ بفرست.")
        return

    score, info = evaluate_username(username)
    image = generate_username_image(username, score, info)

    with open(image, "rb") as img:
        bot.send_photo(message.chat.id, img, caption=f"ارزیابی برای {username}:\nامتیاز: {score}\n{info}")

bot.polling()
