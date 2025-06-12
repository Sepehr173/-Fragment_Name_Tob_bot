import telebot
import openai
import os
import random

# دریافت توکن‌ها از ENV
BOT_TOKEN = os.getenv("8140626997:AAGVJMOoSWPfYBzubK51beuDqNVnCTfsLbM")
CHANNEL_ID = os.getenv("Fragment_User")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

def evaluate_username(username):
    prompt = f"""
    یوزرنیم زیر را از نظر زیبایی، خاص بودن، کوتاهی و ارزش احتمالی در پلتفرم‌هایی مثل تلگرام بررسی کن:
    
    @{username}
    
    توضیح فارسی بده که چرا خوبه یا نه، و در نهایت یه قیمت حدودی بر حسب دلار تتر (USDT) بگو.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.8
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"خطا در ارزیابی: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! روی ارسال پیام بزن تا یه یوزرنیم بررسی بشه و نتیجه به کانال بره.")

@bot.message_handler(func=lambda message: True)
def handle_request(message):
    try:
        with open("usernames.txt", "r") as f:
            usernames = f.read().splitlines()

        if not usernames:
            bot.reply_to(message, "یوزرنیمی باقی نمونده.")
            return

        username = usernames.pop(0)

        result = evaluate_username(username)

        # ارسال نتیجه به کانال
        final_message = f"👤 بررسی یوزرنیم: @{username}\n\n{result}"
        bot.send_message(CHANNEL_ID, final_message)

        # بروزرسانی فایل
        with open("usernames.txt", "w") as f:
            f.write("\n".join(usernames))

        # پاسخ به کاربر
        bot.reply_to(message, f"✅ یوزرنیم @{username} بررسی و به کانال فرستاده شد.")

    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {str(e)}")

bot.polling()
