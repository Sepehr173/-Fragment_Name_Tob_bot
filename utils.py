import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# دریافت قیمت یوزرنیم از Fragment
def get_username_price(username):
    url = f"https://fragment.com/username/{username}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if "Minimum bid" in response.text:
                start_index = response.text.find("Minimum bid")
                text = response.text[start_index:start_index+100]
                price = text.split("Ⓝ")[1].split("<")[0].strip()
                return f"{price} TON"
            elif "Current bid" in response.text:
                start_index = response.text.find("Current bid")
                text = response.text[start_index:start_index+100]
                price = text.split("Ⓝ")[1].split("<")[0].strip()
                return f"{price} TON"
            else:
                return "Price not found"
        else:
            return "Username not available"
    except:
        return "Error fetching price"

# ساخت تصویر با قیمت و یوزرنیم
def generate_price_image(username, price):
    img = Image.new('RGB', (500, 250), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # فونت پیش‌فرض
    font = ImageFont.load_default()

    draw.text((20, 60), f"@{username}", font=font, fill=(255, 255, 255))
    draw.text((20, 130), f"Price: {price}", font=font, fill=(0, 255, 0))

    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return byte_io
