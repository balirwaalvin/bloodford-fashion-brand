import os
from PIL import Image, ImageDraw, ImageFont
import re

brand_red = (196, 30, 58)    # #C41E3A
brand_black = (10, 10, 10)   # #0A0A0A
brand_white = (255, 255, 255) # #FFFFFF
brand_gold = (212, 175, 55)

images_dir = os.path.join("static", "images")
os.makedirs(images_dir, exist_ok=True)

# List of products to generate images for (extracted from app.py)
products = [
    ("suit_black.jpg", "Classic Black Tailored Suit", "black"),
    ("blazer_red.jpg", "Red Power Blazer", "red"),
    ("shirt_white.jpg", "Crisp White Oxford Shirt", "white"),
    ("chinos_black.jpg", "Black Slim-Fit Chinos", "black"),
    ("bomber_rb.jpg", "Red & Black Bomber Jacket", "red"),
    ("polo_mono.jpg", "Monochrome Polo Collection", "black"),
    ("boots_black.jpg", "Black Leather Chelsea Boots", "black"),
    ("joggers_black.jpg", "Designer Black Joggers", "black"),
    ("gown_red.jpg", "Elegant Red Evening Gown", "red"),
    ("pantsuit_black.jpg", "Black Power Pantsuit", "black"),
    ("blouse_white.jpg", "White Silk Blouse", "white"),
    ("skirt_red.jpg", "Red Pencil Skirt", "red"),
    ("bag_black.jpg", "Black Leather Handbag", "black"),
    ("wrap_dress.jpg", "Monochrome Wrap Dress", "black"),
    ("heels_red.jpg", "Red Stiletto Heels", "red"),
    ("crop_jacket.jpg", "Black Cropped Jacket", "black"),
    ("hoodie_logo.jpg", "Signature Logo Hoodie", "black"),
    ("tshirt_logo.jpg", "Classic Logo T-Shirt", "white"),
    ("sunglasses.jpg", "Designer Sunglasses", "black"),
    ("belt_leather.jpg", "Premium Leather Belt", "black"),
]

def generate_image(filename, text, color_theme):
    w, h = 600, 800
    
    if color_theme == "black":
        bg_color = brand_black
        text_color = brand_white
        accent_color = brand_red
    elif color_theme == "red":
        bg_color = brand_red
        text_color = brand_white
        accent_color = brand_black
    else: # white
        bg_color = brand_white
        text_color = brand_black
        accent_color = brand_red
        
    img = Image.new('RGB', (w, h), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw simple frame/border
    draw.rectangle([(20, 20), (w-20, h-20)], outline=accent_color, width=4)
    
    # Try to load a font
    try:
        # Use a generic sans-serif font
        font = ImageFont.truetype("arial.ttf", 36)
        brand_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        brand_font = font
        
    # Draw text (Centered roughly)
    lines = text.split()
    y_text = h // 2 - 50
    for line in lines:
        left, top, right, bottom = font.getbbox(line) if hasattr(font, 'getbbox') else draw.textbbox((0, 0), line, font=font)
        text_w = right - left
        draw.text(((w - text_w) // 2, y_text), line, font=font, fill=text_color)
        y_text += 50
        
    # Draw Brand
    brand_text = "BLOODFORD FASHION BRAND"
    left, top, right, bottom = brand_font.getbbox(brand_text) if hasattr(brand_font, 'getbbox') else draw.textbbox((0, 0), brand_text, font=brand_font)
    text_w = right - left
    draw.text(((w - text_w) // 2, h - 100), brand_text, font=brand_font, fill=accent_color)
    
    img.save(os.path.join(images_dir, filename))

for filename, text, theme in products:
    generate_image(filename, text, theme)
    print(f"Generated {filename}")
