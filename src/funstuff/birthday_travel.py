import numpy as np
from wordcloud import WordCloud, STOPWORDS
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import random

# COLORS
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

text = {
    'Krishna': 25, '50th': 25, 'Birthday': 25, 'Happy': 25, 'globetrotter': 16,
    'wonderful': 9, 'voyager': 9, 'cricket': 9, 'helping': 9, 'captain': 9,
    'foodie': 9, 'reliable': 7, 'travel': 9, 'free-spirit': 9, 'practical': 9,
    'sincere': 9, 'trustworthy': 9, 'jetsetter': 9, 'truthful': 9, 'resourceful': 9,
    'explorer': 9, 'kind': 9
}

# 8x12 @300 DPI
W, H = 2400, 3600

# CENTER IMAGE
travel_size = 1500
travel = Image.open("img/travel_black.png").convert("RGBA")
travel = ImageOps.contain(travel, (travel_size, travel_size))

# remove white bg
arr = np.array(travel)
white = (arr[:,:,0]>240)&(arr[:,:,1]>240)&(arr[:,:,2]>240)
arr[white,3]=0
travel = Image.fromarray(arr)

x = (W - travel.width)//2
y = 800   # slightly higher for visual balance

# MASK
mask = np.zeros((H, W), dtype=np.uint8)
mask[y:y+travel.height, x:x+travel.width] = 255

# WORD CLOUD
wc = WordCloud(
    width=W,
    height=H,
    mask=mask,
    background_color="white",
    max_words=1008,
    repeat=True,
    min_font_size=14,
    max_font_size=240,
    prefer_horizontal=0.9,
    collocations=False
).fit_words(text)

wc.recolor(color_func=color_func)

wc_img = Image.fromarray(wc.to_array()).convert("RGBA")

final = wc_img.copy()
final.alpha_composite(travel, (x, y))

final.save("8x12_premium.png", dpi=(300,300))