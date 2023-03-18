# pick any png image from web, i choose black picture
# here updating the background with while color


from PIL import Image, ImageFilter

im = Image.open('img/cricket.png')
fill_color = (255,255,255)  # your new background color

im = im.convert("RGBA")   # it had mode P after DL it from OP
if im.mode in ('RGBA', 'LA'):
    background = Image.new(im.mode[:-1], im.size, fill_color)
    background.paste(im, im.split()[-1]) # omit transparency
    im = background



im.convert("RGB").save(r"img/cricket_wht_bg.png")

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
mic_mask = np.array(Image.open("img/cricket_wht_bg.png"))
plt.imshow(mic_mask)
plt.axis("off")
plt.show()