#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from PIL import ImageTk, Image

class image_processing:
    @staticmethod
    def greyscale(image):
        image_copy = image.copy()
        pixels = image_copy.load()
        width, height = image.size
        for i in range(width):
            for j in range(height):
                R,G,B = pixels[i,j]
                grey = int(0.3*R + 0.59*G + 0.11*B)
                pixels[i,j] = (grey, grey, grey)
        return image_copy
