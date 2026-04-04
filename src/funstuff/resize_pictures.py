from PIL import Image
import os

# Settings
DPI = 300
WIDTH_IN = 3      # inches
HEIGHT_IN = 2     # inches
PX_W = int(WIDTH_IN * DPI)   # 600px
PX_H = int(HEIGHT_IN * DPI)  # 900px
PADDING_COLOR = (255, 255, 255)  # white padding

input_folder = "/Users/paramraghavan/kRISHNA"        # folder with your JPEGs
output_folder = "prints"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg")):
        img = Image.open(os.path.join(input_folder, filename)).convert("RGB")

        # Scale to fit INSIDE 600x900 without cropping anyone
        img.thumbnail((PX_W, PX_H), Image.LANCZOS)

        # Create white canvas and paste image centered
        canvas = Image.new("RGB", (PX_W, PX_H), PADDING_COLOR)
        x = (PX_W - img.width) // 2
        y = (PX_H - img.height) // 2
        canvas.paste(img, (x, y))

        # Save with 300 DPI metadata so printers know the size
        out_path = os.path.join(output_folder, filename)
        # Rotate 90 degrees so CVS prints correctly in portrait orientation
        canvas = canvas.rotate(90, expand=True)
        canvas.save(out_path, "JPEG", dpi=(DPI, DPI), quality=99)
        print(f"Saved: {out_path} ({canvas.width}x{canvas.height} px)")

print("Done! All prints saved to:", output_folder)