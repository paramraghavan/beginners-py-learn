import numpy as np
from wordcloud import WordCloud, STOPWORDS
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import random

# -----------------------------
# COLORS
# -----------------------------
hsl_arr = [
    "hsl(342, 75%, 62%)",
    "hsl(24, 64%, 45%)",
    "hsl(147, 50%, 47%)",
    "hsl(156, 60%, 27%)",
    "hsl(39, 100%, 50%)",
    "hsl(248, 53%, 58%)"
]

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return hsl_arr[random.randint(0, len(hsl_arr)-1)]

# -----------------------------
# WORDS
# -----------------------------
text = {
    'Krishna': 40, '50th': 40, 'Birthday': 35, 'Happy': 35,
    'globetrotter': 20,
    'wonderful': 10, 'voyager': 10, 'cricket': 10, 'helping': 10,
    'captain': 10, 'foodie': 10, 'reliable': 8,
    'travel': 10, 'free-spirit': 10, 'practical': 10,
    'sincere': 10, 'trustworthy': 10, 'jetsetter': 10,
    'truthful': 10, 'resourceful': 10, 'explorer': 10, 'kind': 10
}

# -----------------------------
# 12 x 8 inches @300 DPI
# -----------------------------
W, H = 3600, 2400

# -----------------------------
# CENTER IMAGE
# -----------------------------
travel_size = 1200   # slightly smaller for landscape balance

travel = Image.open("img/travel_grey.png").convert("RGBA")
travel = ImageOps.contain(travel, (travel_size, travel_size))

# remove white background
arr = np.array(travel)
white = (arr[:,:,0]>240)&(arr[:,:,1]>240)&(arr[:,:,2]>240)
arr[white,3] = 0

# soften icon color (premium look)
dark = (arr[:,:,0] < 120) & (arr[:,:,1] < 120) & (arr[:,:,2] < 120)
arr[dark] = [150, 150, 150, 255]

travel = Image.fromarray(arr)

# center position
x = (W - travel.width)//2
y = (H - travel.height)//2

# -----------------------------
# MASK (block center so words go around)
# -----------------------------
mask = np.zeros((H, W), dtype=np.uint8)

# slightly larger hole for spacing
pad = 80
mask[
    y-pad:y+travel.height+pad,
    x-pad:x+travel.width+pad
] = 255

# -----------------------------
# WORD CLOUD
# -----------------------------
wc = WordCloud(
    width=W,
    height=H,
    mask=mask,
    background_color="#DDE3EA",   # slate background
    stopwords=STOPWORDS,
    max_words=220,
    repeat=True,
    min_font_size=18,
    max_font_size=280,
    prefer_horizontal=0.92,
    collocations=False,
    margin=8,
    random_state=10
).fit_words(text)

wc.recolor(color_func=color_func)

wc_img = Image.fromarray(wc.to_array()).convert("RGBA")

# -----------------------------
# FINAL COMPOSITE
# -----------------------------
final = wc_img.copy()
final.alpha_composite(travel, (x, y))

# Add a title at top
from PIL import ImageDraw, ImageFont
draw = ImageDraw.Draw(final)
# font = ImageFont.truetype("arial.ttf", 120)
from PIL import ImageFont

# font_paths = [
#     "/System/Library/Fonts/Supplemental/Arial.ttf",
#     "/System/Library/Fonts/Supplemental/Helvetica.ttc",
#     "/System/Library/Fonts/SFNS.ttf"
# ]
#
# font = None
# for path in font_paths:
#     try:
#         font = ImageFont.truetype(path, 120)
#         print("Using:", path)
#         break
#     except:
#         pass
#
# if font is None:
#     font = ImageFont.load_default()
#
# draw.text((W//2, 120), "Celebrating 50 Years of Krishna",
#           fill=(60,60,60), anchor="mm", font=font)

# add a border
# from PIL import ImageOps
# final = ImageOps.expand(final, border=40, fill="black")

# SAVE (PRINT READY)
final.save("12x8_travel_premium.png", dpi=(300, 300))

# PREVIEW
plt.figure(figsize=(12, 8))
plt.imshow(final)
plt.axis("off")
plt.tight_layout()
plt.show()