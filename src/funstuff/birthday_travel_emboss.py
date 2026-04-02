import numpy as np
from wordcloud import WordCloud
from PIL import Image, ImageOps, ImageFilter
import random

# COLORS
hsl_arr = [
    "hsl(342, 75%, 62%)", "hsl(24, 64%, 45%)", "hsl(147, 50%, 47%)",
    "hsl(156, 60%, 27%)", "hsl(39, 100%, 50%)", "hsl(248, 53%, 58%)"
]

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return hsl_arr[random.randint(0, len(hsl_arr)-1)]

text = {
    'Krishna': 25, '50th': 25, 'Birthday': 25, 'Happy': 25, 'globetrotter': 16,
    'wonderful': 9, 'voyager': 9, 'cricket': 9, 'helping': 9, 'captain': 9,
    'foodie': 9, 'reliable': 7, 'travel': 9, 'free-spirit': 9, 'practical': 9,
    'sincere': 9, 'trustworthy': 9, 'jetsetter': 9, 'truthful': 9, 'resourceful': 9,
    'explorer': 9, 'kind': 9
}

W, H = 2400, 3600

# 1. PREPARE CENTER IMAGE
travel_size = 1500
travel = Image.open("img/travel_black.png").convert("RGBA")
travel = ImageOps.contain(travel, (travel_size, travel_size))

# Clean background
arr = np.array(travel)
white = (arr[:,:,0] > 240) & (arr[:,:,1] > 240) & (arr[:,:,2] > 240)
arr[white, 3] = 0
travel = Image.fromarray(arr)

x = (W - travel.width) // 2
y = 800

# 2. CREATE SHADOW/GLOW EFFECT (The "Pop" Factor)
# Create a black version of the icon for the shadow
shadow = Image.new("RGBA", travel.size, (0, 0, 0, 150)) # 150 is shadow darkness
shadow.putalpha(travel.getchannel('A'))
# Blur the shadow
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=20))

# 3. CREATE MASK FOR WORDS
mask = np.zeros((H, W), dtype=np.uint8)
icon_alpha = np.array(travel)[:, :, 3]
mask[y:y+travel.height, x:x+travel.width] = icon_alpha

# 4. GENERATE WORD CLOUD
wc = WordCloud(
    width=W, height=H,
    mask=mask,
    background_color=None, mode="RGBA",
    max_words=1000, repeat=True,
    min_font_size=14, max_font_size=240,
    prefer_horizontal=0.9, collocations=False
).generate_from_frequencies(text)

wc.recolor(color_func=color_func)
wc_img = Image.fromarray(wc.to_array()).convert("RGBA")

# 5. FINAL COMPOSITION (Layering for 3D effect)
final = Image.new("RGBA", (W, H), "white")

# Layer 1: The Words (Background)
final.alpha_composite(wc_img)

# Layer 2: The Shadow (Slightly offset for light source effect)
# Offset by 15px down and 10px right
final.paste(shadow, (x + 10, y + 15), shadow)

# Layer 3: The Main Icon (Foreground)
final.paste(travel, (x, y), travel)

# Save
final.save("8x12_3D_pop.png", dpi=(300,300))