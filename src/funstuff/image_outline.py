##
# Creates an image outline

from PIL import Image, ImageFilter

image = Image.open('img/cricket.png')
edges = image.filter(ImageFilter.FIND_EDGES)
veryFatEdges = edges.filter(ImageFilter.MaxFilter(9))
veryFatEdges.save('img/cricket_updated.png')

