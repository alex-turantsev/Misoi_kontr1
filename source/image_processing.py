#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from PIL import ImageTk, Image

class image_processing:
    @staticmethod
    def grayscale(image):
        image_copy = image.copy()
        pixels = image_copy.load()
        width, height = image.size
        for i in range(width):
            for j in range(height):
                R,G,B = pixels[i,j]
                grey = int(0.3*R + 0.59*G + 0.11*B)
                pixels[i,j] = (grey, grey, grey)
        return image_copy

    @staticmethod
    def prepare1(image,gmin,gmax):
        new_d = 255 - (255 - gmax + gmin)
        factor = new_d / 255.0
        pixels = image.load()
        width, height = image.size
        for i in range(width):
            for j in range(height):
                R,G,B = pixels[i,j]
                index = int((R + G + B) / float(3))
                newpix = gmax
                if index < gmin:
                    newpix = gmin
                else:
                    if index <= gmax:
                        newpix = gmin + int(index*factor)
                pixels[i,j] = (newpix, newpix, newpix)
        return image

    @staticmethod
    def prepare2(image,gmin,gmax):
        new_d = 255 - (255 - gmax + gmin)
        factor = new_d / 255.0
        pixels = image.load()
        width, height = image.size
        for i in range(width):
            for j in range(height):
                R,G,B = pixels[i,j]
                index = int((R + G + B) / float(3))
                newpix = 255
                if index < gmin:
                    newpix = 0
                else:
                    if index <= gmax:
                        newpix = int(index/factor)
                pixels[i,j] = (newpix, newpix, newpix)
        return image
