#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter as tk
from PIL import ImageTk, Image
import ntpath

class histogram_window(tk.Tk):
    def __init__(self, image, path):
        tk.Tk.__init__(self)
        self.root = self

        self.title('Histogram '+ntpath.basename(path))
        self.geometry('500x350');
        self.minsize(500, 350)
        self.maxsize(500, 350)

        intensities = self.calculate_intensities(image)
        self.draw_histogram(intensities)

        self.mainloop()

    def calculate_intensities(self,image):
        pixels = image.load()
        width, height = image.size
        intensities = [0]*256
        for i in range(width):    # for every pixel:
            for j in range(height):
                R,G,B = pixels[i,j]
                index = float(R + G + B) / float(3)
                intensities[int(index)] += 1
        return intensities

    def draw_histogram(self, data):
        c_width = 500                                                       # Define it's width
        c_height = 350                                                      # Define it's height
        c = tk.Canvas(self, width=c_width, height=c_height, bg= 'white')    # Create a canvas and use the earlier dimensions
        c.pack()
        y_gap = 10
        y_stretch = c_height -y_gap*2                                                   # The highest y = max_data_value * y_stretch                                                        # The gap between lower canvas edge and x axis
        x_stretch = 2                                                   # Stretch x wide enough to fit the variables
        x_width = 1                                                        # The width of the x-axis
        x_gap = 5                                                        # The gap between left canvas edge and y axis

        max_element = 0
        for i in range(len(data)):
            if data[i] > max_element:
                max_element = data[i]

        for x, y in enumerate(data):                                        # A quick for loop to calculate the rectangle
                                                                            # coordinates of each bar
            x0 = x * x_stretch + x * x_width + x_gap                        # Bottom left coordinate
            y0 = c_height - (y * y_stretch/max_element + y_gap)                         # Top left coordinates
            x1 = x * x_stretch + x * x_width + x_width + x_gap              # Bottom right coordinates
            y1 = c_height - y_gap                                           # Top right coordinates
            c.create_rectangle(x0, y0, x1, y1, fill="grey", outline="grey")                  # Draw the bar
            #c.create_text(x0+2, y0, anchor=tk.SW, text=str(y))              # Put the y value above the bar
