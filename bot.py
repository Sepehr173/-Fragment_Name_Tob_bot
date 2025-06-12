import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
)

from utils import load_usernames, generate_image, evaluate_username, send_to_channel

# لاگ
logging.basicConfig(level=logging.INFO)

# حافظه موقت
usernames = load_usernames()
current_index = 0


# دکمه استارت
async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("🔍 بررسی یوزرنیم بعدی", callback_data="next_username")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("برای بررسی یوزرنیم روی دکمه زیر بزنید:", reply_markup=reply_markup)


# وقتی کاربر دکمه رو میزنه
async def handle_button(update: Update, context: CallbackContext):
    global current_index

    query = update.callback_query
    await query.answer()

    if current_index >= len(usernames):
        await query.edit_message_text("✅ همه یوزرنیم‌ها بررسی شدند.")
        return

    username = usernames[current_index]
    current_index += 1

    image_path = generate_image(username)
    price = evaluate_username(username)

    await send_to_channel(context.bot, username, price, image_path)

    await query.edit_message_text(f"یوزرنیم {username} با موفقیت بررسی شد! ✅")


# اجرای اصلی بات
def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
