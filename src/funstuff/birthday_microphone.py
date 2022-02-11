import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import random

hsl_arr = [ "hsl(342, 75%, 62%)",
            "hsl(24, 64%,  45%)",
            "hsl(147, 50%, 47%)",
            "hsl(156, 60%, 27%)",
            "hsl(39, 100%, 50%)",
            "hsl(248, 53%, 58%)"]

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    # return "hsl(0, 0%%, %d%%)" % random.randint(40, 60)
    return hsl_arr[random.randint(0, 5)]


mic_mask = np.array(Image.open("img/mic.png"))
plt.imshow(mic_mask)
plt.axis("off")
plt.show()

wc_mic = WordCloud(width=1080,
                   height=1080,
                   stopwords=STOPWORDS,
                   background_color="white",
                   max_words=1008,
                   contour_width=6,
                   repeat=True,
                   mask=mic_mask,
                   min_font_size=1,
                   contour_color='darkgreen'
                   )

# wc_mic = WordCloud(background_color="white",
#                       mask=mic_mask,
#                       contour_width=3,
#                       repeat=False,
#                       min_font_size=3,
#                       contour_color='darkgreen')


# 'word text': word weight
text = {'Sangam': 25, '50th': 25, 'Birthday': 25, 'Happy': 25, 'singer':16,
        'wonderful':9, 'honest':9, 'cricket':9, 'helping':9, 'coach':9,
        'toastmaster':9, 'reliable':7, 'music':9, 'warm-hearted':9, 'practical':9,
        'sincere':9, 'trustworthy':9, 'affable':9, 'truthful':9, 'resourceful':9,
        'integrity':9, 'kind':9 }
wc_mic.fit_words(text)


default_colors = wc_mic.to_array()
wc_mic.recolor(color_func=grey_color_func, random_state=3)
# wc.to_file("a_new_hope.png")

# text = 'Happy, Birthday, Sangam'
# # Generate a wordcloud
# wc_mic.generate(text)
wc_mic.to_file('HappyBirthDayTheSinger.png')
