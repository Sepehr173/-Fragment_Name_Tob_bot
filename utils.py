import os
from PIL import Image, ImageDraw, ImageFont
from telegram import InputFile

# مسیر فایل یوزرنیم‌ها
USERNAMES_FILE = "usernames.txt"

# چنلی که پیام می‌فرستیم
CHANNEL_ID = "@fragment_User"  # حتماً جایگزین کن

# بارگذاری یوزرنیم‌ها
def load_usernames():
    if not os.path.exists(USERNAMES_FILE):
        return []
    with open(USERNAMES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# ساخت عکس ساده از یوزرنیم
def generate_image(username):
    img = Image.new("RGB", (500, 250), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    draw.text((50, 100), f"@{username}", fill=(255, 255, 255), font=font)

    image_path = f"{username}.png"
    img.save(image_path)
    return image_path

# قیمت‌گذاری تستی
def evaluate_username(username):
    return f"{len(username) * 500} TON"  # الگوریتم نمونه

# ارسال به چنل تلگرام
async def send_to_channel(bot, username, price, image_path):
    caption = f"🔹 یوزرنیم: @{username}\n💰 قیمت پیشنهادی: {price}"
    await bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(image_path), caption=caption)
    os.remove(image_path)
