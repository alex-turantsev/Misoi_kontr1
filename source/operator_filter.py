#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from PIL import ImageTk, Image

class operator_filter:
    def __init__(self):
        self.operator = [[0,0,0],[0,1,0],[0,0,0]]

    def apply_filter(self, image):
        width, height = image.size
        temp_image = image.copy()
        real_pixels = image.load()
        pixels = temp_image.load()
        width, height = image.size
        for i in range(width):
            for j in range(height):
                around_pixels = self.take_around_pixels(width=width, height=height, pixels=real_pixels, operator=self.operator, ii=i, jj=j)
                pixels[i,j] = self.get_result_pixel(around=around_pixels)
        return temp_image

    #taking around pixels near pixel[ii,jj] using size of operator
    @staticmethod
    def take_around_pixels(width, height, pixels, operator, ii, jj):
        around = list(operator)
        op_width = len(operator[0])
        op_height = len(operator)
        half_width = op_width/2
        half_height = op_height/2

        i0 = ii - half_width
        j0 = jj - half_height
        for i in range(op_width):
            x = i0 + i
            if x < 0:
                 x += half_width;
            if x >= width:
                x -= half_width;
            for j in range(op_height):
                y = j0 + j
                if y < 0:
                     y += half_height;
                if y >= height:
                    y -= half_height;
                around[i][j] = pixels[x,y]
        return around

    @staticmethod
    def get_result_pixel(around):
        return (0, 0, 0)

class min_filter(operator_filter):
    @staticmethod
    def get_result_pixel(around):
        width = len(around[0])
        height = len(around)
        R,G,B = around[0][0]
        min_pix = int((R + G + B) / float(3))
        ii = 0
        jj = 0
        for i in range(width):
            for j in range(height):
                R,G,B = around[i][j]
                res = int((R + G + B) / float(3))
                if res < min_pix:
                    min_pix = res
                    ii = i
                    jj = j
        return around[ii][jj]

class max_filter(operator_filter):
    @staticmethod
    def get_result_pixel(around):
        width = len(around[0])
        height = len(around)
        R,G,B = around[0][0]
        max_pix = int((R + G + B) / float(3))
        ii = 0
        jj = 0
        for i in range(width):
            for j in range(height):
                R,G,B = around[i][j]
                res = int((R + G + B) / float(3))
                if res > max_pix:
                    max_pix = res
                    ii = i
                    jj = j
        return around[ii][jj]

class minmax_filter(operator_filter):
    @staticmethod
    def get_result_pixel(around):
        width = len(around[0])
        height = len(around)
        R,G,B = around[0][0]
        min_pix = int((R + G + B) / float(3))
        max_pix = int((R + G + B) / float(3))
        imin = 0
        jmin = 0
        imax = 0
        jmax = 0
        for i in range(width):
            for j in range(height):
                R,G,B = around[i][j]
                res = int((R + G + B) / float(3))
                if res < min_pix:
                    min_pix = res
                    imin = i
                    jmin = j
                if res > max_pix:
                    max_pix = res
                    imax = i
                    jmax = j
        R,G,B = around[imax][jmax]
        R1,G1,B1 = around[imin][jmin]
        return (R-R1,G-G1,B-B1)
