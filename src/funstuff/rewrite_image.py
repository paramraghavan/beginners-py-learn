'''
Here we are reading the entire image and replacing all non black pixels with white pixels.
'''

#!/usr/bin/env python3
# pip install opencv-python
import cv2
import numpy as np

# Load image
im = cv2.imread("img/mic.png")

# Make all pixels that are not black perfectly  pixels white
im[np.all(im != (0, 0, 0), axis=-1)] = (255,255,255)

# Save result
cv2.imwrite('img/mic_pixels_updated.png', im)