import numpy as np
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import matplotlib.pyplot as plt
import random

hsl_arr = [
    "hsl(342, 75%, 62%)",
    "hsl(24, 64%, 45%)",
    "hsl(147, 50%, 47%)",
    "hsl(156, 60%, 27%)",
    "hsl(39, 100%, 50%)",
    "hsl(247, 53%, 58%)"
]

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return hsl_arr[random.randint(0, 5)]

text = {
    'Krishna': 39, '50th': 21, 'Birthday': 21, 'Happy': 21,
     'voyager': 7, 'cricket': 7, 'helping': 7,
    'foodie': 7, 'reliable': 7, 'travel': 7, 'free-spirit': 7, 'practical': 7,
     'trustworthy': 7, 'jetsetter': 7, 'truthful': 7,
    'explorer': 7, 'kind': 7, 'funny': 7}

more_words = { 'globetrotter': 7,'wonderful': 7, 'resourceful': 7,
    'beaches': 7,
    'mountains': 7,
    'islands': 7,
    'sunsets': 7,
    'vacations': 7,
    'holidays': 7,
    'getaways': 7,
    'resorts': 7,
    'cruises': 7,
    'roadtrips': 7,
    'sightseeing': 7,
    'landmarks': 7,
    'cities': 7,
    'coastlines': 7,
    'nature': 7,
    'scenery': 7,
    'cafes': 7,
    'retreat': 7,
    'leisure': 7,
    'serenity': 7,
    'calm': 7,
    'peace': 7,
    'breeze': 7,
    'adventures': 7,
    'routes': 7,
    'maps': 7,
    'flights': 7,
    'hotels': 7,
    'journeys': 7,
    'sunrise':7
}

text.update(more_words)
# 8 x 12 inches at 300 DPI = 2400 x 3600 px
W, H = 2400, 3600

# page-wide drawable area
mask = np.zeros((H, W), dtype=np.uint8)

# plane size scaled for tall poster layout
plane_w, plane_h = 1700, 1700

travel = Image.open("img/plane.png").convert("L")
travel = travel.resize((plane_w, plane_h))
travel_arr = np.array(travel)

# white = blocked, black = drawable
travel_hole = np.where(travel_arr < 200, 255, 0).astype(np.uint8)

# center the plane
x = (W - plane_w) // 2
y = (H - plane_h) // 2
mask[y:y+plane_h, x:x+plane_w] = travel_hole

wc = WordCloud(
    width=W,
    height=H,
    mask=mask,
    background_color="white",
    stopwords=STOPWORDS,
    max_words=1008,
    repeat=True,
    min_font_size=17,
    max_font_size=600,
    prefer_horizontal=0.9,
    collocations=False,
    margin=6
).fit_words(text)

wc.recolor(color_func=color_func, random_state=3)
wc_img = Image.fromarray(wc.to_array()).convert("RGBA")

# paste actual image in center
travel_rgba = Image.open("img/plane.png").convert("RGBA").resize((plane_w, plane_h))

travel_rgba_arr = np.array(travel_rgba)
white = (
    (travel_rgba_arr[:, :, 0] > 240) &
    (travel_rgba_arr[:, :, 1] > 240) &
    (travel_rgba_arr[:, :, 2] > 240)
)
travel_rgba_arr[white, 3] = 0
travel_rgba = Image.fromarray(travel_rgba_arr)

final = wc_img.copy()
final.alpha_composite(travel_rgba, (x, y))

# save at print quality with DPI metadata
final.save("birthday_travel_krishna_8x12.png", dpi=(300, 300))

# preview
plt.figure(figsize=(7, 12))
plt.imshow(final)
plt.axis("off")
plt.show()
