import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image

mic_mask = np.array(Image.open("img/mic.png"))


wc_mic = WordCloud(width=1200,
                   height=1200,
                   stopwords=STOPWORDS,
                   background_color="white",
                   max_words=1000,
                   contour_width=3,
                   repeat=True,
                   mask=mic_mask,
                   min_font_size=1,
                   contour_color='darkgreen'
                   )

# 'word text': word weight
text = {'SingerName': 21, 'Birthday': 21, 'Happy': 21 }
wc_mic.fit_words(text)
wc_mic.to_file('HappyBirthDayTheSinger.png')
