#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from PIL import ImageTk, Image
from operator_filter import operator_filter

image_path = '/Users/alex/Projects/images.jpeg'
img = Image.open(image_path)

filt = operator_filter()
filt.apply_filter(image=img)
