
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from config import CONFIG


def generate_slide_image(text: str, slide_number: int,
                          total_slides: int, output_path: str):
    W = CONFIG["width"]
    H = CONFIG["height"]
    bg = CONFIG["bg_color"]
    fg = CONFIG["font_color"]
    padding = CONFIG["padding"]
    font_size = CONFIG["font_size"]

    # Create blank image
    img = Image.new("RGB", (W, H), color=bg)
    draw = ImageDraw.Draw(img)

    # Draw gradient-like background (two-tone)
    for y in range(H):
        ratio = y / H
        r = int(bg[0] + (30 - bg[0]) * ratio)
        g = int(bg[1] + (35 - bg[1]) * ratio)
        b = int(bg[2] + (60 - bg[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Draw top accent bar
    draw.rectangle([0, 0, W, 6], fill=(99, 179, 237))

    # Draw bottom accent bar
    draw.rectangle([0, H - 6, W, H], fill=(99, 179, 237))

    # Load font (fallback to default if not available)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
        small_font = ImageFont.truetype("arial.ttf", 22)
    except:
        try:
            # Try common Windows font paths
            font = ImageFont.truetype(
                "C:/Windows/Fonts/arial.ttf", font_size)
            small_font = ImageFont.truetype(
                "C:/Windows/Fonts/arial.ttf", 22)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()

    # Wrap text to fit slide width
    max_chars = int((W - padding * 2) / (font_size * 0.55))
    wrapped = textwrap.wrap(text, width=max_chars)

    # Calculate total text height
    line_height = int(font_size * CONFIG["line_spacing"])
    total_text_h = len(wrapped) * line_height

    # Center text vertically
    start_y = (H - total_text_h) // 2

    # Draw each line
    for i, line in enumerate(wrapped):
        # Get line width for centering
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_w = bbox[2] - bbox[0]
        except:
            line_w = len(line) * (font_size // 2)

        x = (W - line_w) // 2
        y = start_y + i * line_height

        # Draw subtle shadow
        draw.text((x + 2, y + 2), line, font=font,
                  fill=(0, 0, 0, 128))
        # Draw main text
        draw.text((x, y), line, font=font, fill=fg)

    # Draw slide progress at bottom
    progress_text = f"{slide_number} / {total_slides}"
    try:
        bbox = draw.textbbox((0, 0), progress_text, font=small_font)
        pw = bbox[2] - bbox[0]
    except:
        pw = len(progress_text) * 12

    draw.text(
        (W - pw - padding, H - 40),
        progress_text,
        font=small_font,
        fill=(99, 179, 237)
    )

    # Save image
    img.save(output_path, "PNG")