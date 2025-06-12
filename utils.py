import openai
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_image_with_text(text):
    # Create blank image
    img = Image.new('RGB', (512, 512), color=(30, 30, 30))
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    d.text((10, 10), text, font=font, fill=(255, 255, 255))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer

async def evaluate_username(username):
    prompt = f"Evaluate the value and uniqueness of this Telegram username: @{username}."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in digital brand names."},
            {"role": "user", "content": prompt}
        ]
    )

    result_text = response['choices'][0]['message']['content']
    image = generate_image_with_text(f"@{username}\n\n{result_text[:150]}...")

    return {
        "text": f"💎 بررسی نام کاربری: @{username}\n\n{result_text}",
        "image": image
    }
