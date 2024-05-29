'''sh
pip install qrcode
'''

import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_qr_code(text, url, filename):
    # Combine text and URL
    data = f"{text}\n{url}"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    #img = qr.make_image(fill_color="#FBBB04", back_color="white")
    img = qr.make_image(fill_color="#00008b", back_color="white") # dark blue

    # Load a font
    font_path = "/Library/Fonts/Arial.ttf"  # Adjust the path if necessary
    font = ImageFont.truetype(font_path, 15)

    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # Calculate text width and height
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate x, y position for the text
    x = (img.size[0] - text_width) / 2
    y = img.size[1] - text_height - 10  # 10 pixels from the bottom

    # Add text to the image
    #draw.text((x, y), text, fill="#FBBB04", font=font)
    draw.text((x, y), text, fill="#00008b", font=font) #dark blue

    # Save the image
    img.save(filename)

    return img

# Usage
generate_qr_code("Chiranjeevi Yogesh Raghav Upanayanam Ceremony - Date: 9th June 2024", "https://www.google.com", "custom_qr.png")
