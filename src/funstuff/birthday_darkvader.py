import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image

mic_mask = np.array(Image.open("img/darvader1.png"))


# wc_mic = WordCloud(width=1200,
#                    height=1200,
#                    stopwords=STOPWORDS,
#                    background_color="white",
#                    max_words=1000,
#                    contour_width=3,
#                    repeat=True,
#                    mask=mic_mask,
#                    min_font_size=1,
#                    contour_color='black'
#                    )

wc_mic = WordCloud(background_color="white",
                      mask=mic_mask,
                      contour_width=3,
                      repeat=True,
                      min_font_size=3,
                      contour_color='darkgreen')

# 'word text': word weight  'th' superscript unicode for 13th
text = {'Swaroop': 24, 'Birthday': 21, 'Happy': 21 , '13\u1D57\u02B0': 21, 'scout': 3, 'Romeo': 12, 'kind': 3, 'soccer': 3,
        'balavihar': 3, 'tennis': 3, 'swimming': 3, 'minecraft': 3,'piano soloist': 3,
        'director': 3, 'straight forward': 3}
wc_mic.fit_words(text)
wc_mic.to_file('BdaySwaroopDv1.png')
